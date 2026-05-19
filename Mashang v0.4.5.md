#G老师 ，迭代路径图

## v0.5 Eval-driven Stabilization

目标：从 10-case 手工验证升级为稳定自动回归。

- 30~50 条 BI 问题评测集	
- plan_accuracy	
- evidence_sufficiency	
- premature_finish_rate	
- answer_grounded_rate

建议评测层：

| 评测项                   | 含义                  |
| --------------------- | ------------------- |
| intent_accuracy       | intent 是否识别正确       |
| plan_accuracy         | DSL 是否正确            |
| tool_route_accuracy   | 是否路由到正确工具           |
| fact_recall           | required facts 是否抽出 |
| fact_precision        | 是否过多抽出无关 facts      |
| evidence_sufficiency  | required facts 是否满足 |
| premature_finish_rate | 是否过早 finish         |
| answer_grounded_rate  | 回答是否只基于 evidence    |

核心目标：

```
从“能跑通”升级为“稳定不退化”
```

### v0.4.6 — Runtime Decision / Fact Extraction 稳定化

**Agent Loop 空转修复**：`memory_extractor` 三处缺陷导致 query block 始终抽不出 facts → loop 空跑 5 步

- `_DATA_EXCLUDE` 误过滤 `"series"` 维度列 → `dim_cols=[]` → 无 dimension_breakdown

- `tool_router.py` 默认路径调用 `execute_analysis()` 返回 string 而非 DataFrame → `cols=[]`

- `share_summary` 缺少 raw count → 占比的确定性 fallback 计算

### v0.4.5 — 数据集更新 Fast Path

明确触发"数据更新并同步"时连续调用 `skills_order_observation_daily.py`
否则，仅数据更新。

### v0.4.4 MultiTable / Lookup Metric 能力补齐

目标：实现订单表和选配表的打通，比如：“LS8 地暖5座6座的选装率分别是多少？（上市至今）”

- 主表过滤  
- ID 集合提取  
- 子表 lookup  
- merge 回主表  
- group_by ratio

典型问题（用于回测）

- CM2增程 2026 年 1 月 1 日至今，Thor 的选装率
- CM2 激光雷达选装率
- LS8 部分同车型的线控选装率
- LS8 不同轮毂的选装比例
- LS9 不同车型（product_name）的轮毂占比

全部通过 ✅
#	查询	类型
1	CM2增程 2026-01-01至今 Thor选装率	attribute_penetration
2	CM2 激光雷达选装率	attribute_penetration
3	LS8 部分同车型的线控选装率	attribute_penetration
4	LS8 不同轮毂的选装比例	attribute_distribution
5	LS9 不同车型的轮毂占比	attribute_distribution
三个路由路径全部覆盖到：
- attribute_penetration（二值选装率）→ Q1/Q2/Q3
- attribute_distribution（多值分布/share）→ Q4/Q5
- value_contains（variant 模糊匹配）→ Q1

### v0.4.3 Deterministic Fact Builder  

目标：让 required facts 尽量由代码确定性生成，而不是依赖 LLM 抽取。
  
- ✅ _make_fact  
- ✅ column-based summary facts  
- ✅ block_type handlers  
- ✅ _FALLBACK_HINTS  
- ✅ gap-filling  
- ✅ 10-case 回归通过  
  
已覆盖标准 fact types：  
  
- metric_value  
- time_grouped_metric  
- trend_summary  
- comparison_result  
- dimension_breakdown  
- share_summary  
- ranking_result  
- distribution_summary  
- contribution_summary

### v0.4.2 Evidence Contract Template Library  

目标：让 Runtime 知道不同 BI 问题分别需要什么证据。

- ✅ 9 类 analysis intent：metric / trend / compare / composition / share / time_grouped_share / ranking / distribution / diagnosis  
- ✅ required_fact_types 标准化  
- ✅ repair_query_template  
- ✅ infer_intent_from_question 优先级重写  
- ✅ evaluate_state_readiness 统一走 contract missing 判断  

### v0.4.1 Composition / Share 能力补齐  

目标：把“构成 / 占比 / 份额”从通用 QueryTool 中抽象为稳定 BI 能力。

✅ CompositionTool  
✅ share_by_dimension  
✅ weekly_share_by_dimension  
✅ monthly_share_by_dimension  
✅ topn_share  
✅ cumulative_share  
✅ plan.analysis_intent.type == "share_breakdown" 路由

## v0.4 Evidence-driven Agentic BI Runtime

核心目标：从 `has_result -> finish` 升级为 `has_required_evidence -> finish`。

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




