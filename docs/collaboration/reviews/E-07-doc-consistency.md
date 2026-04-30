# Review: E-07-doc-consistency

## Scope

- 核对 tracked 文档与当前工程事实是否一致。
- 覆盖 README、CLAUDE、TASKS、任务计划、package/Vite/Playwright 配置。
- 只读检查根目录未跟踪 `AGENTS.md`，记录它对当前代理上下文的影响，但不修改或提交。

## Findings Checked

- README 仍写 2026-04-28、Task 23.C 完成、下一步 D-01；已修正为 2026-04-30、Task 23.D 完成、Task 23.E 收敛中且下一步 E-07/E-08。
- README 仍把 `search_metrics` 指标列为 `prunes`；已修正为当前 API 和前端使用的 `beta_cutoffs`。
- README 痛点和后续计划仍围绕 D 阶段 UI 未开始；已修正为文档一致性、发布风险、CI、AI 收益评估和下一轮部署/比赛能力。
- CLAUDE、`package.json`、`playwright.config.js`、`vite.config.js` 的 Vite 端口和 Vue3/Vite 技术栈口径与当前代码一致。
- 未跟踪 `AGENTS.md` 仍含旧静态前端与 `4173` 示例；本轮只记录为本地指令风险，不把它作为 tracked 仓库事实提交。

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_skeleton.py -q`：`14 passed`。
- `git diff --check`：无空白错误（仅 CRLF 提示）。
- `Select-String` 确认 README 不再保留旧 D-01 当前状态、旧 `search_metrics` 指标字段或旧 `4173` 入口。

## Blocker

- 无。

## Major

- 无。

## Notes

- 本文件是本地确定性审查记录；当前环境未使用独立 subagent。
- 历史任务记录中的 `prunes` 保留为当时事实，不在 E-07 中批量重写。
- `AGENTS.md` 是未跟踪文件，若后续希望把它作为团队共享指令，需要单独决定是否纳入版本控制并对齐 Vue/Vite 口径。

## Verdict

- PASS，tracked 文档入口已对齐当前主线事实；剩余风险进入 E-08 发布前风险清单。
