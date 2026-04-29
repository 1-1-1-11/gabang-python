# Review: D-09-error-banner

## Scope

- 新增 `frontend/src/components/ErrorBanner.vue`，用 `role="alert"` 展示 API/网络错误并支持关闭。
- `frontend/src/App.vue` 接入错误横幅。
- `frontend/src/composables/useGameState.js` 新增 `errorMessage`、`setError()`、`clearError()` 和 `dismissError()`；各 API action 在开始前清理旧错误，在 catch 中设置错误横幅并保留 status 文本。
- `frontend/src/styles.css` 增加错误横幅样式。
- `backend/tests/test_frontend_skeleton.py` 与 `e2e/gobang.spec.js` 补充组件边界、JSON 错误、非 JSON 错误和关闭横幅验收。

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
- 本地 staged diff 复核：`git diff --cached --name-only` 仅包含 D-09 范围文件；`git diff --cached --check` 无空白错误；未提交 `AGENTS.md`、`deploy.bat` 或 `.learnings`；未发现旧 React/JS 源码、后端/API 改动或无关 staged 改动。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`。
- `npm run test:e2e`：`9 passed`。
- `git diff --check` / `git diff --cached --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS，带记录边界：subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并如实留痕。
