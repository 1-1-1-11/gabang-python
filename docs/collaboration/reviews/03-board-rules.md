# Task 3 审查报告: 棋盘规则迁移

**分支**: `task/03-board-rules`
**Commit**: `8fc9fe3` feat: 迁移五子棋棋盘规则到 Python
**审查时间**: 2026-04-25
**审查者**: Claude Code

---

## 整体评估

代码迁移思路正确，Python 版 Board 类基本保留了原 JS 的逻辑结构。但存在 **2 个 blocker 问题** 和若干质量问题，必须修复后才能合并。

---

## Blocker (阻塞问题，必须修复)

### 1. board.py 存在方法重复定义

**位置**: `backend/app/board.py` 行 29-50 与行 51-78 完全重复

整个 Board 类的后半部分（从 `get_valid_moves` 到 `_is_inside`）被定义了两次。Python 后定义的方法会覆盖先定义的，但在如此短的文件中出现大段重复代码极难维护，且容易在后续修改时出错。

**处理**: 删除行 51-78 的重复代码

---

### 2. test_board.py 存在语法错误，测试无法运行

**位置**: `backend/tests/test_board.py` WINS 列表

WINS 列表中有多处列表缺少前括号 `[`：
- 第 30 行: `0, 1, 6, 2, 12, 3, 18, 4, 24], 1),` → 缺失 `[`
- 第 32 行: `5, [0, 1, 6, 2, 12, 3, 19, 4, 24], 0),` → 缺失 `[`
- 第 37 行: `5, [4, 0, 8, 1, 12, 2, 16, 3, 20], 1),` → 缺失 `[`
- 第 39 行: `5, [4, 0, 8, 1, 12, 2, 16, 20], 0),` → 缺失 `[`

这会导致 `moves` 被解析为 `int` 而非 `list`，参数化测试全部失败。

**处理**: 修复 WINS 列表语法

---

## Major (重要问题，建议修复)

### 1. `is_game_over()` 逻辑顺序

当前先检查胜者再检查平局，语义上可以优化，但结果正确。建议明确逻辑意图。

### 2. `undo()` 恢复 current_player 的假设

通过 `move["role"]` 恢复玩家状态依赖于"每步切换玩家"的规则。建议添加注释说明此假设。

---

## Minor (小问题，可选修复)

1. `coordinate_to_position` 类型注解 `list[int] | tuple[int, int]` 可改为 `Sequence[int]`
2. WINS 列表可读性差，缺乏注释说明每个测试场景

---

## Question (疑问)

WINS 列表中某些预期 winner 需要确认是否与预期一致（如行 30、32）。

---

## 结论

**不可以合并**

| 问题类型 | 数量 | 状态 |
|---------|------|------|
| **Blocker** | 2 | 必须修复 |
| **Major** | 2 | 建议修复 |
| **Minor** | 2 | 可选 |

---

## 必须修复项

1. **删除** `backend/app/board.py` 中重复的方法定义（行 51-78）
2. **修复** `backend/tests/test_board.py` 中 WINS 列表的语法错误

---

## 验证方法

修复后运行：
```bash
pytest backend/tests/test_board.py -v
```

确保所有测试通过。

---

## Codex 处理记录

- Blocker 1：不成立。已核对 `backend/app/board.py`，文件只有 78 行，`get_valid_moves` 到 `_is_inside` 只定义一次；`git diff main...HEAD -- backend/app/board.py` 也显示无重复块。
- Blocker 2：不成立。已核对 `backend/tests/test_board.py`，WINS 列表每个元组均为 `(size, moves, winner)`，`moves` 均为列表。执行 `py -m pytest backend\tests\test_board.py -v`，结果为 `22 passed`。
- Major 1：不修改行为。当前 `is_game_over()` 先判胜再判满盘，和 JS 实现一致，且语义正确。
- Major 2：已处理。`undo()` 增加注释，说明通过最后一步的 `role` 恢复当前玩家。
- Minor 1：已处理。`coordinate_to_position()` 的类型注解改为 `Sequence[int]`。
- Minor 2 / Question：WINS 数据来自原 JS `src/ai/board_manuls.js`，本任务目标是等价迁移现有规则测试；后续若要改善夹具可读性，可在测试重构任务中单独处理。
