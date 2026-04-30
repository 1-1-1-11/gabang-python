# Review: E-08-release-risk-checklist

## Scope

- 汇总 MVP 发布前风险清单。
- 明确哪些能力可以进入本地 MVP 演示，哪些不能作为生产、多实例、比赛或棋力收益承诺。
- 给下一轮任务拆分提供直接入口。

## Checked Items

- 风险清单覆盖本地 MVP 可演示范围：后端 API/规则/会话、Vue3/Vite 前端、当前本地验收基线和文档入口。
- 风险清单覆盖不应承诺的能力：Redis 分布式写锁、`d37ac32` 棋力收益、CI、完整可访问性审计、公网部署、打包、登录、房间、观战、排行榜和比赛系统。
- 风险清单覆盖发布前边界：`GOBANG_CORS_ORIGINS`、未跟踪 `AGENTS.md` 旧 4173 示例、subagent 不可用、GitHub HTTPS 连接重置。
- 下一轮拆分覆盖 CI 与质量门禁、AI 收益评估、Redis/部署可信度、前端质量纵深和比赛体验。
- 回滚处置强调已推送提交使用 `git revert`，不使用破坏共享历史的重置命令。

## Verification

- `Select-String` 核对风险关键词完整出现：`d37ac32`、`GOBANG_CORS_ORIGINS`、`AGENTS.md`、subagent、GitHub HTTPS、Redis、CI、axe、`git revert`、`beta_cutoffs`。
- `git diff --check`：无空白错误（仅 CRLF 提示）。

## Blocker

- 无。

## Major

- 无。

## Notes

- 本文件是本地确定性审查记录；当前环境未使用独立 subagent。
- E-08 只形成风险清单，不实现 CI、部署、AI 评测或 Redis 并发写保护。
- E-07 本地提交首轮 push 因 GitHub HTTPS 连接重置失败；E-08 完成后需统一重试远端同步。

## Verdict

- PASS。发布前风险清单足以支持本地 MVP 演示边界和下一轮任务启动。
