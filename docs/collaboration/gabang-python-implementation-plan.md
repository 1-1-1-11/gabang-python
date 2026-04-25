# gobang-python 双 Agent 分步重构计划

## Summary

- 目标：把现有 React + Web Worker 五子棋项目重构为 FastAPI/Python 后端优先的五子棋项目；远程仓库只保存 Python 重构版代码、测试和相关文档。
- 协作模式：Codex 负责实现、测试、提交；Claude Code 只负责审查 Markdown，不直接改代码。
- 隔离方式：每个能力任务创建 `task/<编号>-<名称>` 分支和 `.worktrees/<编号>-<名称>` worktree。
- 初始例外：如果仓库还没有任何 commit，Task 1 必须先在 `main` 上完成原始项目基线提交和协作骨架提交；从 Task 2 开始再使用 task 分支与 worktree。
- 合并门禁：相关测试通过、subagent 审查通过、Claude Code 审查无 Blocker/Major 后，任务分支才能合回主分支。
- 远程仓库：使用 `https://github.com/1-1-1-11/gabang-python.git`。如果当前环境 HTTPS 访问报 `schannel` 凭据错误，可使用命令级参数 `git -c http.sslBackend=openssl ...`。

## Plan Review Notes

- 当前仓库 `main` 分支没有任何 commit，且所有项目文件处于未跟踪状态。因此不能直接创建每个任务的 worktree；必须先完成 Task 1 的两个基础 commit。
- `python --version` 当前指向 Windows Store shim 且返回失败；后端命令统一使用 `py` 或明确的 Python 3.12+ 解释器。当前可用命令为 `py --version`。
- 当前 `.gitignore` 尚未忽略 `.worktrees/`；Task 1 必须先添加该忽略项，并用 `git check-ignore .worktrees/` 验证。
- 原始 JS 项目基线提交已经通过历史改写清理；远程主线不得保留原始 JS 源码、React 静态资源、旧 JS 测试、原始 README 或 JS 构建配置。

## Collaboration Protocol

- 新增并维护 `docs/collaboration/TASKS.md`：记录任务编号、分支、worktree、状态、实现 commit、审查文件、合并状态。
- 新增 `docs/collaboration/CLAUDE_REVIEW_PROMPT.md`：固定 Claude Code 审查提示词，要求只审本次 diff，不改代码。
- Claude Code 审查写入 `docs/collaboration/reviews/<任务编号>-<任务名>.md`。
- 审查格式固定为 `Blocker / Major / Minor / Question`。
- Blocker/Major 阻塞合并；实现方修复后记录处理结果并跑测试，不强制 Claude 二次复审。
- 协作文档和对应代码一起提交，保证每个任务的实现、审查、处理记录可追溯。
- 远程留痕：每个任务审查结束并记录处理结果后，必须推送任务分支到 GitHub；合回 `main` 后，也必须推送 `main` 到 GitHub。
- README 规则：根 `README.md` 必须只描述 Python 重构版；原始 JavaScript 项目的 README 只能隔离到 `docs/legacy/`，该目录必须被 `.gitignore` 忽略，不得提交到远程。
- 源码边界：`src/`、`public/`、`images/`、旧 `tests/`、`package.json`、`package-lock.json`、`config-overrides.js`、`vue.config.js`、`.eslintignore` 属于原始 JS 项目路径，必须被移出 Git 远程历史并加入忽略规则。

## Key Decisions

- 后端结构：新增 `backend/app` 和 `backend/tests`，使用 FastAPI、pytest、httpx。
- 前端结构：原始 React 源文件不进入远程仓库；后续若需要前端，应在新的任务中以 Python 重构版项目边界重新引入。
- 命名规范：后端 API 和前端 Redux state 统一使用 `snake_case`。
- AI 策略：尽量等价迁移，不主动提升棋力；Zobrist 使用固定种子；搜索深度沿用 `2/4/6/8`；第一阶段不限时。
- 旧代码策略：原始 JS 代码只允许在本地忽略目录中作为人工参考，不得提交到 GitHub。
- 依赖与启动：第一阶段只提交 Python 依赖锁定文件 `backend/requirements.lock.txt`；不提交 `package-lock.json`。
- 文档策略：根 README 始终保持 Python 重构版说明；原 README 只保留在本地忽略目录 `docs/legacy/original-readme.md`，不进入 GitHub 远程。

## Public Interfaces

### `POST /api/games/start`

Request:

```json
{
  "size": 15,
  "ai_first": true,
  "depth": 4
}
```

Response:

```json
{
  "session_id": "uuid",
  "board": [[0]],
  "winner": 0,
  "current_player": 1,
  "history": [],
  "size": 15,
  "score": 0,
  "best_path": [],
  "current_depth": 0
}
```

### `POST /api/games/{session_id}/move`

Request:

```json
{
  "position": [7, 7],
  "depth": 4
}
```

Response: 棋局快照，字段同 start。

### `POST /api/games/{session_id}/undo`

Response: 悔棋两步后的棋局快照。

### `POST /api/games/{session_id}/end`

Response: 最后棋局快照，并释放内存 session。

## Step Plan

### Task 1: Git 基线与协作骨架

- 在 `main` 上执行本任务；这是唯一允许不使用 worktree 的初始化任务。
- 初始历史已改写：远程不得再保存原始 JS 项目基线；只保留 Python 重构版 README、后端代码、测试、协作文档和必要配置。
- 配置远程 `origin` 为 `https://github.com/1-1-1-11/gabang-python.git`
- 新增 `.worktrees/` 到 `.gitignore`，并验证 `git check-ignore .worktrees/` 成功。
- 新增协作 Markdown 模板：
  - `docs/collaboration/TASKS.md`
  - `docs/collaboration/CLAUDE_REVIEW_PROMPT.md`
  - `docs/collaboration/reviews/`
- 跟踪当前已有的 `.spec-workflow/` 模板和本计划文件。
- Commit：`chore: 建立双 Agent 协作流程`

### Task 2: Python 后端骨架

- 从本任务开始，先创建 `task/02-python-backend-skeleton` 分支和 `.worktrees/02-python-backend-skeleton` worktree。
- 新增 `backend/app`、`backend/tests`、`pyproject.toml`
- 添加 `GET /api/health`
- 生成 `backend/requirements.lock.txt`
- 相关测试：FastAPI health check
- Commit：`chore: 初始化 Python 后端项目结构`

### Task 3: 棋盘规则迁移

- 使用 `task/03-board-rules` 分支和 `.worktrees/03-board-rules` worktree。
- 迁移初始化、落子、悔棋、胜负判断、坐标转换、合法落点。
- pytest 覆盖从原始 JS 测试人工转写出的核心棋盘场景；不提交原始 JS 测试文件。
- Commit：`feat: 迁移五子棋棋盘规则到 Python`

### Task 4: 评分与搜索迁移

- 使用 `task/04-ai-search` 分支和 `.worktrees/04-ai-search` worktree。
- 迁移棋形、评分、缓存、minmax、VCT/VCF。
- 验证胜负分值、推荐点集合、无杀棋场景。
- Zobrist 哈希使用固定种子，保证测试可复现。
- Commit：`feat: 迁移五子棋 AI 搜索逻辑`

### Task 5: FastAPI 游戏接口

- 使用 `task/05-game-api` 分支和 `.worktrees/05-game-api` worktree。
- 实现 start、move、undo、end 和内存多 session。
- 不处理同一 session 并发落子，依赖前端 loading 防重复。
- API 字段统一 `snake_case`。
- Commit：`feat: 添加五子棋后端游戏接口`

### Task 6: 前端状态字段统一

- 原计划依赖原始 React 源码，已废弃。
- 如果后续仍需要前端，先新增独立计划，从空白前端或新项目骨架开始，不复用原始 JS 源文件。

### Task 7: 前端接入 Python API

- 原计划依赖原始 React 源码，已废弃。
- 如果后续仍需要前端接入，必须以新前端代码进入远程，并通过单独审查确认没有原始 JS 文件。

### Task 8: 一键启动与文档

- 使用 `task/08-dev-scripts-docs` 分支和 `.worktrees/08-dev-scripts-docs` worktree。
- 增加 Python 后端运行脚本或文档；不得引入 Node/React 原项目依赖。
- 完善 Python 重构版 README。
- 不提交原始 JavaScript README；如需保留，只放在被忽略的 `docs/legacy/original-readme.md`。
- Commit：`docs: 补充 Python 重构运行说明`

## Test And Review

- 每步提交前：运行相关测试，查看 `git diff` 和 `git status`。
- 每步审查链路：实现自查 -> subagent 审查本次 diff -> Claude Code 写审查 Markdown -> 修复阻塞问题 -> 中文 commit。
- 每步远程留痕：审查处理记录提交后执行 `git push -u origin <task-branch>`；任务合回 `main` 后执行 `git push origin main`。
- 每步汇报：做了什么、测了什么、subagent 结论、Claude Code 结论、commit 哈希、下一步。
- 旧 Vue/旧 AI 测试不阻塞第一阶段；有价值的历史 bug 场景逐步转写到 Python 测试。

## Known Environment Notes

- 当前仓库 `.git` 目录曾出现 Windows ACL Deny，导致 Codex 无法创建 `.git/index.lock`。如果再次出现，需要移除 `.git` 上的显式 Deny，并给 Codex 运行用户或 `XJY\CodexSandboxUsers` 授权。
- 当前 HTTPS 远程曾因 Git for Windows `schannel` 报 `SEC_E_NO_CREDENTIALS`。已验证命令级 `http.sslBackend=openssl` 可访问远程空仓库。
- 如果 `git ls-remote` 对空仓库没有输出但退出码为 0，这是正常情况。
