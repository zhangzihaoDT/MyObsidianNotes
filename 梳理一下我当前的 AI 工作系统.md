
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

工作不是一天就能做完的，也不是一成不变的，因此自定义的Agent的目标是不断提升单位token的使用价值；不是越来越“聪明”，  而是让系统把成功路径沉淀下来，  下次用更确定、更低成本、更可复现的方式完成。

永远不要认为Agent能对你完全替代，如果你在工作中的价值是1，那么这个agent能完成的永远都是0.999；

因为LLM没有欲望，没有不满，“诉求来自人的欲望，方向来自人的不满足。AI 是引擎，但引擎不会自己决定去哪”。

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

### 如何获取一个美区ID？

建议走**合规注册新账号**，不要买淘宝/共享/来路不明的美区 Apple ID，风险是被锁号、余额损失、隐私泄露

新注册一个美区 Apple ID

步骤：

1. 进入 Apple 官网注册 Apple Account
2. 国家/地区选择 **United States**
3. 使用一个未注册过 Apple ID 的邮箱
4. 手机号可以用中国手机号接验证码
5. 注册完成后，在 iPhone 上只切换 **App Store 账号**，不要切换 iCloud 主账号  
    路径：  
    **设置 → 你的头像 → 媒体与购买项目 → 退出登录 → 登录美区 Apple ID**

Apple 官方说明里，创建新 Apple Account 可以通过 App Store 完成；修改国家/地区也可以在 account.apple.com 的 Personal Information 里操作。


## 成本清单

TRAE Pro（20/月）
DeepSeek API（10/月）
ChatGPT Plus （20$/月）
Sealos frp服务（0.78/天）
Flomo（99/年）
Obsidian（0 元）


如果你也对上述内容感兴趣，并且想把这一套东西都搬回自己家的话，可以加我微信


