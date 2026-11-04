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
        self.root = Path(self.temp.name).resolve()

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
        self.assertTrue(guard.governed('ios/Flutter/MajesticCrypto.xcconfig'))
        self.assertTrue(guard.governed('ios/Flutter/Release.xcconfig'))

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

    def test_optional_hosting_registry_requires_explicit_native_consumers_and_one_immutable_source(self):
        standard = guard.foundation.read_json(guard.ROOT / 'portfolio/STACK_STANDARD.json')
        self.assertEqual(guard.hosting_policy_errors(standard), [])
        for change in (
            lambda policy: policy['hostingPolicy'].update(approvedConsumers=['App-Template']),
            lambda policy: policy['hostingPolicy'].update(approvedConsumers=['future-unregistered-app']),
            lambda policy: policy['hostingPolicy'].update(capability='network_lookup'),
            lambda policy: policy['hostingPolicy']['packages'].pop(),
            lambda policy: policy['optionalSharedPackages']['majestic_sync']['git'].update(ref='dev'),
            lambda policy: policy['optionalSharedPackages']['majestic_sync']['git'].update(ref='a' * 40),
            lambda policy: policy['optionalSharedPackages']['majestic_sync'].update(capabilities=['network_lookup']),
        ):
            candidate = copy.deepcopy(standard)
            change(candidate)
            self.assertTrue(guard.hosting_policy_errors(candidate))

    def test_qualified_harness_keeps_only_parent_path_and_the_same_three_git_modules(self):
        parent = self.root / 'app'
        root = parent / 'hosting_pilot'
        root.mkdir(parents=True)
        modules = ('majestic_hosting', 'majestic_sync', 'majestic_sync_crypto')
        revision = 'a' * 40
        url = 'https://github.com/MAJESTIC-MADE-LLC/App-Template.git'
        sources = {name: {'version': '0.1.0', 'git': {
            'url': url, 'ref': revision, 'path': f'packages/{name}'}} for name in modules}
        dependencies = ''.join(f'  {name}:\n    git:\n      url: {url}\n      ref: {revision}\n      path: packages/{name}\n' for name in modules)
        parent_spec = 'name: app\ndependencies:\n' + dependencies
        pilot_spec = ('name: pilot\ndependencies:\n  app:\n    path: ..\n' + dependencies +
                      'hooks:\n  user_defines:\n    sqlite3:\n      source: sqlite3mc\n')
        parent_lock = 'packages:\n' + ''.join(
            f'  {name}:\n    source: git\n    version: "0.1.0"\n    description:\n      url: {url}\n      ref: {revision}\n      resolved-ref: {revision}\n      path: packages/{name}\n' for name in modules)
        pilot_lock = parent_lock + '  app:\n    source: path\n    description:\n      path: ..\n    version: "1.0.0"\n'
        for name, text in [('pubspec.yaml', pilot_spec), ('pubspec.lock', pilot_lock), ('.flutter-version', '3.47.8\n')]:
            (root / name).write_text(text)
        (parent / 'pubspec.yaml').write_text(parent_spec)
        (parent / 'pubspec.lock').write_text(parent_lock)
        profile = {'path': 'app/hosting_pilot', 'productionApp': 'app',
                   'kind': 'optional-hosting-consumer', 'pathSources': {'app': 'app'}}
        standard = {'toolchain': {'flutter': '3.47.8'}, 'packages': {}, 'optionalSharedPackages': sources,
                    'coreDependencies': {}, 'compatibilityDependencies': {}, 'resolvedPlatformDependencies': {},
                    'optionalDependencies': {}, 'prohibitedProviderPrefixes': ['firebase'], 'prohibitedProviderPackages': [],
                    'consumers': [{'id': 'Pantry-Clock', 'path': 'app', 'kind': 'application'}],
                    'hostingPolicy': {'packages': list(modules), 'approvedConsumers': ['Pantry-Clock']}}
        resolved = {'app': parent, **{name: self.root / name for name in modules}}
        with patch.object(guard.foundation, 'package_config_roots', return_value=resolved), \
                patch.object(guard.foundation, 'qualified_git_package') as qualify:
            self.assertEqual(guard.check_development_pilot(self.root, profile, standard), [])
            self.assertEqual(qualify.call_count, 3)
            for spec in (pilot_spec.replace(revision, 'dev'),
                         pilot_spec + '\ndependency_overrides:\n  majestic_sync:\n    path: ../../majestic_sync\n'):
                (root / 'pubspec.yaml').write_text(spec)
                self.assertTrue(guard.check_development_pilot(self.root, profile, standard))
            (root / 'pubspec.yaml').write_text(pilot_spec)
            hidden_override = root / 'pubspec_overrides.yaml'
            hidden_override.write_text('dependency_overrides:\n  majestic_sync:\n    path: ../../majestic_sync\n')
            self.assertIn('qualified hosting harness overrides must be declared in its registered manifest',
                          guard.check_development_pilot(self.root, profile, standard))
            hidden_override.unlink()
            profile['pathSources']['majestic_sync'] = 'majestic_sync'
            self.assertTrue(guard.check_development_pilot(self.root, profile, standard))
            del profile['pathSources']['majestic_sync']
            (parent / 'pubspec.lock').write_text(parent_lock.replace(revision, 'b' * 40))
            self.assertTrue(any('same immutable hosting source' in error for error in
                                guard.check_development_pilot(self.root, profile, standard)))
            (parent / 'pubspec.lock').write_text(parent_lock)
            standard['hostingPolicy']['approvedConsumers'] = ['another-app']
            self.assertIn('qualified hosting harness parent is not an approved consumer',
                          guard.check_development_pilot(self.root, profile, standard))

    def test_development_pilot_cannot_drift_or_leak_into_the_production_graph(self):
        parent = self.root / 'app'
        root = parent / 'hosting_pilot'
        shared = self.root / 'foundation/majestic_sync'
        for path in (parent, root, shared):
            path.mkdir(parents=True, exist_ok=True)
        (parent / 'pubspec.yaml').write_text('name: app\ndependencies:\n  flutter:\n    sdk: flutter\n')
        parent_lock = 'packages:\n  drift:\n    source: hosted\n    version: "2.35.0"\n'
        (parent / 'pubspec.lock').write_text(parent_lock)
        (root / '.flutter-version').write_text('3.47.8\n')
        (root / 'pubspec.yaml').write_text('''name: pilot
dependencies:
  app:
    path: ..
  majestic_sync:
    path: ../../foundation/majestic_sync
hooks:
  user_defines:
    sqlite3:
      source: sqlite3mc
''')
        pilot_lock = parent_lock + '''  app:
    source: path
    description:
      path: ..
    version: "1.0.0"
  majestic_sync:
    source: path
    description:
      path: ../../foundation/majestic_sync
    version: "0.1.0"
'''
        (root / 'pubspec.lock').write_text(pilot_lock)
        profile = {'path': 'app/hosting_pilot', 'productionApp': 'app',
                   'kind': 'optional-hosting-development',
                   'pathSources': {'app': 'app', 'majestic_sync': 'foundation/majestic_sync'}}
        standard = {'toolchain': {'flutter': '3.47.8'}, 'packages': {}, 'optionalSharedPackages': {},
                    'coreDependencies': {'drift': '2.35.0'}, 'compatibilityDependencies': {},
                    'resolvedPlatformDependencies': {}, 'optionalDependencies': {},
                    'prohibitedProviderPrefixes': ['firebase'], 'prohibitedProviderPackages': []}
        with patch.object(guard.foundation, 'package_config_roots', return_value={'app': parent, 'majestic_sync': shared}):
            self.assertEqual(guard.check_development_pilot(self.root, profile, standard), [])
            (root / 'pubspec.lock').write_text(pilot_lock.replace('2.35.0', '9.9.9'))
            self.assertTrue(guard.check_development_pilot(self.root, profile, standard))
            (root / 'pubspec.lock').write_text(pilot_lock)
            (parent / 'pubspec.lock').write_text(parent_lock + '  majestic_sync:\n    source: path\n    version: "0.1.0"\n')
            self.assertIn('development hosting packages leaked into the production app graph',
                          guard.check_development_pilot(self.root, profile, standard))


if __name__ == '__main__':
    unittest.main()
