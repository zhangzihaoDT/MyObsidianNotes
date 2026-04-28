---
name: build-note
description: 基于已有素材（要点/结构/洞察）生成可直接写入 Obsidian 的成稿笔记
compatibility: opencode
---

## 你要做什么

- 根据用户给定的主题与素材，组织成一篇可读的笔记
- 用合适的标题层级拆分段落，并补齐必要的过渡说明
- 生成可复用的模板化区块（如 source / takenotes / keywords）

## 输出格式

- 1 篇 Markdown 笔记（含标题结构）
- 末尾提供：keywords 列表（3-8 个）

## 约束

- 保留 Obsidian 链接格式（如 [[Note]]、![[image.png]]）
- 不引入无法从素材推导出的事实性信息
