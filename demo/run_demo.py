#!/usr/bin/env python3
"""Run the evidence-gate demo.

Case 1: the mock agent claims success but never creates target.txt.
Case 2: the mock agent actually creates target.txt and reports its hash.

The gate blocks the first claim and accepts the second.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import evidence_gate
import mock_agent


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="evidence-gate-demo-") as tmp:
        target = Path(tmp) / "target.txt"

        print("== Case 1: agent claims success, file was never written ==")
        lying = mock_agent.run(target, honest=False)
        print(f"agent: {lying.message}")
        print(f"target.txt exists: {target.exists()}")
        first = evidence_gate.verify(lying)
        print(first.render())

        print()
        print("== Case 2: agent actually writes the file and reports a hash ==")
        honest = mock_agent.run(target, honest=True)
        print(f"agent: {honest.message}")
        second = evidence_gate.verify(honest)
        print(second.render())

        print()
        if not first.allowed and second.allowed:
            print("Result: false claim blocked; evidenced claim accepted.")
            return 0
        print("Result: demo invariant failed (the gate did not behave as expected).")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
