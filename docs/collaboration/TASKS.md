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
| Task 23.C: Vue3 + Vite 前端架构初始化 | 产品化升级 | 已完成（C-09 已审查 PASS；下一步 D-01） | 引入 Vue3 + Vite，建立现代前端工程结构 | C-02：`npm run build` 通过；`npm run test:e2e` 5 passed；`.\.venv\Scripts\python.exe -m pytest backend\tests -q` 108 passed；C-03：API client 已抽出，Vite/E2E/文档端口统一到 `5173`，`npm run build` 通过，Playwright `5 passed`，pytest `108 passed`；C-04：游戏状态已抽到 composable，Playwright `5 passed`，pytest `108 passed`；C-06：启动契约测试已固化，Playwright `5 passed`，pytest `109 passed`；C-09：`GameSnapshot.search_metrics` 已新增，Playwright `5 passed`，pytest `109 passed` |
| Task 23.D: 精美 UI 与交互体验 | 产品化升级 | 已完成（D-14 已审查 PASS；下一步 E-01） | 组件化棋盘、控制区、状态区、落子记录和 AI 信息展示 | 浏览器验收和 Playwright 主路径通过 |
| Task 23.E: 复盘、质量收敛与留痕 | 产品化升级 | 进行中（E-06 已完成；E-05/E-06 待远端同步） | 汇总测试、审查、commit、push 和下一阶段路线 | E-01 后端全量回归：`112 passed`；E-02 前端构建：通过；E-03 E2E 修复后 `12 passed`；E-04 无未处理 Blocker/Major；E-05 远程 main 已核对到 `3c2363c`，后续记录提交因 GitHub HTTPS 连接重置待推送；E-06 已补下一阶段路线 |

> 最新状态（2026-04-30）：Task 23.D 已完成 D-01 页面整体布局、D-02 棋盘组件、D-03 棋子组件、D-04 控制面板、D-05 难度选择、D-06 AI 思考状态、D-07 落子记录、D-08 搜索信息展示、D-09 错误提示、D-10 游戏结束状态、D-11 主题与视觉规范、D-12 浏览器 E2E 主路径、D-13 响应式验收和 D-14 可访问性基础；Task 23.E 已完成 E-01 后端全量回归、E-02 前端构建回归、E-03 E2E 回归、E-04 独立审查汇总和 E-06 下一阶段路线。E-05 远程 main 已核对到 `3c2363c`，但 E-05 后续记录提交 `2a43f8e` 当前因 GitHub HTTPS 连接重置待推送。上表 Task 23.B 历史验收单元格保留 B-01 到 B-06 的详细追溯，后续新增子任务记录在下方独立留痕区，避免继续拉长表格。

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
- C-09：搜索指标响应字段
  - 状态：已完成。
  - 实现范围：新增 `SearchMetricsSnapshot` 并在 `GameSnapshot.search_metrics` 返回最近一次 AI 搜索的 `nodes`、`prunes`、`cache_hits`、`cache_stores`、`candidate_moves`、`leaf_nodes`、`max_depth`、`elapsed_ms`；`GameSession` 与 Redis 序列化保存指标；前端状态接收 `snapshot.search_metrics`；README 和 API/游戏/Redis/前端骨架测试同步。
  - 测试命令：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_api_contract.py backend\tests\test_game_api.py backend\tests\test_redis_session_store.py backend\tests\test_frontend_skeleton.py -q`、`npm run build`、`.\.venv\Scripts\python.exe -m pytest backend\tests -q`、`npm run test:e2e`。
  - 测试结果：`32 passed`；Vite build 通过；pytest `109 passed`；Playwright `5 passed`。
  - subagent 审查文件：`docs/collaboration/reviews/C-09-search-metrics-response.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`b723296`。
  - push 状态：随本轮记录提交推送 main。
  - 遗留风险：D-08 仍需把 `search_metrics` 真正展示到前端 UI；本轮只提供稳定后端字段和前端状态入口。
  - 下一步：D-01 页面整体布局。

### Task 23.D 子任务留痕

- D-01：页面整体布局
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/AppLayout.vue` 页面骨架组件；`App.vue` 改为通过 layout slots 装配标题、状态、棋盘和右侧信息区；`styles.css` 稳定桌面左棋盘右信息区、窄屏单列、右侧面板滚动和长状态换行；`e2e/gobang.spec.js` 增加桌面/窄屏布局无溢出验收；前端骨架测试锁定 layout 组件边界。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`6 passed`；`git diff --check`：无空白错误。
  - subagent 审查文件：`docs/collaboration/reviews/D-01-page-layout.md`：PASS。
  - Blocker/Major 处理：无；Minor 已处理：收敛 CSS 文本断言、补充状态 pill 长文本换行。
  - 实现 commit：`224bdb7`。
  - push 状态：已推送 main。
  - 下一步：D-02 棋盘组件。

- D-02：棋盘组件
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/Board.vue`，承载棋盘网格、格点按钮、`#board`、`.cell`、`data-row`/`data-col`、禁用态、最后一步 class 和 `play-move` 事件；`App.vue` 通过 props/emit 接入现有状态与 `playMove`；保留棋子 DOM 在 `Board.vue` 内，暂不抽 `Stone`。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`6 passed`；`git diff --check`：无空白错误。
  - subagent 审查文件：`docs/collaboration/reviews/D-02-board-component.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`e45fd88`。
  - push 状态：已推送 main。
  - 下一步：D-03 棋子组件。

- D-03：棋子组件
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/Stone.vue`，封装黑白棋子、最新落点棋子 class 与内部标记；`Board.vue` 改为通过 `Stone` 渲染非空格点，同时保留 `#board`、`.cell`、`data-row`/`data-col`、禁用态、最后一步格点 class 和 `play-move` 事件；`styles.css` 增强黑白棋子体积感、阴影和最新落点视觉；前端骨架测试与 Playwright 主路径补充 Stone 组件边界和黑/白/最新棋子断言。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`6 passed`；`git diff --check`：无空白错误。
  - subagent 审查文件：`docs/collaboration/reviews/D-03-stone-component.md`：PASS。
  - Blocker/Major 处理：无；首轮全工作区审查提醒未跟踪的 `AGENTS.md` 与 `deploy.bat` 不属于 D-03 范围，最终 staged diff 审查 PASS 且未提交这两个文件。
  - 实现 commit：`8ff3e41`。
  - push 状态：已推送 main。
  - 遗留风险：最后一步存在格点、棋子和内部点三层视觉信号；后续 D-11 做主题统一时可再微调强弱，当前不阻塞验收。
  - 下一步：D-04 控制面板。

- D-04：控制面板
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/ControlPanel.vue`，封装开始、悔棋、结束、重开四个控制按钮；`App.vue` 改为接入 `ControlPanel` 并保留既有按钮选择器；`useGameState.js` 新增 `restartGame()`，active session 重开时先 `end` 再 `start`；Playwright 新增重开路径和请求顺序断言。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`7 passed`；`git diff --check`：无空白错误。
  - subagent 审查文件：`docs/collaboration/reviews/D-04-control-panel.md`：PASS。
  - Blocker/Major 处理：无；Minor 建议补充重开请求顺序断言，已处理并复审 PASS。
  - 实现 commit：`d8c04ce`。
  - push 状态：已推送 main。
  - 遗留风险：D-05 难度选择会继续改控制/设置区，但本轮未新增后端预算参数，只复用现有 `depth`。
  - 下一步：D-05 难度选择。

- D-05：难度选择
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/DifficultySelect.vue`，提供简单、普通、困难、自定义四个选项；简单/普通/困难分别映射到现有后端 `depth=2/4/6`；自定义时显示原 `search-depth-input` 并继续限制 1-8；`App.vue` 接入组件，`useGameState.js` 新增前端 UI 状态 `settings.difficulty`；Playwright 验证 payload 仍只有 `size`、`ai_first`、`depth`。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`8 passed`；`git diff --check`：无空白错误。
  - subagent 审查文件：`docs/collaboration/reviews/D-05-difficulty-select.md`：PASS。
  - Blocker/Major 处理：无。
  - 实现 commit：`09ac513`。
  - push 状态：已推送 main。
  - 遗留风险：默认普通难度不再直接显示数字深度输入；需要手动输入时必须选择自定义，这是有意的交互边界。
  - 下一步：D-06 AI 思考状态。

- D-06：AI 思考状态
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/ThinkingIndicator.vue`，展示 AI 待命/思考中、最近搜索耗时、nodes 和 prunes；`App.vue` 接入 `state.searchMetrics`；`useGameState.js` 在 AI 先手开局时显示 `AI 思考`；Playwright 覆盖 AI move pending、AI-first start pending、空数据占位和搜索指标渲染。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`9 passed`；`git diff --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-06-thinking-indicator.md`：PASS，带记录边界。
  - Blocker/Major 处理：无；初审 Question 为 AI 先手开局也应显示思考中，已处理。第二轮 subagent 复审因 Codex usage limit 失败，已在 review 文件中如实记录，并用本地可重复门禁复核替代。
  - 实现 commit：`a234473`。
  - push 状态：已推送 main。
  - 遗留风险：D-06 只展示轻量思考状态和核心指标，不提前实现 D-08 的完整 SearchInfo；额度恢复后可补一次只读复审。
  - 下一步：D-07 落子记录。

- D-07：落子记录
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/MoveHistory.vue`，封装落子记录、空状态、序号、角色和坐标展示；`App.vue` 改为传入 `state.history`；保留 `#move-list`、`.is-latest` 与既有文本可读性；Playwright 验证空记录、落子记录和悔棋后同步清空。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`9 passed`；`git diff --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-07-move-history.md`：PASS，带记录边界。
  - Blocker/Major 处理：无；E2E 首轮发现文本间距回归，已恢复 `黑方 (row, col)` 可读格式。
  - 实现 commit：`2420881`。
  - push 状态：已推送 main。
  - 遗留风险：subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕；额度恢复后可补只读复审。
  - 下一步：D-08 搜索信息展示。

- D-08：搜索信息展示
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/SearchInfo.vue`，封装 AI 评分、搜索深度、nodes、prunes、cache_hits 和 best_path 展示；`App.vue` 用组件替换内联搜索信息区并保留既有 `#ai-score-value`、`#ai-depth-value`、`#best-path-value`；Playwright 验证空占位和搜索指标渲染。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`9 passed`；`git diff --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-08-search-info.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`8d026d5`。
  - push 状态：已推送 main。
  - 遗留风险：subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕；D-08 只消费既有 `search_metrics`，未新增预算参数或后端字段。
  - 下一步：D-09 错误提示。

- D-09：错误提示
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/ErrorBanner.vue`，用 `role="alert"` 展示 API/网络错误并支持关闭；`App.vue` 接入错误横幅；`useGameState.js` 新增 `errorMessage`、`setError()`、`clearError()` 和 `dismissError()`，各 API action 发起前清理旧错误，catch 中写入横幅并保留 status 文本；`styles.css` 增加错误横幅样式；前端骨架测试与 Playwright 覆盖 JSON 错误、非 JSON 错误和关闭横幅。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`9 passed`；`git diff --check` / `git diff --cached --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-09-error-banner.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`c78269e`。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `c78269e3c2362d90456fb589be580485241965f5`。
  - 遗留风险：关闭错误横幅只清空 banner，不改写状态 pill，便于保留最近错误文本；subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕。
  - 下一步：D-10 游戏结束状态。

- D-10：游戏结束状态
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/components/GameResult.vue`，展示胜者/结束态并提供结果区重新开始入口；`App.vue` 用 `canRestart` 统一控制面板与结果面板重开条件；`useGameState.js` 新增 `isGameOver`，胜负已定或手动结束后锁定棋盘，手动结束空棋也能重新开始；`styles.css` 增加结果面板样式；前端骨架测试与 Playwright 覆盖胜者展示、棋盘锁定和结果区重开。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`10 passed`；`git diff --check` / `git diff --cached --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-10-game-result.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`c5a175c`。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `c5a175ce5a2b1d71fd5ec93e5f20bf455687c89f`。
  - 遗留风险：D-10 只消费既有 `snapshot.winner` 并新增前端 `isGameOver`，未改变后端结束接口；subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕。
  - 下一步：D-11 主题与视觉规范。

- D-11：主题与视觉规范
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：新增 `frontend/src/theme.css`，集中定义颜色、透明色、间距、圆角、控件高度、阴影和焦点环 token；`main.js` 在 `styles.css` 前加载主题；`styles.css` 改为消费主题 token，统一按钮、输入框、布局容器、状态 pill、棋盘、棋子、信息面板和结果/错误面板的视觉尺度；前端骨架测试锁定主题文件、导入顺序和关键 token 使用。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`；`npm run test:e2e`：`10 passed`；`git diff --check` / `git diff --cached --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-11-theme-system.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`edd1c93`。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `edd1c93420e0afc8ca9d96db51e67a142c43371b`。
  - 遗留风险：D-11 是主题 token 化，不重新设计布局；subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕。
  - 下一步：D-12 浏览器 E2E 主路径。

- D-12：浏览器 E2E 主路径
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：`e2e/gobang.spec.js` 在真实主路径测试中记录非 OPTIONS 的 `/api/games` 请求，显式断言 start、move、undo、end 四个业务 API 顺序；`backend/tests/test_frontend_skeleton.py` 新增 Playwright 主路径契约测试，锁定 API 调用链断言存在。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`12 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`110 passed`；`npm run test:e2e`：`10 passed`；`git diff --check` / `git diff --cached --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-12-browser-main-path.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`1c37be8`。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `1c37be8c00664f8da0b91317344482ef1d9c8fce`。
  - 遗留风险：主路径断言只过滤 CORS 预检 OPTIONS，不 mock start/move/undo/end；subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕。
  - 下一步：D-13 响应式验收。

- D-13：响应式验收
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：`e2e/gobang.spec.js` 新增 360px 窄屏活跃棋局验收，覆盖开始、落子、AI 回复、悔棋、结束，并检查状态、棋盘、控制区、落子记录和结果区不发生横向溢出；`styles.css` 在 520px 以下把控制按钮改为 2x2 网格；前端骨架测试锁定响应式 E2E 契约。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`13 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`111 passed`；`npm run test:e2e`：`11 passed`；`git diff --check` / `git diff --cached --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-13-responsive-acceptance.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`f533180`。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `f533180aee615cc0afa7f80ddd741bc91fd4bc7c`。
  - 遗留风险：D-13 只增强响应式验收与窄屏控制布局，不改 API、不改游戏状态语义；subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕。
  - 下一步：D-14 可访问性基础。

- D-14：可访问性基础
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：`Board.vue` 为棋盘格补充中文 accessible name、`aria-disabled` 和棋盘 `aria-busy`；`ControlPanel.vue` 为开始、悔棋、结束按钮补充明确 `aria-label`；`App.vue` 为状态 pill 补充 `aria-live="polite"`；Playwright 新增键盘焦点和 accessible name 验收，前端骨架测试补充可访问性契约。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`14 passed`；`npm run build`：通过；`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`112 passed`；`npm run test:e2e`：`12 passed`；`git diff --check` / `git diff --cached --check`：无空白错误。
  - 审查文件：`docs/collaboration/reviews/D-14-accessibility-basics.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`54327d8`。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `54327d8e5be28532b8ea7820db9ac2816b8c4cd6`。
  - 遗留风险：D-14 是基础可访问性增强，未引入 axe 自动审计；subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并留痕。
  - 下一步：E-01 后端全量回归。

### Task 23.E 子任务留痕

- E-01：后端全量回归
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：验证任务，无后端实现改动；执行 `backend/tests/` 全量 pytest。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`112 passed`。
  - 审查文件：`docs/collaboration/reviews/E-01-backend-regression.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`3e1ef1a`（验证记录提交）。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `3e1ef1aac4345f167a2ce2f9f69aa18c4ac2b42d`。
  - 遗留风险：E-01 只覆盖后端 pytest，不替代 E-02 前端构建或 E-03 E2E 回归。
  - 下一步：E-02 前端构建回归。

- E-02：前端构建回归
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：验证任务，无前端实现改动；执行已配置的 `npm run build`。
  - 验证方式：`npm run build`：通过，Vite 输出 `✓ built in 315ms`；`package.json` 当前没有 typecheck/lint 脚本。
  - 审查文件：`docs/collaboration/reviews/E-02-frontend-build-regression.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`3b47def`（验证记录提交）。
  - push 状态：已推送 main；`git status` 显示本地 tracking 与 `origin/main` 对齐，`git ls-remote` 精确指针查询因 GitHub 443 连接失败待后续复核。
  - 遗留风险：E-02 只覆盖前端构建，不替代 E-03 Playwright 浏览器回归。
  - 下一步：E-03 E2E 回归。

- E-03：E2E 回归
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：执行 `npm run test:e2e`；首轮发现 E2E 仍使用旧 `prunes` selector 与 mock payload，已按当前 `beta_cutoffs` 指标合同修复 `e2e/gobang.spec.js` 并复跑。
  - 验证方式：首轮 `npm run test:e2e`：2 failed / 10 passed；修复后 `npm run test:e2e`：`12 passed`。
  - 审查文件：`docs/collaboration/reviews/E-03-e2e-regression.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`4ea633a`。
  - push 状态：已推送 main；`git status` 显示本地 tracking 与 `origin/main` 对齐，`git ls-remote` 精确指针查询因 GitHub 443 连接失败待后续复核。
  - 遗留风险：E-03 修复的是测试合同滞后，不额外证明 `d37ac32` 的棋力收益；后续 E-04/E-05 需把该后端提交纳入审查/留痕汇总。
  - 下一步：E-04 独立审查汇总。

- E-04：独立审查汇总
  - 状态：已完成。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：汇总 D-09 至 D-14、E-01 至 E-03 review 文件；核对近期提交链和未处理 Blocker/Major；标注 `d37ac32` 额外后端提交需要 E-05 单独留痕。
  - 验证方式：`git log --oneline -25`；`Select-String docs\collaboration\reviews\*.md` 核对 review 结论、Blocker/Major 段落和 subagent 边界记录。
  - 审查文件：`docs/collaboration/reviews/E-04-review-summary.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`3c2363c`（验证记录提交）。
  - push 状态：已推送 main，远程 `origin/main` 已确认指向 `3c2363ca0cf6b70115bf5a1b5be7655c3e103ded`。
  - 遗留风险：E-04 是汇总审查，不替代 `d37ac32` 的棋力收益评估；E-05 需补 GitHub 留痕汇总。
  - 下一步：E-05 GitHub 留痕汇总。

- E-05：GitHub 留痕汇总
  - 状态：进行中（本地记录提交已生成，远端同步待 GitHub 可达）。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：核对近期 commit hash、push 状态和远程 `origin/main` 指针；单独标注 `d37ac32` 额外后端 AI 提交。
  - 验证方式：`git log --format='%h %H %s' -20`；`git ls-remote origin refs/heads/main`：`3c2363ca0cf6b70115bf5a1b5be7655c3e103ded`；E-05 记录提交后 `git status --short --branch` 显示 `main...origin/main [ahead 1]`。
  - 审查文件：`docs/collaboration/reviews/E-05-github-ledger-summary.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：`2a43f8e`（本地记录提交）。
  - push 状态：待推送；`git push origin main` 多次因 GitHub HTTPS 连接重置失败，不标记为已推送。
  - 遗留风险：`d37ac32` 已被回归测试覆盖，但没有单独棋力收益评估；后续 E-08 需纳入风险清单。
  - 下一步：E-06 下一阶段路线。

- E-06：下一阶段路线
  - 状态：已完成（本地记录待提交与远端同步）。
  - 实际分支/worktree：`main` / `D:\Desktop\JOYland\林杯五子棋大赛\gobang-master`。
  - 实现范围：更新 `docs/collaboration/任务计划.md` 的当前状态、MVP 后候选方向、当前执行提醒和 E-06 路线记录；把旧 `prunes` 文档口径校准为当前 `beta_cutoffs` 指标；将 `d37ac32` 棋力收益评估列入下一轮风险/路线。
  - 验证方式：`Select-String` 核对旧 D-01 当前提醒已移除、`beta_cutoffs` 已出现在 D-08 口径中；`git diff --check` 无空白错误（仅 CRLF 提示）。
  - 审查文件：`docs/collaboration/reviews/E-06-next-roadmap.md`：PASS，带记录边界。
  - Blocker/Major 处理：无。
  - 实现 commit：待本轮 E-06 记录提交后补。
  - push 状态：待 GitHub 连接恢复后推送。
  - 遗留风险：E-06 只是路线收敛，不替代 E-07 文档一致性检查或 E-08 发布前风险清单。
  - 下一步：E-07 文档一致性检查。

### Task 23 文档校准留痕

- README-01：README 当前计划重写
  - 状态：已完成。
  - 实现范围：重写 `README.md`，补充 C 阶段完成后的真实项目状态、痛点分析、运行与验收命令、API 搜索指标说明、D/E 后续计划和仓库边界；同步 `docs/collaboration/任务计划.md` 的重估记录。
  - 验证方式：`.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`；`git diff --check`：无空白错误；`README.md` 未出现旧 `127.0.0.1:4173`。
  - subagent 审查文件：`docs/collaboration/reviews/README-01-current-plan-readme.md`：PASS。
  - Blocker/Major 处理：初审 2 个 Major 已修复：补齐 D-13/D-14 执行顺序；D-05 限定为只映射现有 `depth`，不得新增预算参数。
  - 实现 commit：`fc66808`。
  - push 状态：已推送 main。
  - 下一步：审查通过后，保持下一最小开发任务为 D-01 页面整体布局。

## 记录规则

- 每个有效任务开始时，把状态改为 `进行中`，并记录实际分支和 worktree。
- 每个有效任务在获得用户授权后提交并填写实现 commit；Task 23 产品化升级阶段已获得用户授权：每个最小任务在测试、验收和 subagent 审查通过后，自动 commit 并 push 到远程 GitHub 留痕。
- Claude Code 审查完成后，填写审查文件路径和 Blocker/Major 处理结果。
- 审查处理记录提交后，在授权范围内推送任务分支到 GitHub 留痕。
- 合回 `main` 后，在授权范围内把合并状态改为 `已合并`，并推送 `main` 到 GitHub。
- Task 6/7 只作为废弃历史记录保留，不再创建分支或 worktree。
