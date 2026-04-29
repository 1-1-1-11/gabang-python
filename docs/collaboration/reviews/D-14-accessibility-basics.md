# Review: D-14-accessibility-basics

## Scope

- `frontend/src/components/Board.vue` 为棋盘格补充中文 accessible name、`aria-disabled` 和棋盘 `aria-busy`。
- `frontend/src/components/ControlPanel.vue` 为开始、悔棋、结束按钮补充明确 `aria-label`。
- `frontend/src/App.vue` 为状态 pill 补充 `aria-live="polite"`。
- `e2e/gobang.spec.js` 新增键盘焦点和 accessible name 验收，覆盖状态、棋盘、棋盘格、控制按钮、Tab 焦点环和落子后的棋盘格标签。
- `backend/tests/test_frontend_skeleton.py` 补充可访问性基础契约测试。
- `docs/collaboration/TASKS.md` 标记 D-14 进行中。

## Blocker

- 无。

## Major

- 无。

## Minor

- 无。

## Question

- 无。

## Review Notes

- 子代理额度仍不可用，本轮未声称独立 subagent 复审完成。
- 本地 staged diff 复核：`git diff --cached --name-only` 仅包含 D-14 范围文件；`git diff --cached --check` 无空白错误；未提交 `AGENTS.md`、`deploy.bat` 或 `.learnings`；未发现旧 React/JS 源码、后端/API 改动或无关 staged 改动。
- 行为边界：D-14 是基础可访问性增强，不引入 axe 依赖，不改变 API 或游戏规则。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`14 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`112 passed`。
- `npm run test:e2e`：`12 passed`。
- `git diff --check` / `git diff --cached --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS，带记录边界：subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并如实留痕。
