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

新阶段详细计划见：`docs/collaboration/任务计划.md`。

| 任务 | 阶段 | 状态 | 目标 | 验收重点 |
| --- | --- | --- | --- | --- |
| Task 23.A: 协作机制与任务计划落地 | 产品化升级 | 已完成 | 创建可执行任务计划，固化 subagent 审查、commit/push 和留痕规则 | `docs/collaboration/reviews/23A-collaboration-plan.md`：PASS；实现 commit `5e45d44`；已推送 main |
| Task 23.B: AI 优化基线与第一轮算法优化 | 产品化升级 | 已完成（B-10 已审查 PASS；下一步 C-02） | 建立 AI benchmark 和战术测试，再实施低风险算法优化 | B-01 已扩展开局、中盘、立即胜、必须防、简单连续威胁 benchmark；`python -m pytest backend\tests\test_ai_benchmark.py -q`：5 passed；`python -m pytest backend\tests\test_ai_search.py -q`：16 passed；审查文件 `docs/collaboration/reviews/B-01-ai-benchmark-baseline.md`：PASS；实现 commit `7c3f045`；备注 commit `1997ea9`；push 状态：已推送 main；B-02 已补充水平、垂直、反斜线立即胜固定坐标测试；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`：19 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`：5 passed；审查文件 `docs/collaboration/reviews/B-02-immediate-win-tests.md`：PASS；实现 commit `4034db7`；备注 commit `79647ec`；push 状态：已推送 main；B-03 已补充水平、垂直、反斜线必须防守固定坐标测试；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`：22 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`：5 passed；审查文件 `docs/collaboration/reviews/B-03-must-block-tests.md`：PASS；实现 commit `398d855`；备注 commit `5a252c2`；push 状态：已推送 main；B-04 已补充 `minmax`、`vct`、`vcf` 连续威胁路径测试；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`：25 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`：5 passed；审查文件 `docs/collaboration/reviews/B-04-continuous-threat-tests.md`：PASS；实现 commit `f939166`；备注 commit `6bb8aba`；push 状态：已推送 main；B-05 已实现局部终局判断与 undo winner 恢复；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_board.py -q`：24 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`：25 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`：5 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：104 passed；审查文件 `docs/collaboration/reviews/B-05-local-winner-check.md`：PASS；实现 commit `0b58ba3`；备注 commit `19684cd`；push 状态：已推送 main；B-06 已实现候选点局部化，空盘回中心，内部扫描池小于全盘空点；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`：26 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`：5 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：105 passed；中盘 benchmark 耗时约 0.30s，低于 B-06 前约 0.42s；审查文件 `docs/collaboration/reviews/B-06-local-candidate-points.md`：PASS；实现 commit `749f97c`；备注 commit `1037d51`；push 状态：已推送 main；裸 `python` 当前命中 WindowsApps stub，详见 `.learnings/ERRORS.md` |
| Task 23.C: Vue3 + Vite 前端架构初始化 | 产品化升级 | 进行中（C-06 已审查 PASS；下一步 C-09） | 引入 Vue3 + Vite，建立现代前端工程结构 | C-02：`npm run build` 通过；`npm run test:e2e` 5 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests -q` 108 passed；C-03：API client 已抽出，Vite/E2E/文档端口统一到 `5173`，`npm run build` 通过，Playwright `5 passed`，pytest `108 passed`；C-04：游戏状态已抽到 composable，Playwright `5 passed`，pytest `108 passed`；C-06：启动契约测试已固化，Playwright `5 passed`，pytest `109 passed` |
| Task 23.D: 精美 UI 与交互体验 | 产品化升级 | 待开始 | 组件化棋盘、控制区、状态区、落子记录和 AI 信息展示 | 浏览器验收和 Playwright 主路径通过 |
| Task 23.E: 复盘、质量收敛与留痕 | 产品化升级 | 待开始 | 汇总测试、审查、commit、push 和下一阶段路线 | 台账可追溯，无未处理 Blocker/Major |

> 最新状态（2026-04-28）：Task 23.C 已推进到 C-06 审查 PASS；下一步为 C-09 搜索指标响应字段。上表 Task 23.B 历史验收单元格保留 B-01 到 B-06 的详细追溯，后续新增子任务记录在下方独立留痕区，避免继续拉长表格。

### Task 23.B 子任务留痕

- B-07：走法排序增强
  - 状态：已完成。
  - 实现范围：`backend/app/evaluation.py` 新增走法排序权重与排序 helper，在候选截断前按己方立即胜、对方必须防、强威胁等价值排序；`backend/tests/test_ai_search.py` 增加己方立即胜优先于防守阻断、早剪枝收益测试。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`、`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`。
  - 测试结果：`28 passed`、`5 passed`、`107 passed`。
  - 指标对比：B-07 专用局面中，模拟旧 row-major 顺序为 `nodes=6`、`candidate_moves=7`、`max_depth=2`、`leaf_nodes=4`、选点 `[6, 3]`；新排序为 `nodes=2`、`candidate_moves=4`、`max_depth=1`、`leaf_nodes=1`、选点 `[6, 3]`；`prunes` 均为 `1`。
  - subagent 审查文件：`docs/collaboration/reviews/B-07-move-ordering.md`：PASS。
  - Blocker/Major 处理：无 Blocker/Major；Minor 为早剪枝测试断言偏实现细节，作为本轮性能护栏保留。
  - 实现 commit：`66498ed`。
  - push 状态：随本轮备注提交推送 main。
  - 遗留风险：B-08 仍需汇总至少 3 个固定局面的累计指标对比。
  - 下一步：B-08 AI 优化复盘记录。
- B-08：AI 优化复盘记录
  - 状态：已完成。
  - 实现范围：`docs/collaboration/任务计划.md` 新增 B-08 复盘章节，对比 B-04 后基线 commit `6bb8aba` 与当前 commit `abdbc82` 的 6 个固定局面指标。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`、`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`。
  - 测试结果：`28 passed`、`5 passed`、`107 passed`。
  - subagent 审查：最终 staged diff 审查 PASS；实现 commit `2d1c122`；push 状态：已推送 main。
- B-09：搜索缓存语义评估
  - 状态：已完成。
  - 实现范围：`backend/app/minmax.py` 新增 `CacheEntry` / `CacheBound`，缓存写入区分 `exact`、`lower`、`upper`；`_cached_result()` 只在当前窗口允许时复用 bound；`backend/tests/test_ai_search.py` 增加 bound 写入和读取规则测试。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q`、`.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`。
  - 测试结果：`29 passed`、`5 passed`、`108 passed`。
  - subagent 审查文件：`docs/collaboration/reviews/B-09-cache-bound-semantics.md`：PASS。
  - Blocker/Major 处理：首轮审查指出 fail-low 不能写成 `exact`；已通过 `_cache_bound(value, alpha_start, beta)` 修复，并补充测试。
  - 实现 commit：`338f928`。
  - push 状态：已推送 main。
  - 遗留风险：新增测试直接覆盖 helper 语义，尚未构造真实搜索中的旧窗口/新窗口集成场景；后续 cache entry 结构再变时补。
  - 下一步：B-10 节点/时间预算预研。
- B-10：节点/时间预算预研
  - 状态：已完成。
  - 实现范围：`docs/collaboration/任务计划.md` 新增 B-10 预研章节，明确预算参数暂不进入阶段 B，并给出后续“搜索指标响应字段”和“节点预算优先于时间预算”的最小任务拆分。
  - 验证方式：文档任务；核对 `backend/app/schemas.py`、`backend/app/game.py`、`backend/app/minmax.py`、`backend/tests/test_api_contract.py`、`backend/tests/test_game_api.py`、README。
  - subagent 审查文件：`docs/collaboration/reviews/B-10-budget-presearch.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`31a4a9f`。
  - push 状态：已推送 main。
  - 遗留风险：D-08 搜索信息展示前，需要先做 C-09 后端搜索指标响应字段，否则前端只能展示 `score`、`best_path`、`current_depth`。
  - 下一步：C-02 Vue3 + Vite 前端架构初始化。

### Task 23.C 子任务留痕

- C-02：初始化 Vue3 + Vite 工程
  - 状态：已完成。
  - 实现范围：新增 `vite.config.js`，将 `frontend/` 迁移为 Vite root；新增 `frontend/src/App.vue`、`frontend/src/main.js`、`frontend/src/styles.css`；更新 `package.json`、`package-lock.json`、`playwright.config.js`、README、CLAUDE 和前端骨架测试；同步 `start.bat` 使用 Vite dev server。
  - 测试命令：`npm run build`、`npm run test:e2e`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`。
  - 测试结果：Vite build 通过；Playwright `5 passed`；pytest `108 passed`。
  - subagent 审查文件：`docs/collaboration/reviews/C-02-vue-vite-initialization.md`：PASS。
  - Blocker/Major 处理：首轮审查指出缺少 review 留痕与 Node 版本契约；已补齐后通过复审。
  - 实现 commit：`16ca6f7`。
  - push 状态：已推送 main。
  - 遗留风险：C-04 仍需拆出游戏状态模块；当前为架构初始化，未做 D 阶段完整视觉重做。
  - 下一步：C-03 建立 API 客户端模块。
- C-03：建立 API 客户端模块
  - 状态：已完成。
  - 实现范围：新增 `frontend/src/api/client.js`，封装 API base 规范化、JSON 请求、`health`、`startGame`、`playMove`、`undoMove`、`endGame`；`frontend/src/App.vue` 改为通过 `createGameApi()` 调用 API；`backend/tests/test_frontend_skeleton.py` 改为验证 API client 模块边界，并锁定 Vite/Playwright 端口契约；同步 `vite.config.js`、`playwright.config.js`、README、CLAUDE 和 `start.bat` 使用 `5173`。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`、`npm run build`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`、`npm run test:e2e`。
  - 测试结果：`10 passed`；Vite build 通过；pytest `108 passed`；Playwright `5 passed`。
  - subagent 审查文件：`docs/collaboration/reviews/C-03-api-client-module.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`b6c2f4c`。
  - push 状态：随本轮记录提交推送 main。
  - 遗留风险：C-04 仍需拆出游戏状态管理；当前任务只建立 API 客户端边界。
  - 下一步：C-04 建立游戏状态管理。
- C-04：建立游戏状态管理
  - 状态：已完成。
  - 实现范围：新增 `frontend/src/composables/useGameState.js`，集中管理 session、board、history、winner、busy/status、settings、AI 搜索信息以及 start/move/undo/end 流程；`frontend/src/App.vue` 改为消费 composable 并保留模板与展示辅助函数；`backend/tests/test_frontend_skeleton.py` 改为验证状态管理模块边界。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`、`npm run build`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`、`npm run test:e2e`。
  - 测试结果：`10 passed`；Vite build 通过；pytest `108 passed`；Playwright `5 passed`。
  - subagent 审查文件：`docs/collaboration/reviews/C-04-game-state-management.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`d4c97d5`。
  - push 状态：随本轮记录提交推送 main。
  - 遗留风险：C-06 仍需核对 E2E 启动方式是否已经完全落地；D 阶段视觉组件化尚未开始。
  - 下一步：C-06 更新 E2E 启动方式核对。
- C-06：更新 E2E 启动方式核对
  - 状态：已完成。
  - 实现范围：`backend/tests/test_frontend_skeleton.py` 新增前端运行入口契约测试，锁定 `vite.config.js`、`playwright.config.js`、README、CLAUDE 和 `start.bat` 均使用 `http://127.0.0.1:5173`，并防止 tracked runtime docs/config 回退到旧 `4173`。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`、`npm run build`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`、`npm run test:e2e`。
  - 测试结果：`11 passed`；Vite build 通过；pytest `109 passed`；Playwright `5 passed`。
  - subagent 审查文件：`docs/collaboration/reviews/C-06-e2e-startup-alignment.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`91baa21`。
  - push 状态：随本轮记录提交推送 main。
  - 遗留风险：C-09 后端搜索指标字段尚未实现；D 阶段视觉组件化尚未开始。
  - 下一步：C-09 搜索指标响应字段。

## 记录规则

- 每个有效任务开始时，把状态改为 `进行中`，并记录实际分支和 worktree。
- 每个有效任务在获得用户授权后提交并填写实现 commit；Task 23 产品化升级阶段已获得用户授权：每个最小任务在测试、验收和 subagent 审查通过后，自动 commit 并 push 到远程 GitHub 留痕。
- Claude Code 审查完成后，填写审查文件路径和 Blocker/Major 处理结果。
- 审查处理记录提交后，在授权范围内推送任务分支到 GitHub 留痕。
- 合回 `main` 后，在授权范围内把合并状态改为 `已合并`，并推送 `main` 到 GitHub。
- Task 6/7 只作为废弃历史记录保留，不再创建分支或 worktree。
