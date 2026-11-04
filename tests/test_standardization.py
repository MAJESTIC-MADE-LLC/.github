from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_standardization as guard
import install_standardization_hooks as installer


class StandardizationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def node_fixture(self):
        policy = {'nodeExact': '26.13.0', 'sharedDependencies': {'next': '16.4.3', 'react': '19.3.1'}}
        package = {'engines': {'node': '26.13.0'}, 'dependencies': {'next': '16.4.3', 'react': '19.3.1'}}
        lock = {'lockfileVersion': 3, 'packages': {'': copy.deepcopy(package),
                'node_modules/next': {'version': '16.4.3'}, 'node_modules/react': {'version': '19.3.1'}}}
        (self.root / 'package.json').write_text(json.dumps(package))
        (self.root / 'package-lock.json').write_text(json.dumps(lock))
        (self.root / '.nvmrc').write_text('26.13.0\n')
        (self.root / '.npmrc').write_text('engine-strict=true\n')
        return policy

    def test_web_pins_and_lock_resolution_cannot_drift_independently(self):
        policy = self.node_fixture()
        self.assertEqual(guard.check_node(self.root, policy, True), [])
        for name, text in [('package.json', '16.4.3'), ('package-lock.json', '16.4.3'), ('.nvmrc', '26.13.0')]:
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text()
                path.write_text(original.replace(text, '99.0.0'))
                self.assertTrue(guard.check_node(self.root, policy, True))
                path.write_text(original)

    def test_engine_enforcement_cannot_be_disabled_or_overridden(self):
        policy = self.node_fixture()
        for text in ['engine-strict=false\n', '', 'engine-strict=true\nengine-strict=false\n']:
            (self.root / '.npmrc').write_text(text)
            self.assertTrue(guard.check_node(self.root, policy, True))

    def test_deployment_node_version_must_match_local_pin(self):
        policy = self.node_fixture()
        (self.root / 'wrangler.json').write_text(json.dumps({'vars': {'NODE_VERSION': '26.13.0'},
            'env': {'preview': {'vars': {'NODE_VERSION': '24.22.1'}}}}))
        self.assertTrue(guard.check_node(self.root, policy, True))

    def test_baseline_catches_new_dependencies_and_transitive_lock_changes(self):
        self.node_fixture()
        before = guard.dependency_baseline(self.root / 'package.json')
        package = json.loads((self.root / 'package.json').read_text())
        package['dependencies']['surprise'] = '^1.0.0'
        (self.root / 'package.json').write_text(json.dumps(package))
        self.assertNotEqual(before, guard.dependency_baseline(self.root / 'package.json'))
        (self.root / 'package-lock.json').write_text('{}')
        self.assertNotEqual(before['lockSha256'], guard.dependency_baseline(self.root / 'package.json')['lockSha256'])

    def test_manifest_discovery_ignores_historical_and_generated_source(self):
        for name in ['app/pubspec.yaml', 'new-app/package.json', 'app/legacy/package.json',
                     'app/docs/validation/pubspec.yaml', 'app/node_modules/next/package.json']:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{}')
        self.assertEqual(guard.discover_manifests([self.root], self.root),
                         {'app/pubspec.yaml', 'new-app/package.json'})

    def init_repo(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        guard.git(self.root, 'config', 'user.name', 'Fixture')
        guard.git(self.root, 'config', 'user.email', 'fixture@example.invalid')
        (self.root / 'package.json').write_text('{"old": true}\n')
        guard.git(self.root, 'add', 'package.json')
        guard.git(self.root, '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'fixture')

    def test_hook_rejects_good_worktree_hiding_bad_index_or_push_tip(self):
        self.init_repo()
        tip = guard.git(self.root, 'rev-parse', 'HEAD').decode().strip()
        (self.root / 'package.json').write_text('{"approved": true}\n')
        self.assertTrue(guard.snapshot_errors(self.root, None))
        guard.git(self.root, 'add', 'package.json')
        self.assertEqual(guard.snapshot_errors(self.root, None), [])
        self.assertTrue(guard.snapshot_errors(self.root, tip))
        # Partial staging of a governed file must not pass on worktree values.
        (self.root / 'package.json').write_text('{"another": true}\n')
        self.assertTrue(guard.snapshot_errors(self.root, None))

    def test_hook_allows_unstaged_product_code_for_logical_commits(self):
        self.init_repo()
        (self.root / 'feature.dart').write_text('// ordinary product edit\n')
        self.assertEqual(guard.snapshot_errors(self.root, None), [])

    def test_hook_checks_shared_imports_and_native_permission_inputs(self):
        self.init_repo()
        (self.root / 'lib').mkdir()
        app = self.root / 'lib/app.dart'
        app.write_text("import 'package:majestic_app/majestic_app.dart';\n")
        self.assertTrue(guard.snapshot_errors(self.root, None))
        guard.git(self.root, 'add', 'lib/app.dart')
        self.assertEqual(guard.snapshot_errors(self.root, None), [])
        app.write_text('// import removed from this snapshot\n')
        self.assertTrue(guard.snapshot_errors(self.root, None))
        self.assertTrue(guard.governed('hosting/reference_app/ios/Runner/Info.plist'))
        self.assertTrue(guard.governed('hosting/reference_app/android/app/src/main/AndroidManifest.xml'))

    def test_hook_git_reads_ignore_inherited_cross_repository_environment(self):
        self.init_repo()
        with patch.dict(os.environ, {'GIT_DIR': '/absent', 'GIT_INDEX_FILE': '/absent'}):
            self.assertEqual(Path(guard.git(self.root, 'rev-parse', '--show-toplevel').decode().strip()).resolve(), self.root.resolve())

    def test_installer_retains_custom_hooks_without_partial_installation(self):
        self.init_repo()
        hooks = self.root / '.github/.githooks'
        hooks.mkdir(parents=True)
        for name in ('pre-commit', 'pre-push'):
            path = hooks / name
            path.write_text('#!/bin/sh\nexit 0\n')
            path.chmod(0o755)
        custom = self.root / '.git/hooks/pre-commit'
        custom.write_text('#!/bin/sh\nexit 0\n')
        with patch.object(installer, 'repositories', return_value=[self.root]):
            with self.assertRaisesRegex(ValueError, 'existing repository hooks retained'):
                installer.install(self.root)
        self.assertEqual(custom.read_text(), '#!/bin/sh\nexit 0\n')

    def test_checked_in_policy_covers_every_native_and_core_node_project(self):
        policy = guard.foundation.read_json(guard.ROOT / 'portfolio/STANDARDIZATION.json')
        standard = guard.foundation.read_json(guard.ROOT / 'portfolio/STACK_STANDARD.json')
        for consumer in standard['consumers']:
            self.assertIn(consumer['path'] + '/pubspec.yaml', policy['dependencyBaselines'])
        self.assertEqual({p['path'] for p in policy['nodeProjects']},
                         {'Namefold/web', 'Majestic-Made-Hub', 'App-Template/services/workspace_verifier'})
        self.assertEqual(standard['packageProvenance'], 'git-immutable')

    def test_removing_a_consumer_cannot_silently_reduce_the_foundation_gate(self):
        standard = guard.foundation.read_json(guard.ROOT / 'portfolio/STACK_STANDARD.json')
        matrix = guard.foundation.read_json(guard.ROOT / 'portfolio/CAPABILITY_MATRIX.json')
        self.assertEqual(guard.cohort_errors(standard, matrix), [])
        standard['consumers'].pop()
        self.assertTrue(guard.cohort_errors(standard, matrix))


if __name__ == '__main__':
    unittest.main()
