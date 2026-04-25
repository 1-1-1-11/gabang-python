# gobang-python 双 Agent 分步重构计划

## Summary

- 目标：把原 React + Web Worker 五子棋项目重构为以 FastAPI/Python 后端为核心的五子棋项目，并在后续允许从零创建全新前端。
- 远程边界：GitHub 远程不得保存原始 JS 源码、原始 React 静态资源、旧 JS 测试、原始 README 或旧 JS 构建配置。
- 协作模式：Codex 负责实现、测试、提交和推送；Claude Code 负责审查 Markdown，不直接改代码。
- 任务粒度：后续按“能力级”拆分，每个有效任务使用独立分支和 `.worktrees/<编号>-<名称>` worktree。
- 合并门禁：相关测试通过、审查记录写入、Blocker/Major 已处理后，任务分支才能合回 `main`。
- 远程仓库：`https://github.com/1-1-1-11/gabang-python.git`。如 Git for Windows `schannel` 报凭据错误，使用 `git -c http.sslBackend=openssl ...`。

## Current State

- Task 1-5 已完成并合回 `main`。
- 当前后端具备 FastAPI health check、棋盘规则、评分搜索、内存 session 游戏接口。
- 当前验证命令：`py -m pytest backend\tests -q`。
- Task 6/7 的旧定义依赖原始 React/JS 源码，已废弃。
- Task 8 用于重对齐任务台账和后续路线图，不实现功能代码。

## Collaboration Protocol

- `docs/collaboration/TASKS.md` 是任务台账来源，分为已完成、已废弃、待执行三段。
- Claude Code 审查写入 `docs/collaboration/reviews/<任务编号>-<任务名>.md`。
- 审查格式固定为 `Blocker / Major / Minor / Question`，并在末尾记录 Codex 处理结果。
- 每个有效任务完成实现后，推送任务分支到 GitHub 供审查留痕。
- 每个有效任务合回 `main` 后，更新台账合并状态并推送 `main` 到 GitHub。
- 根 `README.md` 只描述当前远程仓库内的项目，不恢复原始 JavaScript README。

## Repository Boundary

- 原始项目路径禁止进入远程历史：`src/`、`public/`、`images/`、旧 `tests/`、`package.json`、`package-lock.json`、`config-overrides.js`、`vue.config.js`、`.eslintignore`、`.spec-workflow/`。
- 原始 JS 代码只允许作为本地人工参考放在被忽略目录，不得提交。
- 全新 JS 前端可以作为后续任务进入远程，但必须满足：
  - 从空白骨架或新写代码开始。
  - 不复制、迁移、改名提交原始 JS 项目文件。
  - 审查记录必须明确检查旧 JS 路径和来源边界。
- Python 后端、Python 测试、协作文档、后续全新前端代码属于允许范围。

## Public Interfaces

### `GET /api/health`

返回服务健康状态：

```json
{"status": "ok"}
```

### `POST /api/games/start`

Request:

```json
{
  "size": 15,
  "ai_first": true,
  "depth": 4
}
```

Response: 棋局快照，包含 `session_id`、`board`、`winner`、`current_player`、`history`、`size`、`score`、`best_path`、`current_depth`。

### `POST /api/games/{session_id}/move`

Request:

```json
{
  "position": [7, 7],
  "depth": 4
}
```

Response: 玩家落子和 AI 应手后的棋局快照。

### `POST /api/games/{session_id}/undo`

Response: 撤销最近一轮落子后的棋局快照；AI 先手只有 1 步历史时撤销该单步。

### `POST /api/games/{session_id}/end`

Response: 最后棋局快照，并释放内存 session。

## Step Plan

### Task 1: Git 基线与协作骨架

- 已完成。当前远程历史已改写为 Python 重构版干净根提交。

### Task 2: Python 后端骨架

- 已完成。新增 FastAPI 后端结构、`GET /api/health`、pytest health check 和 Python 依赖记录。

### Task 3: 棋盘规则迁移

- 已完成。迁移棋盘初始化、落子、悔棋、胜负判断、坐标转换、合法落点，并补充 Python 测试。

### Task 4: 评分与搜索迁移

- 已完成。迁移棋形、评分、Zobrist、缓存、minmax、VCT/VCF 入口，并补充 AI 搜索测试。

### Task 5: FastAPI 游戏接口

- 已完成。实现 start、move、undo、end、内存多 session、session 上限和游戏结束边界处理。

### Task 6: 前端状态字段统一

- 已废弃。旧定义依赖原始 React/JS 源码，不再执行。

### Task 7: 前端接入 Python API

- 已废弃。旧定义依赖原始 React/JS 源码，不再执行。

### Task 8: 任务台账与路线图重对齐

- 使用 `task/08-ledger-realignment` 分支和 `.worktrees/08-ledger-realignment` worktree。
- 重排 `TASKS.md` 为已完成、已废弃、待执行三段。
- 将后续路线图改成能力级任务。
- 明确全新 JS 前端允许范围和原始 JS 禁止范围。
- 不实现 Task 9-12 的功能代码。
- Commit：`docs: 重对齐任务台账与路线图`

### Task 9: 一键启动与文档

- 使用 `task/09-dev-scripts-docs` 分支和 `.worktrees/09-dev-scripts-docs` worktree。
- 增加 Python 后端运行脚本或运行说明。
- 完善 README 的安装、测试、启动、API 入口说明。
- 不引入旧 Node/React 项目依赖。
- Commit：`docs: 补充 Python 重构运行说明`

### Task 10: API 合同与文档稳定

- 使用 `task/10-api-contract-docs` 分支和 `.worktrees/10-api-contract-docs` worktree。
- 为游戏接口补充 response model、错误响应约定、`best_path` 语义和 OpenAPI 示例。
- 保持现有 API 路径兼容。
- Commit：`feat: 稳定游戏 API 合同文档`

### Task 11: 全新前端项目骨架

- 使用 `task/11-new-frontend-skeleton` 分支和 `.worktrees/11-new-frontend-skeleton` worktree。
- 从空白骨架创建全新前端，不复用原始 JS 项目文件。
- 审查时必须验证旧 JS 禁止路径仍未进入远程历史。
- Commit：`feat: 添加全新前端项目骨架`

### Task 12: 全新前端接入游戏 API

- 使用 `task/12-new-frontend-game-api` 分支和 `.worktrees/12-new-frontend-game-api` worktree。
- 实现 start、move、undo、end 的浏览器交互。
- 前端字段使用后端 `snake_case` API 响应，不恢复旧 Redux 状态迁移任务。
- Commit：`feat: 接入全新前端游戏流程`

## Test And Review

- 每步提交前：运行相关测试，查看 `git diff` 和 `git status`。
- 每步边界检查：

```powershell
git log --branches -- src public images tests package.json package-lock.json config-overrides.js vue.config.js .eslintignore .spec-workflow
```

- 期望边界检查无输出。
- 后端回归命令：

```powershell
py -m pytest backend\tests -q
```

- 每步汇报：做了什么、测了什么、Claude Code 结论、处理 commit、下一步。

## Known Environment Notes

- 后端命令统一使用 `py`，不要使用 Windows Store shim 指向的 `python`。
- `.worktrees/` 必须保持被 `.gitignore` 忽略。
- PowerShell 可能在非 UTF-8 输出下显示中文乱码；文件本身按 UTF-8 读取。
- 如果 HTTPS 推送遇到 `schannel` 凭据错误，使用 `git -c http.sslBackend=openssl push ...`。
