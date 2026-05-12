
## 核心生产环境：DeepSeekV4 API 

### 编程IDE：TRAE Pro

一般情况下就开 auto 模式

### 知识管理：Obsidian

使用 opencode ，通过 terminal 插件调用 DeepSeek flash 辅助整理笔记

Flomo 退居一线，主力承担灵感的记录，在手机上使用，从场景上区隔工具使用

### 自定义 Agent

重头戏，逐渐把自己的工作全部搬到这个 Agent 中，让他负责我的工作，他的任务很简单，就是替代我赚工资。所有工作中遇到的事情都应该在这个项目中完成。

自动化配置：

- Worker 算力中心：闲置的一台 Mac（0 元），虽然是 Intel core i5 芯片+16G 内存
- Gateway：作用是云端跳板
	- A. FRP 公网入口｜sealos 上部署 frp 服务，把请求转发到 Worker
	- B. 飞书（WebSocket 长连接）入口｜内部工作流的协作群聊天机器人
- Docker，启动服务
	- 在本地暴露端口，承担实际计算与服务运行
- 24 小时不中断的电源和网络，薅公司羊毛；可能和其他人不同，我这种 24 小时干活的机器我觉得应该放在公司，而是不是家里。


## 思考工作台：ChatGPT Plus 

### 采用的是中国用户使用美区 AI 服务的经典方案

| 项目        | 配置                  |
| --------- | ------------------- |
| 主 iCloud  | 中国区                 |
| App Store | 美区小号                |
| 支付        | Apple Gift Card（美区） |
| 余额        | 长期保持 50 USD 左右      |
礼品卡购买渠道：SEAGM（https://www.seagm.com/）

在华人圈使用很多

为什么不是 Amazon？

| 渠道        | 稳定性  |
| --------- | ---- |
| Amazon    | 中等   |
| ==SEAGM==     | ==高==    |
| OffGamers | 高    |
| G2A/Eneba | 中等偏低 |

Amazon 最大问题不是不能买，而是：  
“风控随机”。


## 成本清单

TRAE Pro（20/月）
DeepSeek API（10/月）
ChatGPT Plus （20$/月）
Sealos frp服务（0.78/天）
Flomo（99/年）
Obsidian（0 元）



