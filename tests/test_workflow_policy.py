from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/workflow_policy.py"
SPEC = importlib.util.spec_from_file_location("workflow_policy", SCRIPT)
policy = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = policy
SPEC.loader.exec_module(policy)

GUARD = "github.ref == 'refs/heads/main' && (github.event_name == 'push' || github.event_name == 'workflow_dispatch')"
VALID = '''name: Example
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  verify:
    if: ${{ GUARD }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09
        with:
          persist-credentials: false
      - name: Validate
        run: python3 --version
'''.replace("GUARD", GUARD)


class WorkflowPolicyTest(unittest.TestCase):
    def assert_rejected(self, text: str, message: str | None = None):
        errors = policy.check_workflow(text)
        self.assertTrue(errors, text)
        if message:
            self.assertTrue(any(message in error for error in errors), errors)

    def test_approved_main_workflow(self):
        self.assertEqual(policy.check_workflow(VALID), [])

    def test_main_push_only_workflow(self):
        text = VALID.replace("  workflow_dispatch:\n", "").replace(GUARD, "github.ref == 'refs/heads/main' && github.event_name == 'push'")
        self.assertEqual(policy.check_workflow(text), [])

    def test_manual_only_workflow_still_requires_main_guard(self):
        text = VALID.replace("  push:\n    branches: [main]\n", "")
        self.assertEqual(policy.check_workflow(text), [])
        self.assert_rejected(text.replace(GUARD, "github.event_name == 'workflow_dispatch'"), "guards")

    def test_only_approved_events(self):
        for event in ["pull_request", "pull_request_target", "schedule", "release", "workflow_run", "repository_dispatch", "workflow_call", "create", "delete", "check_run"]:
            with self.subTest(event=event):
                self.assert_rejected(VALID.replace("  workflow_dispatch:", f"  {event}:"), "mappings")

    def test_rejects_inline_event_lists_and_flow_mappings(self):
        for event in ["[push, workflow_dispatch]", "push", "{push: {branches: [main]}}"]:
            self.assert_rejected(VALID.replace("on:\n  push:\n    branches: [main]\n  workflow_dispatch:", f"on: {event}"))

    def test_branches_must_be_main_only(self):
        for branches in ["[dev]", "[main, dev]", "['*']", "[]", "main", "[main, '!main']"]:
            with self.subTest(branches=branches):
                self.assert_rejected(VALID.replace("[main]", branches), "branches")

    def test_tags_and_alternate_filters_rejected_even_with_main_filter(self):
        for key in ["tags", "tags-ignore", "branches-ignore"]:
            self.assert_rejected(VALID.replace("    branches: [main]", f"    branches: [main]\n    {key}: ['*']"), "filters")

    def test_dispatch_inputs_rejected(self):
        text = VALID.replace("  workflow_dispatch:", "  workflow_dispatch:\n    inputs:\n      branch:\n        default: dev")
        self.assert_rejected(text, "inputs")

    def test_path_filters_cannot_expand_execution(self):
        text = VALID.replace("    branches: [main]", "    branches: ['main']\n    paths: ['lib/**']")
        self.assertEqual(policy.check_workflow(text), [])
        self.assert_rejected(text.replace("    paths:", "    paths-ignore: ['docs/**']\n    paths:"), "combine")

    def test_all_jobs_are_guarded(self):
        extra = "  bypass:\n    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"
        self.assert_rejected(VALID + extra, "job bypass")

    def test_or_cannot_bypass_main_or_event_constraint(self):
        for condition in [
            GUARD + " || true",
            "github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'",
            "github.ref == 'refs/heads/main' && (github.event_name == 'push' || true)",
            "github.ref != 'refs/heads/dev' && github.event_name == 'push'",
            "contains(github.ref, 'main') && github.event_name == 'push'",
            "!(github.ref == 'refs/heads/main') && github.event_name == 'push'",
            "github.ref == 'refs/heads/main'",
            "true",
        ]:
            with self.subTest(condition=condition):
                self.assert_rejected(VALID.replace(GUARD, condition), "guards")

    def test_parentheses_and_additional_and_restrictions_are_safe(self):
        for condition in [
            f"({GUARD}) && success()",
            f"success() && ({GUARD})",
            f"({GUARD}) && (github.repository == 'org/repo' || startsWith(github.actor, 'owner'))",
            "'refs/heads/main' == github.ref && 'push' == github.event_name",
        ]:
            with self.subTest(condition=condition):
                self.assertEqual(policy.check_workflow(VALID.replace(GUARD, condition)), [])

    def test_folded_and_quoted_conditions(self):
        text = VALID.replace("    if: ${{ " + GUARD + " }}", "    if: >-\n      ${{ " + GUARD + " }}")
        self.assertEqual(policy.check_workflow(text), [])
        text = VALID.replace("    if: ${{ " + GUARD + " }}", '    if: "${{ ' + GUARD + ' }}"')
        self.assertEqual(policy.check_workflow(text), [])

    def test_checkout_cannot_select_different_ref_or_repository(self):
        for option in ["ref: dev", "repository: another/repo", "ref: main", "ref: ${{ github.sha }}"]:
            self.assert_rejected(VALID.replace("          persist-credentials: false", f"          {option}"), "checkout")

    def test_permission_inheritance_cannot_widen(self):
        for permissions in ["write-all", "read-all", "{contents: read}"]:
            text = VALID.replace("permissions:\n  contents: read", f"permissions: {permissions}")
            self.assert_rejected(text)
        self.assert_rejected(VALID.replace("  contents: read", "  contents: write"), "permissions")
        self.assert_rejected(VALID.replace("  contents: read", "  contents: read\n  id-token: write"), "permissions")
        self.assert_rejected(VALID.replace("    runs-on:", "    permissions:\n      contents: write\n    runs-on:"), "permissions")
        self.assert_rejected(VALID.replace("permissions:\n  contents: read\n", ""), "permissions")

    def test_empty_or_read_only_job_permissions_allowed(self):
        for permissions in ["{}", "\n      contents: read", "\n      contents: none"]:
            text = VALID.replace("    runs-on:", f"    permissions: {permissions}\n    runs-on:")
            self.assertEqual(policy.check_workflow(text), [])

    def test_malformed_permissions_are_errors_not_exceptions(self):
        for value in ["[read]", "\n    nested: read", "{}"]:
            text = VALID.replace("  contents: read", f"  contents: {value}")
            self.assert_rejected(text, "permissions")

    def test_duplicate_keys_at_every_control_boundary_rejected(self):
        variants = [
            VALID + "on:\n  pull_request:\n",
            VALID.replace("  push:", "  push:\n    branches: [dev]\n  push:"),
            VALID.replace("    branches: [main]", "    branches: [dev]\n    branches: [main]"),
            VALID.replace("    if:", "    if: true\n    if:"),
            VALID.replace("          persist-credentials: false", "          ref: dev\n          ref: main"),
            VALID.replace("      - name: Validate", "      - run: true\n        run: false\n      - name: Validate"),
        ]
        for text in variants:
            self.assert_rejected(text, "duplicate")

    def test_aliases_anchors_merges_and_tags_rejected(self):
        for replacement in [
            "on: *triggers",
            "on: &triggers\n  push:\n    branches: [main]",
            "on:\n  <<: *triggers",
            "on: !!map\n  push:\n    branches: [main]",
        ]:
            self.assert_rejected(VALID.replace("on:\n  push:\n    branches: [main]\n  workflow_dispatch:", replacement))
        self.assert_rejected(VALID.replace("    runs-on:", "    <<: *defaults\n    runs-on:"))

    def test_shell_blocks_and_comments_do_not_create_yaml_controls(self):
        text = VALID.replace("run: python3 --version", "run: |\n          on:\n            pull_request:\n          echo '*alias &anchor !tag'\n          # shell comment\n          printf '\\t'\n          echo ref: dev")
        self.assertEqual(policy.check_workflow(text), [])
        self.assertEqual(policy.check_workflow("# on: [pull_request]\n" + VALID.replace("branches: [main]", "branches: [main] # approved")), [])

    def test_unknown_or_malformed_yaml_fails_closed(self):
        for text in ["", "---\n" + VALID, VALID + "...\n", VALID.replace("    if:", "\tif:"), "{on: push}", VALID.replace("jobs:\n", "jobs: []\n")]:
            self.assert_rejected(text)

    def test_guarded_reusable_caller_and_code_selection(self):
        text = VALID[:VALID.index("    runs-on:")] + "    uses: org/repo/.github/workflows/check.yml@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
        self.assertEqual(policy.check_workflow(text), [])
        self.assert_rejected(text + "    with:\n      ref: dev\n", "code selection")

    def test_external_actions_and_reusable_workflows_require_full_immutable_refs(self):
        approved = "actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09"
        for uses in ["actions/checkout@main", "actions/checkout@v5", "actions/checkout@abc123",
                     "actions/checkout", "actions/checkout@" + "z" * 40,
                     "actions/checkout@${{ inputs.ref }}", "org/repo/path@dev"]:
            with self.subTest(uses=uses):
                self.assert_rejected(VALID.replace(approved, uses), "immutable")
        reusable = VALID[:VALID.index("    runs-on:")] + "    uses: org/repo/.github/workflows/check.yml@dev\n"
        self.assert_rejected(reusable, "immutable")
        self.assertEqual(policy.check_workflow(reusable.replace("@dev", "@" + "a" * 40)), [])

    def test_local_actions_and_digest_pinned_docker_actions(self):
        approved = "actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09"
        for uses in ["./.github/actions/check", "docker://alpine@sha256:" + "a" * 64,
                     "docker://registry.example:5000/org/image@sha256:" + "b" * 64]:
            with self.subTest(uses=uses):
                # Existing checkout options are irrelevant to a non-checkout action.
                self.assertEqual(policy.check_workflow(VALID.replace(approved, uses)), [])
        for uses in ["./../outside", "./", "docker://alpine:latest", "docker://alpine@sha256:abc"]:
            with self.subTest(uses=uses):
                self.assert_rejected(VALID.replace(approved, uses), "immutable")
        reusable = VALID[:VALID.index("    runs-on:")] + "    uses: ./.github/workflows/check.yml\n"
        self.assertEqual(policy.check_workflow(reusable), [])

    def test_organization_workflow_uses_current_supported_subset(self):
        workflow = SCRIPT.parents[1] / ".github/workflows/docs.yml"
        self.assertEqual(policy.check_workflow(workflow.read_text()), [])


if __name__ == "__main__":
    unittest.main()
