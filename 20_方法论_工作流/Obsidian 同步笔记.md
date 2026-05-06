
官方文档：https://obsidian.md/zh/help/sync-notes#Git

## **后续日常同步怎么做**

- 拉取远端最新（推荐无分叉安全模式）：
    - `git fetch --prune`
    - `git merge --ff-only origin/main`（等价于常用的 `git pull --ff-only`）
- 推送本地改动到远端：
    - `git add -A`
    - `git commit -m "更新笔记"`
    - `git push`


## 插件：Git

## 1. source
- https://sug.xyz/rj/2026/04/09/obsidian-%E7%AC%94%E8%AE%B0-github-%E5%90%8C%E6%AD%A5%E5%AE%8C%E6%95%B4%E6%95%99%E7%A8%8B%EF%BC%9A%E4%BB%8E0%E5%88%B01%E5%AE%9E%E7%8E%B0%E5%85%8D%E8%B4%B9%E8%B7%A8%E8%AE%BE%E5%A4%87%E5%A4%87%E4%BB%BD/


## 2. takenotes

- ### 日常同步的3种方式

- **全自动模式（日常推荐）**：配置完成后，无需任何手动操作，每10分钟自动提交、拉取、推送，打开软件自动同步最新笔记。
    
- **手动一键同步（立刻同步）**：按 `Ctrl+P` 打开命令面板，输入 `Git: Commit and sync`，一键完成全流程同步。


## 3. keywords
- 