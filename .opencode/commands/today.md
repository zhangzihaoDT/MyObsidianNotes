---
description: 生成 today.md（汇总今日新建/更新的笔记）
agent: build
subtask: true
---

先执行脚本，收集今天新建/更新的 Markdown 文件并输出摘要（脚本会写入一个 today.md 骨架）：

!`python3 .opencode/tools/today.py --write-empty`

基于上面的摘要与片段，完成 today.md：

- 用中文写「今天都做了什么」的总结（3-7 条要点）
- 分别列出「新建」与「更新」的笔记（使用 Obsidian 链接）
- 每个笔记补一行你从内容里提炼出的要点（必要时再读取对应文件，不要臆测）
