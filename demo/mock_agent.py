#!/usr/bin/env python3
"""A deliberately small mock agent.

It can either lie about modifying a file, or actually modify it. The point is
to give the evidence gate something concrete to verify.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

CLAIM = "任务执行完毕，文件已成功修改"
CONTENT = "target file written by the mock agent\n"


@dataclass(frozen=True)
class AgentResult:
    target: Path
    message: str
    claimed_success: bool
    claimed_sha256: str | None = None


def run(target: Path, *, honest: bool) -> AgentResult:
    """Simulate an agent run.

    honest=False: emit the success claim without touching the file.
    honest=True:  write the file and return its real hash.
    """
    if not honest:
        return AgentResult(target=target, message=CLAIM, claimed_success=True)

    target.write_text(CONTENT, encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return AgentResult(
        target=target,
        message=CLAIM,
        claimed_success=True,
        claimed_sha256=digest,
    )
