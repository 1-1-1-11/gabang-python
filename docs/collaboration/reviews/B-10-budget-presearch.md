# Review: B-10-budget-presearch

## Blocker

- 无。

## Major

- 初审指出当前 tracked diff 还包含 `start.bat`，不属于 B-10 范围；处理方式是本轮只暂存并提交 `docs/collaboration/任务计划.md`、`docs/collaboration/TASKS.md` 和本审查文件，`start.bat` 保留在工作区，留给独立任务。
- 初审指出台账已引用本审查文件但文件尚不存在；已保存为 `docs/collaboration/reviews/B-10-budget-presearch.md`。

## Minor

- B-10 预研内容覆盖请求字段现状 `depth`、未来 `node_limit`；响应字段现状 `score` / `best_path` / `current_depth`、未来 metrics / limited / reason；搜索语义说明了同步完整深度搜索与 deadline 的冲突；测试影响列到了 schema、game、API、README 和 AI 测试。

## Question

- `SearchMetricsSnapshot` 应作为 D-08 前置后端任务单独插入，建议任务 ID 为 `C-09`，在 Vue API client 和状态管理稳定后、D-08 搜索信息展示前执行。

## Verdict

- PASS。

## Notes

- B-10 是文档预研任务，不改后端代码、不改 API、不改前端。
- 下一步推进到 C-02 Vue3 + Vite 前端架构初始化。
