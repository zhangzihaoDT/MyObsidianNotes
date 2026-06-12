# OpenCode 的六大玩法地图

定位：一个 **开源 coding harness**，而不是一个简单的代码补全工具。

## 1、模型接入

运行 `opencode` 后，可以输入：

```text
/connect
```

然后选择 `deepseek`，填入 API Key，再选择 `DeepSeek-V4-Pro` 模型。

这个功能的可玩点在于：OpenCode 不被单一模型锁死。它可以接入不同 provider，同一个 coding harness 可以根据任务需要切换不同模型。

## 2、模型档位调度

OpenCode 里有 `Default / Low / Medium / High / Max` 这样的模型档位选择，可以理解为一种任务分层方式。

不同任务可以使用不同档位：

```text
Low：读代码 / 写文档
Medium：小改动 / 小 bug
High：多文件联动 / 模块级重构
Max：核心架构 / 高价值任务
```

这背后的原则是：

> 不是所有 coding 任务都值得用最高推理成本。

## 3、多 Agents 配置

OpenCode 支持配置专门的 agents。

官方文档中，agents 是 specialized AI assistants，可以配置 custom prompts、models 和 tool access；也可以在 session 中切换 agent，或者用 `@ mention` 调用。

例如：

```text
@planner
@coder
@tester
@reviewer
```

这样就可以把一次开发任务拆成不同角色：

```text
先规划
再实现
再测试
再审查
```

多 Agents 的实操不是为了“同时叫很多 AI”，而是把开发过程拆成不同权限、不同职责的角色：规划者少动手，执行者只做最小修改，测试者只验证，审查者只看风险。

## 4、上下文配置

针对某个项目，可以写 `AGENTS.md`。

也可以在 OpenCode 中通过：

```text
/init
```

生成或更新 `AGENTS.md`。

`AGENTS.md` 的作用，是把这个 workspace 的长期规则写下来，例如项目结构、开发原则、常用命令、测试入口等。它相当于这个项目的长期上下文文件。

## 5、工具调用：MCP + Skills

OpenCode 的工具调用主要可以理解为两部分：

```text
MCP：把外部工具接进来
Skills：把可复用方法沉淀下来
```

MCP 可以把本地或远程 MCP server 中的工具暴露给 agent 使用。

例如：

```text
接浏览器 MCP：
让 agent 能访问网页或内部系统

接 GitHub MCP：
让 agent 能查 issue / PR / repo 信息
```

Skills 是自定义的。放在全局目录下，就是全局共用；放在项目目录下，就是 workspace 专属。

```text
~/.config/opencode/skills/
= 全局 skills

.opencode/skills/
= 当前 workspace 专属 skills
```

一个 workspace 中可以形成这样的结构：

```text
workspace/
├── AGENTS.md
└── .opencode/
    └── skills/
        └── runtime-eval-diagnosis/
            └── SKILL.md
```

对应关系是：

```text
AGENTS.md = workspace 的长期驾驶手册
SKILL.md = 某类任务的专门打法
Session = 一次具体任务过程
```

## 6、Session 任务线

在 OpenCode 中，可以通过：

```text
Ctrl+P → Sessions
```

打开历史 session 列表。

选择一个 session 后，会回到那条 session 的完整对话和任务轨迹，并且可以继续在它后面追加新指令。

所以 Session 不是只保留上一轮最后一句话，而是一条完整的任务线。

例如：

```text
Session A：runtime eval 诊断
Session B：模块级重构
Session C：README 更新
Session D：release curve 脚本生成
```

每一个 session 都可以对应一次具体任务过程。
