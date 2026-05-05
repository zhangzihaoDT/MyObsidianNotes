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

## 使用方式

1. 安装 [Obsidian](https://obsidian.md/)
2. 克隆仓库：

```bash
git clone https://github.com/zhangzihaoDT/MyObsidianNotes.git
```

3. 在 Obsidian 中「打开文件夹作为仓库」，选择克隆目录
4. **轻量自动化** — 通过 `.opencode/skills/` 生成/维护日常摘要等笔记

## 同步

```bash
git pull --ff-only
git add -A
git commit -m "更新笔记"
git push
```
