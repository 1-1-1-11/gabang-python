# Task 5 审查报告: FastAPI 游戏接口

**分支**: `task/05-game-api`
**Commit**: `b617be4` feat: 添加 FastAPI 游戏接口
**审查时间**: 2026-04-25
**审查者**: Claude Code

---

## 整体评估

代码实现了基本的 FastAPI 游戏接口，功能完整，测试覆盖核心场景。API 设计遵循 RESTful 约定，session 管理使用内存存储。无阻塞问题。

---

## Blocker (阻塞问题，必须修复)

**无**

---

## Major (重要问题，建议修复)

### 1. `end_game` 语义问题

**位置**: `backend/app/main.py` 第 67-73 行

```python
def end_game(session_id: Annotated[str, Path(min_length=1)]) -> dict:
    session = remove_session(session_id)  # 先删除
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found.")
    return snapshot(session_id, session)  # 后返回 snapshot
```

**问题**: "删除后再使用"语义容易引起误解。建议重构为先检查存在性，再删除，最后返回。

---

### 2. `undo_move` 没有验证 history 长度

**位置**: `backend/app/main.py` 第 52-64 行

**问题**: 当 history 只有 1 步时（例如 `ai_first=True` 的开局），连续调用两次 `undo()` 会导致第二次无效。建议添加验证或说明边界行为。

---

### 3. Session 存储无内存保护机制

**位置**: `backend/app/game.py` 第 18 行

```python
sessions: dict[str, GameSession] = {}
```

**问题**: 无 TTL 或最大数量限制，长期运行的服务器可能内存耗尽。建议添加基于时间的过期机制或最大 session 数量限制。

---

## Minor (小问题，可选修复)

1. `GameSession.last_best_path` 类型不一致（定义 `None`，初始化 `[]`）
2. `play_ai_move` 返回值被忽略
3. 响应类型标注为 `dict` 不够精确，建议使用 Pydantic Response Model
4. `make_move` 未处理游戏已结束的情况

---

## Question (疑问)

1. **`best_path` 对前端如何使用？** 需要文档说明
2. **`undo` 边界行为是否预期？** AI 先手开局只有 1 步历史，undo 两次会无效

---

## 结论

**可以合并**

| 问题类型 | 数量 | 状态 |
|---------|------|------|
| **Blocker** | 0 | - |
| **Major** | 3 | 建议修复 |
| **Minor** | 4 | 可选 |

---

## Codex 处理记录

- Major 1：已处理。`end_game()` 改为先 `get_session()` 检查存在性，生成响应快照后再 `remove_session()`，避免“删除后再使用”的阅读歧义。
- Major 2：已处理。`undo_move()` 改为按 `min(2, len(history))` 撤销，明确支持 AI 先手只有 1 步历史的边界；新增 `test_undo_reverts_single_ai_first_move`。
- Major 3：已处理。新增 `MAX_SESSIONS = 256`，创建新会话时超过上限会淘汰最早的 session；新增 `test_start_evicts_oldest_session_when_limit_is_reached`。
- Minor 1：已处理。`GameSession.last_best_path` 改为 `field(default_factory=list)`，类型始终为 `list[list[int]]`。
- Minor 2：暂不处理。当前调用点不需要区分 AI 无可落子与游戏终局；`play_ai_move()` 已在 session 状态中记录搜索结果。
- Minor 3：暂不处理。Response Model 会带来一批结构定义，当前阶段先保持最小 API 面；后续接口稳定后再补。
- Minor 4：已处理。`make_move()` 在玩家落子前检查 `board.is_game_over()`，已结束棋局返回 `400`；新增 `test_move_rejects_finished_game`。
- Question 1：`best_path` 当前作为 AI 搜索路径调试/可视化字段返回，前端语义文档留到后续 API 文档任务补充。
- Question 2：已用单步撤销测试固定边界行为：AI 先手开局只有 1 步历史时，undo 撤销这一手并返回空棋盘。
