#G老师 

## v0.4.5 Composition / Share 能力补齐

v0.4 Evidence-driven Agentic BI Runtime  
	✅ State-first  
	✅ Structured Result Blocks  
	✅ Fact Extraction  
	✅ Evidence Contract  
	✅ Runtime Decision  
	✅ Grounded Summary  
  
v0.4.5 Composition / Share 能力补齐  
- share_by_dimension  
- share_by_time_dimension  
- topn_share  
- cumulative_share  
  
v0.5 Eval-driven Stabilization  
- 30~50 条 BI 问题评测集  
- plan_accuracy  
- evidence_sufficiency  
- premature_finish_rate  
- answer_grounded_rate  
  
v0.6 Query Log -> DSL Prior  
- 人工 review query log  
- 抽象 question pattern  
- 沉淀 planner examples  
- 暂不自动学习  
  
v0.7 Multi-step Diagnosis Agent  
- 趋势异常  
- 贡献拆解  
- 结构变化  
- 自动生成诊断链路  
  
v0.8 Visualization & Report Blocks  
- table block  
- chart spec block  
- insight block  
- 飞书 / HTML / PPT 输出  
  
v1.0 Stable Agentic BI Copilot

## v0.4 Evidence-driven Agentic BI Runtime

目标：  
让 Agent 不再依赖 LLM 自主判断“是否查够”，而是基于结构化证据判断是否继续执行或结束回答。  
  
核心能力：  
- State-first：AgentState 作为统一运行时状态容器  
- Structured Result Blocks：工具执行结果结构化  
- Normalized Facts：从执行结果中沉淀可判断事实  
- Evidence Contract：定义不同分析意图所需证据  
- Runtime Decision：基于 facts + contract 决定 run_dsl / finish  
- Grounded Summary：最终回答基于已有证据，不做无依据推断

路线图更新：
v0.1：自然语言 -> SQL -> 答案  
- LLM 直接生成 SQL  
- 查询结果交给 LLM 总结  
- 能跑，但不稳定  
  
v0.2：自然语言 -> DSL -> 答案  
- PlanningAgent 生成 DSL  
- Tool Router 执行 DSL  
- SQL 生成从自由文本转向结构化计划  
  
v0.3：Agent Loop + Tool Router + Result Blocks  
	✅ Agent Loop  
	✅ Tool Router  
	✅ legacy result_blocks  
	✅ Query / Comparison / Statistics / Fast Path 初步路由  
  
v0.4：Evidence-driven Agentic BI Runtime  
	✅ AgentState 分层：loop / planning / results / memory / final  
	✅ Structured Result Blocks  
	✅ Normalized Facts v1  
	✅ Evidence Contract  
	✅ Runtime Decision  
	✅ trend_summary 闭环  
	✅ diagnosis: trend_summary + contribution_summary 两步闭环  
	✅ Grounded Summary 约束  
  
v0.5：Planner Prior / Query Log 经验沉淀  
	⬜ Query Log append-only  
	⬜ Successful Case Filter  
	⬜ Question Pattern Extraction  
	⬜ Planner Prior YAML / JSONL  
	⬜ PlanningAgent 检索相似 pattern 后再生成 DSL  
  
v0.6：**Analysis Strategy 多轮分析策略**  
	⬜ trend / compare / ranking / composition / diagnosis / forecast 策略注册  
	⬜ intent -> required facts -> next action  
	⬜ 多轮任务链条模板化  
	⬜ diagnosis 不再只拆一个维度，而是可选择渠道 / 区域 / 车型 / 门店等维度  
  
v0.7：Advanced Diagnosis 诊断型 Agent  
	⬜ 趋势异常自动触发拆解  
	⬜ 贡献拆解 + 异常检测 + 对比基准  
	⬜ 区分描述性贡献、相关性、因果假设  
	⬜ 支持多维度归因候选排序  
  
v0.8：Visualization / Report Generation  
	⬜ chart_block  
	⬜ table_block  
	⬜ insight_block  
	⬜ Markdown / HTML / 飞书卡片输出  
	⬜ 自动生成分析报告  
	  
v1.0：稳定的 Agentic BI Copilot  
	⬜ 可复现  
	⬜ 可追溯  
	⬜ 可扩展  
	⬜ 可沉淀经验  
	⬜ 支持多业务指标与多分析场景

## Base

v0.1：自然语言 -> SQL -> 答案
v0.2：自然语言 -> DSL -> 答案
v0.3：Agent Loop + Tool Router + Result Blocks
	✅ v0.3.1 State Schema 固化  
	✅ v0.3.2 Structured Result Block  
	✅ v0.3.3 structured_blocks 落 state  
	✅ v0.3.4 facts extractor 接入 structured_blocks  
	✅ v0.3.5 runtime_decision 接入 should_continue  规则化
	✅ v0.3.6 diagnosis 两步分析闭环
v0.4：StatisticsTool / Operators / Fast Path 稳定化
v0.5：Query Log -> Planner Examples 自动沉淀
v0.6：Analysis Intent -> 多轮分析策略
v0.7：诊断型 Agent：趋势异常后自动拆解原因
v0.8：可视化与报告生成
v1.0：稳定的 Agentic BI Copilot

你现在差不多在：

```
v0.3 ~ v0.4
```

非常好的位置。

----

- 不是在做“SQL Agent”，而是在做一个小型 **Agentic BI Runtime**。
- 不是让 LLM 每次重新“聪明地分析”，  而是让系统把成功分析路径沉淀下来，  下次用更确定、更低成本、更可复现的方式完成。




