# Review: B-07-move-ordering

## Scope

- 审查 `backend/app/evaluation.py` 的走法排序增强。
- 审查 `backend/tests/test_ai_search.py` 的新增排序与早剪枝测试。
- 确认本任务未引入缓存 bound 语义、时间预算或前端改动。

## Blocker

- 无。

## Major

- 无。

## Minor

- `backend/tests/test_ai_search.py` 中新增测试断言 `search_metrics["nodes"] == 2` 和 `search_metrics["prunes"] == 1`，能锁住本次早剪枝收益，但属于实现细节断言。后续如果搜索统计、缓存命中路径或等价剪枝策略调整，可能出现战术正确但测试失败；当前不阻塞。

## Question

- 无。

## Verdict

- PASS。

## Validation

```text
.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_search.py -q
28 passed

.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_benchmark.py -q
5 passed

.\.venv\Scripts\python.exe -m pytest backend\tests -q
107 passed
```

## Notes

- subagent 结论：当前 diff 只增强 `backend/app/evaluation.py` 的走法排序和相关 AI 搜索测试，未引入缓存 bound、时间预算或前端改动。
- 排序逻辑会把己方立即胜排在防守阻断前，同时仍保留必须防候选；候选集合没有被放宽到全盘扫描。
- `MOVE_ORDER_SHAPE_SCORE` 是独立排序权重，不改变 `evaluate()` 分值，有利于把搜索顺序优化和棋形估值策略分开演进。
