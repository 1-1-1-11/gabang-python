# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目边界

这是五子棋 AI 的 Python 重构版，目标是以 FastAPI 后端为主承载棋盘规则、AI 搜索和游戏会话管理，并提供从零编写的静态前端骨架。

远程仓库应保持 Python 重构版边界：不要引入、迁移、复制或改名提交原始 JavaScript/React 项目源码、静态资源、Node 构建配置、旧 JS 测试或原始 README 内容。新增前端代码必须是全新代码，当前前端位于 `frontend/`，不依赖 Node 构建工具。

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

运行单个测试文件：

```bash
py -m pytest backend/tests/test_game_api.py -q
```

运行单个测试用例：

```bash
py -m pytest backend/tests/test_game_api.py::test_move_places_player_move_and_ai_reply -q
```

查看静态前端：启动后端后，在浏览器打开 `frontend/index.html`。前端默认通过 `body[data-api-base]` 访问 `http://127.0.0.1:8000`。

开发环境默认 CORS 允许所有来源；部署或需要收窄来源时设置逗号分隔的 `GOBANG_CORS_ORIGINS`。

## 架构概览

- `backend/app/main.py` 定义 FastAPI 应用、CORS、健康检查和游戏 API：`GET /api/health`、`POST /api/games/start`、`POST /api/games/{session_id}/move`、`POST /api/games/{session_id}/undo`、`POST /api/games/{session_id}/end`。
- `backend/app/schemas.py` 是 API request/response 的 Pydantic 合同层。游戏接口统一返回 `GameSnapshot`，字段使用 `snake_case`；错误响应为 `ErrorResponse` 的 `detail` 字段。
- `backend/app/game.py` 管理内存游戏会话。`SessionStore` 使用 TTL、最大容量和锁；`GameSession` 持有 `Board`、AI 参数和最近一次搜索结果；`snapshot()` 负责把内部状态转换为 API 返回结构。
- `backend/app/board.py` 是棋盘规则核心，负责落子、悔棋、胜负判断、坐标转换、候选落点、局面评分入口和 Zobrist 哈希维护。棋子角色用 `1` 和 `-1` 表示，空位为 `0`。
- `backend/app/evaluation.py` 与 `backend/app/shape.py` 实现棋形识别、候选点分组和启发式评分。终局五连分数由 `Board.evaluate()` 处理，候选空点评分由 `CANDIDATE_SHAPE_SCORE` 处理。
- `backend/app/minmax.py` 实现 negamax/alpha-beta 搜索，提供 `minmax()`、`vct()`、`vcf()`，并通过 `backend/app/cache.py` 按棋盘哈希、角色、剩余深度和算杀模式缓存搜索结果。
- `backend/app/zobrist.py` 提供确定性 Zobrist 哈希，用于搜索缓存键。
- `backend/dev_server.py` 是 uvicorn 开发服务器入口。
- `frontend/` 是无构建工具的静态 HTML/CSS/JS 前端，已接入游戏 start/move/undo/end API，并具备基础设置 UI、状态、错误和控件禁用处理；后续计划增强浏览器验收自动化。
- `backend/tests/` 覆盖棋盘规则、AI 搜索、健康检查、游戏 API、OpenAPI 合同、开发服务器、前端骨架和运行时边界。最近初步验收基线为 `py -m pytest backend/tests -q` 通过 59 项测试。

## 协作记录

任务台账在 `docs/collaboration/TASKS.md`。历史审查记录在 `docs/collaboration/reviews/`。下一阶段路线图按小任务推进：文档与项目状态收敛、前端验收增强、AI 能力基准化、运行时与部署准备。有效任务通常使用独立分支和 worktree，命名形如：

```text
task/<编号>-<名称>
.worktrees/<编号>-<名称>
```

任务完成后按台账规则记录实现 commit、审查文件和合并状态。推送或合并属于影响远端共享状态的操作，除非用户明确要求，否则不要主动执行。
