# Review: B-06-local-candidate-points

## Scope

审查了当前 diff 中的：

- `backend/app/evaluation.py`
- `backend/tests/test_ai_search.py`
- `backend/tests/test_ai_benchmark.py`
- `docs/collaboration/TASKS.md`

只读检查了 `git diff`、`git diff --check`、相关调用链 `Board.get_valuable_moves()` / `minmax()`。未运行 pytest，避免只读审查产生缓存文件。

## Blocker

无。

## Major

无。

## Minor

无影响验收的问题。

边界细节：`candidate_moves` 仍是 `minmax.py` 中返回走法数量的累计，不是 `_candidate_points()` 的内部扫描池；本次 benchmark 证据主要应看 `TASKS.md` 记录的中盘耗时约 `0.30s` 相比 B-06 前约 `0.42s` 的改善。

## Question

无。

## Verdict

PASS
