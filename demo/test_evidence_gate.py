from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from evidence_gate import BLOCK_MISMATCH, BLOCK_NO_EVIDENCE, PASS, verify
from mock_agent import run


class EvidenceGateTests(unittest.TestCase):
    def test_lying_agent_is_blocked_with_no_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp) / "target.txt", honest=False)
            decision = verify(result)
            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "NO_EVIDENCE")
            self.assertEqual(decision.render(), BLOCK_NO_EVIDENCE)

    def test_honest_agent_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp) / "target.txt", honest=True)
            decision = verify(result)
            self.assertTrue(decision.allowed)
            self.assertEqual(decision.status, "ACCEPTED")
            self.assertIn(PASS, decision.render())

    def test_hash_mismatch_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp) / "target.txt", honest=True)
            tampered = result.__class__(
                target=result.target,
                message=result.message,
                claimed_success=True,
                claimed_sha256="0" * 64,
            )
            decision = verify(tampered)
            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "EVIDENCE_MISMATCH")
            self.assertEqual(decision.render(), BLOCK_MISMATCH)

    def test_empty_file_is_not_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target.txt"
            target.write_text("", encoding="utf-8")
            result = run(target, honest=False)
            decision = verify(result)
            self.assertFalse(decision.allowed)
            self.assertEqual(decision.status, "NO_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
