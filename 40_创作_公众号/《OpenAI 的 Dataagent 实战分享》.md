# OpenAI 的 data agent 实践

- 定位：专属定制内部 AI 数据智能体
  - 产品替代选择：OpenAI 的数据平台
  - 面向3,500 多名内部用户，面向 600PB 数据、7 万个 dataset
  - Slack / IDE / ChatGPT / CLI 多入口
- How：Codex（GPT5.5）、Evals API⁠ 和 Embeddings API⁠
- 数据分析师的职责
  - 应该是：定义指标、验证假设和制定数据驱动的决策。
  - 而不是调试 SQL 语义或查询性能
- 工作原理
  - 智能体由 GPT‑5.2 驱动
  - 流程：从用户提出复杂的开放式问题，到分析-数据-查询-图表
    - 自动：找表，理解 schema，调试查询，做分析，利用 memory 学习组织上下文
    - 不是SELECT ...
    - 而是NL→ DSL / semantic plan语义推理→ controlled runtime 运行编排→ query compiler 查询编译→ execution 查询执行
  - 原文强调：Codex reads pipeline code

  原文链接：[openai.com...](https://openai.com/zh-Hans-CN/index/inside-our-in-house-data-agent/)
