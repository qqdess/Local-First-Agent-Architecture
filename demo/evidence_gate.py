#!/usr/bin/env python3
"""Verify an agent's success claim against the filesystem.

This is the small, sanitized version of the idea: the agent's sentence is not
evidence. The gate checks that the claimed target exists, is non-empty, and
matches the hash the agent reported (when a hash is reported).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from mock_agent import AgentResult

BLOCK_NO_EVIDENCE = "[BLOCK] No evidence, task failed"
BLOCK_MISMATCH = "[BLOCK] Evidence mismatch, task failed"
PASS = "[PASS] Evidence verified"


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    status: str
    reason: str
    sha256: str | None = None
    size: int | None = None

    def render(self) -> str:
        if self.allowed:
            return f"{PASS}: {self.reason}"
        if self.status == "NO_EVIDENCE":
            return BLOCK_NO_EVIDENCE
        return BLOCK_MISMATCH


def verify(result: AgentResult) -> GateDecision:
    target = result.target
    if not result.claimed_success:
        return GateDecision(False, "REJECTED", "agent reported failure")
    if not target.exists() or not target.is_file():
        return GateDecision(False, "NO_EVIDENCE", "target.txt does not exist")
    data = target.read_bytes()
    if not data:
        return GateDecision(False, "NO_EVIDENCE", "target.txt is empty")
    digest = hashlib.sha256(data).hexdigest()
    if result.claimed_sha256 and result.claimed_sha256 != digest:
        return GateDecision(
            False,
            "EVIDENCE_MISMATCH",
            "reported sha256 does not match target.txt",
            sha256=digest,
            size=len(data),
        )
    return GateDecision(
        True,
        "ACCEPTED",
        f"target.txt exists ({len(data)} bytes, sha256={digest[:16]}...)",
        sha256=digest,
        size=len(data),
    )
