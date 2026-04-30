# Review: 24B-ai-benefit-evaluation

## Scope

- 为 `d37ac32` 后的当前 AI 搜索建立固定局面评估基线。
- 覆盖开局、立即胜、必须防、简单威胁和中盘搜索预算。
- 记录 `nodes`、`beta_cutoffs`、`cache_hits`、`cache_stores`、`candidate_moves`、`leaf_nodes`、`max_depth`、选点和本机参考耗时。

## Fixed Position Results

| Case | Depth | Value | Move | Nodes | beta_cutoffs | cache_hits | cache_stores | candidate_moves | leaf_nodes | max_depth | elapsed_ms |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| opening_center | 3 | 540 | `[4, 4]` | 134 | 13 | 0 | 21 | 331 | 113 | 3 | 222.2 |
| diagonal_immediate_win | 4 | 10000000 | `[4, 4]` | 2 | 1 | 0 | 1 | 2 | 1 | 1 | 1.7 |
| horizontal_must_block | 3 | -160 | `[2, 5]` | 344 | 34 | 0 | 83 | 591 | 261 | 4 | 597.2 |
| simple_threat_sequence | 3 | 10000000 | `[4, 1]` | 21 | 7 | 0 | 11 | 30 | 10 | 3 | 21.9 |
| midgame_search_budget | 3 | 2720 | `[3, 3]` | 1154 | 357 | 10 | 476 | 2492 | 668 | 4 | 1998.0 |

## Checked Items

- `backend/tests/test_ai_quality_evaluation.py` locks tactical moves for immediate win, must-block, opening center and simple threat cases.
- The midgame case verifies legal move selection, bounded node/candidate growth and substantial beta cutoffs without hard-coding a tactical claim.
- The repeated midgame search verifies that the current cache path produces `search_metrics.cache_hits > 0`.
- Timing is recorded in this review as a reference only; tests intentionally avoid elapsed-time assertions.

## Verification

- `.\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_quality_evaluation.py -q`：`2 passed`。
- `.\.venv\Scripts\python.exe -m pytest backend\tests -q`：`115 passed`。
- `npm run build`：通过。
- `npm run test:e2e`：首轮 webServer 30 秒超时；端口检查无活跃占用后立即重跑，`12 passed`。
- `git diff --check`：无空白错误（仅 CRLF 提示）。
- 本机 metrics 采样脚本复用同一批 `QUALITY_CASES`，输出上表。

## Blocker

- 无。

## Major

- 无。

## Notes

- 本文件是本地确定性审查记录；当前环境未使用独立 subagent。
- 24-B 建立的是当前 post-`d37ac32` 行为基线，不证明相对旧提交的棋力收益。
- 若后续要证明“棋力提升”，需要跨提交或固定版本基线对比，并增加更多中盘/终局局面。

## Verdict

- PASS。24-B 已把当前 AI 搜索行为转成可复测固定局面基线，适合作为后续预算、置换表或棋力评估任务的起点。
