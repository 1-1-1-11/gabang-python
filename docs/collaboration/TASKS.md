# gobang-python 协作任务台账

| 任务 | 分支 | Worktree | 状态 | 实现 Commit | 审查文件 | 合并状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Task 1: Git 基线与协作骨架 | `main` | 当前仓库 | 已完成 | `1a42bde` / 本提交 | 不适用 | 不适用 |
| Task 2: Python 后端骨架 | `task/02-python-backend-skeleton` | `.worktrees/02-python-backend-skeleton` | 已完成 | `5e7a596` | `docs/collaboration/reviews/02-python-backend-skeleton.md` | 已合并 |
| Task 3: 棋盘规则迁移 | `task/03-board-rules` | `.worktrees/03-board-rules` | 已完成 | `8fc9fe3` / `bc1f80a` | `docs/collaboration/reviews/03-board-rules.md` | 已合并 |
| Task 4: 评分与搜索迁移 | `task/04-ai-search` | `.worktrees/04-ai-search` | 已完成 | `81e5a5b` / `4a2eff6` | `docs/collaboration/reviews/04-ai-search.md` | 已合并 |
| Task 5: FastAPI 游戏接口 | `task/05-game-api` | `.worktrees/05-game-api` | 已完成 | `b617be4` / `53f49f8` | `docs/collaboration/reviews/05-game-api.md` | 未合并 |
| Task 6: 前端状态字段统一 | - | - | 已废弃：原始 JS 不入远程 | - | - | 不适用 |
| Task 7: 前端接入 Python API | - | - | 已废弃：原始 JS 不入远程 | - | - | 不适用 |
| Task 8: 一键启动与文档 | `task/08-dev-scripts-docs` | `.worktrees/08-dev-scripts-docs` | 未开始 | - | `docs/collaboration/reviews/08-dev-scripts-docs.md` | 未合并 |

## 记录规则

- 每个任务开始时，把状态改为 `进行中`，并记录实际分支和 worktree。
- 每个任务提交后，填写实现 commit。
- 审查完成后，填写审查文件路径和 Blocker/Major 处理结果。
- 合回 `main` 后，把合并状态改为 `已合并`。
