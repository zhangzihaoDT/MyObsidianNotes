#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
整理一个文档文件夹：
1) 备份（_backup_original*/）
2) 创建分类目录并移动文件
3) 标准化文件名（日期/周报/系列）
4) 对 Markdown 写入/更新 YAML frontmatter：category/created_at/updated_at
5) 生成唯一索引：00_索引/INDEX.md（按最后更新时间降序）

设计原则：
- 默认不触碰 .git 与 _backup_original*
- 仅处理 Markdown（.md/.markdown）
"""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote


CATEGORIES = [
    "00_索引",
    "10_周报与复盘",
    "20_方法论_工作流",
    "30_行业_汽车",
    "40_创作_公众号",
]


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def human_size(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024**2:
        return f"{n/1024:.1f}KB"
    return f"{n/1024**2:.1f}MB"


def fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def url_path(rel_posix: str) -> str:
    return quote(rel_posix, safe="/")


def is_backup_path(rel_posix: str, backup_prefix: str) -> bool:
    return rel_posix == backup_prefix or rel_posix.startswith(backup_prefix + "/") or rel_posix.startswith(backup_prefix + "_")


def is_git_path(rel_posix: str) -> bool:
    return rel_posix == ".git" or rel_posix.startswith(".git/") or "/.git/" in rel_posix


def is_system_path(rel_posix: str) -> bool:
    if rel_posix == ".obsidian" or rel_posix.startswith(".obsidian/"):
        return True
    if rel_posix == ".opencode" or rel_posix.startswith(".opencode/"):
        return True
    if rel_posix == "Templates" or rel_posix.startswith("Templates/"):
        return True
    return False


def strip_ext(name: str) -> Tuple[str, str]:
    p = Path(name)
    return p.stem, p.suffix


def normalize_spaces(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def rename_week(name: str, year: int) -> Optional[str]:
    # W25 复盘.md / W26 规划：一键报告.md
    m = re.match(r"^\s*W(\d{1,2})\s*(.+?)\s*$", strip_ext(name)[0])
    if not m:
        return None
    w = int(m.group(1))
    title = normalize_spaces(m.group(2))
    return f"{year}-W{w:02d} {title}{Path(name).suffix}"


def rename_mmdd_prefix(name: str, year: int) -> Optional[str]:
    # 0618 项目进展.md / 0709项目回顾.md / 0707planning 性能优化.md
    stem, suf = strip_ext(name)
    # 已经是 YYYY-MM-DD 格式时不处理
    if re.match(r"^\d{4}-\d{2}-\d{2}\b", stem):
        return None
    if re.match(r"^\d{4}-W\d{2}\b", stem):
        return None

    m = re.match(r"^\s*(\d{2})(\d{2})\s*(.*)$", stem)
    if not m:
        return None
    mm, dd, rest = m.group(1), m.group(2), m.group(3)
    # 防止误把 2025... 当作 MMDD
    try:
        mm_i, dd_i = int(mm), int(dd)
    except Exception:
        return None
    if not (1 <= mm_i <= 12 and 1 <= dd_i <= 31):
        return None
    rest = normalize_spaces(rest) if rest else ""
    # 如果 rest 为空就保留原名
    if not rest:
        return None
    return f"{year}-{mm}-{dd} {rest}{suf}"


def rename_series_copilot(name: str, year: int) -> Optional[str]:
    # 0714 Copilot工作流.md -> Copilot工作流_2025-07-14.md
    stem, suf = strip_ext(name)
    m = re.match(r"^\s*(\d{2})(\d{2})\s*Copilot工作流\s*$", stem)
    if not m:
        return None
    mm, dd = m.group(1), m.group(2)
    return f"Copilot工作流_{year}-{mm}-{dd}{suf}"


def extract_date_from_filename(name: str) -> Optional[str]:
    # YYYY-MM-DD
    m = re.match(r"^(\d{4}-\d{2}-\d{2})\b", name)
    if m:
        return m.group(1)
    # Copilot工作流_YYYY-MM-DD
    m2 = re.match(r"^Copilot工作流_(\d{4}-\d{2}-\d{2})\b", name)
    if m2:
        return m2.group(1)
    return None


def guess_category(filename: str) -> str:
    f = filename.lower()
    stem = Path(filename).stem
    # 去掉日期前缀（YYYY-MM-DD / YYYY-Wxx）后再判断更稳
    stem2 = re.sub(r"^\d{4}-\d{2}-\d{2}\s+", "", stem)
    stem2 = re.sub(r"^\d{4}-w\d{2}\s+", "", stem2, flags=re.I)
    stem2_l = stem2.lower()

    # 索引类（最终统一放 00_索引/INDEX.md）
    if filename == "INDEX.md" or f == "today.md":
        return "00_索引"
    if stem2 == "欢迎" or "欢迎" in stem2:
        return "00_索引"

    # 周报/复盘
    if re.match(r"^\d{4}-W\d{2}\b", filename) or re.match(r"^W\d{1,2}\b", filename):
        return "10_周报与复盘"
    if any(k in stem2 for k in ["复盘", "规划", "周报", "思考"]):
        return "10_周报与复盘"
    if any(k in stem2_l for k in ["resolution", "年度", "月度", "年终", "复盘节奏"]):
        return "10_周报与复盘"

    # 行业/汽车
    if any(k in stem2 for k in ["汽车", "销量", "量价", "LS6", "车型"]):
        return "30_行业_汽车"

    # 创作/公众号
    if any(k in stem2 for k in ["公众号", "选题", "写作", "标题", "提纲", "大纲", "草稿", "初稿", "定稿", "发布", "推文", "文章"]):
        return "40_创作_公众号"

    # 方法论/工作流
    if any(k in stem2_l for k in ["copilot", "agent", "planning", "工作流", "中枢", "智能中台", "cortex", "cortext"]):
        return "20_方法论_工作流"
    # 一些常见但不带关键词的“项目类总结”
    if any(k in stem2 for k in ["项目进展", "阶段性总结", "项目回顾", "信心", "海内外", "角色分工"]):
        return "20_方法论_工作流"

    return "20_方法论_工作流"


def parse_yaml_frontmatter(text: str) -> Tuple[Optional[Dict[str, str]], str]:
    """
    返回：(yaml_dict_or_none, body_text)
    仅支持最简单的 key: value 行，保留不了复杂 YAML（够用即可）。
    """
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    raw = text[4:end].strip("\n")
    body = text[end + len("\n---\n") :]
    d: Dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_\\-]+)\\s*:\\s*(.*)$", line)
        if m:
            d[m.group(1)] = m.group(2).strip()
    return d, body


def render_yaml_frontmatter(d: Dict[str, str]) -> str:
    keys = list(d.keys())
    # 固定顺序：category/created_at/updated_at 优先
    order = ["category", "created_at", "updated_at"]
    rest = [k for k in keys if k not in order]
    out_keys = [k for k in order if k in d] + sorted(rest)
    lines = ["---"]
    for k in out_keys:
        lines.append(f"{k}: {d[k]}")
    lines.append("---\n")
    return "\n".join(lines)


def upsert_yaml(path: Path, category: str, created_at: str, updated_at: str, dry_run: bool) -> None:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    yaml_d, body = parse_yaml_frontmatter(text)
    if yaml_d is None:
        yaml_d = {}
    # created_at：已有则保留
    if "created_at" not in yaml_d or not yaml_d["created_at"].strip():
        yaml_d["created_at"] = created_at
    yaml_d["updated_at"] = updated_at
    yaml_d["category"] = category
    new_text = render_yaml_frontmatter(yaml_d) + body.lstrip("\n")
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")


@dataclass(frozen=True)
class PlanItem:
    src: Path
    dst: Path
    category: str
    renamed: bool


def build_plan(root: Path, year: int, backup_prefix: str) -> List[PlanItem]:
    items: List[PlanItem] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if is_git_path(rel) or is_backup_path(rel, backup_prefix) or is_system_path(rel):
            continue
        if p.suffix.lower() not in {".md", ".markdown"}:
            continue
        if rel in {"README.md", "AGENTS.md"}:
            continue
        # 只处理根目录或分类目录内的文件；避免重复搬运 index
        # （如果用户重复运行脚本，也能按规则稳定归位）
        filename = p.name

        # 重命名
        new_name = filename
        for fn in (lambda n: rename_series_copilot(n, year), lambda n: rename_week(n, year), lambda n: rename_mmdd_prefix(n, year)):
            cand = fn(filename)
            if cand:
                new_name = cand
                break
        new_name = normalize_spaces(new_name)

        cat = guess_category(new_name)
        if cat not in CATEGORIES:
            cat = "20_方法论_工作流"

        dst = root / cat / new_name
        renamed = (new_name != filename) or (dst.parent != p.parent)
        items.append(PlanItem(src=p, dst=dst, category=cat, renamed=renamed))

    # INDEX 最终统一生成到 00_索引/INDEX.md，不保留其它位置的 INDEX.md
    # 但若存在旧 INDEX.md，会被移动到 00_索引/INDEX.md 的位置并随后被重写
    return items


def safe_backup(root: Path, plan: List[PlanItem], backup_dir: Path, dry_run: bool) -> None:
    if dry_run:
        return
    ensure_dir(backup_dir)
    for it in plan:
        rel = it.src.relative_to(root)
        dst = backup_dir / rel
        ensure_dir(dst.parent)
        shutil.copy2(it.src, dst)


def apply_moves(plan: List[PlanItem], dry_run: bool) -> None:
    # dry-run 不创建目录，不移动
    if dry_run:
        return

    # 先建目录
    for it in plan:
        ensure_dir(it.dst.parent)
    # 冲突检测
    seen = set()
    for it in plan:
        k = it.dst.resolve().as_posix()
        if k in seen and it.src.resolve() != it.dst.resolve():
            raise RuntimeError(f"目标路径冲突：{it.dst}")
        seen.add(k)

    # 执行移动（目标已存在则跳过或报错？选择报错更安全）
    for it in plan:
        if it.src.resolve() == it.dst.resolve():
            continue
        if it.dst.exists():
            raise RuntimeError(f"目标已存在，拒绝覆盖：{it.dst}")
        if dry_run:
            continue
        ensure_dir(it.dst.parent)
        it.src.rename(it.dst)


def regen_index(root: Path, dry_run: bool, backup_prefix: str) -> Path:
    index_path = root / "00_索引" / "INDEX.md"
    rows = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel == "00_索引/INDEX.md":
            continue
        if is_git_path(rel) or is_backup_path(rel, backup_prefix):
            continue
        st = p.stat()
        cat = rel.split("/", 1)[0] if "/" in rel else "-"
        name = p.name
        link = "./" + url_path(rel)
        rows.append((st.st_mtime, f"| {fmt_ts(st.st_mtime)} | `{cat}` | [{name}]({link}) | {p.suffix.lower().lstrip('.') or '-'} | {human_size(st.st_size)} |"))
    rows.sort(key=lambda x: x[0], reverse=True)

    content = []
    content.append("# INDEX\n")
    content.append("仅保留这一份索引文件，作为整个文件夹的目录入口。\n\n")
    content.append("## 按最后更新时间（降序）\n\n")
    content.append("> 时间为文件系统记录的“最后修改时间”。\n\n")
    content.append("| 最后更新时间 | 分类 | 文件 | 类型 | 大小 |\n")
    content.append("|---|---|---|---:|---:|\n")
    for _, line in rows:
        content.append(line + "\n")

    if not dry_run:
        ensure_dir(index_path.parent)
        index_path.write_text("".join(content), encoding="utf-8")
    return index_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="目标根目录（要整理的文件夹）")
    ap.add_argument("--year", type=int, default=2025, help="补全年份（用于 0618/0709/W25 等场景）")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不做改动")
    ap.add_argument("--skip-yaml", action="store_true", help="跳过 YAML 写入/更新")
    ap.add_argument("--backup-dir", default="_backup_original", help="备份目录前缀（默认 _backup_original）")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"root 不是有效目录：{root}")

    # 1) 生成计划
    plan = build_plan(root, args.year, args.backup_dir)

    # 2) 备份目录（若已存在且非空，创建带时间戳的备份目录）
    backup_dir = root / args.backup_dir
    if backup_dir.exists() and any(backup_dir.iterdir()):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = root / f"{args.backup_dir}_{ts}"

    # 3) 打印计划
    print(f"[PLAN] root={root}")
    print(f"[PLAN] backup_dir={backup_dir.name}")
    changes = [it for it in plan if it.src.resolve() != it.dst.resolve()]
    print(f"[PLAN] 将处理文件数：{len(plan)}，其中需移动/重命名：{len(changes)}")
    if args.dry_run:
        for it in changes[:200]:
            print(f"- {it.src.relative_to(root)}  ->  {it.dst.relative_to(root)}")
        if len(changes) > 200:
            print(f"... 还有 {len(changes)-200} 条变更未展示")

    # 4) 备份
    safe_backup(root, plan, backup_dir, args.dry_run)
    print("[DRY-RUN] 跳过备份写入" if args.dry_run else "[OK] 备份完成")

    # 5) 移动/重命名
    apply_moves(plan, args.dry_run)
    print("[DRY-RUN] 跳过移动/重命名" if args.dry_run else "[OK] 移动/重命名完成")

    # 6) YAML 打标（基于移动后的路径）
    if not args.skip_yaml:
        for it in plan:
            dst = it.dst if it.dst.exists() or args.dry_run else it.dst
            # created_at：优先从文件名日期推断，否则用 mtime
            st = (it.dst if not args.dry_run else it.src).stat()
            inferred = extract_date_from_filename(it.dst.name)
            created_at = f"{inferred} 00:00" if inferred else fmt_ts(st.st_mtime)
            updated_at = fmt_ts(st.st_mtime)
            # dry-run 下不写入
            if args.dry_run:
                continue
            if it.dst.exists():
                upsert_yaml(it.dst, it.category, created_at, updated_at, dry_run=False)
        print("[OK] YAML 打标完成")
    else:
        print("[SKIP] YAML 打标已跳过")

    # 7) 重建 INDEX
    index_path = regen_index(root, args.dry_run, args.backup_dir)
    if args.dry_run:
        print(f"[DRY-RUN] 将生成 INDEX：{index_path.relative_to(root)}")
    else:
        print(f"[OK] INDEX 生成完成：{index_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
