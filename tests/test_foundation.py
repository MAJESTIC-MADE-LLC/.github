from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_foundation.py"
SPEC = importlib.util.spec_from_file_location("check_foundation", SCRIPT)
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)


class FoundationPolicyTest(unittest.TestCase):
    def test_dependency_parser_keeps_exact_constraints_and_path_overrides_separate(self):
        spec = foundation.parse_pubspec('''name: example
version: 1.0.0
environment:
  sdk: ">=3.13.7 <4.0.0"
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: 3.4.3
  majestic_app: 0.1.0
dependency_overrides:
  majestic_app:
    path: ../App-Template/packages/majestic_app
hooks:
  user_defines:
    sqlite3:
      source: sqlite3mc
''')
        self.assertEqual(spec["dartConstraint"], ">=3.13.7 <4.0.0")
        self.assertEqual(spec["dependencies"]["flutter_riverpod"]["version"], "3.4.3")
        self.assertEqual(spec["dependency_overrides"]["majestic_app"]["path"], "../App-Template/packages/majestic_app")
        self.assertTrue(spec["encryptedSqliteHook"])
        self.assertFalse(foundation.parse_pubspec("name: plain\n")["encryptedSqliteHook"])

    def test_lock_parser_does_not_confuse_sdk_minimums_with_resolved_versions(self):
        lock = foundation.parse_lock('''packages:
  majestic_app:
    dependency: "direct main"
    description:
      path: "../App-Template/packages/majestic_app"
      relative: true
    source: path
    version: "0.1.0"
  go_router:
    source: hosted
    version: "18.0.1"
sdks:
  dart: ">=3.13.7 <4.0.0"
  flutter: ">=3.44.0"
''')
        self.assertEqual(lock["majestic_app"]["source"], "path")
        self.assertEqual(lock["go_router"]["version"], "18.0.1")
        self.assertNotIn("dart", lock)

    def test_provider_boundary_covers_transitive_provider_families_not_all_http(self):
        policy = foundation.read_json(foundation.STANDARD_PATH)
        for name in ["supabase_flutter", "firebase_core", "sentry_flutter", "purchases_flutter", "dart_openai"]:
            self.assertTrue(foundation.provider_is_prohibited(name, policy), name)
        self.assertFalse(foundation.provider_is_prohibited("http", policy))

    def test_workflow_rejects_non_main_events_and_guard_bypass(self):
        valid = '''on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  check:
    if: ${{ github.ref == 'refs/heads/main' && (github.event_name == 'push' || github.event_name == 'workflow_dispatch') }}
    steps:
      - run: python3 --version
'''
        self.assertEqual(foundation.check_workflow(valid), [])
        for invalid in [
            valid.replace("branches: [main]", "branches: [dev]"),
            valid.replace("  workflow_dispatch:", "  pull_request:"),
            valid.replace("github.ref == 'refs/heads/main' &&", "github.ref == 'refs/heads/main' ||"),
            valid.replace("    steps:", "    steps:\n      - uses: actions/checkout@abc\n        with:\n          ref: dev"),
        ]:
            self.assertTrue(foundation.check_workflow(invalid))

    def test_verified_label_alone_cannot_satisfy_source_bound_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertTrue(foundation.evidence_errors({"status": "verified"}, ["tests"], root, "source"))
            artifact = root / "tests.txt"
            artifact.write_text("Recorded local test output\n")
            entry = {"status": "passed", "record": "tests.txt", "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "recordedAt": "2026-11-03T12:00:00Z", "sourceFingerprint": "source"}
            self.assertEqual(foundation.evidence_errors({"tests": entry}, ["tests"], root, "source"), [])
            self.assertTrue(foundation.evidence_errors({"tests": entry}, ["tests"], root, "changed-source"))
            artifact.write_text("Changed evidence\n")
            self.assertTrue(foundation.evidence_errors({"tests": entry}, ["tests"], root, "source"))

    def test_paths_and_duplicate_json_are_not_trusted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(foundation.FoundationError):
                foundation.within(root, "../outside")
            path = root / "data.json"
            path.write_text('{"status":"pending","status":"verified"}')
            with self.assertRaises(foundation.FoundationError):
                foundation.read_json(path)

    def test_optional_modules_are_selected_only_for_consumers_that_use_them(self):
        policy = foundation.read_json(foundation.STANDARD_PATH)
        spec = foundation.parse_pubspec("dependencies:\n  flutter:\n    sdk: flutter\n")
        selected = foundation.selected_shared_packages(policy, {}, spec, {})
        self.assertEqual(set(selected), set(policy["packages"]))
        for name in policy["optionalSharedPackages"]:
            for manifest, lock, direct in [({"packages": {name: {}}}, {}, {}), ({}, {name: {}}, {}), ({}, {}, {name: {}})]:
                current = {**spec, "dependencies": direct}
                self.assertIn(name, foundation.selected_shared_packages(policy, manifest, current, lock))

    def test_used_optional_source_changes_invalidate_consumer_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / "app"
            optional = root / "module"
            for base in [app, optional]:
                (base / "lib").mkdir(parents=True)
                (base / "lib/main.dart").write_text("// Original implementation\n")
            before = foundation.source_fingerprint(app, [optional], root)
            (optional / "lib/main.dart").write_text("// Updated implementation\n")
            self.assertNotEqual(before, foundation.source_fingerprint(app, [optional], root))
            unchanged = foundation.source_fingerprint(app, [], root)
            (app / "build").mkdir()
            (app / "build/output.txt").write_text("Generated build output\n")
            self.assertEqual(unchanged, foundation.source_fingerprint(app, [], root))

    def test_android_native_toolchain_drift_is_reported(self):
        baseline = {"agp": "9.1.0", "kotlin": "2.4.0", "gradle": "9.3.1", "jvmTarget": 17}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "android/app").mkdir(parents=True)
            (root / "android/gradle/wrapper").mkdir(parents=True)
            settings = root / "android/settings.gradle.kts"
            settings.write_text('id("com.android.application") version "9.1.0"\nid("org.jetbrains.kotlin.android") version "2.4.0"\n')
            (root / "android/gradle/wrapper/gradle-wrapper.properties").write_text("distributionUrl=https://services.gradle.org/distributions/gradle-9.3.1-all.zip\n")
            (root / "android/app/build.gradle.kts").write_text("sourceCompatibility = JavaVersion.VERSION_17\ntargetCompatibility = JavaVersion.VERSION_17\njvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17\n")
            self.assertEqual(foundation.android_toolchain_errors(root, baseline), [])
            settings.write_text(settings.read_text().replace("9.1.0", "9.2.1"))
            self.assertIn("Android agp must be 9.1.0", foundation.android_toolchain_errors(root, baseline))

    def test_sdk_generated_inputs_do_not_invalidate_source_but_real_native_inputs_do(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / "app"
            real_inputs = ["lib/main.dart", "pubspec.yaml", "pubspec.lock", "ios/Podfile",
                           "ios/Podfile.lock", "ios/Runner/OwnerPlugin.swift",
                           "ios/Runner/Info.plist", "ios/Flutter/Debug.xcconfig",
                           "ios/Flutter/Release.xcconfig", "android/app/src/main/AndroidManifest.xml"]
            for name in real_inputs:
                path = app / name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("qualified source\n")
            before = foundation.source_fingerprint(app, [], root)
            generated = set(foundation.GENERATED_SOURCE_FILES) | {
                "ios/Flutter/ephemeral/Packages/FlutterGeneratedPluginSwiftPackage/Package.swift"
            }
            for name in generated:
                path = app / name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("machine SDK path and integration_test registration\n")
            self.assertEqual(before, foundation.source_fingerprint(app, [], root))
            for name in real_inputs:
                path = app / name
                with self.subTest(name=name):
                    path.write_text("changed real source\n")
                    self.assertNotEqual(before, foundation.source_fingerprint(app, [], root))
                    path.write_text("qualified source\n")

    def test_machine_policy_names_the_exact_fingerprint_exclusions(self):
        policy = foundation.read_json(foundation.STANDARD_PATH)["sourceFingerprintPolicy"]
        self.assertEqual(policy["version"], foundation.SOURCE_FINGERPRINT_POLICY_VERSION)
        self.assertEqual(set(policy["excludedGeneratedFiles"]), foundation.GENERATED_SOURCE_FILES)
        self.assertEqual(set(policy["excludedGeneratedDirectories"]), foundation.GENERATED_SOURCE_DIRECTORIES)

    def test_ci_sdk_pin_supports_exact_env_but_rejects_unpinned_stable(self):
        valid = "env:\n  FLUTTER_VERSION: 3.47.8\nsteps:\n  - uses: subosito/flutter-action@immutable\n    with:\n      flutter-version: ${{ env.FLUTTER_VERSION }}\n"
        self.assertEqual(foundation.flutter_ci_version_errors(valid, "3.47.8"), [])
        self.assertTrue(foundation.flutter_ci_version_errors(valid.replace("3.47.8", "3.47.3"), "3.47.8"))
        self.assertTrue(foundation.flutter_ci_version_errors("  - uses: subosito/flutter-action@immutable\n    with:\n      channel: stable\n", "3.47.8"))

    def test_log_evidence_cannot_bypass_unpublished_package_release_gate(self):
        rows = [{"application": "example", "packageProvenance": "workspace-unpublished", "foundationEvidence": "passed",
                 "evidence": {"immutable_package_revisions": {"status": "passed"}}}]
        self.assertIn("immutable_package_revisions pending", foundation.immutable_revision_errors(rows)[0])

    def test_gate_preserves_order_and_excludes_experiments(self):
        standard = foundation.read_json(foundation.STANDARD_PATH)
        self.assertEqual(len(standard["gate"]["requiredApps"]), 7)
        self.assertEqual(standard["toolchain"]["platforms"], ["ios", "android"])
        self.assertNotIn("dossier", [row["id"] for row in standard["consumers"]])
        self.assertNotIn("off-record", [row["id"] for row in standard["consumers"]])
        manifest = foundation.read_json(foundation.REPO_ROOT / "portfolio/REPOSITORIES.json")
        self.assertEqual(manifest["launchOrder"][:7], standard["gate"]["requiredApps"])


if __name__ == "__main__":
    unittest.main()
