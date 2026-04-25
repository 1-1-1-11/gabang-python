# Task 4 审查报告: 评分与搜索迁移

**分支**: `task/04-ai-search`
**Commit**: `81e5a5b` feat: 迁移五子棋 AI 搜索逻辑
**审查时间**: 2026-04-25
**审查者**: Claude Code

---

## 整体评估

此次迁移涉及 Zobrist 哈希、棋形识别、评估函数和极大极小搜索算法四个核心模块。代码结构清晰，模块职责划分合理，但存在 **3 个 Blocker 问题**导致代码无法正常运行，以及若干逻辑不一致需要修正。

---

## Blocker (阻塞问题，必须修复)

### 1. `minmax.py` vct/vcf 调用参数顺序错误

**位置**: `backend/app/minmax.py` 第 12-13 行

```python
def vct(board, role: int, depth: int = 8):
    return _search(board, role, depth, 0, [], -MAX, MAX, only_three=True)
```

`_search` 签名：
```python
def _search(board, role: int, depth: int, current_depth: int, ...)
```

**问题**: `depth` 被传入了 `current_depth` 参数位置，导致搜索深度始终为 0。

**修复**: 确认参数顺序是否应为 `_search(board, role, depth, 0, [], -MAX, MAX, only_three=True)`

---

### 2. `evaluation.py` SHAPE_SCORE 映射严重错误

**位置**: `backend/app/evaluation.py` 第 16-24 行

```python
SHAPE_SCORE = {
    Shape.FIVE: FOUR,
    Shape.BLOCK_FIVE: BLOCK_FOUR,
    Shape.FOUR: THREE,
    ...
}
```

**问题**:
- `Shape.FIVE` 应为最高分，但被映射到 100_000
- `Shape.BLOCK_FIVE`（对手已五连）被映射到最低分 1_500，这会导致 AI 无法正确识别需要立即阻挡的威胁

**修复**: 重新检查 SHAPE_SCORE 映射是否符合原 JS 逻辑

---

### 3. `minmax.py` best_path 初始化使用未定义变量

**位置**: `backend/app/minmax.py` 第 30-31 行

```python
value = -MAX
best_move = moves[0]
best_path = path + [best_move]
```

**问题**: `best_path` 初始化使用了 `best_move`，但 `best_move` 在此时已定义。如果后续循环没有更新 `best_move`，返回的路径可能不正确。

**修复**: 将 `best_path = path + [best_move]` 移到循环内更新 `best_move` 的条件下

---

## Major (重要问题，建议修复)

### 4. alpha-beta 裁剪逻辑疑问

**位置**: `backend/app/minmax.py` 第 35 行

```python
current_value, _, current_path = _search(board, -role, depth, current_depth + 1, path + [move], -beta, -alpha, ...)
```

递归返回后 beta/alpha 的更新逻辑可能不完整。

### 5. get_shape_fast 的 contiguous 值被忽略

`get_shape_fast` 返回的第二个值 `contiguous` 在评估中未被使用。

### 6. board.hash() 和 Cache 类未被使用

Zobrist 哈希和缓存功能未被集成到搜索算法中。

---

## Minor (小问题，可选修复)

### 7. Cache 类未使用

### 8. BLOCK_FIVE 常量定义与使用不一致

### 9. current_path 被忽略

---

## Question (疑问)

1. `_role_score` 只评估空位但遍历整个棋盘，效率较低
2. `_point_groups` 同时评估己方和对方，这与 `_role_score` 只评估单方不一致，是否预期行为？

---

## 结论

**不可以合并**

| 问题类型 | 数量 | 状态 |
|---------|------|------|
| **Blocker** | 3 | 必须修复 |
| **Major** | 3 | 建议修复 |
| **Minor** | 3 | 可选 |

---

## 必须修复项

1. **minmax.py**: 修复 vct/vcf 参数顺序
2. **evaluation.py**: 修复 SHAPE_SCORE 映射
3. **minmax.py**: 修复 best_path 初始化逻辑

---

## 验证方法

修复后运行：
```bash
pytest backend/tests/test_ai_search.py -v
```

建议增加 VCT/VCF 测试用例。

---

## Codex 处理记录

- Blocker 1：不成立。`vct()`/`vcf()` 已按 `_search(board, role, depth, current_depth, ...)` 传参，第三个位置是 `depth`，第四个位置是 `0`。已补充 VCT/VCF 一步胜测试防止回归。
- Blocker 2：不按建议改为终局分。原 JS 的 `getRealShapeScore()` 对“空位候选点”就是 `FIVE -> FOUR`、`BLOCK_FIVE -> BLOCK_FOUR`；真正的终局胜负分在 `Board.evaluate()` 中返回 `FIVE * winner * role`。已将 `SHAPE_SCORE` 改名为 `CANDIDATE_SHAPE_SCORE` 并添加注释，避免语义误读。
- Blocker 3：部分采纳。原代码没有未定义变量，但初始化路径确实容易误读；已改为只在循环内更新 `best_move` 和 `best_path`。
- Major 4：保留当前 negamax alpha-beta 结构，现有一步胜和开局非必胜测试覆盖基本行为。
- Major 5：不处理。`contiguous` 是与 JS 函数签名兼容的辅助返回值，当前评估不需要直接使用。
- Major 6 / Minor 7：已处理。`minmax` 接入基于 `board.hash()` 的缓存，并新增重复搜索命中测试。
- Minor 8：保留。`BLOCK_FIVE = FIVE` 作为终局常量，候选点分值由 `CANDIDATE_SHAPE_SCORE` 单独表达。
- Minor 9：已通过 best path 更新逻辑调整处理。
- Question 1：当前第一阶段优先等价迁移和可测性，性能优化留到后续。
- Question 2：预期行为。`_point_groups()` 同时纳入己方进攻点和对方防守点，用于候选点生成；`_role_score()` 单方评分用于局面评估。
