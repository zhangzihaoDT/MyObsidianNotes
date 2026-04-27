from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class FileEvent:
    path: Path
    created_at: Optional[dt.datetime]
    modified_at: dt.datetime


def _parse_day(value: str) -> dt.date:
    s = value.strip()
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def _iter_markdown_files(vault: Path, ignore_globs: Iterable[str]) -> Iterable[Path]:
    ignore_parts = [p for p in ignore_globs if p]
    for path in vault.rglob("*.md"):
        rel = path.relative_to(vault).as_posix()
        if rel == "today.md":
            continue
        if _is_ignored(rel, ignore_parts):
            continue
        yield path


def _is_ignored(rel: str, patterns: List[str]) -> bool:
    for pat in patterns:
        p = pat.strip()
        if not p:
            continue
        if p.endswith("/**"):
            prefix = p[:-3].rstrip("/")
            if rel == prefix or rel.startswith(prefix + "/"):
                return True
            continue
        if p.endswith("/"):
            prefix = p.rstrip("/")
            if rel == prefix or rel.startswith(prefix + "/"):
                return True
            continue
        if fnmatch.fnmatchcase(rel, p):
            return True
    return False


def _get_times(path: Path) -> Tuple[Optional[dt.datetime], dt.datetime]:
    st = path.stat()
    modified = dt.datetime.fromtimestamp(st.st_mtime)
    created_ts = getattr(st, "st_birthtime", None)
    if created_ts is None:
        created_ts = st.st_ctime
    created = dt.datetime.fromtimestamp(created_ts) if created_ts else None
    return created, modified


def _to_obsidian_link(vault: Path, path: Path) -> str:
    rel = path.relative_to(vault).with_suffix("")
    return f"[[{rel.as_posix()}]]"


def _strip_frontmatter(lines: List[str]) -> List[str]:
    if not lines or lines[0].strip() != "---":
        return lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[i + 1 :]
    return lines


def _preview_text(text: str, *, max_lines: int, max_chars: int) -> str:
    lines = _strip_frontmatter(text.splitlines())
    out: List[str] = []
    total = 0
    for line in lines:
        if not line.strip() and not out:
            continue
        piece = line.rstrip()
        if piece == "" and (not out or out[-1] == ""):
            continue
        if total + len(piece) + 1 > max_chars:
            remaining = max_chars - total
            if remaining > 0:
                out.append(piece[:remaining])
            break
        out.append(piece)
        total += len(piece) + 1
        if len(out) >= max_lines:
            break
    return "\n".join(out).strip()


def collect_events(
    vault: Path,
    *,
    day: dt.date,
    ignore_globs: List[str],
) -> Tuple[List[FileEvent], List[FileEvent]]:
    new_files: List[FileEvent] = []
    updated_files: List[FileEvent] = []

    for path in _iter_markdown_files(vault, ignore_globs):
        created, modified = _get_times(path)
        created_day = created.date() if created else None
        modified_day = modified.date()

        if created_day == day:
            new_files.append(FileEvent(path=path, created_at=created, modified_at=modified))
            continue
        if modified_day == day:
            updated_files.append(FileEvent(path=path, created_at=created, modified_at=modified))

    new_files.sort(key=lambda e: e.modified_at, reverse=True)
    updated_files.sort(key=lambda e: e.modified_at, reverse=True)
    return new_files, updated_files


def render_digest(
    vault: Path,
    *,
    day: dt.date,
    new_files: List[FileEvent],
    updated_files: List[FileEvent],
    preview_lines: int,
    preview_chars: int,
    max_files: int,
) -> str:
    def _render_section(title: str, events: List[FileEvent]) -> List[str]:
        lines: List[str] = [f"## {title}", ""]
        if not events:
            lines.append("- 无")
            lines.append("")
            return lines

        for e in events[:max_files]:
            link = _to_obsidian_link(vault, e.path)
            rel = e.path.relative_to(vault).as_posix()
            m = e.modified_at.strftime("%H:%M")
            c = e.created_at.strftime("%H:%M") if e.created_at else ""
            meta = f"mtime {m}" + (f", ctime {c}" if c else "")
            lines.append(f"### {link}")
            lines.append(f"- path: {rel}")
            lines.append(f"- {meta}")
            try:
                text = e.path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = e.path.read_text(encoding="utf-8", errors="replace")
            preview = _preview_text(text, max_lines=preview_lines, max_chars=preview_chars)
            if preview:
                lines.append("")
                lines.append("```md")
                lines.append(preview)
                lines.append("```")
            lines.append("")
        if len(events) > max_files:
            lines.append(f"- 其余 {len(events) - max_files} 个文件已省略（超过 max-files）")
            lines.append("")
        return lines

    header = [
        f"# Digest ({day.isoformat()})",
        "",
        f"- new: {len(new_files)}",
        f"- updated: {len(updated_files)}",
        "",
    ]
    body = _render_section("今日新建", new_files) + _render_section("今日更新", updated_files)
    return "\n".join(header + body).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=".", help="Vault root directory")
    parser.add_argument("--day", default="", help="YYYY-MM-DD, defaults to today")
    parser.add_argument(
        "--ignore",
        default=".obsidian/**,.opencode/**",
        help="Comma-separated glob patterns to ignore (relative paths)",
    )
    parser.add_argument("--preview-lines", type=int, default=40)
    parser.add_argument("--preview-chars", type=int, default=2500)
    parser.add_argument("--max-files", type=int, default=30)
    parser.add_argument(
        "--write-empty",
        action="store_true",
        help="Write a minimal today.md even if there are no changed files",
    )
    parser.add_argument("--out", default="today.md", help="Output file path, relative to vault")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    day = _parse_day(args.day) if str(args.day).strip() else dt.date.today()
    ignore_globs = [v.strip() for v in str(args.ignore).split(",") if v.strip()]

    new_files, updated_files = collect_events(vault, day=day, ignore_globs=ignore_globs)
    digest = render_digest(
        vault,
        day=day,
        new_files=new_files,
        updated_files=updated_files,
        preview_lines=max(5, int(args.preview_lines)),
        preview_chars=max(200, int(args.preview_chars)),
        max_files=max(1, int(args.max_files)),
    )
    print(digest)

    if new_files or updated_files or args.write_empty:
        out_path = vault / args.out
        minimal = "\n".join(
            [
                "---",
                f"date: {day.isoformat()}",
                "type: daily",
                "---",
                "",
                f"# Today ({day.isoformat()})",
                "",
                "## 总结",
                "",
                "- ",
                "",
                "## 新建",
                "",
                "- ",
                "",
                "## 更新",
                "",
                "- ",
                "",
            ]
        ).rstrip() + "\n"
        out_path.write_text(minimal, encoding="utf-8")
        rel_out = out_path.relative_to(vault).as_posix()
        print(f"Wrote {rel_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
