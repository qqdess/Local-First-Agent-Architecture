# Minimal Evidence Gate Demo

A runnable, dependency-free demonstration of the core rule:

> A success claim without evidence is not a success.

No model, network, credentials, RPA, or host paths. It is a small mock agent
plus a filesystem gate, deliberately kept small enough to read in one sitting.

## Run

From the repository root:

```bash
python demo/run_demo.py
```

Expected output:

```text
== Case 1: agent claims success, file was never written ==
agent: 任务执行完毕，文件已成功修改
target.txt exists: False
[BLOCK] No evidence, task failed

== Case 2: agent actually writes the file and reports a hash ==
agent: 任务执行完毕，文件已成功修改
[PASS] Evidence verified: target.txt exists (39 bytes, sha256=...)

Result: false claim blocked; evidenced claim accepted.
```

The first case is the important one: the agent's sentence is fluent and
confident, but `target.txt` does not exist, so the gate refuses the claim.

## Files

- `mock_agent.py`: emits a success claim; with `honest=True` it actually writes
  `target.txt` and returns its SHA-256.
- `evidence_gate.py`: checks existence, non-empty content, and the reported
  hash. Missing evidence produces `NO_EVIDENCE`; a bad hash produces
  `EVIDENCE_MISMATCH`.
- `run_demo.py`: runs the lying case and the honest case back to back.
- `test_evidence_gate.py`: four tests covering block, pass, hash mismatch, and
  empty file.

## Test

```bash
python -m unittest discover -s demo -v
```

## Boundary

The gate only checks the declared evidence contract. It does not prove the
file's content is correct, and it does not detect every hallucination. A real
system needs action-specific verifiers; this demo supplies filesystem ones.
