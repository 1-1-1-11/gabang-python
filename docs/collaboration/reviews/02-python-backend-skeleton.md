# Task 2 审查报告: Python 后端骨架

**分支**: `task/02-python-backend-skeleton`
**Commit**: `5e7a596` chore: 初始化 Python 后端项目结构
**审查时间**: 2026-04-25
**审查者**: Claude Code

---

## 整体评估

这是一个符合预期的 Python 后端骨架实现。代码结构清晰，目录划分合理（backend/app/ + backend/tests/），FastAPI 入口最小化，依赖版本全部锁定。作为"骨架"阶段的第一个 commit，功能完整且可以运行。

---

## Blocker (阻塞问题，必须修复)

**无**

---

## Major (重要问题，建议修复)

### 1. 依赖管理不一致
- `backend/requirements.lock.txt` 和 `pyproject.toml` 中依赖重复定义
- `httpx` 仅出现在 `requirements.lock.txt`，不在 `pyproject.toml` 的 dependencies 中
- **建议**: 统一使用 `pyproject.toml` 作为单一依赖来源，`requirements.lock.txt` 应通过 `pip freeze` 生成或删除

### 2. 健康检查端点过于基础
- 当前 `/api/health` 只返回静态 JSON
- **建议**: 预留检查扩展能力（注释说明未来可扩展数据库/缓存检查）

### 3. `health_check()` 函数缺少文档和类型注解
```python
# 当前
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# 建议
@app.get("/api/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
```

---

## Minor (小问题，可选修复)

1. **`__init__.py` 空文件** - 可接受，可添加包描述

2. **pyproject.toml 缺少 Python 版本上界** - `requires-python = ">=3.12"` 建议添加 `<3.14`

3. **无 TODO 标记** - 可添加注释指引后续开发方向

---

## Question (疑问)

1. **CORS 配置**: 后续 FastAPI 接口是否会供前端调用？若是，建议预留 CORS 中间件
2. **日志**: 是否需要日志框架？当前无日志记录
3. **API 版本策略**: `/api/health` 是否有意作为 v1？

---

## 结论

**可以合并**，建议处理 Major 问题后再合并。主要问题是依赖管理不一致，建议统一依赖来源。

---

## 处理结果

| 问题类型 | 数量 | 处理方式 |
|---------|------|---------|
| Blocker | 0 | - |
| Major | 3 | Codex 选择处理 / 暂不处理 |
| Minor | 3 | 可选 |
| Question | 3 | 需明确 |

## Codex 处理记录

- Major 1：部分采纳。`httpx` 已存在于 `pyproject.toml` 的 `dev` optional dependencies 中；保留 `requirements.lock.txt` 是原计划要求。已在 lock 文件中标明它当前锁定 Task 2 bootstrap 的直接运行与测试依赖。
- Major 2：不扩展 health check 行为。当前阶段没有数据库、缓存或外部依赖，添加伪检查会制造未使用接口。
- Major 3：已处理。`health_check()` 增加返回类型、docstring 和 `system` tag。
- Minor 2：已处理。`requires-python` 改为 `>=3.12,<3.14`，与当前可用 Python 3.13 兼容。
- Questions：CORS 在 Task 7 前端接入 API 时处理；日志在出现业务接口和错误路径后处理；当前 API 不引入 `/v1` 前缀，沿用计划中的 `/api/*`。
