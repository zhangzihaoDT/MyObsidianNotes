---
name: doc-folder-tagger
description: 为本地文档/笔记文件夹执行“分类标签归档 + 标准化命名 + YAML 头部打标（分类/创建时间/最后更新时间）+ 生成唯一索引”。当用户提到“整理文件夹/打标/分类/归档/重命名/命名规范/加 YAML frontmatter/生成 INDEX”时使用。
---

# 目标

把一个“杂乱的文档文件夹”整理成固定结构，并给 **Markdown** 文档写入 YAML 头部信息：

- `category`: 分类目录名（如 `20_方法论_工作流`）
- `created_at`: 创建时间（若已存在则保留）
- `updated_at`: 最后更新时间（使用文件系统 mtime 写入/刷新）

同时生成唯一索引：`00_索引/INDEX.md`（按 `updated_at`/mtime 降序）。

# 约定（默认规则）

分类标签与命名规则见：`references/rules.md`。

**默认忽略：**
- `_backup_original*/`（备份目录）
- `.git/`（如果存在）

# 推荐工作流

1. **确认目标根目录**：用户选中的文件夹路径（通常就是 workspace 根）。
2. **先备份**：脚本会自动创建 `_backup_original/`（若已存在会自动创建带时间戳的备份目录）。
3. **执行整理（移动 + 重命名 + YAML 打标 + 重建 INDEX）**：

```bash
python3 scripts/organize_and_tag.py --root "<目标文件夹>" --year 2025
```

常用参数：
- `--dry-run`：只打印计划，不做任何改动
- `--backup-dir _backup_original`：自定义备份目录名
- `--skip-yaml`：只做分类/命名，不写 YAML

# YAML 写入规则（Markdown）

- 若文件开头没有 YAML frontmatter（`---`），则插入一段新的
- 若已有 YAML frontmatter：更新/补齐 `category/created_at/updated_at`，保留其他字段

> 注意：脚本不会尝试“语义理解全文”，分类主要基于文件名关键词与已知模式（可按需在脚本里扩展映射）。

