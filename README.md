# gobang-python

五子棋 AI 项目。当前仓库以 Python/FastAPI 承载棋盘规则、AI 搜索和游戏会话管理，并使用全新 Vue3 + Vite 前端提供本地对弈与演示界面。

本 README 反映 2026-04-28 的真实项目进度：Task 23.A、23.B、23.C 已完成，下一步进入 Task 23.D 的 D-01 页面整体布局。详细任务台账见 `docs/collaboration/TASKS.md`，产品化升级计划见 `docs/collaboration/任务计划.md`。

## 当前状态

已完成：

- 后端：FastAPI 游戏 API、棋盘规则、胜负判断、悔棋、会话管理、可选 Redis 会话存储。
- AI：negamax / alpha-beta 搜索、VCT / VCF 入口、Zobrist 缓存、候选点局部化、走法排序、搜索指标记录。
- API 合同：游戏接口统一返回 `GameSnapshot`，其中包含 `search_metrics`。
- 前端工程：Vue3 + Vite 已落地，API client 与 `useGameState` 状态模块已拆出。
- 验收：后端 pytest、Playwright E2E、Vite build 已作为当前回归基线。
- 协作：每个最小任务要求自测、subagent 审查、commit、push 和文档留痕。

未完成：

- D 阶段 UI 产品化尚未开始，当前页面仍是可运行控制台，不是最终视觉体验。
- `search_metrics` 已进入 API 和前端状态，但还没有完整 UI 展示。
- 节点预算、时间预算、迭代加深、真实棋力评测和生产部署还不属于当前 MVP。
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
- 展示落子记录、最近一步、AI 评分、搜索深度和主变路径。

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
- `prunes`
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
| README 曾出现编码显示异常 | 普通 PowerShell 读取时中文曾出现乱码，需要显式 UTF-8 读取才可靠 | 新接手者可能误判文档已损坏，无法快速判断进度 | 本次重写为清晰 UTF-8 中文文档，并把运行入口、进度和计划合并到一个入口 |
| UI 仍是控制台式页面 | C 阶段只完成 Vite、API client、状态 composable | 继续堆功能会让 `App.vue` 变重，后续交互难验收 | D-01 到 D-04 先拆布局、棋盘、棋子、控制面板 |
| 搜索指标还未产品化展示 | C-09 只把 `search_metrics` 接入 API 和状态 | 用户看不到 AI 为什么慢、搜索是否有效 | D-08 单独做 `SearchInfo`，避免和布局任务混在一起 |
| AI 预算能力仍未实现 | 当前请求只有 `depth`，搜索是同步完整深度 | 直接加时间限制会引入不完整结果语义 | 后续先做确定性 `node_limit`，再考虑时间预算和迭代加深 |
| Redis 不是完整分布式协作方案 | Redis session store 不含 per-session lock | 多实例下同一 session 并发写可能冲突 | 当前文档明确边界，生产前再做并发写保护任务 |
| benchmark 仍偏 smoke | 小棋盘、浅深度、宽松阈值 | 不能证明比赛棋力，只能防明显退化 | 下一轮 AI 优化必须增加固定局面和指标对比 |
| 协作文档需要持续对齐 | README、CLAUDE、TASKS、任务计划承担不同角色 | 后续 agent 可能误用旧端口、旧前端或旧任务状态 | 文档任务也走审查和 commit/push，D/E 阶段继续做一致性检查 |

## 后续计划

后续计划按照三个原则重排：

1. 先处理会阻塞体验验收的结构问题，再处理视觉细节。
2. 每个任务都绑定可验证证据，避免只靠主观判断。
3. 每个任务保持最小边界，通过测试和 subagent 审查后再 commit/push。

### 当前最近任务

| 优先级 | 任务 | 为什么现在做 | 验收证据 |
| --- | --- | --- | --- |
| P0 | D-01 页面整体布局 | D 阶段所有 UI 组件需要先落在稳定页面结构中 | 桌面端左棋盘右信息区清晰，窄屏不重叠，E2E 主路径不坏 |
| P0 | D-02 棋盘组件 | 当前棋盘逻辑仍在主页面，后续棋子、可访问性和响应式都依赖它 | 点击空点能落子，请求中禁用，Playwright 选择器保持可用 |
| P0 | D-03 棋子组件 | 黑白棋子、最后一步标记是最核心可读性 | 黑白清晰，最后一步明显，移动端不变形 |
| P0 | D-04 控制面板 | 开始、悔棋、结束是主流程门槛 | 按钮状态与 session、busy、winner 同步 |
| P1 | D-05 至 D-10 体验组件 | 难度、AI 思考、落子记录、搜索指标、错误和结束态决定产品完成度 | 每个组件连接真实状态或真实 API，不做静态展示 |
| P1 | D-11 至 D-14 视觉与验收 | 主题、响应式、可访问性和 E2E 是进入 E 阶段前的质量门槛 | 桌面和窄屏无重叠，核心控件可识别，`npm run test:e2e` 通过 |
| P2 | E-01 至 E-08 收敛 | D 阶段完成后才能做最终回归、审查汇总和风险清单 | pytest、build、E2E、审查文件、commit/push、风险都可追溯 |

### 不建议现在插入的任务

| 任务 | 暂缓原因 | 适合进入的时机 |
| --- | --- | --- |
| 节点预算和时间预算 | 会改变 API 合同与搜索语义，且不阻塞 D 阶段 UI | D-08 搜索信息展示完成后 |
| 迭代加深 | 需要预算语义、上一完整深度结果和更强测试 | 节点预算稳定后 |
| 真实 Redis 并发锁 | 当前本地 MVP 不需要多实例同写 | 准备生产或多实例部署前 |
| CI/CD | 当前优先级低于 UI 产品化和本地验收 | E 阶段完成后作为下一轮工程化任务 |
| 比赛系统、房间、排行榜 | 超出当前单机对弈 MVP | 现代 UI 和质量收敛完成后 |

## 协作流程

后续有效任务按以下流程执行：

1. 在 `docs/collaboration/TASKS.md` 或计划记录中确认任务状态和范围。
2. 只修改当前任务需要的文件，不混入无关重构。
3. 运行与任务相关的最小测试。
4. 使用 subagent 做只读审查，审查文件保存到 `docs/collaboration/reviews/`。
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
    api/client.js
    composables/useGameState.js
e2e/
  gobang.spec.js
docs/
  collaboration/
    TASKS.md
    任务计划.md
    reviews/
package.json
package-lock.json
playwright.config.js
vite.config.js
start.bat
pyproject.toml
backend/requirements.lock.txt
```
