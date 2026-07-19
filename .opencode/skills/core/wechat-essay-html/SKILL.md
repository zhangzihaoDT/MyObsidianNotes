---
name: wechat-essay-html
description: 将 Markdown 文章转成适合微信公众号的 HTML，并可同步到草稿箱。适用于用户要生成公众号排版稿、HTML 草稿或直接发布到公众号草稿箱时。
compatibility: opencode
---

## 你要做什么

- 将 Markdown 文章转换为适合微信公众号编辑器的 HTML
- 在需要时，使用内联样式模式生成可直接同步到公众号草稿箱的内容
- 保持文章适合手机阅读，版式克制、清晰、适合公众号发布
- 在用户明确要求时，直接同步到公众号草稿箱

## 何时使用

- 用户要求把 Markdown 转成公众号 HTML
- 用户要求按公众号风格排版
- 用户要求生成可以粘贴到公众号草稿箱的 HTML
- 用户要求直接发布到微信公众号草稿箱

## 输出格式

- 若用户要求 HTML：输出完整 HTML
- 若用户要求同步草稿箱：执行同步并返回标题、结果和阻塞点

## 同步约束

- 默认使用 `/Users/zihao_/Documents/github/notes/.skill/wechat-essay-html/sync_to_wechat.py`
- 默认封面占位图为 `/Users/zihao_/Documents/github/notes/.skill/wechat-essay-html/0ebee294-486a-4164-81b7-5a58bfa1cffe.png`
- 凭据从 `/Users/zihao_/Documents/github/notes/.env` 读取
- 不输出、不粘贴、不回显任何密钥内容
- 若同步失败，只返回错误类型和必要上下文，不泄露敏感信息

## 风格要求

- 保持移动端可读性
- 段落尽量短
- 标题清晰
- 装饰克制
- 不要过度表格化或卡片化
- 整体像可发布的公众号文章，而不是文档导出页
