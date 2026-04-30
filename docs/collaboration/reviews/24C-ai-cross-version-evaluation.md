# Review: 24C-ai-cross-version-evaluation

## Scope

- 对比 `d37ac32` 前后同一批固定局面搜索指标。
- 旧基线：`832702751a1f2226b4f642d1865e4d8c1c407546`，即 `d37ac32` 的父提交。
- 当前：`5d7933d70ad6a29a352ef40030c6c0f9ef33922c`。
- 旧指标 `prunes` 在表中统一记为当前口径 `beta_cutoffs`。

## Comparison

| Case | Move before -> after | Nodes before -> after | beta_cutoffs before -> after | cache_hits before -> after | candidate_moves before -> after | max_depth before -> after | elapsed_ms before -> after |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| opening_center | `[4, 4]` -> `[4, 4]` | 114 -> 134 | 13 -> 13 | 0 -> 0 | 313 -> 331 | 3 -> 3 | 97.1 -> 195.7 |
| diagonal_immediate_win | `[4, 4]` -> `[4, 4]` | 2 -> 2 | 1 -> 1 | 0 -> 0 | 2 -> 2 | 1 -> 1 | 0.9 -> 1.0 |
| horizontal_must_block | `[2, 5]` -> `[2, 5]` | 82 -> 344 | 19 -> 34 | 0 -> 0 | 421 -> 591 | 3 -> 4 | 103.3 -> 549.5 |
| simple_threat_sequence | `[4, 1]` -> `[4, 1]` | 6 -> 21 | 3 -> 7 | 0 -> 0 | 10 -> 30 | 3 -> 3 | 4.2 -> 20.8 |
| midgame_search_budget | `[5, 5]` -> `[3, 3]` | 393 -> 1154 | 25 -> 357 | 0 -> 10 | 673 -> 2492 | 3 -> 4 | 600.0 -> 1800.4 |

## Interpretation

- Tactical correctness held for the locked cases: immediate win, must-block, simple threat and opening center kept expected moves.
- The current search explores deeper in the must-block and midgame cases (`max_depth` 4 instead of 3), consistent with quiescence search.
- `beta_cutoffs` increased substantially in midgame, indicating more alpha-beta cutoffs during the deeper search.
- Runtime and node counts increased on non-terminal cases; `d37ac32` should not be described as a speed optimization.
- The midgame move changed from `[5, 5]` to `[3, 3]`; this needs future chess-strength evaluation before being called better or worse.

## Verification

- Baseline collected in temporary detached worktree `.worktrees/24c-pre-d37ac32` at `8327027`, then removed after sampling.
- Current collected on main at `5d7933d`.
- Same inline script and same fixed position definitions were used in both worktrees.

## Blocker

- 无。

## Major

- 无。

## Notes

- 本文件是本地确定性审查记录；当前环境未使用独立 subagent。
- Timing is a local reference only. The strongest signal is selected move, search depth, nodes, candidate count, cache hits and beta cutoffs.
- This comparison supports “deeper/more instrumented search” rather than “faster search” or “proven stronger play.”

## Verdict

- PASS。24-C gives a cross-version baseline and corrects the risk wording: `d37ac32` preserved key tactical moves while increasing search work on deeper positions.
