# Trace Chain（脱敏样本）

同一次任务，`trace_id = e3582bdb2ad8` 出现在三个位置：

| 层 | 字段 | 值 |
|---|---|---|
| local console | trace_id / provider | e3582bdb2ad8 / cloud-a |
| executor | trace_id / ok / duration | e3582bdb2ad8 / true / 0.485s |
| gateway audit | trace_id / kind / provider | e3582bdb2ad8 / chat / cloud-a |

原始日志中的任务文本、路径、凭据已移除或替换为占位符；provider 名称做了抽象。
