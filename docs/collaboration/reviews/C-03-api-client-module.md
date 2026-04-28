# Review: C-03-api-client-module

## Scope

- 当前未提交 diff：`frontend/src/api/client.js`、`frontend/src/App.vue`、`backend/tests/test_frontend_skeleton.py`、`vite.config.js`、`playwright.config.js`、README、CLAUDE、`start.bat` 和协作文档。
- 验收重点：API client 封装 `health`、`startGame`、`playMove`、`undoMove`、`endGame`；`App.vue` 通过 client 调用 API；默认 API base、`?apiBase=` 覆盖、http(s) 校验和错误抛出行为保持有效；Vite、Playwright、文档和一键启动端口契约统一。

## Blocker

- 无。

## Major

- 无。

## Minor

- 无。

## Question

- 无。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`10 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`108 passed`。
- `npm run test:e2e`：`5 passed`。
- 中间一次 E2E 在旧 `4173` 端口等待 webServer 超时；统一到 `5173` 后复测通过。

## Verdict

- PASS。
