from __future__ import annotations

import copy
import json
import subprocess
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

        self.assertEqual(len(repositories), 28)
        self.assertEqual(
            {repository["name"] for repository in repositories},
            {
                ".github",
                "Fine-Notes",
                "Skepbook",
                "App-Template",
                "Campsake",
                "Kinwall",
                "Claim-Crate",
                "Tender-Days",
                "Divefolio",
                "Creelmark",
                "Majestic-Made-Hub",
                "Paws",
                "Brassmark",
                "Namefold",
                "Ridelore",
                "Turnstamp",
                "Daymerit",
                "What-We-Own",
                "Object-Lore",
                "Pantry-Clock",
                "app-legal",
                "wolfe-server-apps",
                "wolfe-server-infra",
                "steward",
                "lockbox",
                "dossier",
                "off-record",
                "brand-assets",
            },
        )
        self.assertEqual(
            sum(repository["role"] == "release-candidate" for repository in repositories),
            7,
        )
        self.assertEqual(
            self.manifest["launchOrder"],
            [
                "Skepbook", "Ridelore", "Paws", "Pantry-Clock", "Fine-Notes",
                "Namefold", "Daymerit", "Turnstamp", "What-We-Own", "Creelmark",
                "Campsake", "Tender-Days", "Divefolio", "Brassmark", "Object-Lore",
                "quiet-arcade", "lockbox",
            ],
        )

    def test_inventory_counts_are_derived_and_not_a_fixed_launch_gate(self) -> None:
        expanded = copy.deepcopy(self.manifest)
        shared = copy.deepcopy(expanded["repositories"][0])
        shared["name"] = "Additional-Support"
        shared["displayName"] = "Additional Support"
        expanded["repositories"].append(shared)

        portfolio_status.validate_manifest(expanded)

        self.assertIn("29 repositories", portfolio_status.render_status(expanded))
        self.assertIn("17 products", portfolio_status.render_status(expanded))

    def test_virtual_product_is_rendered_without_becoming_a_repository(self) -> None:
        self.assertNotIn(
            "quiet-arcade", portfolio_status.repositories_by_name(self.manifest)
        )
        self.assertIn("| 16 | Quiet Arcade |", portfolio_status.render_launch_table(self.manifest))

    def test_virtual_product_rejects_collisions_and_unsafe_source_paths(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["virtualProducts"][0]["id"] = "Skepbook"
        with self.assertRaisesRegex(portfolio_status.PortfolioError, "collides"):
            portfolio_status.validate_manifest(invalid)

        invalid = copy.deepcopy(self.manifest)
        invalid["virtualProducts"][0]["sourcePath"] = "../outside.md"
        with self.assertRaisesRegex(portfolio_status.PortfolioError, "normalized relative path"):
            portfolio_status.validate_manifest(invalid)

    def test_launch_queue_rejects_support_excluded_and_consolidating_repositories(self) -> None:
        for name in ("App-Template", "dossier", "off-record", "Claim-Crate", "steward", "Kinwall"):
            with self.subTest(name=name):
                invalid = copy.deepcopy(self.manifest)
                invalid["launchOrder"][-1] = name
                with self.assertRaisesRegex(portfolio_status.PortfolioError, "launchOrder"):
                    portfolio_status.validate_manifest(invalid)

    def test_consolidation_requires_an_active_product_target(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        repository = portfolio_status.repositories_by_name(invalid)["Claim-Crate"]
        repository["consolidatesInto"] = "Kinwall"
        with self.assertRaisesRegex(portfolio_status.PortfolioError, "active product"):
            portfolio_status.validate_manifest(invalid)

    def test_data_matrix_covers_concept_and_virtual_queue_entries(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["dataMatrix"] = [
            row for row in invalid["dataMatrix"] if row["productId"] != "quiet-arcade"
        ]
        with self.assertRaisesRegex(portfolio_status.PortfolioError, "every active product"):
            portfolio_status.validate_manifest(invalid)

    def test_duplicate_repository_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["repositories"].append(copy.deepcopy(invalid["repositories"][0]))

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "duplicate"):
            portfolio_status.validate_manifest(invalid)

    def test_unsafe_repository_names_are_rejected(self) -> None:
        for name in ("../outside", "owner/repository", "-option", "bad\nname"):
            with self.subTest(name=name):
                invalid = copy.deepcopy(self.manifest)
                invalid["repositories"][0]["name"] = name

                with self.assertRaises(portfolio_status.PortfolioError):
                    portfolio_status.validate_manifest(invalid)

    def test_unsafe_required_paths_are_rejected(self) -> None:
        for path in (
            "../secret",
            "/etc/passwd",
            "folder//file",
            "C:\\secret",
            "folder/C:/secret",
        ):
            with self.subTest(path=path):
                invalid = copy.deepcopy(self.manifest)
                invalid["repositories"][0]["requiredPaths"] = [path]

                with self.assertRaisesRegex(
                    portfolio_status.PortfolioError, "normalized relative path"
                ):
                    portfolio_status.validate_manifest(invalid)

    def test_manifest_requires_typed_fields(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["repositories"][0]["localCheckout"] = "yes"

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "boolean"):
            portfolio_status.validate_manifest(invalid)

    def test_manifest_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(
                '{"schemaVersion": 1, "schemaVersion": 2}', encoding="utf-8"
            )

            with self.assertRaisesRegex(portfolio_status.PortfolioError, "duplicate key"):
                portfolio_status.load_manifest(path)

    def test_data_matrix_rejects_non_string_product_id(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["dataMatrix"][0]["productId"] = []

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "non-empty string"):
            portfolio_status.validate_manifest(invalid)

    def test_launch_order_cannot_omit_a_release_candidate(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["launchOrder"][-1] = "Campsake"

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "launchOrder"):
            portfolio_status.validate_manifest(invalid)

    def test_generated_block_replacement_is_bounded(self) -> None:
        current = "before\n<!-- BEGIN GENERATED: demo -->\nold\n<!-- END GENERATED: demo -->\nafter\n"
        replacement = portfolio_status.generated_block("demo", "new")

        self.assertEqual(
            portfolio_status.replace_generated_block(current, "demo", replacement),
            "before\n<!-- BEGIN GENERATED: demo -->\nnew\n<!-- END GENERATED: demo -->\nafter\n",
        )

    def test_duplicate_generated_markers_are_rejected(self) -> None:
        duplicated = (
            portfolio_status.generated_block("demo", "first")
            + "\n"
            + portfolio_status.generated_block("demo", "second")
        )

        with self.assertRaisesRegex(portfolio_status.PortfolioError, "duplicate"):
            portfolio_status.replace_generated_block(
                duplicated, "demo", portfolio_status.generated_block("demo", "new")
            )

    def test_markdown_text_encodes_structure_and_control_characters(self) -> None:
        malicious = "cell | value\n<!-- END GENERATED: demo --> [link](https://example.test)"

        encoded = portfolio_status.markdown_text(malicious)

        self.assertNotIn("\n", encoded)
        self.assertNotIn("|", encoded)
        self.assertNotIn("<!--", encoded)
        self.assertNotIn("[link]", encoded)
        self.assertIn("&#10;", encoded)
        self.assertIn("&#124;", encoded)

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

    def test_workspace_verification_rejects_checkout_symlink_escape(self) -> None:
        manifest = {
            "repositories": [
                {
                    "name": "Example",
                    "localCheckout": True,
                    "requiredPaths": ["README.md"],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            outside = root / "outside"
            workspace.mkdir()
            (outside / ".git").mkdir(parents=True)
            (outside / "README.md").write_text("outside", encoding="utf-8")
            (workspace / "Example").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(portfolio_status.PortfolioError, "escapes"):
                portfolio_status.verify_workspace(manifest, workspace)

    def test_generated_write_rejects_symlink_without_touching_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generated = root / "portfolio" / "STATUS.md"
            victim = root / "victim.md"
            generated.parent.mkdir()
            victim.write_text(
                portfolio_status.generated_block("demo", "old"), encoding="utf-8"
            )
            generated.symlink_to(victim)

            with mock.patch.object(portfolio_status, "REPO_ROOT", root):
                with self.assertRaises(portfolio_status.PortfolioError):
                    portfolio_status.synchronize_file(
                        generated,
                        "demo",
                        portfolio_status.generated_block("demo", "new"),
                        write=True,
                    )

            self.assertEqual(
                victim.read_text(encoding="utf-8"),
                portfolio_status.generated_block("demo", "old"),
            )

    def test_generated_write_atomically_updates_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generated = root / "portfolio" / "STATUS.md"
            generated.parent.mkdir()
            generated.write_text(
                portfolio_status.generated_block("demo", "old"), encoding="utf-8"
            )

            with mock.patch.object(portfolio_status, "REPO_ROOT", root):
                portfolio_status.synchronize_file(
                    generated,
                    "demo",
                    portfolio_status.generated_block("demo", "new"),
                    write=True,
                )

            self.assertEqual(
                generated.read_text(encoding="utf-8"),
                portfolio_status.generated_block("demo", "new"),
            )

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

    def test_github_verification_allows_concept_governance_files(self) -> None:
        manifest = {"repositories": [{"name": "Example", "role": "concept"}]}
        tree = {
            "truncated": False,
            "tree": [
                {"path": path, "type": "blob"}
                for path in sorted(
                    portfolio_status.CONCEPT_REMOTE_ALLOWLIST
                    | {"docs/PORTFOLIO_ALIGNMENT.md", "docs/handoff/planning.md"}
                )
            ]
        }
        with mock.patch.object(
            portfolio_status,
            "run_command",
            side_effect=[json.dumps([{"name": "Example"}]), json.dumps(tree)],
        ):
            portfolio_status.verify_github(manifest, "example")

    def test_github_verification_rejects_concept_implementation(self) -> None:
        manifest = {"repositories": [{"name": "Example", "role": "concept"}]}
        tree = {
            "truncated": False,
            "tree": [
                {"path": "README.md", "type": "blob"},
                {"path": "app/lib/main.dart", "type": "blob"},
            ]
        }
        with mock.patch.object(
            portfolio_status,
            "run_command",
            side_effect=[json.dumps([{"name": "Example"}]), json.dumps(tree)],
        ):
            with self.assertRaisesRegex(
                portfolio_status.PortfolioError, "app/lib/main.dart"
            ):
                portfolio_status.verify_github(manifest, "example")

    def test_github_verification_uses_main_for_legacy_planning_repository(self) -> None:
        manifest = {
            "repositories": [{"name": "Example", "role": "concept", "sourceRef": "main"}]
        }
        tree = {"truncated": False, "tree": [{"path": "README.md", "type": "blob"}]}
        with mock.patch.object(
            portfolio_status,
            "run_command",
            side_effect=[json.dumps([{"name": "Example"}]), json.dumps(tree)],
        ) as command:
            portfolio_status.verify_github(manifest, "example")
        self.assertEqual(
            command.call_args_list[-1].args[0][-1],
            "repos/example/Example/git/trees/main?recursive=1",
        )

    def test_github_verification_rejects_truncated_tree(self) -> None:
        manifest = {"repositories": [{"name": "Example", "role": "concept"}]}
        tree = {
            "truncated": True,
            "tree": [{"path": "README.md", "type": "blob"}],
        }
        with mock.patch.object(
            portfolio_status,
            "run_command",
            side_effect=[json.dumps([{"name": "Example"}]), json.dumps(tree)],
        ):
            with self.assertRaisesRegex(portfolio_status.PortfolioError, "incomplete"):
                portfolio_status.verify_github(manifest, "example")

    def test_github_verification_rejects_malformed_json(self) -> None:
        manifest = {"repositories": [{"name": "Example", "role": "concept"}]}
        with mock.patch.object(
            portfolio_status,
            "run_command",
            return_value='{"not": "a list"}',
        ):
            with self.assertRaisesRegex(portfolio_status.PortfolioError, "list JSON"):
                portfolio_status.verify_github(manifest, "example")

    def test_github_verification_rejects_duplicate_json_keys(self) -> None:
        manifest = {"repositories": [{"name": "Example", "role": "concept"}]}
        duplicate_name = '[{"name": "Example", "name": "Other"}]'
        with mock.patch.object(
            portfolio_status,
            "run_command",
            return_value=duplicate_name,
        ):
            with self.assertRaisesRegex(portfolio_status.PortfolioError, "duplicate key"):
                portfolio_status.verify_github(manifest, "example")

    def test_github_verification_escapes_remote_paths_in_diagnostics(self) -> None:
        manifest = {"repositories": [{"name": "Example", "role": "concept"}]}
        malicious_path = "evil\n::error::forged\x1b[31m"
        tree = {
            "truncated": False,
            "tree": [
                {"path": "README.md", "type": "blob"},
                {"path": malicious_path, "type": "blob"},
            ],
        }
        with mock.patch.object(
            portfolio_status,
            "run_command",
            side_effect=[json.dumps([{"name": "Example"}]), json.dumps(tree)],
        ):
            with self.assertRaises(portfolio_status.PortfolioError) as context:
                portfolio_status.verify_github(manifest, "example")

        message = str(context.exception)
        self.assertNotIn(malicious_path, message)
        self.assertIn(r"evil\n::error::forged\u001b[31m", message)

    def test_github_owner_option_injection_is_rejected_before_subprocess(self) -> None:
        with mock.patch.object(portfolio_status, "run_command") as run_command:
            with self.assertRaisesRegex(portfolio_status.PortfolioError, "GitHub owner"):
                portfolio_status.verify_github(self.manifest, "--help")

        run_command.assert_not_called()

    def test_subprocess_stderr_is_escaped_for_one_line_diagnostics(self) -> None:
        error = subprocess.CalledProcessError(
            1, ["gh"], stderr="failed\n::error::forged\x1b[31m"
        )
        with mock.patch("subprocess.run", side_effect=error):
            with self.assertRaises(portfolio_status.PortfolioError) as context:
                portfolio_status.run_command(["gh"], "run GitHub command")

        self.assertIn(r"failed\n::error::forged\u001b[31m", str(context.exception))


if __name__ == "__main__":
    unittest.main()
