from __future__ import annotations
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("foundation_snapshot", SCRIPTS / "foundation_evidence_snapshot.py")
snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snapshot)


class SnapshotTests(unittest.TestCase):
    def test_log_hash_tracks_bytes_without_promoting_log_text_to_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.log"
            path.write_text("All tests passed!\n")
            first = snapshot.file_record(path)
            self.assertNotIn("status", first)
            path.write_text("Different run\n")
            self.assertNotEqual(first["sha256"], snapshot.file_record(path)["sha256"])

    def test_source_comparison_reports_drift_and_missing_consumers(self):
        before = {"consumers": [{"application": "one", "sourceFingerprint": "a"}, {"application": "two", "sourceFingerprint": "b"}]}
        after = {"consumers": [{"application": "one", "sourceFingerprint": "changed"}]}
        self.assertEqual(snapshot.compare_sources(before, after), ["one", "two"])
        self.assertEqual(snapshot.compare_sources(before, before), [])


if __name__ == "__main__":
    unittest.main()
