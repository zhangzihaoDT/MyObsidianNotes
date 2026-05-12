---
created: 2026-05-12
---

## 1. takenotes

### 数据可视化部分

全局依赖 Echarts 完成

**Chart 技术栈**

|层|判断|
|---|---|
|图表库|**Apache ECharts**|
|渲染方式|前端 JS 静态页面，按 panel 初始化|
|数据|`us-market/data` 下 JSON 数据|
|交互|ECharts `tooltip`、`dataZoom`、`markLine`、`markArea`、`graphic draggable`|
|表格/热力格|部分不是 ECharts，而是 DOM + CSS 自绘，如年度矩阵、月度热力图|
### Design平面设计部分/ Rule

### 1. Font

主字体：

```
"Inter", -apple-system, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif
```

图表字体：

```
"Inter", -apple-system, "PingFang SC", sans-serif
```

也就是说：**英文 Inter，中文 PingFang SC / Noto Sans SC，系统字体兜底**。

### 2. Color

整体是“金融研究报告风”：

|用途|颜色|
|---|---|
|背景|`#ffffff` / dark: `#0a0a0a`|
|正文|`#1a1a1a`|
|次级文字|`#666666`|
|网格线|`#f0f0f0`|
|主线|黑色|
|上涨|`#389e0d`|
|下跌|`#cf1322`|
|强调蓝|`#4758e0`|
|卡片背景|`#ffffff`|
|边框|`#e8e8e8`|

暗色模式也做了完整变量映射。

### 3. Chart Type

主要图表类型：

|类型|用途|
|---|---|
|Line chart|长周期走势、波动率、EPS、CAPE、VIX|
|Area chart|回撤、恐慌/高波动区间|
|Scatter|成分股市值 × 近一年收益率|
|Heatmap-like DOM table|月度涨跌、年化收益矩阵|
|Bar / stacked bar|年回报、回报分解、权重累计|
|Pie / donut|成分股权重分布|

### 4. Spacing / Layout

核心布局规则：

```
.main { margin-left: 140px; padding-bottom: 40px; }.hero-banner { padding: 64px 24px 56px; min-height: 220px; }
```

页面左侧是固定导航，主体内容左移 140px；每个 panel 像一张独立研究卡片，图表通常设置：

```
grid: { left: 65, right: 20, top: 20, bottom: 60 }
```

这说明它的图表设计偏 **低装饰、高信息密度、留足坐标轴和 dataZoom 空间**。

### 一句话总结

这是一个 **原生 HTML/CSS/JS + ECharts + JSON 数据** 做出来的金融数据看板，设计风格接近：

> 极简研究报告 + Bloomberg/TradingView 的交互能力 + 少量 Apple 风格留白。

## 2. keywords

无

## 3. source

网站地址：https://laoqianritan-create-github-io.pages.dev/

#老钱 
公众号来源：《百年美股：Time in the market》https://mp.weixin.qq.com/s/QSkZz_37HRYN-gHF-ZJjQQ