# gobang-python

一个基于 Python 的五子棋 AI 项目，使用 FastAPI 提供后端接口，并提供 Vue3 + Vite 前端用于本地对弈和演示。

## 功能概览

- 五子棋棋盘规则：落子、悔棋、胜负判断、和棋判断、合法落点生成。
- AI 搜索：棋形识别、启发式评分、Zobrist 缓存、minmax / negamax 搜索、VCT / VCF 入口。
- 游戏会话接口：开局、玩家落子、AI 回复、悔棋、结束会话。
- 可选 Redis 会话存储：默认使用进程内内存，也可以切换到 Redis 以支持基础跨进程共享。
- Vue3 + Vite 前端：支持棋盘大小、搜索深度、AI 先手、API 地址配置、落子记录、最近一步高亮和 AI 搜索信息展示。
- 自动化测试：pytest 覆盖后端规则、搜索、API 合同、运行时边界和前端结构；Playwright 覆盖浏览器主路径与错误路径。

## 一键启动

Windows 用户可以直接双击项目根目录下的：

```text
start.bat
```

它会自动完成这些事情：

1. 检查并创建 Python 虚拟环境。
2. 安装后端依赖。
3. 安装前端依赖。
4. 启动后端服务。
5. 启动前端 Vite 开发服务。
6. 自动打开浏览器进入游戏页面。

启动成功后会打开：

```text
http://127.0.0.1:4173/?apiBase=http://127.0.0.1:8000
```

如果要关闭项目，请关闭启动时弹出的 `gobang backend` 和 `gobang frontend` 两个黑色窗口。

## 环境要求

建议使用 Python 3.12 或 3.13。Windows 环境推荐使用 `py` 命令。

如需运行前端或浏览器端验收测试，还需要安装 Node.js 和 npm。Vite 8 要求 Node `^20.19.0` 或 `>=22.12.0`。

## 安装依赖

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r backend\requirements.lock.txt
```

## 启动后端

本地开发启动：

```powershell
py -m backend.dev_server --reload
```

默认服务地址：

```text
http://127.0.0.1:8000
```

指定监听地址和端口：

```powershell
py -m backend.dev_server --host 0.0.0.0 --port 9000 --reload
```

FastAPI 自动文档：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

## 使用前端

安装前端依赖：

```powershell
npm install
```

启动后端后，再启动 Vite 前端：

```powershell
npm run dev:frontend
```

默认前端地址：

```text
http://127.0.0.1:4173
```

前端默认连接：

```text
http://127.0.0.1:8000
```

也可以通过 URL 查询参数临时指定 API 地址：

```text
http://127.0.0.1:4173/?apiBase=http://127.0.0.1:9000
```

页面中可以配置：

- 棋盘大小：5-25
- 搜索深度：1-8
- 是否 AI 先手
- API 地址

基本操作流程：

1. 启动后端。
2. 启动 `npm run dev:frontend` 并打开 `http://127.0.0.1:4173`。
3. 设置棋盘大小、搜索深度和是否 AI 先手。
4. 点击“开始”创建会话。
5. 点击棋盘空位落子，等待 AI 回复。
6. 查看落子记录、最近一步高亮和 AI 搜索信息。
7. 点击“悔棋”撤销最近一轮玩家与 AI 落子。
8. 点击“结束”结束当前会话。

## API 概览

- `GET /api/health`
- `POST /api/games/start`
- `POST /api/games/{session_id}/move`
- `POST /api/games/{session_id}/undo`
- `POST /api/games/{session_id}/end`

开局示例：

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/games/start `
  -ContentType application/json `
  -Body '{"size":15,"ai_first":false,"depth":4}'
```

游戏接口统一返回 `GameSnapshot`。错误响应使用 `detail` 字段。`best_path` 表示 AI 搜索主变路线，格式为若干 `[row, column]` 坐标。

## 会话存储配置

默认使用进程内内存保存游戏会话：

- 默认最多保留 256 个会话。
- 默认单个会话 TTL 为 1 小时。
- 服务重启后会话会丢失。
- 多进程或多实例部署时，默认内存会话不会共享。

可以通过环境变量调整内存会话限制：

```powershell
$env:GOBANG_MAX_SESSIONS="512"
$env:GOBANG_SESSION_TTL_SECONDS="7200"
py -m backend.dev_server
```

如需基础跨进程会话共享，可以切换到 Redis：

```powershell
$env:GOBANG_SESSION_BACKEND="redis"
$env:GOBANG_REDIS_URL="redis://127.0.0.1:6379/0"
py -m backend.dev_server
```

Redis 后端会保存棋盘尺寸、棋盘历史、当前玩家、AI 参数和最近一次搜索信息，并使用 `GOBANG_SESSION_TTL_SECONDS` 设置 key TTL。当前 Redis 后端不提供分布式锁，同一 session 的并发写需要由调用方或部署层避免。

## CORS 配置

开发模式下默认允许所有来源，方便本地前端访问。部署时应显式设置允许来源：

```powershell
$env:GOBANG_CORS_ORIGINS="https://gobang.example"
py -m backend.dev_server
```

多个来源用逗号分隔：

```powershell
$env:GOBANG_CORS_ORIGINS="https://gobang.example,https://admin.gobang.example"
py -m backend.dev_server
```

如果未设置 `GOBANG_CORS_ORIGINS`，或变量内容为空白，服务会回退为 `*`。生产环境不要使用 `*`。

## 运行测试

后端测试：

```powershell
py -m pytest backend\tests -q
```

浏览器验收测试：

```powershell
npm install
npx playwright install chromium
npm run test:e2e
```

前端构建：

```powershell
npm run build
```

可选 Redis 测试需要先提供 Redis 服务，再设置 `GOBANG_SESSION_BACKEND=redis` 和 `GOBANG_REDIS_URL` 后运行：

```powershell
py -m pytest backend\tests\test_redis_session_store.py -q
```

AI 基准测试位于 `backend/tests/test_ai_benchmark.py`，使用小棋盘、浅搜索深度和宽松阈值，只用于发现明显退化，不代表正式性能承诺或比赛强度评估。

## 部署提示

部署前建议至少完成：

1. 安装依赖。
2. 运行 `py -m pytest backend\tests -q`。
3. 设置 `GOBANG_CORS_ORIGINS`，不要在生产环境使用默认 `*`。
4. 启动后端时不要使用 `--reload`。
5. 访问 `http://127.0.0.1:8000/api/health`，确认返回 `{"status":"ok"}`。
6. 访问 `http://127.0.0.1:8000/docs`，确认 OpenAPI 文档可打开。
7. 打开 Vite 前端，完成“开始、落子、AI 回复、悔棋、结束”流程。
8. 如果需要多进程或多实例部署，配置 Redis 会话后端。

## 项目结构

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
  src/
    App.vue
    main.js
    styles.css
e2e/
  gobang.spec.js
vite.config.js
playwright.config.js
package.json
pyproject.toml
backend/requirements.lock.txt
```
