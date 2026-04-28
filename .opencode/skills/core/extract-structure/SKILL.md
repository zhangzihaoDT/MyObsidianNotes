---
name: extract-structure
description: 从一篇 Obsidian 笔记中提取结构（标题层级/列表/关键段落）并输出大纲
compatibility: opencode
---

## 你要做什么

- 识别笔记的标题层级（H1-H4 为主）
- 提取每个章节的核心句与要点列表
- 输出可作为目录/大纲的结构化结果

## 输出格式

- 1 份分层大纲（使用缩进列表）
- 每个一级标题下：最多 3 条要点

## 约束

- 保留 Obsidian 链接格式（如 [[Note]]、![[image.png]]）
- 不发明原文不存在的章节或要点
