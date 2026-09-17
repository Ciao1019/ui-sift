import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/update_install_badge.py"
spec = importlib.util.spec_from_file_location("install_badge", SCRIPT)
badge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(badge)


def record(count, repository="example/ui-sift"):
    return {"id": repository + "/ui-sift", "source": repository, "installs": count}


class InstallBadgeTests(unittest.TestCase):
    def test_selects_exact_skill_from_fuzzy_results(self):
        payload = {"skills": [record(8000, "someone/ui-sift"), record(12)]}
        self.assertEqual(badge.find_install_count(payload, "example/ui-sift", "ui-sift"), 12)

    def test_source_matching_handles_case(self):
        payload = {"skills": [record(7, "Example/UI-Sift")]}
        self.assertEqual(badge.find_install_count(payload, "example/ui-sift", "ui-sift"), 7)

    def test_missing_record_is_unknown_not_zero(self):
        self.assertIsNone(badge.find_install_count({"skills": []}, "example/ui-sift", "ui-sift"))

    def test_actual_zero_is_preserved(self):
        payload = {"skills": [record(0)]}
        self.assertEqual(badge.find_install_count(payload, "example/ui-sift", "ui-sift"), 0)

    def test_malformed_counts_and_duplicate_records_fail(self):
        payloads = [{"skills": [record(value)]} for value in (-1, True, "12", None)]
        payloads += [{}, {"skills": [record(1), record(2)]},
                     {"skills": [{"id": "example/ui-sift/ui-sift", "source": "other/repo", "installs": 4}]}]
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                badge.find_install_count(payload, "example/ui-sift", "ui-sift")

    def test_failed_fetch_preserves_previous_badge(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "installs.json"
            badge.write_badge(output, 12)
            before = output.read_bytes()
            with patch.object(badge, "fetch_install_count", side_effect=OSError("offline")):
                with self.assertRaises(OSError):
                    badge.update("example/ui-sift", "ui-sift", output)
            self.assertEqual(output.read_bytes(), before)

    def test_unchanged_count_does_not_rewrite_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "installs.json"
            self.assertTrue(badge.write_badge(output, 12))
            before = output.stat().st_mtime_ns
            self.assertFalse(badge.write_badge(output, 12))
            self.assertEqual(output.stat().st_mtime_ns, before)

    def test_pending_badge_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "installs.json"
            badge.write_badge(output, None)
            self.assertIn('"message": "pending"', output.read_text())


if __name__ == "__main__":
    unittest.main()
