#!/usr/bin/env python3
"""
flomo_sync.py — 将内容同步到 Flomo

用法:
  python flomo_sync.py "要发送的内容"
  echo "内容" | python flomo_sync.py
  python flomo_sync.py -f /path/to/note.md

从 .env 文件读取 flomo_api webhook URL。
.env 文件查找顺序：
  1. 当前工作目录
  2. --env-dir 参数指定目录
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from urllib import request, error as urllib_error


def load_env(env_dir: str | None = None) -> dict[str, str]:
    """从 .env 文件读取键值对，返回 dict。"""
    candidates = []
    if env_dir:
        candidates.append(Path(env_dir) / ".env")
    candidates.append(Path.cwd() / ".env")
    # 也尝试脚本所在目录往上找到 notes 仓库根目录
    script_dir = Path(__file__).resolve().parent
    for parent in [script_dir, script_dir.parent, script_dir.parent.parent]:
        candidates.append(parent / ".env")

    env: dict[str, str] = {}
    seen = set()
    for path in candidates:
        p = path.resolve()
        if p in seen or not p.exists():
            continue
        seen.add(p)
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip("'\"")
            if key:
                env[key] = val
    return env


def sync_to_flomo(content: str, webhook_url: str) -> bool:
    """发送 Markdown 内容到 Flomo webhook。"""
    if not webhook_url:
        print("❌ 错误: 未找到 flomo_api webhook URL", file=sys.stderr)
        return False

    payload = {
        "content": content,
        "content_type": "markdown",
    }

    import json

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        resp = request.urlopen(req, timeout=15)
        body = resp.read().decode("utf-8")
        if resp.status == 200:
            print(f"✅ 同步成功 (HTTP {resp.status})")
            if body.strip():
                print(f"回应: {body.strip()}")
            return True
        else:
            print(f"❌ 同步失败 (HTTP {resp.status}): {body}", file=sys.stderr)
            return False
    except urllib_error.HTTPError as e:
        print(f"❌ HTTP 错误 ({e.code}): {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        return False
    except urllib_error.URLError as e:
        print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="同步内容到 Flomo")
    parser.add_argument("content", nargs="?", help="要发送的内容（如不提供则从 stdin 读取）")
    parser.add_argument("-f", "--file", help="从文件读取内容")
    parser.add_argument("--env-dir", help="包含 .env 的目录路径")
    parser.add_argument("--dry-run", action="store_true", help="仅打印内容，不实际发送")
    args = parser.parse_args()

    # 读取内容
    content: str | None = None

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"❌ 文件不存在: {args.file}", file=sys.stderr)
            return 1
        content = path.read_text(encoding="utf-8").strip()
    elif args.content:
        content = args.content.strip()
    elif not sys.stdin.isatty():
        content = sys.stdin.read().strip()

    if not content:
        print("❌ 未提供内容。用法: python flomo_sync.py '要发送的内容'", file=sys.stderr)
        return 1

    # 加载 .env
    env = load_env(args.env_dir)
    webhook_url = env.get("flomo_api", "")

    if not webhook_url:
        print(
            "❌ 错误: 未找到 flomo_api。请在 .env 中设置:\n"
            "  flomo_api=https://flomoapp.com/iwh/NDIwOTAx/...",
            file=sys.stderr,
        )
        return 1

    # 检查内容长度
    if len(content) > 2000:
        print("⚠️  内容超过 2000 字，请精简后再发送。", file=sys.stderr)
        return 1

    if args.dry_run:
        print("═══ DRY RUN ═══")
        print(f"Webhook: {webhook_url[:40]}...")
        print(f"内容 ({len(content)} 字):")
        print(content)
        print("═══════════════")
        return 0

    success = sync_to_flomo(content, webhook_url)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
