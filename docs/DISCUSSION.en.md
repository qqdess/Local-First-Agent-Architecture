# Discussion draft (English)

Title: Execution-level evidence gates: what do you require before accepting an agent's "done"?

Body:

Most agent failures I hit are not wrong answers. They are **false successes**:
the model says the task is done, but no file changed, no command ran, and no
result was read back.

I run a local-first agent on a Windows desktop. The architecture is deliberately
small:

- generation and execution are separated: cloud models parse/draft, one local
  executor acts;
- a single router owns intent, so there is no second planner to disagree with;
- every success claim must carry evidence in a trace ledger: command output,
  file hash, screenshot, or read-back;
- missing evidence is a failure (`NO_EVIDENCE`), not a warning;
- watchdogs use a named mutex, because two self-healing loops restarting each
  other is its own outage.

I am not claiming this is novel. [AgentClaimGuard](https://github.com/konoeph/AgentClaimGuard)
(claim-level evidence/policy gate, Apache-2.0) and
[Agent Evidence Guard](https://github.com/ivanovaruso/agent-evidence-guard)
(deterministic completion-claim guard) already cover the claim layer. My focus
is **execution-level evidence**: proving the action happened, not just that the
sentence is supported.

A minimal runnable demo is in the repo (standard library only; no model,
network, or credentials):

```bash
python demo/run_demo.py
```

Case 1: the mock agent claims success but never writes `target.txt`; the gate
returns `[BLOCK] No evidence, task failed`.
Case 2: the mock agent writes the file and reports SHA-256; the gate re-hashes
it and returns `[PASS]`.

Repo: https://github.com/qqdess/Local-First-Agent-Architecture
Demo: https://github.com/qqdess/Local-First-Agent-Architecture/tree/main/demo

Questions:

1. What evidence do you require before an agent's "done" is accepted in
   production?
2. Do you gate at the claim layer, the execution layer, or both?
3. What false-success pattern broke your system that a return-code or test
   check missed?
4. Is execution-level evidence practical at scale, or does it collapse into
   custom verifiers for every action?

I am looking for harsh critique, especially from people running agents against
real files, browsers, or internal tools.
