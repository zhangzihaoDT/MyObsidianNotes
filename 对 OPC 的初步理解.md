How To Build a One-Person Company With Claude Fable 5
如何像克劳德·法布尔在《5》中那样创建一家单人公司

作者：Rahul@sairahul1 • 16h

To view keyboard shortcuts, press question mark
View keyboard shortcuts

How To Build a One-Person Company With Claude Fable 5
如何像克劳德·法布尔在《5》中那样创建一家单人公司
Rahul
@sairahul1
·
16h

10 万
Five years ago you needed a team to build a real company.
五年前，你需要一个团队来打造一家真正的公司。
Marketers. Researchers. Developers. Sales reps. Support staff.
营销人员、研究人员、开发人员、销售代表以及支持团队成员。
Even a small company meant 10–20 people and $1M+ in payroll.
即使是一家小型公司，其员工数量也至少有 10 到 20 人，而薪资开支则达到 100 万美元以上。
That changed.
情况已经改变了。
Claude Fable 5 is the first AI model I've used that doesn't feel like a chatbot.
Claude Fable 5 是我使用过的第一个并不让人感觉像聊天机器人的 AI 模型。
It feels like infrastructure.
这感觉就像是一种基础设施罢了。
Most people are still using it like this:
大多数人仍然采用这样的方式使用它：
Prompt → Response → Done
提示 → 响应 → 完成
That's not what Fable was built for.
那并非《Fable》这款游戏的初衷。
Fable runs for days.
传说在几天内就会流传开来。
It plans. Researches. Executes. Verifies. Learns. Keeps going.
它进行规划、研究、执行、验证、学习，并持续不断地运作下去。
The biggest opportunity isn't using AI to save a few minutes.
最大的机会并非是利用人工智能来节省几分钟时间。
It's using AI to replace entire departments.
它正在利用人工智能来取代整个部门的工作。
Here is the exact company architecture I would build from zero today.
这是我今天从零开始构建的公司的确切架构。
Every prompt below is copy-paste ready. Run it tonight.
下面的每个提示都可以直接复制粘贴使用。今晚就执行吧。
The old model vs the new model
旧模式与新模式
Old model:
旧模型：
You → hire people → manage people → pay people → hope it works
你 → 雇佣员工 → 管理员工 → 支付员工工资 → 希望一切顺利
New model:
新模型：
You → design the system → Fable runs the departments → departments improve themselves
你们设计这个系统 → Fable 负责管理各个部门 → 各个部门则不断自我改进。
The founder no longer does the work.
创始人已经不再从事这项工作了。
The founder designs the operating system.
创始人负责设计这个操作系统。
Everything else runs.

其他的一切都正常运转着。

Step 0 — Build the company brain first
步骤 0——首先构建公司的思维体系
Every founder skips this step.
每个创始人都会跳过这一步。
They jump straight into prompts and wonder why the AI acts like a clueless intern.
它们直接开始回答问题，却不明白为什么人工智能的行为举止就像个无知的新手一样。
The difference between a clueless intern and a great employee is context.
一个无见识的实习生和一位优秀的员工之间的区别，就在于所处的环境不同。
Create this folder structure right now:
立即创建这个文件夹结构：
bash
mkdir -p ~/company/{memory,skills,state,content,docs,sops}

touch ~/company/founder.md
touch ~/company/strategy.md
touch ~/company/products.md
touch ~/company/customers.md
touch ~/company/memory/lessons.md
touch ~/company/state/projects.md
touch ~/company/state/pipeline.md
touch ~/company/state/seo-tracker.md
Fill each file with these templates:
用这些模板填充每个文件：
~/company/founder.md
markdown
标记式书写方式

# About Me

## How I think

[Fast and intuitive? Slow and deliberate? Risk-tolerant or cautious?]

## My strengths

[What you're genuinely good at — specific, not generic]

## My weaknesses

[What drains you or where you consistently make mistakes]

## Communication style

[How you want outputs — bullet points? prose? short? detailed?]

## Non-negotiables

[Things you will never compromise — quality bar, ethics, speed]

## Decision framework

[How you make hard calls — data first? gut first? consensus?]
~/company/strategy.md
markdown
标记式书写方式

# Company Strategy

## 2026 Goals

1. [Specific measurable goal]
2. [Specific measurable goal]
3. [Specific measurable goal]

## Target market

[Job title, company size, industry, pain they have right now]

## Pricing

[$X for Y. Why this price. What the alternatives cost.]

## Positioning

[One sentence: We help [who] do [what] without [pain].]

## Competitive advantage

[The one thing we do better than anyone — be specific]

## What we will NOT do

[The 3 things we explicitly refuse to compete on]
~/company/customers.md
markdown
标记式书写方式

# Customer Intelligence

## Ideal customer profile

[Demographics, company type, job to be done, budget authority]

## Top 5 customer pains (ranked)

1. [Pain] — [how often they mention it]
2.
3.
4.
5.

## Common objections and real reason behind them

- "Too expensive" — actually means: [real concern]
- "Not right now" — actually means: [real concern]
- "We built something internal" — actually means: [real concern]

## Best customer testimonials

1. "[Quote]" — [Name, Role, Company]
2.
3.

## Where customers hang out

[Reddit subs, LinkedIn groups, newsletters, Slack communities]
Add this instruction to the start of every Fable session:
在每次《Fable》游戏开始时，请添加这条指令：
plaintext
明文
Before starting any task, read:

- ~/company/founder.md
- ~/company/strategy.md
- ~/company/customers.md

After completing any task, write key lessons to:

- ~/company/memory/lessons.md

Format: Date | Department | What worked | What failed | Next time
One entry per lesson. Update existing entries instead of creating duplicates.
Without these files: AI acts like a freelancer getting a cold brief.
如果没有这些文件，AI 就像一名没有详细任务的自由职业者一样，无法进行有效的操作。
With these files: AI acts like someone who has worked with you for two years.
拥有这些文件后，AI 就像是一位已经与你合作了两年的朋友一样。
Department 1 — Research
第一部门——研究部门
Most founders do 15 minutes of Google and call it market research.
大多数创始人会花 15 分钟时间搜索谷歌，然后称之为市场调研。
That's why most products miss the market.
这就是为什么大多数产品都无法进入市场的原因。
Your research department runs every week without you.
你的研究部门在没有你的情况下每周都正常运作。
Copy this prompt. Run it every Monday:
复制这个提示。每周一都执行它：
plaintext
明文
You are my Research Director.

Read ~/company/strategy.md and ~/company/customers.md first.

Run the full weekly research loop:

━━━ COMPETITOR RESEARCH ━━━

Search for the following about each competitor: [list 3-5 competitors]

Find in the past 7 days:
→ Any new product launches or feature announcements
→ Any pricing page changes (use cached vs current comparison if possible)
→ Their 3 most-engaged social posts and why they performed
→ Customer complaints on Reddit, G2, Trustpilot, App Store

━━━ CUSTOMER RESEARCH ━━━

Search these Reddit communities: [r/sub1, r/sub2, r/sub3]

Search queries to run:
→ "I wish [competitor name] would..."
→ "frustrated with [product category]"
→ "looking for alternative to [competitor]"
→ "anyone else having trouble with [pain area]"

Find the top 10 complaints ranked by upvotes.
Group similar complaints into themes.

━━━ OPPORTUNITY RESEARCH ━━━

Find in my niche:
→ Keywords with search volume but weak top-10 competition
→ Questions on Reddit/Quora with many upvotes but no satisfying answer
→ Products people are asking for in forums that don't exist yet
→ Any competitor who just raised prices (opportunity to position against)

━━━ OUTPUT FORMAT ━━━

Return exactly this structure:

## Weekly Research Report — [Date]

### Top 3 Competitor Moves This Week

| Competitor | What they did | Why it matters | Recommended action |

### Top 5 Customer Complaints (by frequency)

| Complaint | How often | Opportunity this creates |

### Top 3 Opportunities This Week

| Opportunity | Evidence | Effort | Revenue potential | Recommended action |

### One Contrarian Observation

[Something you found that goes against conventional wisdom in this space]

Save full report to: ~/company/state/research-[YYYY-MM-DD].md
Update ~/company/memory/lessons.md with key discoveries.
You get a strategic report every Monday.
你每周一都会收到一份战略报告。
Not information. Decisions.
不是信息。是决策。
Department 2 — Marketing
第二部门——市场营销
Part A: Virality engineering for X
部分 A：用于 X 的病毒性工程技术
Virality is not luck.
病毒性传播并非运气使然。
It is a repeatable science. 95% automatable.
这是一项可重复进行的科学操作。其中 95%的过程可以通过自动化来完成。
Here's how the X algorithm actually works:
X 算法的实际运作方式如下：
Every post gets tested on a tiny sample first.
每一条帖子都会先经过极小的样本测试来确认其正确性。
The algorithm measures exactly three things: → Did people stop scrolling? → Did they read through to the end? → Did they comment?
该算法精确测量了三件事：→ 人们是否停止了滚动页面？→ 他们是否读到了页面末尾？→ 他们是否发表了评论？
Pass all three → post goes to a bigger pool → pass again → distribution unlocks.
通过了所有三项测试 → 结果将进入更大的筛选池 → 再次通过测试 → 分发过程就此启动。
Fail any one → post is dead in 20 minutes. Doesn't matter how good the content is.
只要有一个环节出错，那么这篇文章在 20 分钟内就会失效。无论内容有多好，都无济于事。
This means every post must be engineered before you publish.
这意味着在发布之前，每一个帖子都必须经过处理修改。
Copy this. Run it before every post:
复制这个内容。每次发布之前都运行它：
plaintext
明文
I'm about to publish this post on X. Run the full viral engineering audit.

MY POST:
[paste your draft here]

MY AUDIENCE: [describe your audience — e.g., indie hackers, developers, founders]

━━━ STEP 1: HOOK ANALYSIS ━━━

Score the current first line 1-10 for scroll-stopping power.
What emotion does it trigger? (curiosity / fear / desire / surprise / anger)
What is the implied promise? Will the post deliver on it?

Rewrite the hook 5 different ways:
Version 1: Curiosity hook
Version 2: Fear/pain hook
Version 3: Desire/aspiration hook
Version 4: Surprise/counterintuitive hook
Version 5: Bold claim hook

Score each 1-10. Recommend the strongest.

━━━ STEP 2: ALGORITHM TEST ━━━

Run the 4-criteria check:
□ Bold claim bigger than the product? [Yes/No — if No, suggest improvement]
□ Dopamine delivered in first 2 lines? [Yes/No — if No, rewrite opening]
□ Any context gaps where reader might get lost? [List them]
□ Strongest outcome front-loaded? [Yes/No — if No, reorder]

Predicted reader behavior: Scroll past / Like / Comment / Repost
What would make them repost instead of just like?

━━━ STEP 3: COMMENT ENGINEERING ━━━

Write the 5 most likely first comments this post will get.
For each comment, write my ideal reply that:

- Adds new information not in the original post
- Extends the conversation
- Is under 100 words

Write 3 quote tweet angles for accounts in adjacent niches.

━━━ STEP 4: FIRST HOUR PLAN ━━━

The algorithm weights the first 60 minutes heavily.
Pre-write:

1. My reply to my own post (adds the one key insight I didn't include)
2. A follow-up post to schedule 90 minutes after this one
3. The one sub-reddit or community where I should cross-post this today

━━━ STEP 5: FINAL CALL ━━━
Verdict: Publish as-is / Minor edits / Major rewrite needed
If edits: show me the improved version ready to copy-paste.
After posting — stay active for 60 minutes. Here's what to do:
发布内容后，请保持活跃状态，持续活跃 60 分钟。具体步骤如下：
Every comment gets a response that adds new information.
每条评论都会得到相应的回应，这些回应会提供新的信息。
Never reply with just "great point!" — add something.
不要只回复“很有道理！”——请补充一些内容吧。
After 60 minutes, walk away. The algorithm does the rest.
经过 60 分钟后，就离开那里吧。剩下的事情就由算法来处理了。
Part B: SEO content factory
部分 B：SEO 内容工厂
Copy this. Use for every target keyword:
复制此内容。适用于每一个目标关键词：
plaintext
明文
You are my SEO Content Director.

Read ~/company/strategy.md and ~/company/customers.md first.

Target keyword: [exact keyword]
My domain authority is approximately: [low/medium/high or DA score if known]

━━━ STEP 1: COMPETITOR ANALYSIS ━━━

Search Google for this exact keyword.
Analyze the top 5 ranking pages:

For each page:

- Main angle and thesis
- Subheadings (H2s and H3s)
- Questions they answered
- Topics they covered well
- Topics they missed or covered poorly
- Approximate word count
- Type of content (list / guide / comparison / case study)

━━━ STEP 2: WINNING BRIEF ━━━

Create a superior article brief:

- Our angle: [more specific / more contrarian / more practical]
- Must cover: [all topics competitors covered]
- Must also cover: [3+ topics competitors missed]
- Semantic keywords to include: [related terms Google expects]
- Ideal structure: [outline with all H2s and H3s]
- Target word count: [X words]

━━━ STEP 3: WRITE THE ARTICLE ━━━

Write the full article following the brief.
Tone: [direct and conversational — no corporate speak, no filler sentences]
Format: Introduction (hook + promise) → sections → conclusion with CTA

Rules:

- Every sentence must earn its place. Delete anything that doesn't add value.
- Use short paragraphs (1-3 sentences max)
- Real examples over generic statements
- If you're unsure of a fact, write [VERIFY: claim] instead of guessing

━━━ STEP 4: METADATA ━━━

Title tag: [60 chars max, primary keyword first, benefit clear]
Meta description: [155 chars max, keyword + specific benefit + CTA]
H1: [optimized for search intent]
URL slug: [short, keyword-rich, no stop words]
Internal linking suggestions: [3 pages on my site this should link to]

Save article to: ~/company/content/[slug].md
Log to: ~/company/state/seo-tracker.md
Format: [Keyword] | [Target URL] | [Status: Draft/Published] | [Date]
Part C: Newsletter on autopilot
第三部分：关于自动驾驶功能的通讯报道
plaintext
明文
You are my Newsletter Director.

Every Sunday at 6pm, run the weekly newsletter workflow:

━━━ RESEARCH PHASE ━━━

Search for the most important developments this week in [your niche]:
→ 3 industry news items (filter: actually matters, not just announcements)
→ 2 interesting threads or debates from X/LinkedIn
→ 1 contrarian take or counterintuitive finding
→ 1 tool or resource worth sharing

For each item: one sentence on why it matters to my audience.

━━━ WRITING PHASE ━━━

Write the newsletter:
Subject line options: 3 versions (curiosity / benefit / contrarian)
Preview text: [under 90 chars, completes the subject line story]

Structure:

- Opening hook (1 paragraph — the most interesting thing this week)
- Main section 1: [item 1 + why it matters + one action they can take]
- Main section 2: [item 2 + angle]
- Quick hits: [3 bullet items in under 150 words total]
- One question for readers to reply to (drives engagement)
- Sign-off

Rules:

- Under 600 words total
- Every section earns its place
- Sound like a smart friend, not a publication

━━━ DISTRIBUTION ━━━

Write the 3 social posts to promote this issue:

- X post (hook + key insight + link)
- LinkedIn post (slightly more formal, different angle)
- Short teaser for stories/reels

Save newsletter to: ~/company/content/newsletter-[YYYY-MM-DD].md
And similarly, Fable can be used for TikTok Automation, to grow your facebook, instagram LinkedIn accounts too. Just need to ask
同样地，Fable 也可以用于 TikTok 的自动化操作，还能帮助您拓展 Facebook、Instagram 和 LinkedIn 等社交平台的账号。只需要使用一下就可以了。
Department 3 — Sales
第三部门——销售部
Most founders think sales is cold email.
大多数创始人都认为，销售其实就是发送冷邮件的工作。
Cold email is 5% of sales.
冷邮件在销售中的占比为 5%。
Copy the full machine:
复制整个机器：
plaintext
明文
You are my Sales Director.

Read ~/company/customers.md and ~/company/strategy.md first.

My product: [what you sell in one sentence]
My ICP: [ideal customer — exact title, company size, industry, pain]
My price: [what you charge]
My best proof point: [strongest result or customer name]

For each prospect I give you, run the full sequence:

━━━ STEP 1: PROSPECT RESEARCH ━━━

Research this prospect fully:
Company: [size, funding stage, recent news, tech stack if relevant]
Person: [role, how long in position, what they post about, mutual connections]
Pain signals: [job postings that reveal problems, support reviews, product complaints]
Trigger: [what just changed at their company that makes them a buyer NOW]

Rate their fit: A (close now) / B (nurture) / C (not our ICP)
If C: do not proceed. Flag for me.

━━━ STEP 2: EMAIL OUTREACH ━━━

Write a cold email using this exact structure:
Line 1: One specific observation about them or their company [NOT generic]
Line 2: The exact pain this creates for someone in their role
Line 3: What we do about it in one sentence
Line 4: One proof point — customer name or specific number
Line 5: One soft CTA — a question that invites a reply, not a meeting request

Rules:

- Under 100 words total
- No "I hope this email finds you well"
- No "revolutionary" or "game-changing" or "excited to share"
- Subject line: under 6 words, specific to them

━━━ STEP 3: LINKEDIN SEQUENCE ━━━

Connection request (under 300 chars):
[Specific reason for connecting — shared interest, their content, mutual connection]

DM 1 (after connecting — add value, zero pitch):
[Share something genuinely useful related to their pain — article, framework, observation]

DM 2 (5 days no response — different angle):
[New insight or social proof. Still no hard pitch.]

DM 3 (10 days no response — soft close):
["Worth a quick chat or not your priority right now — either way no worries."]

━━━ STEP 4: FOLLOW-UP LOGIC ━━━

If no email open in 3 days: resend with different subject, same body
If opened but no reply in 5 days: send follow-up with different angle
If replied "not now": schedule check-in for exactly 90 days, note the trigger to reference then
If interested but stalled: send one piece of social proof per week for 3 weeks

━━━ STEP 5: CRM UPDATE ━━━

Log to ~/company/state/pipeline.md:
| Name | Company | Stage | Email sent | LinkedIn status | Last touch | Next action | Date |

After processing 10 prospects, show me:

- How many are A, B, C tier
- Total pipeline value if all A-tier close
- Recommended priority order for follow-ups
  The AI calling layer — add this on top:
  人工智能通话层——将其添加到顶部：
  Connect Bland.ai, Vapi, or Retell to your prospect list (and recently X launched their Ai voice SDK too)
  将 Bland.ai、Vapi 或 Retell 与你的潜在客户名单连接在一起（最近 X 公司还推出了他们的 AI 语音 SDK）。
  Every non-email-opener within 48 hours gets a call.
  在 48 小时内，每个不经常使用电子邮件的人都会接到一个电话。
  The AI agent:
  → References their business by name
  → Mentions the specific pain from your research
  → Asks for 10 minutes, not a sale
  → Books directly into your calendar via Cal.com or Calendly
  → Updates your CRM with call outcome automatically
  人工智能代理：
  → 通过名称来引用他们的业务
  → 提到了你们研究中所发现的具体疼痛问题
  请求 10 分钟的时间，并非进行促销活动。
  通过 Cal.com 或 Calendly 直接将日程安排写入你的日历中。
  → 自动将通话结果更新到你的 CRM 系统中。
  Set it up once.
  只需设置一次即可。
  Runs while you sleep.
  在你沉睡时也能运行。
  Every morning your calendar has new meetings.

每天早晨，你的日历上都会新增一些会议安排。

Department 4 — Engineering
第四部门——工程学
This is where the one-person company becomes genuinely unfair.
这就是单人公司真正变得不公平的地方。
Stripe gave Fable 5 their Ruby codebase. 50 million lines. Full migration.
Stripe 将他们的 Ruby 代码库交给了 Fable 5。总共有 5000 万行代码。完全迁移到了新的系统上。
Normally two months for a whole team.
通常整个团队需要两个月的时间来完成这项工作。
Fable did it in one day.
Fable 在一天之内就完成了这项工作。
But day-to-day engineering for a solo founder isn't big migrations.
但对于一个独立创业的创始人来说，日常的工程开发工作并不涉及大规模的迁移操作。
It's bugs. Features. PRs. Tests.
就是这些麻烦事。各种问题。公关活动。测试工作。
And the thing that kills most solo founders isn't lack of engineering skill.
而真正扼杀大多数独立创业者的因素，并非缺乏工程技能。
It's bugs that ship without anyone catching them.
那些虫子会在没人注意到的情况下离开的。
A broken payment flow. A silent API failure. A crash on edge case inputs.
支付流程出现中断。API 在关键时刻出现故障。面对特殊输入情况时，系统崩溃。
You don't know until Monday when customers are angry.
直到周一你才会知道顾客们的情绪如何，那时他们肯定会很生气。
Here's how to fix that completely.
以下是如何彻底解决这个问题的方法。
Layer 1 — Fable as your engineering team
第 1 层——以《Fable》作为你的工程团队
plaintext
明文
You are my Engineering Director.

Read ~/company/products.md and ~/company/strategy.md first.

For every feature request or bug report, run the full engineering workflow:

━━━ STEP 1: PRD ━━━

Write a complete Product Requirements Document:

- Problem: what breaks or what's missing, and for who
- Success criteria: how will we know this worked? (measurable)
- User flow: step-by-step what the user does
- Technical requirements: what the code must do
- Edge cases: what can go wrong, what inputs might break this
- Out of scope: what we are explicitly NOT building in this version

━━━ STEP 2: ARCHITECTURE ━━━

Design the implementation before writing code:

- What existing files change and how
- What new files need to be created
- What tests need to be written
- Any new dependencies (and whether they're justified)
- Potential performance impacts
- Any security considerations

━━━ STEP 3: BUILD ━━━

Write the code following the architecture.
After writing each function, verify it satisfies its PRD requirement.
Write tests alongside the code — not after.
If you hit uncertainty: write a comment [VERIFY: assumption] instead of guessing.

━━━ STEP 4: SELF-REVIEW BEFORE HANDING TO ME ━━━

Run this checklist before delivering:
□ Does it satisfy every PRD requirement? (check each one)
□ Are all edge cases handled?
□ Is there a test for every critical path?
□ Are there any obvious security issues?
□ Is the code readable without comments?
□ What is the most likely way this could fail in production?

If you find a problem: fix it before delivering to me.

━━━ STEP 5: PR DESCRIPTION ━━━

Write a pull request description with:

- What this does and why (2 sentences)
- How to test it manually
- What automated tests cover it
- Any follow-up work this creates
- Risk level: Low / Medium / High

━━━ ESCALATION RULES ━━━

Come to me ONLY for:
→ Irreversible actions (database migrations, deletes, API breaking changes)
→ Security decisions
→ Architecture choices that affect the roadmap

Otherwise: run until done. Report back with the PR.
Log lessons to ~/company/memory/engineering.md
Layer 2 — Entelligence (it's e not I): bugs fixed before you even know they exist
第 2 层——Entelligence（其实是“它”，而不是“我”）：在您意识到有漏洞之前，我们已经修复了这些漏洞。
This is the part most solo founders don't have. And it's the difference between sleeping well and getting 2am Slack alerts.
这是大多数独立创业者都缺乏的技能。而这正是能否睡得好与凌晨两点收到 Slack 通知之间的重要区别。
Here's the problem without it:
如果没有它，问题就会如下所示：
A PR ships. It contains a pattern identical to an incident from 6 months ago.
有一艘 PR 飞船正在航行。它携带的图案与 6 个月前发生的一起事件中的图案完全相同。
Nobody catches it because nobody remembers.
没有人能抓住它，因为没有人记得这件事。
The bug hits production on Friday.
该漏洞将在周五影响生产流程。
You find out Monday from angry customers.
你将在周一从那些愤怒的顾客那里得知真相。
Entelligence is a production reliability engine that connects to your entire stack — GitHub, Sentry, PagerDuty, Linear, Datadog — and builds a memory of every incident your codebase has ever had.
Entelligence 是一种生产可靠性监控工具，它可以连接到你的所有系统平台——如 GitHub、Sentry、PagerDuty、Linear 和 Datadog 等——从而记录你代码库中发生的所有事件。
Every PR gets reviewed against that incident history automatically.
每一份公关资料都会自动根据相关事件历史进行审核。
If a diff matches a pattern that caused a past failure, Entelligence flags it with the exact incident cited.
如果差异与导致过去故障的某种模式相匹配，Entelligence 就会标记该差异，并明确指出具体的事件原因。
Real example of what it catches:
这就是它所能捕捉到的真实例子：
plaintext
明文
PR #4821 adds a fetch() call with no timeout.

Entelligence review comment:
"This pattern matches Incident #2847 (SEV-1, payment timeout).
The original incident took 4 hours to resolve.
This fetch() has no timeout and no connection-pool metrics —
the same gap that caused the cascade.

Suggested fix:
response = await fetch('/api/charge', {
timeout: 5000,
signal: AbortSignal.timeout(5000),
});
"
It cites the incident. It shows the fix. It prevents the repeat.
它提到了那起事件。它展示了解决方案。这样的措施可以防止类似情况再次发生。
Measured across 1M+ PRs and 2,400+ organizations:
在超过 100 万家用户和 2400 多家组织中进行了测量：
→ $0.44 of every AI coding dollar goes to bug fixing
→ $0.27 goes to rework
→ Only $0.18 reaches production
每投入 1 美元用于人工智能编程开发，就有 0.44 美元被用于缺陷修复工作。
→ 0.27 美元将用于重新处理工作。
→只需 0.18 美元即可实现生产
Teams using Entelligence moved that from $0.18 to $0.41 reaching production.
使用 Entelligence 的团队将价格从 0.18 美元提高到了 0.41 美元，从而实现了量产。
43% of incidents auto-resolved. 61 recurring bugs blocked per quarter.
43%的故障情况能够自行解决。每季度有 61 个重复出现的漏洞被修复。
For a one-person company: you cannot afford a Friday night production outage.
对于一家只有一个人组成的公司来说，你无法承受周五晚上生产中断的情况。
Entelligence is the senior engineer who never sleeps, remembers every incident, and reviews every PR.
Entelligence 是那位永远不休息的高级工程师，他记得所有的事件，还会审查每一份公关报告。
Set it up in 20 minutes:
在 20 分钟内就能设置好：
plaintext
明文
Step 1: Go to entelligence.ai → Sign up free

Step 2: Connect your stack:
→ GitHub or GitLab (PR review — takes 5 minutes)
→ Sentry / PagerDuty / Datadog (incident history — takes 10 minutes)
→ Linear or Jira (ticket tracking — optional)

Step 3: Let Entelligence index your incident history
(20-30 minutes for existing repos. Runs in background.)

Step 4: Add to your Fable engineering prompt:
"Note: Entelligence will review every PR against our incident history.
When writing code, flag anything that:

- Makes external calls without timeouts
- Modifies shared state without proper locking
- Changes authentication or payment paths
- Skips error handling on critical paths
  These are our highest-risk incident patterns."

Step 5: When any incident fires, run this Fable prompt:
"Entelligence detected this incident: [paste alert]
Investigate the root cause.
Generate a fix with tests.
Write the lesson to ~/company/memory/engineering.md in this format:
Incident: [description]
Root cause: [what actually broke]
Fix applied: [what changed]
Prevention: [how to detect this pattern in future PRs]"
The full bug lifecycle on complete autopilot:
在完全自动驾驶的情况下，整个故障生命周期的运作过程：
plaintext
明文
Production alert fires (Sentry / PagerDuty)
↓
Entelligence detects the anomaly in spans/logs/metrics
↓
Spawns parallel diagnosis agents
↓
Fable investigates root cause against codebase
↓
Fable writes the fix + tests
↓
Entelligence verifies fix against full incident history
↓
PR created automatically with full context
↓
You review and approve — 5 minutes ← only step requiring you
↓
Fix deployed and verified in production
↓
Incident closed. Lesson written to memory.
↓
Same pattern automatically blocked in all future PRs
You never wake up to broken production again.
你永远不会再经历那种生产设施被破坏的情况了。
You never pay to fix the same bug twice.

你永远不必为修复同一个错误而支付两次费用。

Department 5 — Support
第五部门——支持部门
Support is where solo founders quietly bleed.
支持是那些独自创业的人默默付出代价的地方。
Tickets pile up. Customers churn. Nobody notices until revenue drops.
门票数量不断增加。顾客们来来去去。直到收入下降之前，没有人注意到这个问题。
plaintext
明文
You are my Support Director.

Read ~/company/products.md and ~/company/customers.md first.

For every incoming support ticket, run this workflow:

━━━ STEP 1: TRIAGE ━━━

Classify the ticket:

- Type: Bug / Feature request / How-to question / Billing / Complaint / Praise
- Urgency: Critical (blocks usage) / High (frustrates significantly) / Low
- Sentiment score: 1-5 (1=very angry, 5=happy)
- Churn risk: High / Medium / Low

If churn risk is HIGH: do NOT process normally. Escalate immediately to me with:
[Customer name] | [Plan] | [MRR] | [Their complaint] | [Suggested response]

━━━ STEP 2: DRAFT RESPONSE ━━━

Write a response that:

- Opens by acknowledging their specific issue (not "I understand your frustration")
- Answers the question completely and practically
- If it's a bug: gives a workaround now + honest timeline if possible
- If it's a feature request: thanks them genuinely + adds to feature tracker
- Ends with one question to confirm we resolved it

Rules:

- Sound like a human, not a help desk
- Under 150 words unless technical depth is genuinely needed
- Never use: "per my last email" / "as mentioned" / "I understand your frustration"

━━━ STEP 3: KNOWLEDGE BASE UPDATE ━━━

After drafting:

- Is this question asked more than once per month? Yes/No
- If yes: write an FAQ entry → save to ~/company/docs/faq.md
- Did the product confuse them? Yes/No
- If yes: note the UX issue → save to ~/company/state/ux-issues.md

━━━ STEP 4: WEEKLY CHURN SCAN ━━━

Every Friday, scan ~/company/state/support-tickets.md from the past 14 days.

Flag any customer who:
→ Submitted 2+ tickets in 2 weeks
→ Used words: disappointed, frustrated, cancel, refund, switching, considering
→ Had a ticket unresolved for more than 48 hours
→ Downgraded their plan

Output:
| Customer | Plan | MRR at risk | Complaint pattern | Recommended action |
Sort by MRR at risk, highest first.

I will personally contact everyone on this list today.
The churn prevention scan is the one that pays for everything.
防滚动扫描功能可以承担所有费用。
Most companies find out a customer churned after they cancel.
大多数公司在客户取消订阅服务后才会意识到该客户已经流失了。
Your company finds out three weeks before.
你的公司是在三个月前才得知这一情况的。
Department 6 — Operations
第六部门——运营事务
Most underrated department. Highest leverage.
最被低估的部门。拥有最大的影响力。
Daily briefing — runs every morning at 9am:
每日简报——每天上午 9 点举行：
plaintext
明文
/loop every day at 9am →

You are my Executive Assistant.

Read:

- ~/company/state/projects.md
- ~/company/state/pipeline.md
- ~/company/state/support-tickets.md
- ~/company/memory/lessons.md (last 7 days only)

Generate my daily briefing:

━━━ TODAY'S BRIEFING — [Date] ━━━

### 🚨 Needs attention today (time-sensitive, cannot wait)

[2-3 items max. If nothing: say "Nothing critical today."]

### 💰 Pipeline status

[Deals in each stage. Any that went cold or moved forward. Revenue at risk.]

### 🎧 Support

[Open tickets: count by urgency. Any churn risks from yesterday.]

### ⚡ Top 3 priorities for today

[Ranked by impact × urgency. Not just what's loudest.]

### 💡 One lesson from the past 7 days

[The single most relevant insight from ~/company/memory/lessons.md]

Keep the entire briefing under 300 words.
I read this in 2 minutes and know exactly what to do.
SOP generator — captures every process automatically:
Every time I describe a process to you, do the following:

1. Document it as a Standard Operating Procedure
2. Save to ~/company/sops/[process-name].md
3. Use this format:

# [Process Name]

What this does: [one sentence]
When to run: [trigger or schedule]
Who runs it: [Fable / Me / Both]

## Steps

1.
2.
3. ...

## Success looks like

[How to know it worked]

## Common mistakes

[What goes wrong and how to avoid it]

## Automation opportunity

[Any step that could be fully automated — flag it]

After documenting: tell me which steps I could eliminate entirely
by connecting this to another system or agent.

2 layers that make this compound
这种化合物由两层结构组成。
Verification layer
验证层
Most people build: Task → Output → Done
大多数人遵循的顺序是：任务 → 输出结果 → 完成工作。
You build: Task → Output → Verify → Fix → Done
你进行以下操作：任务 → 输出结果 → 验证 → 修复 → 完成
Add to every department prompt:
将所有部门的提示都添加进去：
plaintext
明文
After completing this task, self-review your output:

1. Does it directly address what was asked?
2. What's missing that would make this more useful?
3. What assumption did I make that might be wrong?
4. What's the most likely failure mode in practice?

If you find a problem: fix it before delivering.
If uncertain: flag with [VERIFY] so I know to check it.
Do not deliver work you know has gaps.
Memory layer — the actual moat
记忆层——真正的沟壑
Not your prompts. Not your tools. Your memory.
不是你的提示。不是你的工具。是你的记忆。
Every department already writes to ~/company/memory/.
每个部门都已经开始撰写相关报告了，这些报告将提交给~/company/memory/.。
Add this meta-instruction once:
请重复添加这条元指令一次：
plaintext
明文
Every Sunday at 7pm, run the weekly memory consolidation:

Read all files in ~/company/memory/ from the past 7 days.

Generate a consolidated weekly report:

- Top 3 things that worked across all departments
- Top 3 things that failed and why
- One system-level improvement to make next week
- Any pattern emerging across multiple departments

Save to ~/company/memory/weekly-[YYYY-MM-DD].md

Then: suggest the one workflow that would give me the highest
leverage improvement based on this week's lessons.
The system gets smarter every week without you doing anything extra.
这个系统每周都会变得更加智能，而您无需做任何额外的事情来支持这一进程。
5 Fable prompting rules that change everything (finally)
5 条传说中的规则，它们改变了一切（终于）
Most people use Fable like they used ChatGPT.
大多数人使用 Fable 的方式，就像使用 ChatGPT 一样。
That's why most people get mediocre results.
这就是为什么大多数人只能取得中等水平的效果。
Rule 1 — Match effort to the task
规则 1——根据任务的性质来调整努力程度
→ Low/medium: quick answers, rewrites, simple lookups
→ High: your default for everything that matters
→ Xhigh: hardest problems, complex builds, non-negotiable quality
→ /loop: recurring workflows you never want to start manually again
→ 低/中等难度：能够快速给出答案，进行改写操作，以及进行简单的查找任务。
→ 高：你对所有重要事物的默认行为/态度
→ Xhigh：最困难的问题，复杂的构建方式，不可妥协的质量要求
→ /loop：这些工作流程是重复进行的，你根本不想再次手动启动它们。
Rule 2 — Tell it why, not just what
规则 2——要说明原因，而不仅仅是事情本身
plaintext
明文
❌ "Write a cold email to this prospect"

✅ "I'm doing outreach for [product] targeting [role] at [company type].
They have [specific pain]. The goal is a reply, not a booked meeting.
Write a cold email: specific observation → pain → solution → proof → soft CTA.
Under 100 words. No corporate language."
Rule 3 — Shorter beats longer
规则 3——较短的拍号对应更长的音符
Over-prompting constrains Fable.
过度提示会限制 Fable 的表现能力。
Give it the goal and constraints. Let it decide the method.
给定目标与约束条件后，让系统自行决定采用何种方法来实现目标。
If you write a 500-word prompt for something a 50-word prompt would handle: the 500-word version often produces worse results.
如果你为那些只需要 50 个单词就能描述的内容编写一个 500 字的提示，那么这样的版本往往会产生更糟糕的结果。
Rule 4 — Set your checkpoints explicitly
规则 4——明确设定你的检查点
plaintext
明文
"Pause for me only when:
→ The next action is irreversible
→ You hit a blocker you cannot resolve
→ You need information only I have

Otherwise: keep going. Report back when complete."
Without this: Fable checks in constantly. With this: it runs.
没有这个的话，Fable 会一直处于检查状态。有了这个之后，程序就能正常运行了。
Rule 5 — Use /loop for everything recurring
规则 5——所有重复出现的操作都使用/loop 标签表示。
plaintext
明文
/loop every Monday at 8am → run research department workflow
/loop every day at 9am → generate daily briefing
/loop every Friday at 5pm → run churn prevention scan
/loop every Sunday at 7pm → run memory consolidation
Set once. Runs forever.
设置一次后，就会一直运行下去。
The implementation order
实施顺序
Do not build all six departments at once.
不要一次性构建所有六个部门。
Build in this order. Each one unlocks the next.
按照以下顺序进行构建。每一个步骤的完成都会解锁下一个步骤。
Week 1 — Foundation (2 hours)Create the company brain folder. Fill all 5 templates. This is the foundation everything else reads from. Nothing else works properly without this.
第 1 周——基础部分（2 小时）  
创建公司的知识文件夹。填写所有 5 个模板。这是一切的基础，其他所有内容都是基于这个基础来展开的。没有这个基础，其他的一切都无法正常运行。
Week 2 — Research department (1 hour setup)Copy the Research Director prompt. Run the first weekly research loop manually. Monday: you get your first strategic report.
第 2 周——研究部门工作（1 小时的准备工作）  
复制研究主管的指令。手动运行第一个每周的研究流程。周一：你将得到你的第一份战略报告。
Week 3 — Marketing: X virality (1 hour setup)Copy the pre-launch engineering prompt. Run it on your next 3 posts before publishing. Stay active for 60 minutes after each post.
第 3 周——市场营销：X 型病毒式传播效果分析（1 小时的准备工作）请复制发布前的工程化提示信息，在发布前对接下来 3 篇帖子进行应用。发布后，每篇帖子后保持活跃状态 60 分钟。
Week 4 — Engineering layers (2 hours)Connect Entelligence to GitHub + Sentry (20 minutes). Copy the Engineering Director prompt. First PR gets reviewed against incident history automatically.
第 4 周——构建层结构（2 小时时间）。将 Entelligence 与 GitHub 以及 Sentry 连接起来（20 分钟）。复制工程总监的指令。第一个提交将被自动审核，以检查是否存在与事件历史相关的冲突。
Month 2 — Sales machineCopy the Sales Director prompt. Run it on first 20 prospects. Set up AI calling layer for non-openers.
第 2 个月——销售提升计划  
复制销售主管的提示内容，将其应用于前 20 位潜在客户。为那些尚未被转化的客户设置人工智能语音通话功能。
Month 3 — Support + OpsCopy the Support Director prompt. Set up daily briefing /loop. Set up weekly churn prevention scan.
第三个月——支持与运维方面的工作。复制“支持主管”的提示信息。安排每日的会议/循环通知。同时开展每周的流量波动预防扫描工作。
Month 6 — Full systemEvery department runs on schedule without you starting it. Memory compounds weekly. You design. Fable executes.
第 6 个月——完整系统  
每个部门都在按计划运行，无需你亲自启动它们。内存量每周都会增加。你负责设计，Fable 则负责执行。
What month 6 looks like
6 年级的校园生活是什么样的呢？
Monday 9am. You open your laptop.
周一，上午 9 点。你打开笔记本电脑。
The briefing is ready:
简报已经准备好了：
→ Research report filed — 3 opportunities, 2 competitor moves
→ 3 SEO articles published while you slept
→ 200 outreach emails sent, 4 qualified meetings booked
→ 12 support tickets triaged, 2 escalated to you
→ 2 PRs reviewed by Entelligence — 0 incident patterns detected, ready to approve
→ Newsletter drafted and ready to send
→ 1 churn-risk customer flagged with recommended action
已提交研究报告——存在 3 个机会，有 2 个竞争对手的动向
→ 在你睡觉的时候，发布了 3 篇关于搜索引擎优化的文章
→ 发送了 200 封宣传邮件，成功安排了 4 场合适的会议。
→ 已处理 12 个支持问题，其中 2 个需要上报给上级处理
→ 有 2 个 PR 被 Entelligence 审核了——未发现任何问题，可以批准了。
→ 新闻通讯已起草完成，可以发送了。
→ 有 1 位存在欺诈风险的客户已被标记，并给出了相应的建议措施
Your job today:
你今天的任务：
→ Review 2 PRs: 20 minutes
→ Approve the newsletter: 5 minutes
→ 4 sales calls: 2 hours
→ Call the churn-risk customer: 30 minutes
→ 审核 2 个公关计划：需要 20 分钟时间
批准这份通讯：只需 5 分钟时间
→ 4 次销售拜访：每次 2 小时
→ 联系那些容易流失客户的团队：需要 30 分钟时间
Total: 3 hours of high-judgment work.
总时长：3 小时的高强度工作。
Everything else ran without you.
没有你，其他的一切都能正常运转。
The bottleneck is no longer production.
瓶颈问题不再存在于生产环节。
The bottleneck is now judgment.
现在的瓶颈在于判断力。
And that's exactly where founders create the most value.
而正是在这个阶段，创始人能够创造出最大的价值。
The companies that win over the next decade won't have the best prompts.
在接下来的十年里，能够取得成功的公司不会拥有最优秀的策略或方案。
They'll have the best operating systems.
他们将拥有最优秀的操作系统。
Claude Fable 5 is the first model capable of running one.
Claude Fable 5 是第一个能够运行该模型的模型。
If this was useful:
如果这能有所帮助的话：
→ Repost to share it with every solo founder you know → Follow @sairahul1 for more systems that work without you → Bookmark this — every prompt above is copy-paste ready
→ 分享这个帖子，与你认识的每一位创业者一起分享→ 关注@sairahul1，了解更多无需你参与的运作系统→ 收藏这个页面——以上所有提示都可以直接复制粘贴使用
I write about AI, building products, and systems that run while you sleep.
我撰写关于人工智能、产品开发以及那些在您沉睡时运行着的系统的文章。
Tools mentioned:
→ Claude Fable 5: claude.ai
→ Entelligence (automated PR review + incident prevention): entelligence.ai
→ Bland / Vapi / Retell: AI calling agents
提到的工具：
→ 克劳德·法布尔 5：claude.ai
→ Entelligence（自动化公关审核 + 事件预防）：entelligence.ai
→ 布兰德/瓦皮/雷特尔：人工智能呼叫代理
Want to publish your own Article?
想要发表自己的文章吗？
Upgrade to Premium
升级为高级版
Rahul
@sairahul1
Building with AI. Sharing what's wild, what's practical, and what's next. Founder of http://nichetraffickit.com and http://theaibuilders.co
采用人工智能技术的建筑。分享那些疯狂的想法、实用的解决方案以及未来的发展方向。 http://nichetraffickit.com 和 http://theaibuilders.co 的创始人
