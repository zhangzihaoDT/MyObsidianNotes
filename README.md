# MyObsidianNotes

个人 Obsidian 笔记库，用于记录与整理日常学习、工具使用与思考笔记。

## 项目结构

```
├── 📝 *.md               # 笔记本体（Markdown）
├── Templates/             # 模板文件（卡片笔记模板等）
├── .obsidian/             # Obsidian 配置（插件、主题、设置）
├── .opencode/             # OpenCode Agent 命令与技能
└── .gitignore             # 忽略 workspace 等本地状态文件
```

## 特点

- **纯笔记库** — 非软件项目，无 `src/`、`package.json`、测试/CI
- **双链驱动** — 以 Obsidian `[[双链]]` 组织知识网络，而非目录分层
- **配置可复现** — `.obsidian/` 纳入版本控制，跨设备保持主题/插件一致；`workspace.json` 等本地状态文件被 `.gitignore` 排除，减少同步冲突
- **轻量自动化** — 通过 `.opencode/skills/` 生成/维护日常摘要等笔记

## 使用方式

1. 安装 [Obsidian](https://obsidian.md/)
2. 克隆仓库：

```bash
git clone https://github.com/zhangzihaoDT/MyObsidianNotes.git
```

3. 在 Obsidian 中「打开文件夹作为仓库」，选择克隆目录

## 同步

```bash
git pull --ff-only
git add -A
git commit -m "更新笔记"
git push
```
