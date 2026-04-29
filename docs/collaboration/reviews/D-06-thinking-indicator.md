# Review: D-06-thinking-indicator

## Scope

- 新增 `frontend/src/components/ThinkingIndicator.vue`，显示 AI 待命/思考中状态，以及最近搜索的耗时、节点和剪枝指标。
- `frontend/src/App.vue` 接入 `ThinkingIndicator`，只使用已有 `state.isBusy`、`state.status` 与 `state.searchMetrics`。
- `frontend/src/composables/useGameState.js` 调整 AI 先手开局状态：`aiFirst` 时启动阶段显示 `AI 思考`，普通开局仍显示 `连接中`。
- `frontend/src/styles.css` 增加思考状态与指标样式。
- `backend/tests/test_frontend_skeleton.py` 与 `e2e/gobang.spec.js` 补充组件边界、占位、AI move pending、AI-first start pending 和搜索指标验收。

## Blocker

- 无。

## Major

- 无。

## Minor

- 无。

## Question

- 初审 Question：`AI 先手` 开局时 `/start` 也可能触发 AI 搜索；若产品定义包含该场景，应补断言。
- 处理结果：已处理。`startGame()` 在 `state.settings.aiFirst` 为真时显示 `AI 思考`；Playwright 已断言 AI 先手启动 pending 期间 `ThinkingIndicator` 显示 `AI 思考中`。

## Review Notes

- 第一轮 staged diff 只读审查：PASS；指出上面的 AI 先手 Question。
- Question 处理后尝试进行第二轮 subagent 复审，但子代理因 Codex usage limit 失败，未返回独立复审结论。
- 因用户要求继续自动推进，本轮采用明确记录的本地门禁复核：`git diff --cached --name-only` 仅包含 D-06 范围文件；`git diff --cached --check` 无空白错误；未提交 `AGENTS.md`、`deploy.bat` 或 `.learnings`；未发现旧 React/JS 源码、后端/API 改动或 D-08 SearchInfo 提前实现。
- 边界保留：本文件不声称 Question 处理后的第二轮独立 subagent 复审已经完成；若额度恢复，可后续补一个只读复审。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`11 passed`。
- `npm run build`：通过。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`109 passed`。
- `npm run test:e2e`：`9 passed`。
- `git diff --check` / `git diff --cached --check`：无空白错误，仅 CRLF 工作区提示。

## Verdict

- PASS，带记录边界：第二轮 subagent 复审因 usage limit 不可用，已用本地可重复门禁替代并如实留痕。
