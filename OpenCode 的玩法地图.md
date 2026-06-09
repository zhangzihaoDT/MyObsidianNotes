#定位 ：一个 **开源 coding harness**，而不是一个简单的代码补全工具。

1、模型接入：运行 opencode 后输入 /connect，选择 deepseek，填入 API Key，再选择 DeepSeek-V4-Pro 模型。可玩点：不被单一模型锁死。它可以接不同 provider

2、模型档位调度：Default / Low / Medium / High / Max：任务分层；
这背后其实是一个原则：不是所有 coding 任务都值得用最高推理成本。

3、多Agents 配置
OpenCode 支持配置专门的 agents。官方文档说 agents 是 specialized AI assistants，可以配置 custom prompts、models 和 tool access；也可以在 session 中切换 agent，或者用 `@` mention 调用。

4、上下文配置：针对某个项目写 AGENTS.md
上下文文件：用 `/init` 生成或更新 `AGENTS.md`

5、工具调用：OpenCode 支持 MCP，可以把本地或远程 MCP server 中的工具暴露给 agent 使用。

6、Session 工作流