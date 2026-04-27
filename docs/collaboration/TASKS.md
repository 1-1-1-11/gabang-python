# gobang-python 协作任务台账

## 初步验收状态

- 2026-04-26 完成 MVP 初步验收审查。
- 验证命令：`py -m pytest backend\tests -q`。
- 最近结果：`59 passed in 2.08s`。
- 结论：当前后端 API、棋盘规则、AI MVP、内存会话、静态前端骨架和自动化测试可作为初步验收基线。
- 后续优先级：先做文档与项目状态收敛，再做前端验收增强、AI 能力基准化、运行时与部署准备。

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

## 已废弃任务

| 任务 | 分支 | Worktree | 状态 | 实现 Commit | 审查文件 | 合并状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Task 6: 前端状态字段统一 | - | - | 已废弃：依赖原始 React/JS 源码，违反 Python-only 远程边界 | - | - | 不适用 |
| Task 7: 前端接入 Python API | - | - | 已废弃：依赖原始 React/JS 源码，违反 Python-only 远程边界 | - | - | 不适用 |

## 下一阶段计划

| 任务 | 阶段 | 状态 | 目标 | 验收重点 |
| --- | --- | --- | --- | --- |
| Task 14.1: 校准 README 当前状态 | 文档与项目状态收敛 | 已完成，待提交 | README 准确反映当前 MVP、限制、结构和验收步骤 | 文档复现、全量 pytest |
| Task 14.2: 整理协作任务台账 | 文档与项目状态收敛 | 已完成，待提交 | 清晰区分已完成、已废弃和后续待执行任务 | 台账状态一致、全量 pytest |
| Task 14.3: 纳入根级 CLAUDE.md | 文档与项目状态收敛 | 已完成，待提交 | 保留未来 Claude Code 实例项目指南 | 与 README/TASKS 不冲突 |
| Task 15.1: 前端基础状态与错误验收 | 前端验收增强 | 已完成，待提交 | 补强请求失败、非 JSON、busy 和按钮状态验收 | 自动测试、浏览器实测 |
| Task 15.2: 前端可配置开局 UI | 前端验收增强 | 已完成，待提交 | 支持棋盘大小、搜索深度、AI 先手设置 | 自动测试、浏览器实测 |
| Task 15.3: 浏览器主路径验收步骤 | 前端验收增强 | 已完成，待提交 | 记录 start/move/undo/end 手动验收流程 | 文档复现、浏览器实测 |
| Task 16.1: AI 固定棋局搜索基准 | AI 能力基准化 | 已完成，待提交 | 增加必胜、防守、开放四、冲四、双三等测试 | AI 测试、全量 pytest |
| Task 16.2: 搜索状态不污染测试 | AI 能力基准化 | 已完成，待提交 | 验证搜索前后 history/hash/棋盘矩阵/current_player 不变 | AI 测试、全量 pytest |
| Task 16.3: 明确 enable_vct 语义 | AI 能力基准化 | 已完成，待提交 | 移除未生效的误导参数，保留 VCT/VCF 独立入口 | AI 测试、全量 pytest |
| Task 17.1: 运行时配置文档化 | 运行时与部署准备 | 已完成，待提交 | 文档化 CORS、内存会话、开发/生产边界 | 文档复现、自动测试 |
| Task 17.2: 对局生命周期硬化测试 | 运行时与部署准备 | 已完成，待提交 | 覆盖重复操作、未知 session、非法请求状态保持 | 自动测试 |
| Task 17.3: 最小部署验收清单 | 运行时与部署准备 | 已完成，待提交 | 形成启动、访问、CORS、测试检查清单 | 文档复现 |
| Task 18.1: Playwright 主路径 E2E | 浏览器验收自动化 | 已完成，待提交 | 引入 Node Playwright 骨架并覆盖 start/move/undo/end 主路径 | E2E、全量 pytest |
| Task 18.2: E2E 错误路径与控件状态 | 浏览器验收自动化 | 已完成，待提交 | 覆盖请求失败、非 JSON、busy、防重复操作 | E2E、全量 pytest |
| Task 19.1: AI 搜索全局指标 | AI 性能基准化 | 已完成，待提交 | 暴露搜索调用、剪枝、深度等全局指标 | AI 测试、全量 pytest |
| Task 19.2: AI 宽松性能阈值 | AI 性能基准化 | 已完成，待提交 | 为小棋局浅深度添加宽松耗时与指标阈值 | AI 基准、全量 pytest |
| Task 19.3: AI 基准文档化 | AI 性能基准化 | 已完成，待提交 | 说明阈值用途和非 SLA 边界 | 文档复现、全量 pytest |
| Task 20.1: 会话后端配置化 | Redis 会话准备 | 已完成，待提交 | 增加 memory/redis 配置入口并保留 memory 默认 | 自动测试 |
| Task 20.2: 基础 Redis SessionStore | Redis 会话准备 | 已完成，待提交 | 实现可选 Redis 会话读写与序列化 | 自动测试、可选 Redis 验收 |
| Task 20.3: Redis 生命周期与文档 | Redis 会话准备 | 已完成，待提交 | 验证 Redis 后端基础生命周期并补充部署说明 | 自动测试、文档复现 |
| Task 21.1: 前端落子可读性 | 前端体验增强 | 待执行 | 最近一步高亮、1-based 落子记录、空格 hover | E2E、浏览器实测 |
| Task 21.2: AI 信息展示 | 前端体验增强 | 待执行 | 展示 score、best_path、current_depth | E2E、浏览器实测 |
| Task 21.3: 配置体验 | 前端体验增强 | 待执行 | 优化 size/depth/API 地址配置与提示 | E2E、浏览器实测 |
| Task 22.1: README 最终收敛 | 验收演示交付 | 待执行 | README 反映 E2E、AI 基准、Redis 可选能力 | 文档复现 |
| Task 22.2: TASKS 台账校准 | 验收演示交付 | 待执行 | 对齐 Task 18-22 状态、提交、审查与验收结果 | 台账一致 |
| Task 22.3: CLAUDE.md 项目指南更新 | 验收演示交付 | 待执行 | 更新 Node 工具链、Redis、AI 基准协作指南 | 文档一致 |

## 记录规则

- 每个有效任务开始时，把状态改为 `进行中`，并记录实际分支和 worktree。
- 每个有效任务提交后，填写实现 commit。
- Claude Code 审查完成后，填写审查文件路径和 Blocker/Major 处理结果。
- 审查处理记录提交后，必须推送任务分支到 GitHub 留痕。
- 合回 `main` 后，把合并状态改为 `已合并`，并推送 `main` 到 GitHub。
- Task 6/7 只作为废弃历史记录保留，不再创建分支或 worktree。
- 推送、合并、提交等影响远端或历史的操作需要明确授权后再执行。
