# gobang-python

五子棋 AI 项目。当前仓库以 Python/FastAPI 承载棋盘规则、AI 搜索和游戏会话管理，并使用全新 Vue3 + Vite 前端提供本地对弈与演示界面。

本 README 反映 2026-04-30 的真实项目进度：Task 23.A、23.B、23.C、23.D 已完成，Task 23.E 已完成后端回归、前端构建、E2E 回归、审查汇总、GitHub 留痕汇总和下一阶段路线；下一步是 E-07 文档一致性检查与 E-08 发布前风险清单。详细任务台账见 `docs/collaboration/TASKS.md`，产品化升级计划见 `docs/collaboration/任务计划.md`。

## 当前状态

已完成：

- 后端：FastAPI 游戏 API、棋盘规则、胜负判断、悔棋、会话管理、可选 Redis 会话存储。
- AI：negamax / alpha-beta 搜索、VCT / VCF 入口、Zobrist 缓存、候选点局部化、走法排序、迭代加深、静态搜索和搜索指标记录。
- API 合同：游戏接口统一返回 `GameSnapshot`，其中包含 `search_metrics`。
- 前端工程：Vue3 + Vite 已落地，API client、`useGameState` 状态模块、布局、棋盘、棋子、控制面板、难度、AI 思考、落子记录、搜索信息、错误提示、结束状态、主题、响应式和基础可访问性已完成。
- 验收：当前收敛基线为后端 `112 passed`、Vite build 通过、Playwright E2E `12 passed`。
- CI：`.github/workflows/quality.yml` 已新增，覆盖后端 pytest、前端 build、Playwright E2E 和最新提交空白检查。
- 协作：每个最小任务要求自测、审查记录、commit、push 和文档留痕；subagent 不可用时使用本地确定性审查并写明边界。

未完成：

- E-07 文档一致性检查和 E-08 发布前风险清单仍需完成。
- `d37ac32` 引入的迭代加深、静态搜索和 `beta_cutoffs` 指标已被回归测试覆盖，但棋力收益还没有单独评估。
- 节点预算、时间预算、真实棋力评测、生产部署和比赛系统还不属于当前 MVP。
- Redis 后端只提供基础跨进程会话共享，不提供同一 session 的分布式写锁。

## 快速启动

Windows 用户可以在仓库根目录双击：

```text
start.bat
```

脚本会创建或复用 Python 虚拟环境，安装后端和前端依赖，启动后端与 Vite 前端，并打开：

```text
http://127.0.0.1:5173/?apiBase=http://127.0.0.1:8000
```

关闭项目时，关闭脚本打开的 `gobang backend` 和 `gobang frontend` 两个终端窗口。

## 环境要求

- Python 3.12 或 3.13。
- Node.js 满足 Vite 8 要求：`^20.19.0` 或 `>=22.12.0`。
- npm。
- 如需运行浏览器验收，安装 Playwright Chromium。

Windows 下如果 `py` 启动器不可用，可以在创建虚拟环境后直接使用 `.\.venv\Scripts\python.exe`。

## 手动安装

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r backend\requirements.lock.txt
npm install
```

如果当前机器没有 `py` 启动器，可以改用：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.lock.txt
npm install
```

## 启动后端

```powershell
py -m backend.dev_server --reload
```

默认地址：

```text
http://127.0.0.1:8000
```

指定监听地址和端口：

```powershell
py -m backend.dev_server --host 0.0.0.0 --port 9000 --reload
```

接口文档：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

## 启动前端

前端依赖和脚本都在仓库根目录 `package.json`，不是独立的 `frontend/package.json`。

```powershell
npm run dev:frontend
```

默认前端地址：

```text
http://127.0.0.1:5173
```

前端默认连接：

```text
http://127.0.0.1:8000
```

也可以临时指定后端 API：

```text
http://127.0.0.1:5173/?apiBase=http://127.0.0.1:9000
```

当前前端支持：

- 设置棋盘大小，范围 `5-25`。
- 设置 AI 搜索深度，范围 `1-8`。
- 配置是否 AI 先手。
- 配置 API 地址。
- 开始、落子、等待 AI 回复、悔棋、结束。
- 展示落子记录、最近一步、AI 评分、搜索深度、搜索指标和主变路径。
- 展示 API 错误、网络错误、AI 思考状态和游戏结束结果。
- 支持桌面与窄屏响应式布局，主要控件具备基础 aria 标签和可见焦点。

## API 概览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/api/health` | 健康检查 |
| `POST` | `/api/games/start` | 创建游戏会话 |
| `POST` | `/api/games/{session_id}/move` | 玩家落子并触发 AI 回复 |
| `POST` | `/api/games/{session_id}/undo` | 撤销最近一轮落子 |
| `POST` | `/api/games/{session_id}/end` | 结束当前会话 |

开局示例：

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/games/start `
  -ContentType application/json `
  -Body '{"size":15,"ai_first":false,"depth":4}'
```

游戏接口统一返回 `GameSnapshot`：

- `session_id`：会话 ID。
- `board`：棋盘矩阵，`0` 为空，`1` 和 `-1` 为双方棋子。
- `winner`：胜者，未结束时为 `0`。
- `current_player`：下一手角色。
- `history`：落子记录。
- `score`：最近一次 AI 搜索评分。
- `best_path`：AI 主变路径，格式为若干 `[row, column]`。
- `current_depth`：最近一次 AI 搜索深度。
- `search_metrics`：最近一次 AI 搜索指标。

`search_metrics` 字段包括：

- `nodes`
- `beta_cutoffs`
- `cache_hits`
- `cache_stores`
- `candidate_moves`
- `leaf_nodes`
- `max_depth`
- `elapsed_ms`

未发生 AI 搜索时，这些指标返回零值。

## 会话与运行配置

默认使用进程内内存会话：

- 默认最多保留 `256` 个会话。
- 默认单个会话 TTL 为 `3600` 秒。
- 服务重启后会话丢失。
- 多进程或多实例部署时，内存会话不会共享。

调整内存会话限制：

```powershell
$env:GOBANG_MAX_SESSIONS="512"
$env:GOBANG_SESSION_TTL_SECONDS="7200"
py -m backend.dev_server
```

切换到 Redis 会话后端：

```powershell
$env:GOBANG_SESSION_BACKEND="redis"
$env:GOBANG_REDIS_URL="redis://127.0.0.1:6379/0"
py -m backend.dev_server
```

Redis 后端会保存棋盘、历史、当前玩家、AI 参数和最近一次搜索指标，并使用 `GOBANG_SESSION_TTL_SECONDS` 设置 key TTL。它不提供分布式锁，同一 session 的并发写需要由调用方或部署层避免。

CORS 配置：

```powershell
$env:GOBANG_CORS_ORIGINS="https://gobang.example,https://admin.gobang.example"
py -m backend.dev_server
```

未设置或设置为空时，开发模式会回退到 `*`。生产环境不要依赖默认 `*`。

## 测试与验收

后端全量测试：

```powershell
py -m pytest backend\tests -q
```

前端构建：

```powershell
npm run build
```

浏览器验收：

```powershell
npx playwright install chromium
npm run test:e2e
```

与 README、Vite 端口、前端骨架相关的快速检查：

```powershell
.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q
```

AI benchmark 位于：

```text
backend/tests/test_ai_benchmark.py
```

它只用于 smoke regression 和优化趋势观察，不代表正式性能 SLA 或比赛棋力评估。

## 当前痛点分析

| 痛点 | 证据 | 风险 | 当前处理策略 |
| --- | --- | --- | --- |
| README/TASKS/CLAUDE 需要持续对齐 | E-07 已被列为下一步 | 后续 agent 可能误用旧端口、旧任务状态或旧指标字段 | 文档一致性检查单独成任务，修正 tracked 文档并记录本地 AGENTS 边界 |
| AI 收益未独立证明 | `d37ac32` 已通过回归，但没有固定局面对比复盘 | 测试通过可能被误读为棋力提升已证明 | 下一轮先做 AI 指标与棋力评估，再决定预算能力和置换表增强 |
| CI 初始门禁云端首跑被阻塞 | 24-A 已新增 GitHub Actions workflow，本地同等门禁通过；GitHub annotation 显示账户 billing issue 阻止 job 启动 | 云端质量门禁暂不能提供保护 | 恢复 GitHub Actions 计费/账户状态后 rerun workflow，再决定是否拆 Linux 兼容、缓存或 artifact 上传 |
| Redis 不是完整分布式协作方案 | Redis session store 不含 per-session lock | 多实例下同一 session 并发写可能冲突 | 当前文档明确边界，生产前再做并发写保护任务 |
| 可访问性仍是基础级 | D-14 做了 aria/focus 基础，没有 axe 自动审计 | 复杂交互可能仍有辅助技术盲区 | 下一轮补 axe 或等价扫描，并把关键路径纳入自动验收 |

## 后续计划

后续计划按照三个原则重排：

1. 先完成 E-07/E-08，把文档一致性和发布前风险说清。
2. 下一轮先补自动化质量门禁，再扩展 AI、部署和比赛能力。
3. 每个任务保持最小边界，通过测试和审查记录后再 commit/push。

### 当前最近任务

| 优先级 | 任务 | 为什么现在做 | 验收证据 |
| --- | --- | --- | --- |
| P0 | E-07 文档一致性检查 | README、CLAUDE、TASKS、任务计划和本地 AGENTS 扫描已发现 README 过期 | tracked 文档不再指向旧 D-01、旧剪枝指标名或旧端口 |
| P0 | E-08 发布前风险清单 | MVP 是否进入下一轮需要清楚区分已覆盖和未覆盖 | 风险清单列出 AI 收益、subagent、Redis 并发、CI 和部署边界 |
| P1 | CI 首跑恢复与门禁收紧 | 24-A 已新增初始 GitHub Actions workflow，但云端 job 被 billing issue 阻止启动 | 账户恢复后 rerun，首跑通过再考虑 Linux 兼容、缓存优化、artifact 上传和分 job 并行 |
| P1 | AI 指标与棋力复盘 | `d37ac32` 的收益还缺固定局面对比 | 固定局面记录 nodes、beta_cutoffs、cache_hits、耗时和选点稳定性 |
| P2 | 部署与比赛能力 | 多实例、部署和比赛体验超出当前 MVP | Redis 并发演练、Docker/公网部署、房间/观战/排行榜分任务进入下一轮 |

### 不建议现在插入的任务

| 任务 | 暂缓原因 | 适合进入的时机 |
| --- | --- | --- |
| 节点预算和时间预算 | 会改变 API 合同与搜索语义，需要先复盘当前迭代加深收益 | AI 指标与棋力复盘完成后 |
| 置换表 bound 语义 | 会影响搜索正确性和缓存解释，需要更强战术测试 | 固定局面评测稳定后 |
| 真实 Redis 并发锁 | 当前本地 MVP 不需要多实例同写 | 准备生产或多实例部署前 |
| 公网部署和打包 | 会引入环境、CORS、进程管理和发布产物边界 | CI 门禁稳定后 |
| 比赛系统、房间、排行榜 | 超出当前单机对弈 MVP | 现代 UI 和质量收敛完成后 |

## 协作流程

后续有效任务按以下流程执行：

1. 在 `docs/collaboration/TASKS.md` 或计划记录中确认任务状态和范围。
2. 只修改当前任务需要的文件，不混入无关重构。
3. 运行与任务相关的最小测试。
4. 可用时使用 subagent 做只读审查；不可用时执行本地确定性审查，并在 `docs/collaboration/reviews/` 写明边界。
5. 无 Blocker/Major 后更新留痕。
6. commit 并 push 到远程 GitHub。

当前仓库边界：

- 不恢复旧 React / JavaScript 项目源码。
- 不复制旧静态资源、旧构建配置或旧 README。
- 新增前端代码必须服务当前 Vue3 + Vite 项目。
- 打包、公网部署、登录、房间、排行榜、神经网络 AI 不属于当前 MVP。

## 项目结构

```text
backend/
  app/
    main.py
    board.py
    cache.py
    evaluation.py
    game.py
    minmax.py
    redis_session_store.py
    schemas.py
    settings.py
    shape.py
    zobrist.py
  tests/
frontend/
  index.html
  src/
    App.vue
    main.js
    styles.css
    theme.css
    api/client.js
    components/
      AppLayout.vue
      Board.vue
      ControlPanel.vue
      DifficultySelect.vue
      ErrorBanner.vue
      GameResult.vue
      MoveHistory.vue
      SearchInfo.vue
      Stone.vue
      ThinkingIndicator.vue
    composables/useGameState.js
e2e/
  gobang.spec.js
docs/
  collaboration/
    TASKS.md
    任务计划.md
    reviews/
.github/
  workflows/quality.yml
package.json
package-lock.json
playwright.config.js
vite.config.js
start.bat
pyproject.toml
backend/requirements.lock.txt
```
