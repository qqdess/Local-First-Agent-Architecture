# Evidence

这里放的是“跑通过”的最小证据，不是完整日志。

- `executor_sample.jsonl`：调度记录样本（字段完整：ts / trace_id / task / provider / ok / error / duration / evidence）
- `trace_chain.md`：同一 trace_id 在本地入口、执行器、网关审计中的对应关系
- `trace_id_proof.png`：上述记录的截图版（文本渲染，无宿主信息）

脱敏规则：

- 任务文本 → `demo-prompt` 等抽象名
- provider → `cloud-a` / `gateway` 等抽象名
- PID、路径、凭据 → 占位符或移除
- 保留 trace_id、耗时、ok、evidence 字段，用于说明结构
