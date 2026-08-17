---
created: 2026-08-13
---
## 1. takenotes

承接：[[Effective Reasoning Horizon（有效推理跨度）]]、[[Agent 独立运行 6 小时意味着什么]]

给 MIIT 这个 Agent-friendly environment 一个更完整的定义：

> 一个拥有明确事实模型、稳定边界、可执行工具、持久状态、自动反馈、异常恢复和明确验收条件的任务环境。

它实际上已经具备了六个组成部分：

- **Knowledge**：README / schema / pipeline / rules
- **Tools**：scripts / parser / extractor / Makefile
- **State**：source files / canonical / summaries / git
- **Feedback**：tests / reconciliation / validation
- **Recovery**：fallback extractor / retry / legacy evidence
- **Goal**：canonical contract / acceptance criteria

这六样东西放在一起以后，Agent 才能真正"待在里面工作"。

### 一句话抽象

> Agent-friendly 不是让代码更容易被 AI 阅读，而是让环境能够不断告诉 Agent：你在哪里、发生了什么、下一步能做什么、做完以后对不对。

这也是为什么 6h08m 不主要是模型能力的结果。

### 对照：没有轨道的环境

如果同一个模型放进一个没有文档、没有测试、目录混乱、输出不可验证的 repo，可能 30 分钟就开始漂移；而 MIIT 给了它一条可以不断闭环的"轨道"。

### MIIT 像一个认知操作系统

- **filesystem** 是长期记忆
- **schema** 是世界模型
- **scripts** 是行动能力
- **tests** 是感知反馈
- **git** 是时间与恢复机制
- **canonical** 是共同现实
- **acceptance criteria** 是任务终止条件

这才是这次工程实践最值得沉淀的 Agent engineering 资产。

## 2. keywords

- Agent-friendly environment、Knowledge、Tools、State、Feedback、Recovery、Goal

## 3. source

MIIT 实践总结（与 [[Effective Reasoning Horizon（有效推理跨度）]] 同源）
