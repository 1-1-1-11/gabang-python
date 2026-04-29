# Review: D-05-difficulty-select

## Scope

- 新增 `frontend/src/components/DifficultySelect.vue`，提供简单、普通、困难、自定义四个难度选项。
- `frontend/src/App.vue` 将原深度输入替换为 `DifficultySelect`。
- `frontend/src/composables/useGameState.js` 新增 `settings.difficulty`，默认普通难度；开始、重开和落子仍只使用现有 `depth`。
- `frontend/src/styles.css` 增加难度分段按钮与自定义深度输入样式。
- `backend/tests/test_frontend_skeleton.py` 与 `e2e/gobang.spec.js` 补充难度组件边界、payload depth 映射和自定义深度验收。

## Blocker

- 无。

## Major

- 无。

## Minor

- 无。

## Question

- 无。

## Review Notes

- staged diff 只读审查：PASS。
- `settings.difficulty` 仅为前端 UI 状态；`frontend/src/api/client.js` 仍只发送 `size`、`ai_first`、`depth`。
- 简单/普通/困难分别映射到现有后端 `depth=2/4/6`，未新增预算参数、后端 schema 或 API 字段。
- 默认普通难度下 `#search-depth-input` 不渲染，只有选择自定义时出现。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`。
- `npm run test:e2e`：`8 passed`。
- `git diff --check` / `git diff --cached --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS。
