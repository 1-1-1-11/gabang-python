# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目边界

这是五子棋 AI 的 Python 重构版，目标是以 FastAPI 后端为主承载棋盘规则、AI 搜索和游戏会话管理，并提供从零编写的 Vue3 + Vite 前端。

远程仓库应保持 Python 重构版边界：不要引入、迁移、复制或改名提交原始 JavaScript/React 项目源码、静态资源、旧 Node 构建配置、旧 JS 测试或原始 README 内容。新增前端代码必须是全新 Vue3 + Vite 代码，当前前端位于 `frontend/`，Node 配置只服务当前 Vite 前端和全新 Playwright E2E，不代表恢复旧 JS 项目。

## 常用命令

本 Windows 环境优先使用 `py` 命令。

```bash
py -m venv .venv
py -m pip install -r backend/requirements.lock.txt
```

启动开发服务器：

```bash
py -m backend.dev_server --reload
```

指定地址和端口：

```bash
py -m backend.dev_server --host 0.0.0.0 --port 9000 --reload
```

运行全部测试：

```bash
py -m pytest backend/tests -q
```

运行 Playwright E2E：

```bash
npm install
npx playwright install chromium
npm run test:e2e
```

运行前端开发服务：

```bash
npm run dev:frontend
```

构建前端：

```bash
npm run build
```

Vite 8 要求 Node `^20.19.0` 或 `>=22.12.0`。

运行单个测试文件：

```bash
py -m pytest backend/tests/test_game_api.py -q
```

运行单个测试用例：

```bash
py -m pytest backend/tests/test_game_api.py::test_move_places_player_move_and_ai_reply -q
```

查看前端：启动后端后运行 `npm run dev:frontend`，在浏览器打开 `http://127.0.0.1:5173`。前端默认通过 `#app[data-api-base]` 访问 `http://127.0.0.1:8000`，也支持用 `?apiBase=http://127.0.0.1:9000` 临时覆盖；前端会把 API 地址规范化为 http(s) origin。

开发环境默认 CORS 允许所有来源；部署或需要收窄来源时设置逗号分隔的 `GOBANG_CORS_ORIGINS`。

会话后端默认是内存模式。可用 `GOBANG_SESSION_BACKEND=redis` 和 `GOBANG_REDIS_URL` 切换到基础 Redis 会话共享；Redis 后端不提供分布式锁，同一 session 并发写仍需由调用方或部署层避免。

AI 基准位于 `backend/tests/test_ai_benchmark.py`，使用小棋盘、浅深度和宽松阈值，只用于 smoke regression，不是性能 SLA 或比赛强度评估。

## 架构概览

- `backend/app/main.py` 定义 FastAPI 应用、CORS、健康检查和游戏 API：`GET /api/health`、`POST /api/games/start`、`POST /api/games/{session_id}/move`、`POST /api/games/{session_id}/undo`、`POST /api/games/{session_id}/end`。
- `backend/app/schemas.py` 是 API request/response 的 Pydantic 合同层。游戏接口统一返回 `GameSnapshot`，字段使用 `snake_case`；错误响应为 `ErrorResponse` 的 `detail` 字段。
- `backend/app/game.py` 管理游戏会话。默认 `SessionStore` 使用 TTL、最大容量和锁；`GameSession` 持有 `Board`、AI 参数和最近一次搜索结果；`snapshot()` 负责把内部状态转换为 API 返回结构。可选 Redis 后端由配置工厂创建，用于基础跨进程会话共享。
- `backend/app/board.py` 是棋盘规则核心，负责落子、悔棋、胜负判断、坐标转换、候选落点、局面评分入口和 Zobrist 哈希维护。棋子角色用 `1` 和 `-1` 表示，空位为 `0`。
- `backend/app/evaluation.py` 与 `backend/app/shape.py` 实现棋形识别、候选点分组和启发式评分。终局五连分数由 `Board.evaluate()` 处理，候选空点评分由 `CANDIDATE_SHAPE_SCORE` 处理。
- `backend/app/minmax.py` 实现 negamax/alpha-beta 搜索，提供 `minmax()`、`vct()`、`vcf()`，并通过 `backend/app/cache.py` 按棋盘哈希、角色、剩余深度和算杀模式缓存搜索结果；`search_metrics` 暴露搜索调用、剪枝、深度等全局指标。
- `backend/app/zobrist.py` 提供确定性 Zobrist 哈希，用于搜索缓存键。
- `backend/app/redis_session_store.py` 实现可选 Redis 会话读写与序列化，默认测试使用 fake，不要求真实 Redis 服务。
- `backend/dev_server.py` 是 uvicorn 开发服务器入口。
- `frontend/` 是 Vue3 + Vite 前端，已接入游戏 start/move/undo/end API，并具备设置 UI、状态、错误恢复、控件禁用、最近一步高亮、AI 搜索信息和 API 地址配置。
- `e2e/` 是全新 Playwright 浏览器验收测试，只服务当前 Vue/Vite 前端和 Python 后端，不复用旧 JS 项目。
- `backend/tests/` 覆盖棋盘规则、AI 搜索、AI benchmark、健康检查、游戏 API、OpenAPI 合同、开发服务器、前端骨架、Redis 会话和运行时边界。当前验收基线为 `py -m pytest backend/tests -q` 与 `npm run test:e2e`。

## 协作记录

任务台账在 `docs/collaboration/TASKS.md`。历史审查记录在 `docs/collaboration/reviews/`。当前已进入验收演示交付收敛阶段，后续主要维护 README/TASKS/CLAUDE 一致性，并按需扩展真实 Redis 环境验收、多实例部署演练和更强 AI 棋力评估。有效任务通常使用独立分支和 worktree，命名形如：

```text
task/<编号>-<名称>
.worktrees/<编号>-<名称>
```

任务完成后按台账规则记录实现 commit、审查文件和合并状态。推送或合并属于影响远端共享状态的操作，除非用户明确要求，否则不要主动执行。
