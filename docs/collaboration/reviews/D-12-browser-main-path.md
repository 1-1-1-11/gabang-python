# Review: D-12-browser-main-path

## Scope

- `e2e/gobang.spec.js` 在真实主路径测试中记录非 OPTIONS 的 `/api/games` 请求，显式断言 start、move、undo、end 四个业务 API 顺序。
- `backend/tests/test_frontend_skeleton.py` 新增 Playwright 主路径契约测试，锁定 API 调用链断言存在。
- `docs/collaboration/TASKS.md` 标记 D-12 进行中。

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
- 本地 staged diff 复核：`git diff --cached --name-only` 仅包含 D-12 范围文件；`git diff --cached --check` 无空白错误；未提交 `AGENTS.md`、`deploy.bat` 或 `.learnings`；未发现旧 React/JS 源码、后端/API 改动或无关 staged 改动。
- 行为边界：主路径继续使用真实后端与 Vite dev server；只过滤 CORS 预检 OPTIONS，不 mock start/move/undo/end。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`12 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`110 passed`。
- `npm run test:e2e`：`10 passed`。
- `git diff --check` / `git diff --cached --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS，带记录边界：subagent review 因当前 usage limit 不可用，已用本地可重复门禁替代并如实留痕。
