结论先说清楚：

> **OpenCode 建议“全局安装 + 项目内配置”，而不是二选一。**

单纯放全局或单纯放项目，都不是最优解。

---

# 一、为什么不能只选一个？

## ❌ 只全局安装的问题

优点：

- 到处能用（CLI 很方便）
    

但问题是：

- ❌ 不同项目的 Agent / skills 会冲突
    
- ❌ 配置不可复现（换机器就废）
    
- ❌ 无法版本化（你后面一定会踩坑）
    

---

## ❌ 只项目安装的问题

优点：

- 可控、可复现
    

但问题是：

- ❌ 使用成本高（每个项目都要装）
    
- ❌ 不适合 CLI 工具的“随手调用”场景
    
- ❌ 失去“操作系统”的感觉
    

---

# 二、最佳实践（推荐你直接用这个）

## ✅ 模式：Global Runtime + Project Config

---

## 1️⃣ 全局安装（一次即可）

```bash
brew install anomalyco/tap/opencode
opencode --version
```

👉 作用：

> 提供一个“Agent 操作系统入口”（CLI runtime）

补充：

- macOS 上推荐用 Homebrew 安装与升级（版本更新更及时）。
- 如果不方便用 Homebrew，也可以用官方脚本或 Node 全局安装（包名是 `opencode-ai`，不是 `opencode`）：
  - `curl -fsSL https://opencode.ai/install | bash`
  - `npm install -g opencode-ai`

---

## 2️⃣ 每个项目放配置（核心）

在你的 Obsidian 项目里：

```text
.opencode/
├── agents/
│   └── planner.md
└── skills/
    ├── summarize-note/
    │   └── SKILL.md
    └── build-note/
        └── SKILL.md
```

👉 作用：

> 定义你的“Agent 能力系统”

---

## 3️⃣ memory（项目级）

用：

```text
AGENTS.md
```

或：

```text
.opencode/
```

👉 存：

- 项目规则
    
- 写作风格
    
- 知识结构
    

---

# 三、类比一下（帮助你建立长期认知）

这个结构其实非常经典：

|层|类比|
|---|---|
|全局 opencode|Python / Node runtime|
|项目 config|requirements.txt / package.json|
|skills|你的函数库|
|agent|应用逻辑|

---

👉 关键 insight：

> **OpenCode ≈ Node.js  
> 你的项目 ≈ npm package**

---

# 四、结合你现在的目标（Obsidian Agent）

你应该这样组织：

---

## 📂 Vault 结构

```text
Vault/
├── 02 Sources/
├── 03 Notes/
├── .opencode/
│   ├── agents/
│   ├── skills/
│   │   └── summarize-note/
│   │       └── SKILL.md
│   └── commands/
├── opencode.json
└── AGENTS.md
```

---

## 使用方式

```bash
cd Vault
opencode
```

👉 OpenCode 会自动读取当前目录配置

---

# 五、一个更高级但很实用的建议

## 👉 给不同项目做“Agent Profile”

比如：

```text
~/.opencode/profiles/
├── obsidian/
├── coding/
├── trading/
```

然后：

```bash
opencode --profile obsidian
```

---

👉 这样你可以：

- 知识型 Agent
    
- 编程型 Agent
    
- 投资分析 Agent
    

**完全隔离**

---

# 六、什么时候需要“项目内安装”？

只有两种情况：

---

### 1️⃣ 团队协作

你需要：

```json
"devDependencies": {
  "opencode": "x.x.x"
}
```

---

### 2️⃣ 你在开发 opencode 插件 / runtime

---

否则：

> ❌ 不建议项目内安装

---

# 七、帮你压缩成一句话

> **OpenCode 装在全局，是“操作系统”；  
> 能力定义放在项目，是“你的大脑”。**

---

# 八、给你一个落地建议（直接可执行）

你下一步可以这样做：

---

## Step 1

```bash
brew install anomalyco/tap/opencode
opencode --version
```

---

## Step 2（你的 Vault 里）

创建：

```bash
mkdir -p .opencode/skills/summarize-note
```

---

## Step 3

写第一个 skill：

```markdown
---
name: summarize-note
description: 总结一篇 Obsidian 笔记，输出要点与行动项
---

## 输出格式

- 5 条要点
- 3 条行动项（如果适用）
- 1 段 2-3 句的结论

## 约束

- 全程中文
- 保留 Obsidian 链接格式（如 [[Note]]）
```

---

## Step 4

```bash
opencode
```

直接开始跑

---

如果你愿意，下一步我可以帮你：

👉 设计一套 **“最小可用 Obsidian skills（5个就够）”**

这一步会让你从“架构理解”进入“真正开始生产内容”。
