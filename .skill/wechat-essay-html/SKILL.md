# WeChat Essay HTML Skill

## Purpose

This skill converts Markdown articles into clean, readable HTML suitable for pasting into the WeChat Official Account draft editor.

The target style is **Zihaology Essay Style**:

- personal essay
- strong judgment
- short paragraphs
- mobile-first reading
- restrained visual design
- clean typography
- suitable for public account publishing

The output should feel like a thoughtful personal methodology article, not a product manual, report, or marketing landing page.

---

## When to Use

Use this skill when the user asks to:

- convert Markdown to WeChat HTML
- format an article for WeChat Official Account
- generate HTML for a public account draft
- apply Zihaology Essay Style
- turn notes into a polished WeChat article
- improve article layout and mobile readability

Typical user requests:

- “帮我把这篇 Markdown 转成公众号 HTML”
- “按 Zihaology Essay Style 排版”
- “生成可以粘贴到公众号草稿箱的 HTML”
- “md2html2公众号草稿箱”
- “帮我排版成微信公众号风格”

---

## Style Philosophy

The style should be:

**clean, restrained, opinionated, readable.**

The article should not look like:

- a corporate report
- a documentation page
- a Notion export
- a sales page
- a dense Markdown dump

It should look like:

- a personal essay with clear judgment
- a calm but sharp methodology note
- a mobile-friendly public account article
- a structured thinking output

Core principles:

1. Short titles.
2. Short paragraphs.
3. Strong section headings.
4. Generous spacing.
5. Minimal decoration.
6. Emphasis only for real judgments.
7. Tables only when necessary.
8. Avoid over-designed cards.
9. Avoid excessive colors.
10. Optimize for mobile reading.

---

## Writing Style Rules

When editing the content before HTML conversion, follow these rules.

### 1. Use short paragraphs

Prefer:

```md
我现在越来越不想把 AI 当成“聊天工具”用了。

聊天当然有用，但那只是第一层。

真正让我兴奋的是：

**AI 开始有自己的工位了。**
```

Avoid:

```md
我现在越来越不想把 AI 当成聊天工具用了，因为聊天当然有用，但它只是第一层，真正让我兴奋的是 AI 开始有自己的工位了。
```

Rule:

**One judgment, one paragraph.**

---

### 2. Section titles should sound like judgments

Prefer:

```md
## 一个能自己干活的 AI

## 不是更聪明，而是更能干活

## 自定义 Agent，才是重头戏
```

Avoid:

```md
## 当前 AI 工具介绍

## 编程 IDE 配置说明

## 自动化环境搭建情况
```

Good section titles feel like article arguments, not documentation headings.

---

### 3. Emphasis should be rare

Use bold only for important judgments.

Good:

```md
**AI 是引擎，但引擎不会自己决定去哪。**
```

Avoid bolding every tool name:

```md
**TRAE Pro**、**DeepSeek API**、**Obsidian**
```

Tool names can usually stay normal.

---

### 4. Reduce table usage

Tables are allowed, but use them sparingly.

Tables are suitable for:

- cost lists
- tool-role mapping
- comparison between options
- infrastructure components

Do not overuse tables for narrative content.

---

### 5. Ending should feel like an invitation

Prefer:

```md
这套东西我已经跑通了。

如果你也想搭，我可以带你从 0 到 1 跑一遍。
```

Avoid:

```md
本人现提供一对一私教服务，如有需要请联系。
```

The conversion section should feel natural, not like an advertisement.

---

## HTML Output Requirements

Always output complete HTML that can be copied directly into the WeChat Official Account draft editor.

The output mode depends on the target:

- Preview output can use a `<style>` block + class selectors.
- WeChat draft sync via API must use inline styles on each HTML element and must not rely on `<style>`, class selectors, CSS variables, or pseudo-elements.

---

## CSS Style Definition

Use this CSS as the default style.

```html
<style>
  :root {
    --banner-title: #2f3036;
    --banner-blue: #466a9c;
    --banner-bg: #f5f6f8;
    --banner-muted: #949ead;
    --banner-light-blue: #c2cdde;
  }

  .zihaology-essay {
    max-width: 760px;
    margin: 0 auto;
    padding: 24px 18px 40px;
    background: #ffffff;
    color: #2f3437;
    font-family:
      -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB',
      'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif;
    font-size: 17px;
    line-height: 2.05;
    letter-spacing: 0.03em;
    word-break: break-word;
  }

  .zihaology-essay h1 {
    font-size: 26px;
    line-height: 1.45;
    font-weight: 700;
    color: var(--banner-title);
    font-family:
      'Source Han Serif SC', 'Noto Serif CJK SC', 'Songti SC', 'SimSun', serif;
    letter-spacing: 0.08em;
    margin: 0 0 28px;
  }

  .zihaology-essay h2 {
    position: relative;
    font-size: 21px;
    line-height: 1.5;
    font-weight: 800;
    color: var(--banner-title);
    margin: 46px 0 22px;
    padding-left: 16px;
  }

  .zihaology-essay h2::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.18em;
    width: 5px;
    height: 1.35em;
    background: var(--banner-blue);
    border-radius: 2px;
  }

  .zihaology-essay h3 {
    font-size: 18px;
    line-height: 1.6;
    font-weight: 700;
    color: #253041;
    margin: 32px 0 14px;
  }

  .zihaology-essay p {
    margin: 0 0 1.35em;
  }

  .zihaology-essay strong {
    font-weight: 800;
    color: #111827;
  }

  .zihaology-essay em {
    color: #4b5563;
  }

  .zihaology-essay blockquote {
    margin: 28px 0;
    padding: 16px 18px;
    border-left: 5px solid var(--banner-blue);
    background: var(--banner-bg);
    color: #263044;
    border-radius: 8px;
  }

  .zihaology-essay blockquote p {
    margin: 0;
    font-weight: 700;
  }

  .zihaology-essay ul,
  .zihaology-essay ol {
    padding-left: 1.3em;
    margin: 18px 0 26px;
  }

  .zihaology-essay li {
    margin: 8px 0;
    line-height: 1.9;
  }

  .zihaology-essay table {
    width: 100%;
    border-collapse: collapse;
    margin: 26px 0 32px;
    font-size: 15px;
    line-height: 1.75;
  }

  .zihaology-essay th {
    background: var(--banner-bg);
    color: var(--banner-title);
    font-weight: 700;
  }

  .zihaology-essay th,
  .zihaology-essay td {
    border: 1px solid var(--banner-light-blue);
    padding: 10px 12px;
    text-align: left;
  }

  .zihaology-essay td {
    color: #374151;
  }

  .zihaology-essay hr {
    border: none;
    height: 1px;
    background: var(--banner-light-blue);
    margin: 44px 0;
  }

  .zihaology-essay a {
    color: var(--banner-blue);
    text-decoration: none;
    border-bottom: 1px solid rgba(70, 106, 156, 0.25);
  }

  .zihaology-essay pre {
    background: #f6f8fa;
    border-radius: 10px;
    padding: 16px;
    overflow-x: auto;
    font-size: 14px;
    line-height: 1.7;
    margin: 24px 0;
  }

  .zihaology-essay code {
    font-family:
      'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  }

  .zihaology-essay p code,
  .zihaology-essay li code {
    background: #f3f4f6;
    color: #374151;
    padding: 2px 6px;
    border-radius: 5px;
    font-size: 0.92em;
  }

  .banner-title {
    font-family:
      'Source Han Serif SC', 'Noto Serif CJK SC', 'Songti SC', 'SimSun', serif;
    color: var(--banner-title);
    font-weight: 700;
    letter-spacing: 0.08em;
  }

  .banner-subtitle {
    font-family: Georgia, 'Times New Roman', serif;
    color: var(--banner-blue);
    letter-spacing: 0.04em;
  }

  .banner-muted {
    color: var(--banner-muted);
  }

  .banner-accent {
    background: var(--banner-blue);
  }
</style>
```

---

## HTML Structure

The final output should follow this structure:

```html
<style>
  /* Zihaology Essay Style CSS here */
</style>

<section class="zihaology-essay">
  <h1>文章标题</h1>

  <p>正文第一段。</p>

  <h2>章节标题</h2>

  <p>正文内容。</p>

  <blockquote>
    <p>核心判断。</p>
  </blockquote>
</section>
```

---

## Conversion Rules

When converting Markdown to HTML:

### Markdown headings

Convert:

```md
# Title
```

to:

```html
<h1>Title</h1>
```

Convert:

```md
## Section
```

to:

```html
<h2>Section</h2>
```

Convert:

```md
### Subsection
```

to:

```html
<h3>Subsection</h3>
```

---

### Paragraphs

Convert each paragraph into:

```html
<p>...</p>
```

Keep short paragraphs separate.

Do not merge short paragraphs.

---

### Bold

Convert:

```md
**text**
```

to:

```html
<strong>text</strong>
```

Only preserve bold when it is a real judgment or key conclusion.

If the original Markdown overuses bold, reduce it.

---

### Blockquotes

Convert:

```md
> text
```

to:

```html
<blockquote>
  <p>text</p>
</blockquote>
```

Use blockquotes for:

- gold sentences
- core arguments
- methodological summaries
- memorable conclusions

---

### Lists

Convert Markdown lists into standard HTML:

```html
<ul>
  <li>item</li>
</ul>
```

or:

```html
<ol>
  <li>item</li>
</ol>
```

Keep lists short when possible.

---

### Tables

Convert Markdown tables into HTML tables.

Keep table design light and readable.

Do not add unnecessary icons, badges, or colored labels.

---

### Links

Convert Markdown links into:

```html
<a href="URL">text</a>
```

Do not expose raw URLs unless the article intentionally discusses a specific website.

---

## WeChat Compatibility Notes

WeChat Official Account editors may strip some CSS depending on the editor or copy method.

Therefore:

1. Avoid JavaScript.
2. Avoid external CSS.
3. Avoid external fonts.
4. Avoid complex CSS selectors.
5. Avoid CSS grid or flex for main article layout.
6. Avoid fixed-width desktop layouts.
7. Keep the design mostly typography-based.
8. Use simple HTML tags.

When syncing to WeChat draft via API, always prefer inline styles.

---

## WeChat Draft Sync Mode

When syncing to WeChat draft via API, do not rely on `<style>`, class selectors, CSS variables, or pseudo-elements.

The sync output must use inline styles on each HTML element.

The default rendering mode for `sync_to_wechat.py` is inline-style mode.

Defaults:

1. Always use `/Users/zihao_/Documents/github/notes/.skill/wechat-essay-html/0ebee294-486a-4164-81b7-5a58bfa1cffe.png` as the default cover placeholder if no cover is provided.
2. Credentials live in `/Users/zihao_/Documents/github/notes/.env`. Never output, paste, or log secret values in responses.

---

## Final Answer Behavior

When the user asks for HTML conversion:

1. Do not over-explain.
2. Output the complete HTML.
3. If the article is long, still output the full HTML unless the user asks for a partial sample.
4. Do not wrap the final HTML in unnecessary commentary.
5. Use a code block with `html`.

When the user asks for style definition or modification:

1. Explain the style briefly.
2. Provide the reusable CSS or updated `SKILL.md`.
3. Keep the answer practical.

---

## Quality Checklist

Before final output, check:

- Is the article mobile-readable?
- Are paragraphs short?
- Are section headings strong?
- Is the style restrained?
- Is bold used only for key judgments?
- Are tables readable?
- Is the HTML complete?
- Can it be copied into WeChat draft editor?
- Does it avoid over-design?
- Does the article still sound like a person, not a manual?

---

## Default Voice

The default voice should be close to:

- direct
- calm
- judgment-driven
- slightly sharp
- personal
- practical
- not overly polished
- not corporate

The article should feel like:

> 一个有经验的人，在讲自己刚跑通的一套系统。

Not like:

> 一个营销号在介绍 AI 工具合集。

```

```
