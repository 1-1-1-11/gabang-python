# gobang-python

五子棋 AI 的 Python 重构版。

## 目标

本仓库正在把原 React + Web Worker 五子棋项目重构为 Python 版五子棋项目。

- FastAPI 后端：承载棋盘规则、AI 搜索、会话管理
- Python 测试：用 pytest 覆盖棋盘规则、评分、搜索和 API 行为

远程仓库只保存 Python 重构版代码、测试和相关文档。原始 JavaScript 源码、React 静态资源、旧 JS 测试和 Node 构建配置不进入 GitHub。

当前阶段已完成：

- FastAPI 后端骨架
- `GET /api/health`
- Python 棋盘规则迁移
- 棋盘规则测试
- AI 评分与搜索迁移
- FastAPI 游戏会话接口

## 当前验证

```powershell
py -m pytest backend\tests -q
```

## 当前结构

```text
backend/
  app/
    main.py
    board.py
    game.py
    minmax.py
  tests/
    test_health.py
    test_board.py
    test_ai_search.py
    test_game_api.py
docs/
  collaboration/
    TASKS.md
    CLAUDE_REVIEW_PROMPT.md
    reviews/
pyproject.toml
```

## 协作流程

每个任务使用独立分支和 worktree：

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

原始 JavaScript 项目的 README 和源码只允许保留在本地忽略目录，不作为 GitHub 远程内容提交。远程仓库的根 README 只描述 Python 重构版。
