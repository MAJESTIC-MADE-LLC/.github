from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import portfolio_status  # noqa: E402


class PortfolioStatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = portfolio_status.load_manifest()

    def test_current_manifest_has_expected_inventory(self) -> None:
        repositories = self.manifest["repositories"]

        self.assertEqual(len(repositories), 23)
        self.assertEqual(
            {repository["name"] for repository in repositories},
            {
                ".github",
                "Almanac",
                "Apiary",
                "App-Template",
                "Bivy",
                "Chat-Armor",
                "Convoy",
                "Cradle",
                "Deep-Six",
                "Hook",
                "Majestic-Made-Hub",
                "Paws",
                "Range",
                "ReachMe",
                "RideBinder",
                "RoomProof",
                "RoutineCue",
                "Steward",
                "Trove",
                "Use-By",
                "app-legal",
                "wolfe-server-apps",
                "wolfe-server-infra",
            },
        )

    def test_duplicate_repository_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["repositories"].append(copy.deepcopy(invalid["repositories"][0]))

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "duplicate"):
            portfolio_status.validate_manifest(invalid)

    def test_launch_order_cannot_omit_a_release_candidate(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["launchOrder"][-1] = "Bivy"

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "launchOrder"):
            portfolio_status.validate_manifest(invalid)

    def test_generated_block_replacement_is_bounded(self) -> None:
        current = "before\n<!-- BEGIN GENERATED: demo -->\nold\n<!-- END GENERATED: demo -->\nafter\n"
        replacement = portfolio_status.generated_block("demo", "new")

        self.assertEqual(
            portfolio_status.replace_generated_block(current, "demo", replacement),
            "before\n<!-- BEGIN GENERATED: demo -->\nnew\n<!-- END GENERATED: demo -->\nafter\n",
        )

    def test_missing_generated_markers_are_rejected(self) -> None:
        with self.assertRaisesRegex(portfolio_status.PortfolioError, "missing"):
            portfolio_status.replace_generated_block(
                "handwritten content", "demo", portfolio_status.generated_block("demo", "new")
            )

    def test_workspace_verification_requires_declared_evidence(self) -> None:
        manifest = {
            "repositories": [
                {
                    "name": "Example",
                    "localCheckout": True,
                    "requiredPaths": ["README.md", "tests"],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "Example"
            (checkout / ".git").mkdir(parents=True)
            (checkout / "README.md").write_text("example", encoding="utf-8")
            with mock.patch.object(portfolio_status, "run_command", return_value="dev\n"):
                with self.assertRaisesRegex(
                    portfolio_status.PortfolioError, "missing tests"
                ):
                    portfolio_status.verify_workspace(manifest, Path(directory))

    def test_github_verification_detects_unlisted_repository(self) -> None:
        repository_names = [
            {"name": repository["name"]}
            for repository in self.manifest["repositories"]
        ]
        repository_names.append({"name": "Unexpected"})
        with mock.patch.object(
            portfolio_status,
            "run_command",
            return_value=json.dumps(repository_names),
        ):
            with self.assertRaisesRegex(
                portfolio_status.PortfolioError, "missing from manifest: Unexpected"
            ):
                portfolio_status.verify_github(self.manifest, "example")


if __name__ == "__main__":
    unittest.main()
