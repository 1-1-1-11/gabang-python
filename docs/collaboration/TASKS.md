# gobang-python 协作任务台账

## 初步验收状态

- 2026-04-27 完成验收演示阶段收敛。
- 验证命令：`py -m pytest backend\tests -q`、`npm run test:e2e`。
- 最近结果：`91 passed in 2.34s`；Playwright E2E `5 passed`。
- 结论：当前 FastAPI 后端、棋盘规则、AI 搜索与 smoke 基准、可选 Redis 会话、静态前端、Playwright 浏览器验收和交付文档可作为验收演示基线。
- 后续优先级：维护 README/TASKS/CLAUDE 一致性；可选增强真实 Redis 环境验收、多实例部署演练和更强 AI 棋力评估。

## 已完成任务

| 任务 | 分支 | Worktree | 状态 | 实现 Commit | 审查文件 | 合并状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Task 1: Git 基线与协作骨架 | `main` | 当前仓库 | 已完成 | `f5ec6bf` | 不适用 | 不适用 |
| Task 2: Python 后端骨架 | `task/02-python-backend-skeleton` | `.worktrees/02-python-backend-skeleton` | 已完成 | `5e7a596` | `docs/collaboration/reviews/02-python-backend-skeleton.md` | 已合并 |
| Task 3: 棋盘规则迁移 | `task/03-board-rules` | `.worktrees/03-board-rules` | 已完成 | `8fc9fe3` / `bc1f80a` | `docs/collaboration/reviews/03-board-rules.md` | 已合并 |
| Task 4: 评分与搜索迁移 | `task/04-ai-search` | `.worktrees/04-ai-search` | 已完成 | `81e5a5b` / `4a2eff6` | `docs/collaboration/reviews/04-ai-search.md` | 已合并 |
| Task 5: FastAPI 游戏接口 | `task/05-game-api` | `.worktrees/05-game-api` | 已完成 | `b617be4` / `53f49f8` | `docs/collaboration/reviews/05-game-api.md` | 已合并 |
| Task 8: 任务台账与路线图重对齐 | `task/08-ledger-realignment` | `.worktrees/08-ledger-realignment` | 已完成 | `58a8782` / `466f2aa` | `docs/collaboration/reviews/08-ledger-realignment.md` | 已合并 |
| Task 9: 一键启动与文档 | `task/09-dev-scripts-docs` | `.worktrees/09-dev-scripts-docs` | 已完成 | `b8e302e` / `23572a5` | `docs/collaboration/reviews/09-dev-scripts-docs.md` | 已合并 |
| Task 10: API 合同与文档稳定 | `task/10-api-contract-docs` | `.worktrees/10-api-contract-docs` | 已完成 | `9cb1718` / `30c1a29` | `docs/collaboration/reviews/10-api-contract-docs.md` | 已合并 |
| Task 11: 全新前端项目骨架 | `task/11-new-frontend-skeleton` | `.worktrees/11-new-frontend-skeleton` | 已完成 | `cb0ae11` / `7be6a5b` | `docs/collaboration/reviews/11-new-frontend-skeleton.md` | 已合并 |
| Task 12: 全新前端接入游戏 API | `task/12-new-frontend-game-api` | `.worktrees/12-new-frontend-game-api` | 已完成 | `45ddb2f` / `325dbac` | `docs/collaboration/reviews/12-new-frontend-game-api.md` | 已合并 |
| Task 13: 运行时边界硬化 | `task/13-runtime-hardening` | `.worktrees/13-runtime-hardening` | 已完成 | `7912523` / `e7ab758` / `79bffb2` | `docs/collaboration/reviews/13-runtime-hardening.md` | 已合并 |
| Task 14: 文档与项目状态收敛 | `main` | 当前仓库 | 已完成 | `f918163` | 未单独建档 | 已推送 main |
| Task 15: 前端验收增强 | `main` | 当前仓库 | 已完成 | `f918163` | 未单独建档 | 已推送 main |
| Task 16: AI 能力基准化 | `main` | 当前仓库 | 已完成 | `f209827` | 未单独建档 | 已推送 main |
| Task 17: 运行时与部署准备 | `main` | 当前仓库 | 已完成 | `433b2ae` | 未单独建档 | 已推送 main |
| Task 18.1: Playwright 主路径 E2E | `main` | 当前仓库 | 已完成 | `eb9fef7` | subagent 只读审查 | 已推送 main |
| Task 18.2: E2E 错误路径与控件状态 | `main` | 当前仓库 | 已完成 | `2a5f55d` | subagent 只读审查 | 已推送 main |
| Task 19.1: AI 搜索全局指标 | `main` | 当前仓库 | 已完成 | `db89d51` | subagent 只读审查 | 已推送 main |
| Task 19.2: AI 宽松性能阈值 | `main` | 当前仓库 | 已完成 | `65dd7c4` | subagent 只读审查 | 已推送 main |
| Task 19.3: AI 基准文档化 | `main` | 当前仓库 | 已完成 | `f9cc58b` | subagent 只读审查 | 已推送 main |
| Task 20.1: 会话后端配置化 | `main` | 当前仓库 | 已完成 | `e9578f3` | subagent 只读审查 | 已推送 main |
| Task 20.2: 基础 Redis SessionStore | `main` | 当前仓库 | 已完成 | `0ea0062` | subagent 只读审查 | 已推送 main |
| Task 20.3: Redis 生命周期与文档 | `main` | 当前仓库 | 已完成 | `e5ef636` | subagent 只读审查 | 已推送 main |
| Task 21.1: 前端落子可读性 | `main` | 当前仓库 | 已完成 | `09cfb1f` | subagent 只读审查 | 已推送 main |
| Task 21.2: AI 信息展示 | `main` | 当前仓库 | 已完成 | `91a942b` | subagent 只读审查 | 已推送 main |
| Task 21.3: 配置体验 | `main` | 当前仓库 | 已完成 | `1b6dc00` | subagent 只读审查 | 已推送 main |
| Task 22.1: README 最终收敛 | `main` | 当前仓库 | 已完成 | `284c7ad` | subagent 只读审查 | 已推送 main |
| Task 22.2: TASKS 台账校准 | `main` | 当前仓库 | 已完成 | `b591fa3` | subagent 只读审查 | 已推送 main |

## 已废弃任务

| 任务 | 分支 | Worktree | 状态 | 实现 Commit | 审查文件 | 合并状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Task 6: 前端状态字段统一 | - | - | 已废弃：依赖原始 React/JS 源码，违反 Python-only 远程边界 | - | - | 不适用 |
| Task 7: 前端接入 Python API | - | - | 已废弃：依赖原始 React/JS 源码，违反 Python-only 远程边界 | - | - | 不适用 |

## 下一阶段计划

| 任务 | 阶段 | 状态 | 目标 | 验收重点 |
| --- | --- | --- | --- | --- |
| Task 22.3: CLAUDE.md 项目指南更新 | 验收演示交付 | 进行中 | 更新 Node 工具链、Redis、AI 基准协作指南 | 文档一致 |

## 记录规则

- 每个有效任务开始时，把状态改为 `进行中`，并记录实际分支和 worktree。
- 每个有效任务提交后，填写实现 commit。
- Claude Code 审查完成后，填写审查文件路径和 Blocker/Major 处理结果。
- 审查处理记录提交后，必须推送任务分支到 GitHub 留痕。
- 合回 `main` 后，把合并状态改为 `已合并`，并推送 `main` 到 GitHub。
- Task 6/7 只作为废弃历史记录保留，不再创建分支或 worktree。
- 推送、合并、提交等影响远端或历史的操作需要明确授权后再执行。
