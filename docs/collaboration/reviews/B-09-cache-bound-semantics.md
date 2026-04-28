# Review: B-09-cache-bound-semantics

## Scope

- 审查 `backend/app/minmax.py` 的缓存条目 bound 语义。
- 审查 `backend/tests/test_ai_search.py` 中缓存 bound 写入和读取窗口规则测试。
- 确认本任务未引入时间预算、节点预算、前端改动、候选点生成改动或 `Board` / `Evaluate` 行为改动。

## Blocker

- 无。

## Major

- 首轮审查发现 fail-low 结果仍可能写成 `exact`，该问题已修复：当前 `_cache_bound(value, alpha_start, beta)` 会把 `value <= alpha_start` 标为 `upper`，把 `value >= beta` 标为 `lower`，其余标为 `exact`。

## Minor

- `FIVE` 早停依赖“`FIVE` 是终局胜利上限”的项目假设；已在代码注释和测试中明确该 invariant。

## Question

- 无。

## Verdict

- PASS。

## Validation

```text
.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q
29 passed

.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q
5 passed

.\.venv\Scripts\python.exe -m pytest backend\tests -q
108 passed
```

## Notes

- B-09 最小实现新增 `CacheEntry` 和 `CacheBound`，使缓存条目显式标记为 `exact`、`lower` 或 `upper`。
- `_cached_result()` 只在当前 alpha-beta 窗口允许时复用 lower/upper bound；exact 条目保持直接复用。
- 本轮不扩展迭代加深、aspiration window、节点预算或时间预算；这些保留给 B-10 或后续任务。
