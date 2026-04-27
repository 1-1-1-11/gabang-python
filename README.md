# gobang-python

五子棋 AI 的 Python 重构版。

## 目标

本仓库正在把原 React + Web Worker 五子棋项目重构为 Python 后端优先的五子棋项目。

- FastAPI 后端：承载棋盘规则、AI 搜索和会话管理。
- Python 测试：用 pytest 覆盖棋盘规则、评分、搜索、API 合同和运行时边界。
- 浏览器验收：用全新 Node Playwright E2E 覆盖静态前端主路径、错误路径、控件状态和配置路径。
- 全新静态前端：位于 `frontend/`，不依赖 Node 构建工具，不复用原始 JS 项目文件。

远程仓库只保存 Python 重构版代码、测试、全新静态前端和相关文档。原始 JavaScript 源码、React 静态资源、旧 JS 测试、原始 README 和旧 Node 构建配置不进入 GitHub。当前 Node 配置仅用于全新 Playwright 浏览器验收，不参与前端构建。

## 当前能力

- `GET /api/health`
- Python 棋盘规则：落子、悔棋、胜负判断、和棋判断、合法落点生成。
- AI 评分与搜索：棋形识别、启发式评分、Zobrist 缓存、minmax/negamax、VCT/VCF 入口。
- AI 搜索 smoke 基准：小棋盘、浅深度、宽松耗时和搜索指标阈值。
- FastAPI 游戏会话接口：开局、落子、悔棋、结束会话。
- 可选 Redis 会话存储：默认仍使用内存会话，可通过环境变量切换为 Redis 以支持基础跨进程共享。
- OpenAPI response model、错误响应说明和请求示例。
- 全新静态前端骨架，已接入 start/move/undo/end API，支持棋盘大小、搜索深度、AI 先手和 API 地址配置，并展示落子记录、最近一步高亮和 AI 搜索信息。
- Python 开发服务器启动入口。

## 当前限制

- 前端仍是基础静态实现：已提供配置、状态、错误恢复、AI 信息展示和 Playwright E2E 验收，但没有复杂 UI 框架、账号体系或持久化前端状态。
- AI 强度已有正确性测试和宽松 smoke 基准，但这些基准只用于发现明显回归，不代表比赛强度评估或性能 SLA。
- 默认会话后端仍是进程内内存：服务重启会丢失棋局，多进程部署不能共享会话；Redis 后端是可选能力，仅提供基础跨进程读写，不提供分布式锁。
- 开发模式默认 CORS 允许所有来源；部署时必须用 `GOBANG_CORS_ORIGINS` 收窄允许来源。

## 环境准备

建议使用 Python 3.12 或 3.13。在当前 Windows 环境中使用 `py` 命令。

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r backend\requirements.lock.txt
```

## 启动后端

```powershell
py -m backend.dev_server --reload
```

默认地址：

```text
http://127.0.0.1:8000
```

可选参数：

```powershell
py -m backend.dev_server --host 0.0.0.0 --port 9000 --reload
```

CORS 在开发模式下默认允许所有来源，方便本地静态前端直接访问。部署时应使用逗号分隔的环境变量收窄允许来源：

```powershell
$env:GOBANG_CORS_ORIGINS="https://gobang.example"
py -m backend.dev_server
```

也可以同时允许多个来源：

```powershell
$env:GOBANG_CORS_ORIGINS="https://gobang.example,https://admin.gobang.example"
py -m backend.dev_server
```

如果未设置 `GOBANG_CORS_ORIGINS`，或变量内容为空白，服务会回退为 `*`。生产环境不要使用 `*`，应只填写实际前端域名。该环境变量在后端进程启动时读取，修改后需要重启服务才会生效。

FastAPI 自动文档：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

OpenAPI 中的游戏接口统一返回 `GameSnapshot`。错误响应使用 `ErrorResponse`，字段为 `detail`。`best_path` 表示 AI 搜索主变路线，格式是若干 `[row, column]` 坐标。

## 运行时边界

后端默认使用进程内内存保存游戏会话。`SessionStore` 默认最多保留 256 个会话，单个会话 TTL 为 1 小时；达到容量上限时会淘汰最早创建的会话，过期会话会在读取或创建新会话时清理。服务重启会丢失全部棋局，多进程或多实例部署也不会共享会话。

可以通过环境变量调整默认内存会话限制：

```powershell
$env:GOBANG_MAX_SESSIONS="512"
$env:GOBANG_SESSION_TTL_SECONDS="7200"
py -m backend.dev_server
```

如需基础跨进程会话共享，可以切换为 Redis 后端：

```powershell
$env:GOBANG_SESSION_BACKEND="redis"
$env:GOBANG_REDIS_URL="redis://127.0.0.1:6379/0"
py -m backend.dev_server
```

Redis 后端会把棋盘尺寸、棋盘历史、当前玩家、AI 参数和最近一次搜索信息序列化到 Redis，并使用 `GOBANG_SESSION_TTL_SECONDS` 设置 key TTL。默认测试不依赖真实 Redis 服务；如需真实 Redis 验收，需要本机或部署环境先提供 Redis 服务。当前 Redis 后端不实现分布式锁，同一 session 的并发写仍应由调用方或部署层避免。

游戏 API 的单个内存会话操作会串行化，避免同一会话内并发落子互相覆盖。这个锁只存在于当前 Python 进程内，不适合直接扩展到多进程生产会话。

`py -m backend.dev_server --reload` 只用于本地开发；部署时不要使用 `--reload`，并且需要显式设置 `GOBANG_CORS_ORIGINS`。如果要支撑长期或多实例运行，应使用 Redis 等外部会话存储，并接受当前无分布式锁限制。

## 查看前端骨架

当前前端位于 `frontend/`，是从零创建的静态 HTML/CSS/JS 骨架，不依赖 Node 构建工具，也不复用原始 JS 项目文件。

```powershell
Start-Process .\frontend\index.html
```

前端默认读取 `body[data-api-base]`，当前值为 `http://127.0.0.1:8000`；也可以用 URL 查询参数临时覆盖，例如 `frontend/index.html?apiBase=http://127.0.0.1:9000`。启动后端后打开 `frontend/index.html`，可以选择棋盘大小、搜索深度和是否 AI 先手，再点击“开始”创建会话。棋盘大小支持 5-25，搜索深度支持 1-8；深度越高 AI 思考越慢，演示推荐使用较小棋盘和低深度。点击棋盘落子后，前端会渲染后端返回的 `GameSnapshot`。

## 验收命令

必跑后端与合同测试：

```powershell
py -m pytest backend\tests -q
```

推荐浏览器验收，仅用于 Playwright，不参与前端构建：

```powershell
npm install
npx playwright install chromium
npm run test:e2e
```

可选 Redis 验收需要先提供 Redis 服务，再设置 `GOBANG_SESSION_BACKEND=redis` 和 `GOBANG_REDIS_URL` 后运行 `py -m pytest backend\tests\test_redis_session_store.py -q`。

AI 基准测试位于 `backend/tests/test_ai_benchmark.py`，使用小棋盘、浅搜索深度和宽松阈值，只用于 smoke regression：发现搜索节点数、候选点数量或耗时出现数量级退化。耗时受硬件和系统负载影响，不应作为正式性能承诺或比赛强度评估。

## 验收演示步骤

1. 安装依赖。
2. 运行必跑测试，确认 pytest 通过。
3. 启动后端开发服务器。
4. 打开 `http://127.0.0.1:8000/docs`，确认 OpenAPI 文档可访问。
5. 打开 `frontend/index.html`。
6. 点击“开始”创建会话。
7. 点击棋盘落子，确认玩家落子和 AI 回复都会显示在棋盘、落子记录和 AI 搜索信息中。
8. 点击“悔棋”，确认最近一轮玩家与 AI 落子被撤销。
9. 点击“结束”，确认当前会话结束。

## 浏览器主路径验收

1. 启动后端：

   ```powershell
   py -m backend.dev_server --reload
   ```

2. 打开静态前端：

   ```powershell
   Start-Process .\frontend\index.html
   ```

3. 在 Settings 区域设置棋盘大小、搜索深度、API 地址和是否 AI 先手；对局开始后这些配置应禁用，结束后恢复。
4. 点击“开始”，确认状态变为“进行中”，棋盘尺寸和深度显示与设置一致。
5. 如果勾选 AI 先手，确认落子记录中已有 1 条 AI 首手记录。
6. 点击一个空棋盘格，确认玩家落子和 AI 回复都显示在棋盘和落子记录中。
7. 点击“悔棋”，确认最近一轮玩家与 AI 落子被撤销；无落子记录时“悔棋”按钮应禁用。
8. 点击“结束”，确认状态变为“已结束”，棋盘格和“结束”按钮禁用。
9. 刷新页面或重新打开前端后，可以重新开始一局。

## 最小部署验收清单

部署或演示前至少完成以下检查：

1. 安装依赖并运行全量测试：

   ```powershell
   py -m pip install -r backend\requirements.lock.txt
   py -m pytest backend\tests -q
   ```

2. 设置生产前端来源，不使用默认 `*`：

   ```powershell
   $env:GOBANG_CORS_ORIGINS="https://gobang.example"
   ```

3. 启动后端，不使用开发热重载：

   ```powershell
   py -m backend.dev_server --host 0.0.0.0 --port 8000
   ```

4. 访问 `http://127.0.0.1:8000/api/health`，确认返回 `{"status":"ok"}`。
5. 访问 `http://127.0.0.1:8000/docs`，确认 OpenAPI 文档可打开。
6. 打开 `frontend/index.html` 或部署后的静态前端，完成“开始、落子、AI 回复、悔棋、结束”主路径；如果后端地址不是 `http://127.0.0.1:8000`，可以修改 `frontend/index.html` 中的 `body[data-api-base]`，或在访问地址后追加 `?apiBase=https://your-api.example` 临时覆盖。
7. 确认部署形态：单进程可以使用默认内存会话；多进程或多实例需要设置 `GOBANG_SESSION_BACKEND=redis` 和 `GOBANG_REDIS_URL`，并接受当前 Redis 后端不提供分布式锁。

## API 概览

- `GET /api/health`
- `POST /api/games/start`
- `POST /api/games/{session_id}/move`
- `POST /api/games/{session_id}/undo`
- `POST /api/games/{session_id}/end`

示例：

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/games/start `
  -ContentType application/json `
  -Body '{"size":15,"ai_first":false,"depth":4}'
```

## 当前结构

```text
backend/
  app/
    main.py
    board.py
    cache.py
    evaluation.py
    game.py
    redis_session_store.py
    minmax.py
    schemas.py
    settings.py
    shape.py
    zobrist.py
  tests/
    test_health.py
    test_board.py
    test_ai_search.py
    test_ai_benchmark.py
    test_game_api.py
    test_api_contract.py
    test_dev_server.py
    test_frontend_skeleton.py
    test_redis_session_store.py
    test_runtime_hardening.py
frontend/
  index.html
  styles.css
  app.js
e2e/
  gobang.spec.js
playwright.config.js
package.json
docs/
  collaboration/
    TASKS.md
    CLAUDE_REVIEW_PROMPT.md
    reviews/
pyproject.toml
backend/requirements.lock.txt
```

## 协作流程

每个有效任务使用独立分支和 worktree：

```text
task/<编号>-<名称>
.worktrees/<编号>-<名称>
```

任务完成后必须：

1. 运行相关测试。
2. 写入 Claude Code 审查记录。
3. 记录 Codex 处理结果。
4. 推送任务分支到 GitHub。
5. 合回 `main` 后把合并状态记入台账，并推送 `main` 到 GitHub。

推送、合并、提交等影响远端或历史的操作需要明确授权后再执行。

## 后续方向

1. 交付文档维护：README、TASKS 台账和 CLAUDE.md 随功能变化继续保持一致。
2. 可选增强：真实 Redis 环境验收、多实例部署演练和更强 AI 棋力评估。

## 原始项目说明

原始 JavaScript 项目的 README 和源码只允许保留在本地忽略目录，不作为 GitHub 远程内容提交。远程仓库的根 README 只描述当前重构版项目。后续新增的前端代码必须是全新代码，不得复制、迁移或改名提交原始 JS 项目文件。
