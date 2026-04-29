# Review: D-04-control-panel

## Scope

- 新增 `frontend/src/components/ControlPanel.vue`，封装开始、悔棋、结束、重开四个控制按钮。
- `frontend/src/App.vue` 接入 `ControlPanel`，保留既有 `#start-button`、`#undo-button`、`#end-button` 选择器，并新增 `#restart-button`。
- `frontend/src/composables/useGameState.js` 新增 `restartGame()`，当前存在 session 时先结束当前局，再按当前设置启动新局。
- `frontend/src/styles.css` 增加四按钮控制网格。
- `backend/tests/test_frontend_skeleton.py` 与 `e2e/gobang.spec.js` 补充组件边界、按钮状态和重开路径验收。

## Blocker

- 无。

## Major

- 无。

## Minor

- 无。

## Question

- 无。

## Review Notes

- 第一轮 staged diff 只读审查：PASS；确认未跟踪的 `AGENTS.md` 与 `deploy.bat` 未纳入本次提交，未见旧 React/JS 源码或无关 staged 改动。
- 审查建议补强重开请求顺序断言；已在 Playwright 用例中记录 `requestOrder`，锁定 active session 重开顺序为 `start -> end -> start`。
- 第二轮 staged diff 复审：PASS；确认 `ControlPanel` 的开始、悔棋、结束禁用语义与原实现一致，`restartGame` 先 `end` 再 `start`。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`。
- `npm run test:e2e`：`7 passed`。
- `git diff --check` / `git diff --cached --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS。
