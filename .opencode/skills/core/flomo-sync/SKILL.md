---
name: flomo-sync
description: 将笔记内容或摘要同步到 Flomo，使用 .env 中配置的 flomo_api webhook
compatibility: opencode
---

## 你要做什么

- 将用户选定的笔记内容、思考片段或摘要同步到 Flomo
- 支持 Markdown 格式内容（加粗、标签、链接等）
- 从 `.env` 读取 `flomo_api` webhook URL，无需手动输入

## 工作流程

1. 用户提供要同步的内容（文本或指定笔记）
2. 如果是笔记，先调用 `summarize-note` 或按需摘取要点
3. 使用 `flomo_sync.py` 脚本将内容 POST 到 Flomo
4. 返回同步结果

## 用法

```
@opencode 把这段内容同步到 flomo：...
@opencode 把 [[笔记名]] 的要点同步到 flomo
```

## 约束

- 不修改用户笔记原文
- 内容超过 2000 字时自动截断或提示用户精简
- Flomo API 返回非 200 时输出错误信息
