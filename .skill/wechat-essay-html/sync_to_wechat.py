import json
import mimetypes
import os
import re
import ssl
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request

from renderers.wechat_inline_renderer import render_wechat_inline


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _env_load(path: str) -> dict:
    raw = _read_text(path)
    data = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
        elif "：" in line:
            k, v = line.split("：", 1)
        elif ":" in line:
            k, v = line.split(":", 1)
        else:
            continue
        data[k.strip()] = v.strip()
    return data


def _http_json(url: str, method: str = "GET", body: dict | None = None) -> dict:
    headers = {"Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}


def _http_multipart(url: str, fields: dict, files: dict) -> dict:
    boundary = f"----PythonBoundary{uuid.uuid4().hex}"
    parts: list[bytes] = []

    def add_field(name: str, value: str):
        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        parts.append(value.encode("utf-8"))
        parts.append(b"\r\n")

    def add_file(name: str, filename: str, content: bytes, content_type: str):
        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode(
                "utf-8"
            )
        )
        parts.append(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        parts.append(content)
        parts.append(b"\r\n")

    for k, v in fields.items():
        add_field(k, str(v))

    for name, file_info in files.items():
        add_file(
            name=name,
            filename=file_info["filename"],
            content=file_info["content"],
            content_type=file_info["content_type"],
        )

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(parts)

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}


def _wechat_get_access_token(app_id: str, app_secret: str) -> str:
    qs = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": app_id, "secret": app_secret}
    )
    url = f"https://api.weixin.qq.com/cgi-bin/token?{qs}"
    data = _http_json(url)
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"获取 access_token 失败：{data}")
    return token


def _wechat_upload_cover(access_token: str, image_path: str) -> str:
    content = _read_bytes(image_path)
    filename = os.path.basename(image_path)
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    qs = urllib.parse.urlencode({"access_token": access_token, "type": "image"})
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?{qs}"
    data = _http_multipart(
        url,
        fields={},
        files={"media": {"filename": filename, "content": content, "content_type": content_type}},
    )
    media_id = data.get("media_id")
    if not media_id:
        raise RuntimeError(f"上传封面失败：{data}")
    return media_id


def _wechat_draft_add(access_token: str, article: dict) -> dict:
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={urllib.parse.quote(access_token)}"
    data = _http_json(url, method="POST", body={"articles": [article]})
    if data.get("errcode", 0) not in (0, None):
        raise RuntimeError(f"创建草稿失败：{data}")
    return data


def _derive_title_from_path(md_path: str) -> str:
    base = os.path.basename(md_path)
    if base.lower().endswith(".md"):
        base = base[:-3]
    return base


def _derive_digest(md: str) -> str:
    for line in md.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("- "):
            s = s[2:].strip()
        s = re.sub(r"\s+", " ", s)
        if len(s) > 90:
            s = s[:90]
        return s
    return ""


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    default_env = os.path.abspath(os.path.join(root, "..", "..", ".env"))
    default_cover = os.path.join(root, "0ebee294-486a-4164-81b7-5a58bfa1cffe.png")

    md_path = None
    env_path = default_env
    cover_path = default_cover

    args = sys.argv[1:]
    for arg in args:
        if arg.startswith("--env="):
            env_path = arg.split("=", 1)[1]
        elif arg.startswith("--cover="):
            cover_path = arg.split("=", 1)[1]
        elif not arg.startswith("--") and md_path is None:
            md_path = arg

    if not md_path:
        raise RuntimeError("请传入要同步的 Markdown 路径")

    env = _env_load(env_path)
    app_id = env.get("AppID") or env.get("appid") or env.get("APPID")
    app_secret = env.get("AppSecret") or env.get("appsecret") or env.get("APPSECRET")
    if not app_id or not app_secret:
        raise RuntimeError("未在 .env 中找到 AppID / AppSecret")

    md = _read_text(md_path).strip()
    title = _derive_title_from_path(md_path)
    digest = _derive_digest(md)

    html = render_wechat_inline(md, title)

    print("开始同步到公众号草稿箱…")
    started = time.time()
    access_token = _wechat_get_access_token(app_id, app_secret)
    thumb_media_id = _wechat_upload_cover(access_token, cover_path)

    article = {
        "title": title,
        "author": "",
        "digest": digest,
        "content": html,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }

    resp = _wechat_draft_add(access_token, article)
    media_id = resp.get("media_id", "")
    elapsed = round(time.time() - started, 2)
    print(f"完成：media_id={media_id}（{elapsed}s）")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        try:
            raw = e.read().decode("utf-8", errors="replace")
        except Exception:
            raw = str(e)
        print(f"HTTP 错误：{e.code} {e.reason}\n{raw}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
