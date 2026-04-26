# Task 13 审查报告: 运行时边界硬化

**分支**: `task/13-runtime-hardening`
**Commit**: `7912523` fix: 强化运行时边界
**审查时间**: 待 Claude Code 填写
**审查者**: Claude Code

---

## 审查来源

Claude 项目整体审查指出：当前项目适合作为早期骨架，但进入长期运行或多人使用阶段前，需要优先处理会话状态、并发安全、输入边界、CORS 和 AI 搜索缓存风险。

---

## 待审查范围

- `backend/app/game.py`
- `backend/app/main.py`
- `backend/app/schemas.py`
- `backend/app/settings.py`
- `backend/app/cache.py`
- `backend/app/minmax.py`
- `backend/tests/test_runtime_hardening.py`
- `backend/tests/test_frontend_skeleton.py`
- `frontend/app.js`
- `frontend/styles.css`
- `README.md`
- `docs/collaboration/TASKS.md`

---

## Codex 处理摘要

- 已处理高优先级 1：新增带锁 `SessionStore`，支持最大 session 数和 TTL 过期清理。
- 已处理高优先级 2：CORS 来源改为 `GOBANG_CORS_ORIGINS` 环境变量配置，默认保留本地开发所需的 `*`。
- 已处理高优先级 3：`MoveRequest.position` 增加非负校验；会话棋盘尺寸范围由 API 层返回明确 `400`。
- 已处理高优先级 4：搜索缓存 key 加入 `board.size`；默认缓存容量从 `1_000_000` 降为 `100_000`。
- 已处理中优先级 7：前端请求改为先读文本再解析 JSON，非 JSON 响应显示“响应格式错误”。
- 已处理中优先级 8：前端新增 `isBusy`，请求期间禁用按钮和棋盘，降低重复点击风险。
- 暂未处理中优先级 5/6：`enable_vct` 与 SearchResult 类型化会改变搜索接口，建议后续单独任务处理。
- 暂未处理中优先级 9：前端 API 地址部署策略需要结合实际部署方式决定，当前保留本地演示默认值。
- 低优先级建议暂不处理，避免在硬化任务中引入大重构。

---

## Blocker

待 Claude Code 审查。

## Major

待 Claude Code 审查。

## Minor

待 Claude Code 审查。

## Question

待 Claude Code 审查。

---

## Codex 处理记录

待 Claude Code 审查结束后填写。
