# Task 13 审查报告: 运行时边界硬化

**分支**: `task/13-runtime-hardening`
**初始实现提交**: `7912523` fix: 强化运行时边界
**任务记录提交**: `e7ab758` docs: 记录 Task 13 实现提交
**审查时间**: 2026-04-26
**审查者**: Claude Code

---

## 审查范围

`main...task/13-runtime-hardening`，包含提交 `7912523` 和 `e7ab758`。

---

## 审查结论

整体方向正确，覆盖了上次整体审查中的主要运行时风险：会话 TTL/上限、CORS 配置、坐标校验、缓存 key、前端 busy 状态和非 JSON 错误处理。未发现必须阻塞合并的严重问题。

---

## Major

### 1. SessionStore 的锁只保护容器，不保护单局棋盘状态

`backend/app/game.py:42-51` 返回的是可变 `GameSession` 对象，之后 `backend/app/main.py:73-79` 会在锁外执行 `board.put()`、`play_ai_move()` 和 `snapshot()`。

这意味着同一个 `session_id` 的并发 `/move`、`/undo`、`/end` 仍可能交错修改同一个 `Board`。本任务声称“带锁 SessionStore 降低并发风险”，但初始实现只解决了 `sessions` 字典并发，不解决单局状态竞争。

建议：给 `GameSession` 增加 per-session lock，或在 `SessionStore` 提供 `with_session(session_id, fn)` 之类的原子操作接口，让 `move` / `undo` / `end` 在同一把锁下完成。

**Codex 处理**:

- 已给 `GameSession` 增加 per-session `RLock`。
- 已新增 `SessionStore.with_session(session_id, action, remove=False)`，在获取有效 session 后持有单局锁执行回调。
- 已将 `/move`、`/undo`、`/end` 改为通过 `with_session()` 完成读取、修改、快照生成；`/end` 使用 `remove=True` 在同一临界区内移除会话。
- 已新增测试覆盖同一 session 操作串行化，以及持锁移除会话。

---

## Minor

### 2. CORS README 描述与默认行为不完全一致

`README.md` 写“CORS 默认允许本地静态前端访问”，但 `backend/app/settings.py` 默认是 `*`，实际是允许所有来源。

**Codex 处理**: 已改为“开发模式下默认允许所有来源；部署时应通过 `GOBANG_CORS_ORIGINS` 收窄”。

### 3. SessionStore.create() 中嵌套获取同一把锁，当前可用但略显绕

`SessionStore.create()` 在持有 `_lock` 时调用 `prune_expired()`，后者再次获取 `_lock`。因为使用 `RLock` 不会死锁，但结构上增加了理解成本。

**Codex 处理**: 已提取 `_prune_expired_locked()`，由已持锁路径直接调用，避免内部重复加锁。

### 4. 前端 busy 状态测试偏字符串断言

`backend/tests/test_frontend_skeleton.py` 目前只检查 `"isBusy"`、`"setBusy(true)"` 等字符串，无法验证失败时是否恢复按钮、重复点击是否真的被拦截。

**Codex 处理**: 本任务暂不引入 JS 测试框架。该建议保留为后续前端测试增强项；当前 Python 静态检查继续作为低成本边界测试。

---

## 验证记录

- Claude Code 尝试运行 `python -m pytest -q "D:/Desktop/JOYland/林杯五子棋大赛/gobang-master/.worktrees/13-runtime-hardening/backend/tests"`，结果仍为 exit code 49 且无输出，和主分支此前现象一致，暂无法确认测试实际通过。
- Codex 使用项目约定的 Windows 命令 `py -m pytest backend\tests -q` 进行回归验证。
