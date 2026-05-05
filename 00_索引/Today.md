# Digest (2026-04-27)

- new: 7
- updated: 0

## 今日新建

### [[Opencode 安装]]

- path: 20*方法论*工作流/Opencode 安装.md
- mtime 16:43, ctime 16:00

```md
结论先说清楚：

> **OpenCode 建议"全局安装 + 项目内配置"，而不是二选一。**

单纯放全局或单纯放项目，都不是最优解。

---

# 一、为什么不能只选一个？

## ❌ 只全局安装的问题

优点：

- 到处能用（CLI 很方便）

但问题是：

- ❌ 不同项目的 Agent / skills 会冲突

- ❌ 配置不可复现（换机器就废）

- ❌ 无法版本化（你后面一定会踩坑）

---

## ❌ 只项目安装的问题

优点：

- 可控、可复现

但问题是：

- ❌ 使用成本高（每个项目都要装）

- ❌ 不适合 CLI 工具的"随手调用"场景

- ❌ 失去"操作系统"的感觉
```

### [[AGENTS]]

- path: AGENTS.md
- mtime 16:30, ctime 16:30

```md
# AGENTS.md

## Repo type

Obsidian vault (Markdown notes), not a software project. No `package.json`, tests, CI, linters, or formatters.

## Language

All note content is in **Chinese (中文)**. Reply in Chinese when discussing notes.

## Obsidian specifics

- Wiki-style links: `[[Note Name]]`
- Embeds: `![[image.png]]` or `![[Note]]`
- Config is in `.obsidian/` — do not modify unless asked.
- Community plugins: `terminal`, `apple-books-import-highlights`
- Theme: Things; Obsidian Sync enabled.

## Git

No commits yet. Init with `git add -A && git commit -m "initial commit"` when asked.
```

### [[在Obsidian 中调用 claude 这样 AI 工具]]

- path: 20*方法论*工作流/在Obsidian 中调用 claude 这样 AI 工具.md
- mtime 16:00, ctime 10:42

```md
不是"在 Obsidian 里用 AI"
✅ 而是"让 Obsidian 成为 Agent 系统的 UI"

但是 Claude code 需要账号，codex 也要花钱
所以，想到了[[OpenCode#和 codex、cc 的差异]]
```

### [[OpenCode]]

- path: 20*方法论*工作流/OpenCode.md
- mtime 15:54, ctime 15:45

```md
如何发现？
A：DeepSeek 的介绍中（https://api-docs.deepseek.com/zh-cn/guides/coding_agents）

[**OpenCode**](https://opencode.ai/) 是一个开源的 AI 编码代理。它提供终端界面、桌面应用和 IDE 扩展等多种使用方式（https://opencode.ai/docs/zh-cn/）

## 和 codex、cc 的差异

**Codex / Claude Code（封闭型 Agent）**

**OpenCode（开放型 Agent OS）**

CLI（OpenCode）
↓
Agent Runtime（可改）
↓
Model（你选：DeepSeek / GPT / Claude）
↓
Tools / Skills（你定义）

==Codex / Claude Code 是"别人写好的 Agent"， OpenCode 是"让你自己写 Agent 的操作系统"。==
```

### [[Pinkoi]]

- path: Pinkoi.md
- mtime 11:08, ctime 10:54

```md
亚洲设计跨境平台
![[Pasted image 20260427110734.png]
```

### [[Instapaper readwise ibooks]]

- path: 20*方法论*工作流/Instapaper readwise ibooks.md
- mtime 10:52, ctime 10:16

```md
## 差异

- Instapaper：网页为主
- Readwise：**全格式（最强）**
- Apple Books：书

## 和 Obsidian 的关系

信息（网页/书/PDF）
↓
Instapaper / Apple Books
↓
Readwise（高亮 + 标签 + 复习）
↓
Obsidian（结构化 + 连接 + 创造）

## 推荐使用方法

Level 1（基础）：Readwise → Obsidian 自动同步

## 知识管理的三层

将"自动同步"理解为
1️⃣ 捕获（Capture）：cubox、Feedly、Web Clipper、readwise
2️⃣ 同步（Sync）：Zapier / n8n、Cubox ⚠️（半自动）
3️⃣ 再利用（Reuse）（决定上限）：Readwise ✅（复习 + 高亮系统）Obsidian ✅（结构化）
```

### [[欢迎]]

- path: 00\_索引/欢迎.md
- mtime 10:15, ctime 10:15

```md
这是你的新*仓库*。

写点笔记，[[创建链接]]，或者试一试[导入器](https://help.obsidian.md/Plugins/Importer)插件!

当你准备好了，就将该笔记文件删除，使这个仓库为你所用。
```

## 今日更新

- 无
