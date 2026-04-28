# MyObsidianNotes

这是一个 Obsidian 笔记库（Vault），用于记录与整理日常学习、工具使用与思考笔记。

## 项目结构

- 根目录：以 Markdown 笔记为主
- `Templates/`：模板文件（例如卡片模板）
- `.obsidian/`：Obsidian 配置（核心插件开关、社区插件、主题等）
- `.opencode/`：与 OpenCode/Agent 相关的命令、skills 与脚本工具
- `.gitignore`：忽略容易产生多设备冲突的本地状态文件（例如 workspace）

## 项目特点

- 这是笔记库，不是传统软件项目：没有 `src/`、`package.json`、测试/CI 等工程结构
- 以 Obsidian 的 `[[双链]]` 组织知识网络，而不是依赖复杂目录分层
- 配置与同步策略偏“可复现 + 少冲突”：纳入必要的 `.obsidian/` 配置，同时忽略 `workspace.json` 等状态文件
- 具备轻量自动化能力：通过 `.opencode/` 内的工具脚本生成/维护日常摘要（例如 `today.md`）

## 使用方式

1. 安装 Obsidian：https://obsidian.md/
2. 将仓库克隆到本地：

```bash
git clone https://github.com/zhangzihaoDT/MyObsidianNotes.git
```

3. 在 Obsidian 中选择「打开文件夹作为仓库」，打开克隆后的目录即可。

## 说明

- 笔记以 Markdown 为主，内部链接使用 Obsidian 的 `[[双链]]` 语法。
- 仓库包含 `.obsidian/` 配置，用于跨设备保持主题/插件/设置一致。

## 同步（Git）

常用同步流程：

```bash
git pull --ff-only
git add -A
git commit -m "更新笔记"
git push
```
