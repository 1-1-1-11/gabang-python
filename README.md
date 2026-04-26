# gobang-python

五子棋 AI 的 Python 重构版。

## 目标

本仓库正在把原 React + Web Worker 五子棋项目重构为 Python 后端优先的五子棋项目。

- FastAPI 后端：承载棋盘规则、AI 搜索、会话管理
- Python 测试：用 pytest 覆盖棋盘规则、评分、搜索和 API 行为
- 后续前端：允许从零创建全新 JS 前端，但不得复用、迁移或复制原始 JS 项目文件

远程仓库当前只保存 Python 重构版代码、测试和相关文档。原始 JavaScript 源码、React 静态资源、旧 JS 测试、原始 README 和 Node 构建配置不进入 GitHub。

## 当前能力

- `GET /api/health`
- Python 棋盘规则
- AI 评分与搜索
- FastAPI 游戏会话接口
- Python 开发服务器启动入口
- OpenAPI response model 和错误响应说明
- 全新静态前端骨架

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

FastAPI 自动文档：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

OpenAPI 中的游戏接口统一返回 `GameSnapshot`。错误响应使用 `ErrorResponse`，字段为 `detail`。`best_path` 表示 AI 搜索主变路线，格式是若干 `[row, column]` 坐标。

## 查看前端骨架

当前前端位于 `frontend/`，是从零创建的静态 HTML/CSS/JS 骨架，不依赖 Node 构建工具，也不复用原始 JS 项目文件。

```powershell
Push-Location frontend
py -m http.server 8080 --bind 127.0.0.1
Pop-Location
```

然后打开：

```text
http://127.0.0.1:8080/
```

前端已经接入 `POST /api/games/start`、`move`、`undo`、`end`。启动后端和前端静态服务器后，点击“开始”创建会话，点击棋盘落子，前端会渲染后端返回的 `GameSnapshot`。

不要直接用 `file://` 打开 `frontend/index.html` 做验收；现代浏览器会阻止 `type="module"` 脚本从本地文件源加载。

## 运行测试

```powershell
py -m pytest backend\tests -q
```

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

前端默认读取 `body[data-api-base]`，当前值为 `http://127.0.0.1:8000`。

## 当前结构

```text
backend/
  app/
    main.py
    board.py
    game.py
    schemas.py
    minmax.py
  tests/
    test_health.py
    test_board.py
    test_ai_search.py
    test_game_api.py
    test_api_contract.py
    test_dev_server.py
docs/
  collaboration/
    TASKS.md
    CLAUDE_REVIEW_PROMPT.md
    reviews/
pyproject.toml
frontend/
  index.html
  styles.css
  app.js
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
5. 合回 `main` 后推送 `main` 到 GitHub。

## 原始项目说明

原始 JavaScript 项目的 README 和源码只允许保留在本地忽略目录，不作为 GitHub 远程内容提交。远程仓库的根 README 只描述当前重构版项目。后续新增的前端代码必须是全新代码，不得复制、迁移或改名提交原始 JS 项目文件。
