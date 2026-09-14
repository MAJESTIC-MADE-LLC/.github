from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class CommunityHealthTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        contents = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        self.assertTrue(contents.strip(), f"{relative_path} must not be empty")
        return contents

    def test_default_community_health_files_exist(self) -> None:
        for relative_path in (
            "CODE_OF_CONDUCT.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "SUPPORT.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ):
            with self.subTest(path=relative_path):
                self.read(relative_path)

    def test_security_reporting_remains_private(self) -> None:
        security = self.read("SECURITY.md")
        issue_form = self.read(".github/ISSUE_TEMPLATE/bug_report.yml")
        chooser = self.read(".github/ISSUE_TEMPLATE/config.yml")

        self.assertIn("Do not open a public issue", security)
        self.assertIn("support@majesticmade.dev", security)
        self.assertIn("This issue may be public", issue_form)
        self.assertIn("This is not a vulnerability", issue_form)
        self.assertIn("organization security policy", issue_form)
        self.assertIn("blank_issues_enabled: false", chooser)
        self.assertIn("SECURITY.md", chooser)

    def test_default_workflow_targets_dev(self) -> None:
        contributing = self.read("CONTRIBUTING.md")
        pull_request = self.read(".github/PULL_REQUEST_TEMPLATE.md")

        self.assertIn("pull request against `dev`", contributing)
        self.assertIn("`main` branch is release-only", contributing)
        self.assertIn("targets `dev`", pull_request)
        self.assertIn("privacy, security, data lifecycle", pull_request)

    def test_published_contact_is_consistent(self) -> None:
        for relative_path in (
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SUPPORT.md",
        ):
            with self.subTest(path=relative_path):
                self.assertIn("support@majesticmade.dev", self.read(relative_path))


if __name__ == "__main__":
    unittest.main()
