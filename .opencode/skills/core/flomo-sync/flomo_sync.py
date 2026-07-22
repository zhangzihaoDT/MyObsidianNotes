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


def normalize_input_content(content: str) -> str:
    """
    将 OpenCode 或命令行输入整理为可发送到 Flomo 的正文。

    OpenCode 可能将真实换行传递为字面量：
        第一段\\n\\n第二段

    本函数将其恢复为：
        第一段

        第二段
    """
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    content = content.replace(r"\r\n", "\n")
    content = content.replace(r"\n", "\n")

    lines = [line.rstrip() for line in content.splitlines()]
    content = "\n".join(lines)

    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()


def parse_pipe_row(line: str) -> list[str] | None:
    """解析使用竖线分隔的一行内容。"""
    stripped = line.strip()

    if "|" not in stripped:
        return None

    cells = [
        cell.strip()
        for cell in stripped.strip("|").split("|")
    ]

    if len(cells) < 2 or any(not cell for cell in cells):
        return None

    # 忽略 Markdown 表格的分隔行，例如 --- | ---
    if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return []

    return cells


def convert_pipe_blocks(content: str) -> str:
    """
    将连续的竖线分隔内容转换成 Flomo 友好的箭头列表。

    支持竖线行之间存在空行的情况。
    """
    lines = content.splitlines()
    output: list[str] = []
    index = 0

    while index < len(lines):
        first_row = parse_pipe_row(lines[index])

        if first_row is None:
            output.append(lines[index])
            index += 1
            continue

        rows: list[list[str]] = []
        cursor = index

        while cursor < len(lines):
            line = lines[cursor]

            # 允许表格行之间存在多余空行
            if not line.strip():
                cursor += 1
                continue

            row = parse_pipe_row(line)

            if row is None:
                break

            if row:
                rows.append(row)

            cursor += 1

        column_counts = {len(row) for row in rows}

        # 至少包括表头和一行数据，并且列数一致
        if len(rows) >= 2 and len(column_counts) == 1:
            headers = rows[0]
            data_rows = rows[1:]

            output.append(
                f"映射顺序：**{' → '.join(headers)}**"
            )
            output.append("")

            for row in data_rows:
                first_cell = row[0]
                remaining_cells = " → ".join(row[1:])
                output.append(
                    f"- **{first_cell}** → {remaining_cells}"
                )

            index = cursor
            continue

        # 无法可靠识别时保留原内容
        output.append(lines[index])
        index += 1

    return "\n".join(output)


def format_flomo_content(content: str) -> str:
    """将原始输入转换成适合 Flomo 阅读的 Markdown。"""
    content = normalize_input_content(content)
    content = convert_pipe_blocks(content)

    lines = content.splitlines()
    output: list[str] = []

    title_added = False
    in_definition_section = False

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            if output and output[-1] != "":
                output.append("")
            continue

        # 第一行作为标题
        if not title_added:
            if line.startswith("**") and line.endswith("**"):
                output.append(line)
            else:
                title = line.rstrip("：:")
                output.append(f"**{title}**")

            title_added = True
            continue

        # 定义区块标题
        if line in {
            "最简洁的定义：",
            "最简洁的定义:",
            "最简洁的定义",
        }:
            if output and output[-1] != "":
                output.append("")

            output.append("**最简洁的定义**")
            output.append("")
            in_definition_section = True
            continue

        # 一句话总结
        summary_match = re.match(
            r"^一句话总结[：:]\s*(.*)$",
            line,
        )

        if summary_match:
            if output and output[-1] != "":
                output.append("")

            output.append("**一句话总结**")
            output.append("")

            summary = summary_match.group(1).strip()
            if summary:
                output.append(summary)

            in_definition_section = False
            continue

        # 定义区块里的"术语：解释"
        if in_definition_section:
            definition_match = re.match(
                r"^([^：:]{1,30})[：:]\s*(.+)$",
                line,
            )

            if definition_match:
                term = definition_match.group(1).strip()
                description = definition_match.group(2).strip()

                output.append(
                    f"- **{term}**：{description}"
                )
                continue

        output.append(line)

    formatted = "\n".join(output)

    # 连续列表项之间不要保留空行
    formatted = re.sub(
        r"(?m)(^- .+)\n\n(?=- )",
        r"\1\n",
        formatted,
    )

    # 最多保留一个空行
    formatted = re.sub(r"\n{3,}", "\n\n", formatted)

    return formatted.strip()


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
        "--raw",
        action="store_true",
        help="仅恢复换行，不执行 Flomo 格式转换",
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
        raw_content = read_content(args)

        if args.raw:
            body = normalize_input_content(raw_content)
        else:
            body = format_flomo_content(raw_content)
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
