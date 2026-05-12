---
created: 2026-05-11
---
## 1. takenotes

- Markdown 已成为代理们与我们沟通的主流文件格式。它简单、便携，具备丰富的文本功能，且编辑起来很方便。
- 但人很难读懂超一百行的 markdown 文件。我想要更丰富的可视化、色彩和图表，并且能够轻松分享。

**为什么选择 HTML？**

1、信息密度
- Table：表格数据
- Design：（CSS）支持良好的平面设计，font、color、type、spacing
- Illustration：（SVG）支持做插图
- Code：带有tags的脚本片段
- Interaction：JavaScript + CSS 的交互
- workflow：使用svg+html 做工作的流程图
- Spatial：在 canvas 范围内的绝对坐标系空间 
- Image：插入图片

2、视觉清晰度与阅读便利性
3、分享便利性
- Markdown 文件比较难分享，用 HTML 时，只要上传文件（比如上传到 S3），就能轻松分享链接。你的同事们可以随意打开并轻松查阅。

**如何开始**

- Thariq 风格 HTML 的典型特征
		- 1. **单文件**：里面只有index.html，里面包含：HTML CSS JS 全部内联。
		- 2. **Tailwind 风格 UI**：典型视觉：黑色背景、毛玻璃、紫蓝渐变、rounded-xl、卡片、hover 动画、grid；像：- Claude Artifacts风格。
		- 3. **数据可视化**：常见：Chart.js、ECharts、Mermaid、D3，然后 AI 自动生成图。
		- 4. 交互式组件：- Tab、Accordion、Search、Filter、Expand、Timeline，这才是它比 Markdown 强的地方。

- 你应该怎么生成
		- 你不应该自己手写。
		- 而是：正确工作流
		- 写需求    
		↓Claude Code / GPT-5 / Gemini    
		↓生成完整 HTML    
		↓本地打开


----

## 2. keywords：artifacts

Artifact 的核心：

```
AI 直接生成一个“东西”
```

而不是：

```
AI 生成“描述”
```

传统 AI 输出的问题，输出的是一段文字，是“死的”

传统软件开发里：artifact 指：build 产物，即：

```
“真正可用的东西”
```

## 3. source

**Thariq、X、HTML**

“我已经停止为几乎所有内容写 markdown 文件，改用 Claude 代码为自己生成 HTML。原因就是这个。”

https://x.com/trq212/status/2052811606032269638

---
Anthropic Claude Code 团队成员 Thariq 发表于 X
https://x.com/trq212/article/2052809885763747935
