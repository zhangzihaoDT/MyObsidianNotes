#!/usr/bin/env python3
"""
flomo_sync.py — 将 Markdown 内容同步到 Flomo。

常用方式：
  python3 flomo_sync.py "要发送的内容"
  echo "内容" | python3 flomo_sync.py
  python3 flomo_sync.py -f /path/to/note.md
  python3 flomo_sync.py --title "标题" --tags "思考,数据分析" < note.md
  python3 flomo_sync.py --dry-run < note.md

默认从 .env 读取 flomo_api，也兼容 FLOMO_API。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib import error as urllib_error
from urllib import request


DEFAULT_MAX_LENGTH = 2000
ENV_KEYS = ("flomo_api", "FLOMO_API")


def unique_paths(paths: list[Path]) -> list[Path]:
    """按顺序去重路径。"""
    result: list[Path] = []
    seen: set[Path] = set()

    for path in paths:
        try:
            resolved = path.expanduser().resolve()
        except OSError:
            resolved = path.expanduser().absolute()

        if resolved not in seen:
            seen.add(resolved)
            result.append(resolved)

    return result


def env_candidates(env_dir: str | None = None) -> list[Path]:
    """
    返回 .env 查找路径，优先级从高到低：

    1. --env-dir
    2. 当前工作目录及其父目录
    3. 脚本目录及其父目录
    """
    candidates: list[Path] = []

    if env_dir:
        candidates.append(Path(env_dir) / ".env")

    cwd = Path.cwd()
    candidates.extend(parent / ".env" for parent in (cwd, *cwd.parents))

    script_dir = Path(__file__).resolve().parent
    candidates.extend(
        parent / ".env" for parent in (script_dir, *script_dir.parents)
    )

    return unique_paths(candidates)


def parse_env_file(path: Path) -> dict[str, str]:
    """解析简单 KEY=VALUE 格式的 .env 文件。"""
    env: dict[str, str] = {}

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return env

    for raw_line in lines:
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        if line.startswith("export "):
            line = line[7:].lstrip()

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]

        env[key] = value

    return env


def load_env(env_dir: str | None = None) -> tuple[dict[str, str], Path | None]:
    """
    查找并加载第一个包含 Flomo webhook 配置的 .env。

    返回：
      (环境变量字典, 命中的 .env 路径)
    """
    fallback_env: dict[str, str] = {}
    fallback_path: Path | None = None

    for path in env_candidates(env_dir):
        if not path.is_file():
            continue

        parsed = parse_env_file(path)

        if fallback_path is None:
            fallback_env = parsed
            fallback_path = path

        if any(parsed.get(key, "").strip() for key in ENV_KEYS):
            return parsed, path

    return fallback_env, fallback_path


def get_webhook_url(env: dict[str, str]) -> str:
    """优先读取进程环境变量，其次读取 .env。"""
    for key in ENV_KEYS:
        value = os.environ.get(key, "").strip()
        if value:
            return value

    for key in ENV_KEYS:
        value = env.get(key, "").strip()
        if value:
            return value

    return ""


def read_content(args: argparse.Namespace) -> str:
    """从文件、位置参数或 stdin 读取内容。"""
    if args.file:
        path = Path(args.file).expanduser()

        if not path.is_file():
            raise ValueError(f"文件不存在: {path}")

        try:
            return path.read_text(encoding="utf-8").strip()
        except UnicodeError as exc:
            raise ValueError(f"文件不是有效的 UTF-8 文本: {path}") from exc
        except OSError as exc:
            raise ValueError(f"无法读取文件: {path} ({exc})") from exc

    if args.content is not None:
        return args.content.strip()

    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    return ""


def normalize_tag(tag: str) -> str:
    """把标签转换为 Flomo 可用的 #tag 形式。"""
    tag = tag.strip().lstrip("#").strip()
    tag = re.sub(r"\s+", "-", tag)
    tag = re.sub(r"#+", "", tag)
    return tag


def parse_tags(raw_tags: list[str] | None) -> list[str]:
    """解析可重复的 --tags 参数，支持逗号、中文逗号和空格分隔。"""
    if not raw_tags:
        return []

    tags: list[str] = []
    seen: set[str] = set()

    for item in raw_tags:
        for raw_tag in re.split(r"[,，\s]+", item):
            tag = normalize_tag(raw_tag)
            if tag and tag not in seen:
                seen.add(tag)
                tags.append(tag)

    return tags


def compose_content(
    body: str,
    *,
    title: str | None = None,
    tags: list[str] | None = None,
    source: str | None = None,
) -> str:
    """
    将标题、正文、来源和标签组合为轻量 Flomo Markdown。

    若未传入额外字段，正文保持原样，仅规范首尾空白。
    """
    sections: list[str] = []

    clean_title = (title or "").strip()
    clean_body = body.strip()
    clean_source = (source or "").strip()
    clean_tags = tags or []

    if clean_title:
        sections.append(f"**{clean_title}**")

    if clean_body:
        sections.append(clean_body)

    if clean_source:
        sections.append(f"来源：{clean_source}")

    if clean_tags:
        sections.append(" ".join(f"#{tag}" for tag in clean_tags))

    return "\n\n".join(sections).strip()


def truncate_content(content: str, max_length: int) -> str:
    """尽量在自然边界处截断内容。"""
    if len(content) <= max_length:
        return content

    suffix = "\n\n…"
    cutoff = max_length - len(suffix)

    if cutoff <= 0:
        return content[:max_length]

    candidate = content[:cutoff]

    search_start = max(0, cutoff - 300)
    boundaries = [
        candidate.rfind("\n\n", search_start),
        candidate.rfind("\n", search_start),
        candidate.rfind("。", search_start),
        candidate.rfind("；", search_start),
        candidate.rfind("，", search_start),
        candidate.rfind(" ", search_start),
    ]
    boundary = max(boundaries)

    if boundary > search_start:
        candidate = candidate[: boundary + 1]

    return candidate.rstrip() + suffix


def sync_to_flomo(content: str, webhook_url: str, timeout: int = 15) -> tuple[bool, str]:
    """发送 Markdown 内容到 Flomo webhook。"""
    payload = {
        "content": content,
        "content_type": "markdown",
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = request.Request(
        webhook_url,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "flomo-sync/2.0",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace").strip()
            status = response.status

        if 200 <= status < 300:
            detail = f"HTTP {status}"
            if body:
                detail += f": {body}"
            return True, detail

        return False, f"HTTP {status}: {body}"

    except urllib_error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace").strip()
        return False, f"HTTP {exc.code}: {body or exc.reason}"

    except urllib_error.URLError as exc:
        return False, f"网络错误: {exc.reason}"

    except TimeoutError:
        return False, f"请求超时（{timeout} 秒）"

    except Exception as exc:  # 防止 CLI 因未知网络异常直接输出堆栈
        return False, f"未知错误: {exc}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将 Markdown 内容同步到 Flomo")
    parser.add_argument(
        "content",
        nargs="?",
        help="要发送的内容；省略时从 stdin 读取",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="从 UTF-8 文本文件读取内容",
    )
    parser.add_argument(
        "--env-dir",
        help="优先查找 .env 的目录",
    )
    parser.add_argument(
        "--title",
        help="在正文前添加加粗标题",
    )
    parser.add_argument(
        "--tags",
        action="append",
        help="添加标签，可重复使用，支持逗号或空格分隔",
    )
    parser.add_argument(
        "--source",
        help="在正文后添加来源",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=DEFAULT_MAX_LENGTH,
        help=f"最大字符数，默认 {DEFAULT_MAX_LENGTH}",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="超长时自动截断；默认超长即报错",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP 超时秒数，默认 15",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅预览最终内容，不发送",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 输出执行结果，便于 Agent 解析",
    )
    return parser


def emit_result(
    *,
    ok: bool,
    message: str,
    json_output: bool,
    content_length: int | None = None,
) -> None:
    """统一输出 CLI 结果。"""
    if json_output:
        result: dict[str, object] = {
            "ok": ok,
            "message": message,
        }
        if content_length is not None:
            result["content_length"] = content_length
        print(json.dumps(result, ensure_ascii=False))
        return

    stream = sys.stdout if ok else sys.stderr
    prefix = "✅" if ok else "❌"
    print(f"{prefix} {message}", file=stream)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.max_length <= 0:
        emit_result(
            ok=False,
            message="--max-length 必须大于 0",
            json_output=args.json,
        )
        return 2

    if args.timeout <= 0:
        emit_result(
            ok=False,
            message="--timeout 必须大于 0",
            json_output=args.json,
        )
        return 2

    try:
        body = read_content(args)
    except ValueError as exc:
        emit_result(
            ok=False,
            message=str(exc),
            json_output=args.json,
        )
        return 1

    if not body:
        emit_result(
            ok=False,
            message="未提供内容。可使用位置参数、--file 或 stdin。",
            json_output=args.json,
        )
        return 1

    final_content = compose_content(
        body,
        title=args.title,
        tags=parse_tags(args.tags),
        source=args.source,
    )

    if len(final_content) > args.max_length:
        if args.truncate:
            final_content = truncate_content(final_content, args.max_length)
        else:
            emit_result(
                ok=False,
                message=(
                    f"内容共 {len(final_content)} 字，超过 "
                    f"{args.max_length} 字限制。请精简、拆分，"
                    "或显式使用 --truncate。"
                ),
                json_output=args.json,
                content_length=len(final_content),
            )
            return 1

    if args.dry_run:
        if args.json:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "dry_run": True,
                        "content_length": len(final_content),
                        "content": final_content,
                    },
                    ensure_ascii=False,
                )
            )
        else:
            print("═══ FLOMO DRY RUN ═══")
            print(f"内容长度: {len(final_content)} 字")
            print("─────────────────────")
            print(final_content)
            print("═════════════════════")
        return 0

    env, env_path = load_env(args.env_dir)
    webhook_url = get_webhook_url(env)

    if not webhook_url:
        searched_hint = (
            f"已找到 .env：{env_path}，但未发现 flomo_api 或 FLOMO_API。"
            if env_path
            else "未找到可用的 .env。"
        )
        emit_result(
            ok=False,
            message=(
                f"{searched_hint} 请配置：\n"
                "flomo_api=https://flomoapp.com/iwh/..."
            ),
            json_output=args.json,
        )
        return 1

    success, detail = sync_to_flomo(
        final_content,
        webhook_url,
        timeout=args.timeout,
    )

    if success:
        emit_result(
            ok=True,
            message=f"同步成功（{detail}）",
            json_output=args.json,
            content_length=len(final_content),
        )
        return 0

    emit_result(
        ok=False,
        message=f"同步失败：{detail}",
        json_output=args.json,
        content_length=len(final_content),
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
