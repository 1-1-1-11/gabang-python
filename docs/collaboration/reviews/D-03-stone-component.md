# Review: D-03-stone-component

## Scope

- 新增 `frontend/src/components/Stone.vue`，封装黑白棋子与最后一步棋子标记。
- `frontend/src/components/Board.vue` 改为渲染 `Stone`，继续保留 `#board`、`.cell`、`data-row`、`data-col`、点击、禁用和最后一步格点 class。
- `frontend/src/styles.css` 增强黑白棋子体积感、阴影和最新落点视觉。
- `backend/tests/test_frontend_skeleton.py` 与 `e2e/gobang.spec.js` 补充 Stone 组件和浏览器主路径验收。

## Blocker

- 无。

## Major

- 无。

## Minor

- 无。

## Question

- 无。

## Review Notes

- 第一轮全工作区只读审查指出 `AGENTS.md` 与 `deploy.bat` 是未跟踪本地文件，且不属于 D-03 范围；本任务已明确不暂存、不提交这两个文件。
- 第二轮只读审查限定为 `git diff --cached` 后通过：暂存范围仅包含 D-03 的组件、样式、测试和台账状态文件；未发现 Board 行为回归。
- 最后一步现在同时具备 `.cell.is-latest`、`.stone.is-latest` 和 `.stone-latest-dot` 三层信号。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`。
- `npm run test:e2e`：`6 passed`。
- `git diff --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS。
