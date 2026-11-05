from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_foundation.py'
SPEC = importlib.util.spec_from_file_location('foundation_git', SCRIPT)
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)
URL = 'https://example.test/App-Template.git'


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL, text=True).strip()


class GitSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='foundation git ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.workspace = self.root / 'workspace'
        self.provider = self.workspace / 'App-Template'
        self.package = self.provider / 'packages/majestic_app'
        (self.package / 'lib').mkdir(parents=True)
        (self.package / 'ios/Sources').mkdir(parents=True)
        (self.package / 'assets').mkdir()
        (self.package / 'lib/majestic_app.dart').write_text('const version = 1;\n')
        (self.package / 'ios/Sources/Privacy.swift').write_text('// native implementation\n')
        (self.package / 'assets/offline.bin').write_bytes(b'qualified offline asset')
        (self.package / 'pubspec.yaml').write_text('name: majestic_app\nversion: 0.1.0\n')
        git(self.provider, 'init', '-b', 'dev')
        git(self.provider, 'config', 'user.name', 'Synthetic qualification fixture')
        git(self.provider, 'config', 'user.email', 'fixture@example.test')
        git(self.provider, 'add', '.')
        git(self.provider, 'commit', '-m', 'qualified fixture')
        self.revision = git(self.provider, 'rev-parse', 'HEAD')
        self.source = {'url': URL, 'ref': self.revision, 'path': 'packages/majestic_app'}
        self.config = {'path': 'App-Template/packages/majestic_app', 'version': '0.1.0', 'git': self.source}
        self.cache = self.root / 'pub cache'
        self.checkout = self.make_cache(self.cache)
        self.app = self.workspace / 'consumer'
        (self.app / 'lib').mkdir(parents=True)
        (self.app / 'lib/main.dart').write_text("import 'package:majestic_app/majestic_app.dart';\n")
        (self.app / '.dart_tool').mkdir()
        self.write_config(self.checkout / self.source['path'])
        self.env = mock.patch.dict(os.environ, {'PUB_CACHE': str(self.cache)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def make_cache(self, cache: Path) -> Path:
        mirror = cache / 'git/cache' / ('App-Template-' + hashlib.sha1(URL.encode()).hexdigest())
        mirror.parent.mkdir(parents=True)
        git(self.provider, 'clone', '--bare', str(self.provider), str(mirror))
        git(mirror, 'config', 'remote.origin.url', URL)
        checkout = cache / 'git' / ('App-Template-' + self.revision)
        git(self.provider, 'clone', str(mirror), str(checkout))
        git(checkout, 'checkout', '--detach', self.revision)
        return checkout

    def write_config(self, package: Path):
        (self.app / '.dart_tool/package_config.json').write_text(json.dumps({'configVersion': 2, 'packages': [
            {'name': 'majestic_app', 'rootUri': package.as_uri(), 'packageUri': 'lib/'}]}))

    def verify(self):
        package = foundation.package_config_roots(self.app)['majestic_app']
        return foundation.qualified_git_package('majestic_app', self.config, package, self.workspace)

    def consumer_fixture(self):
        policy = foundation.read_json(foundation.STANDARD_PATH)
        policy = {**policy, 'packages': {'majestic_app': self.config}, 'optionalSharedPackages': {},
                  'coreDependencies': {}, 'optionalDependencies': {}, 'compatibilityDependencies': {},
                  'resolvedPlatformDependencies': {}}
        consumer = {'id': 'consumer', 'path': 'consumer', 'kind': 'template'}
        matrix = {'consumers': [{'id': 'consumer', 'capabilities': {}}]}
        manifest = {'schemaVersion': 1, 'application': 'consumer', 'foundationVersion': policy['foundationVersion'],
                    'status': 'adopting', 'toolchain': policy['toolchain'], 'packageProvenance': 'git-immutable',
                    'capabilities': {}, 'packages': {'majestic_app': {'version': '0.1.0', 'git': self.source}}}
        (self.app / 'foundation.json').write_text(json.dumps(manifest))
        (self.app / '.flutter-version').write_text(policy['toolchain']['flutter'])
        (self.app / 'pubspec.yaml').write_text(f'''name: consumer
environment:
  sdk: "{policy['toolchain']['dartConstraint']}"
dependencies:
  majestic_app:
    git:
      url: {URL}
      ref: {self.revision}
      path: packages/majestic_app
hooks:
  user_defines:
    sqlite3:
      source: sqlite3mc
''')
        (self.app / 'pubspec.lock').write_text(f'''packages:
  majestic_app:
    description:
      path: packages/majestic_app
      ref: {self.revision}
      resolved-ref: {self.revision}
      url: {URL}
    source: git
    version: "0.1.0"
''')
        (self.app / 'ios').mkdir()
        (self.app / 'android/app').mkdir(parents=True)
        (self.app / 'android/gradle/wrapper').mkdir(parents=True)
        (self.app / 'android/settings.gradle.kts').write_text('id("com.android.application") version "9.1.0"\nid("org.jetbrains.kotlin.android") version "2.4.0"\n')
        (self.app / 'android/gradle/wrapper/gradle-wrapper.properties').write_text('distributionUrl=https://services.gradle.org/distributions/gradle-9.3.1-all.zip\n')
        (self.app / 'android/app/build.gradle.kts').write_text('sourceCompatibility = JavaVersion.VERSION_17\ntargetCompatibility = JavaVersion.VERSION_17\njvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17\n')
        git(self.app, 'init', '-b', 'dev')
        return consumer, policy, matrix

    def test_consumer_git_manifest_lock_and_override_mismatches_fail_closed(self):
        args = self.consumer_fixture()
        valid = foundation.inspect_consumer(*args, self.workspace)
        self.assertEqual(valid['errors'], [])
        self.assertEqual(valid['immutablePackageRevisions'], 'passed')
        for filename, transform in [
            ('foundation.json', lambda s: s.replace(self.revision, 'dev')),
            ('pubspec.yaml', lambda s: s.replace(URL, 'https://example.test/other.git')),
            ('pubspec.lock', lambda s: s.replace('resolved-ref: ' + self.revision, 'resolved-ref: ' + 'a' * 40)),
            ('pubspec.lock', lambda s: s.replace('source: git', 'source: path')),
            ('pubspec.yaml', lambda s: s + '\ndependency_overrides:\n  majestic_app:\n    path: ../App-Template/packages/majestic_app\n'),
        ]:
            path = self.app / filename; original = path.read_text()
            with self.subTest(filename=filename, transform=transform):
                path.write_text(transform(original))
                result = foundation.inspect_consumer(*args, self.workspace)
                self.assertEqual(result['staticAdoption'], 'pending')
                self.assertEqual(result['immutablePackageRevisions'], 'pending')
                path.write_text(original)
        override = self.app / 'pubspec_overrides.yaml'
        override.write_text('dependency_overrides:\n  majestic_app:\n    path: ../App-Template/packages/majestic_app\n')
        self.assertEqual(foundation.inspect_consumer(*args, self.workspace)['immutablePackageRevisions'], 'pending')

    def test_workspace_mode_stays_available_but_cannot_pass_production_provenance(self):
        args = self.consumer_fixture()
        path = '../App-Template/packages/majestic_app'
        manifest = json.loads((self.app / 'foundation.json').read_text())
        manifest.update(packageProvenance='workspace-unpublished', packages={'majestic_app': {'version': '0.1.0', 'path': path}})
        (self.app / 'foundation.json').write_text(json.dumps(manifest))
        spec = (self.app / 'pubspec.yaml').read_text()
        start = spec.index('    git:\n'); end = spec.index('hooks:\n')
        (self.app / 'pubspec.yaml').write_text(spec[:start] + '    path: ' + path + '\n' + spec[end:])
        (self.app / 'pubspec.lock').write_text(f'packages:\n  majestic_app:\n    description:\n      path: {path}\n    source: path\n    version: "0.1.0"\n')
        self.write_config(self.package)
        result = foundation.inspect_consumer(*args, self.workspace)
        self.assertIn('package provenance differs from the approved production baseline', result['errors'])
        self.assertEqual(result['immutablePackageRevisions'], 'pending')
        self.assertTrue(foundation.immutable_revision_errors([result]))

    def test_portfolio_workflow_deduplication_retains_flutter_version_checks(self):
        args = self.consumer_fixture()
        workflows = self.app / '.github/workflows'
        workflows.mkdir(parents=True)
        (workflows / 'ci.yml').write_text('''on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  verify:
    if: ${{ github.ref == 'refs/heads/main' && github.event_name == 'push' }}
    steps:
      - uses: subosito/flutter-action@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        with:
          flutter-version: 0.0.0
''')
        result = foundation.inspect_consumer(*args, self.workspace, validate_workflows=False)
        self.assertTrue(any('Flutter CI SDK' in error for error in result['errors']))

    def test_real_git_objects_and_encoded_cache_uri_are_qualified(self):
        qualified = self.verify()
        self.assertIn(self.revision, qualified['identity'])
        self.assertEqual(len(qualified['contentSha256']), 64)
        self.assertEqual(qualified['root'], self.checkout / self.source['path'])

    def test_object_checks_are_deduplicated_only_within_one_invocation(self):
        with mock.patch.object(foundation, 'git_read', wraps=foundation.git_read) as read:
            with foundation.git_verification_scope():
                self.verify()
                with foundation.git_verification_scope():
                    self.verify()
            fsck = [call for call in read.call_args_list if call.args[1] == 'fsck']
            # Provider and Pub checkout are separate object databases.
            self.assertEqual(len(fsck), 2)
            with foundation.git_verification_scope():
                self.verify()
            self.assertEqual(sum(call.args[1] == 'fsck' for call in read.call_args_list), 4)

    def test_deduplicated_objects_never_cache_mutable_package_bytes(self):
        with foundation.git_verification_scope():
            self.verify()
            path = self.checkout / self.source['path'] / 'lib/majestic_app.dart'
            path.write_text('// changed during validation\n')
            with self.assertRaisesRegex(foundation.FoundationError, 'content differs'):
                self.verify()

    def test_failed_object_checks_are_not_cached(self):
        original = foundation.git_read
        attempts = 0

        def fail_once(repository, *args):
            nonlocal attempts
            if args[0] == 'fsck':
                attempts += 1
                if attempts == 1:
                    raise foundation.FoundationError('synthetic corrupt objects')
            return original(repository, *args)

        with foundation.git_verification_scope(), mock.patch.object(foundation, 'git_read', side_effect=fail_once):
            with self.assertRaisesRegex(foundation.FoundationError, 'corrupt objects'):
                self.verify()
            self.verify()
        self.assertEqual(attempts, 3)

    def test_cached_dart_native_asset_and_extra_source_tampering_are_rejected(self):
        for relative in ['lib/majestic_app.dart', 'ios/Sources/Privacy.swift', 'assets/offline.bin']:
            path = self.checkout / self.source['path'] / relative
            original = path.read_bytes()
            with self.subTest(relative=relative):
                path.write_bytes(original + b'changed')
                with self.assertRaisesRegex(foundation.FoundationError, 'content differs'):
                    self.verify()
                path.write_bytes(original)
        extra = self.checkout / self.source['path'] / 'lib/unreviewed.dart'
        extra.write_text('// injected runtime source\n')
        with self.assertRaisesRegex(foundation.FoundationError, 'extra package file'):
            self.verify()

    def test_cache_symlinks_and_provider_source_drift_are_rejected(self):
        path = self.checkout / self.source['path'] / 'lib/majestic_app.dart'
        path.unlink()
        path.symlink_to(self.package / 'lib/majestic_app.dart')
        with self.assertRaisesRegex(foundation.FoundationError, 'symlink'):
            self.verify()
        path.unlink()
        path.write_bytes((self.package / 'lib/majestic_app.dart').read_bytes())
        (self.package / 'lib/majestic_app.dart').write_text('// changed provider\n')
        with self.assertRaisesRegex(foundation.FoundationError, 'content differs'):
            self.verify()

    def test_provider_later_root_only_commit_does_not_require_self_reference(self):
        (self.provider / 'README.md').write_text('Root app now consumes the previous package commit.\n')
        git(self.provider, 'add', 'README.md')
        git(self.provider, 'commit', '-m', 'root app integration')
        self.assertNotEqual(git(self.provider, 'rev-parse', 'HEAD'), self.revision)
        self.verify()

    def test_development_guard_allows_provider_edits_but_not_consumer_cache_edits(self):
        (self.package / 'lib/majestic_app.dart').write_text('// upcoming maintained implementation\n')
        with self.assertRaises(foundation.FoundationError):
            self.verify()  # Release qualification still compares provider source.
        package = foundation.package_config_roots(self.app)['majestic_app']
        result = foundation.qualified_git_package('majestic_app', self.config, package, self.workspace,
                                                  verify_provider_worktree=False)
        self.assertEqual(result['source']['ref'], self.revision)
        (package / 'lib/majestic_app.dart').write_text('// modified pinned consumer source\n')
        with self.assertRaises(foundation.FoundationError):
            foundation.qualified_git_package('majestic_app', self.config, package, self.workspace,
                                             verify_provider_worktree=False)

    def test_tracked_git_package_files_are_not_relaxed_by_app_generated_exclusions(self):
        path = self.package / 'ios/Flutter/Generated.xcconfig'
        path.parent.mkdir(parents=True)
        path.write_text('qualified tracked package content\n')
        git(self.provider, 'add', '.')
        git(self.provider, 'commit', '-m', 'tracked package native input')
        source = {**self.source, 'ref': git(self.provider, 'rev-parse', 'HEAD')}
        foundation.git_package_content(self.provider, source)
        path.write_text('changed tracked package content\n')
        with self.assertRaisesRegex(foundation.FoundationError, 'content differs'):
            foundation.git_package_content(self.provider, source)

    def test_package_map_cannot_redirect_a_git_lock_to_workspace_source(self):
        self.write_config(self.package)
        with self.assertRaisesRegex(foundation.FoundationError, 'Pub Git cache'):
            self.verify()

    def test_wrong_cache_head_and_wrong_mirror_origin_are_rejected(self):
        mirror = self.cache / 'git/cache' / ('App-Template-' + hashlib.sha1(URL.encode()).hexdigest())
        git(mirror, 'config', 'remote.origin.url', 'https://example.test/wrong.git')
        with self.assertRaisesRegex(foundation.FoundationError, 'mirror URL'):
            self.verify()
        git(mirror, 'config', 'remote.origin.url', URL)
        git(self.checkout, 'config', 'user.name', 'Synthetic fixture')
        git(self.checkout, 'config', 'user.email', 'fixture@example.test')
        git(self.checkout, 'commit', '--allow-empty', '-m', 'unapproved cached HEAD')
        with self.assertRaisesRegex(foundation.FoundationError, 'not at the qualified'):
            self.verify()

    def test_forged_object_file_is_not_accepted_as_a_real_commit(self):
        obj = self.provider / '.git/objects' / self.revision[:2] / self.revision[2:]
        body = zlib.decompress(obj.read_bytes())
        obj.chmod(0o600)
        obj.write_bytes(zlib.compress(body.replace(b'qualified fixture', b'forged---fixture')))
        with self.assertRaises(foundation.FoundationError):
            foundation.git_package_content(self.provider, self.source)

    def test_fingerprint_uses_qualified_identity_not_machine_cache_location(self):
        first = self.verify()
        before = foundation.source_fingerprint(self.app, [first['root']], self.workspace, {first['root']: first})
        cache2 = self.root / 'other-cache-location'
        checkout2 = self.make_cache(cache2)
        self.write_config(checkout2 / self.source['path'])
        with mock.patch.dict(os.environ, {'PUB_CACHE': str(cache2)}):
            second = self.verify()
            after = foundation.source_fingerprint(self.app, [second['root']], self.workspace, {second['root']: second})
        self.assertEqual(before, after)
        changed = {**second, 'identity': second['identity'] + '-different-revision'}
        self.assertNotEqual(before, foundation.source_fingerprint(self.app, [second['root']], self.workspace, {second['root']: changed}))

    def test_descriptor_requires_full_sha_safe_path_and_credential_free_url(self):
        for delta in [{'ref': 'dev'}, {'ref': self.revision[:12]}, {'path': '../outside'},
                      {'path': 'packages/../outside'}, {'url': 'https://token@example.test/repo.git'},
                      {'url': 'file:///tmp/local.git'}, {'tag_pattern': 'v1'}]:
            with self.subTest(delta=delta):
                with self.assertRaises(foundation.FoundationError):
                    foundation.git_descriptor({**self.source, **delta})

    def test_package_config_rejects_duplicate_or_remote_entries(self):
        path = self.app / '.dart_tool/package_config.json'
        value = json.loads(path.read_text())
        value['packages'].append(value['packages'][0])
        path.write_text(json.dumps(value))
        with self.assertRaises(foundation.FoundationError):
            foundation.package_config_roots(self.app)
        self.write_config(self.checkout / self.source['path'])
        value = json.loads(path.read_text()); value['packages'][0]['rootUri'] = 'https://example.test/source'
        path.write_text(json.dumps(value))
        with self.assertRaises(foundation.FoundationError):
            foundation.package_config_roots(self.app)


class GitDescriptorParsingTests(unittest.TestCase):
    def test_nested_git_pubspec_and_resolved_lock_commit_are_preserved(self):
        ref = 'a' * 40
        spec = foundation.parse_pubspec(f'''dependencies:
  majestic_app:
    git:
      url: {URL}
      ref: {ref}
      path: packages/majestic_app
''')
        self.assertEqual(spec['dependencies']['majestic_app']['git'], {'url': URL, 'ref': ref, 'path': 'packages/majestic_app'})
        lock = foundation.parse_lock(f'''packages:
  majestic_app:
    description:
      path: packages/majestic_app
      ref: {ref}
      resolved-ref: {ref}
      url: {URL}
    source: git
    version: "0.1.0"
''')
        self.assertEqual(lock['majestic_app']['resolved-ref'], ref)
        self.assertEqual(lock['majestic_app']['url'], URL)

    def test_duplicate_git_and_lock_descriptors_fail_closed(self):
        with self.assertRaises(foundation.FoundationError):
            foundation.parse_pubspec('dependencies:\n  x:\n    git:\n      ref: first\n      ref: second\n')
        with self.assertRaises(foundation.FoundationError):
            foundation.parse_lock('packages:\n  x:\n    source: path\n    source: git\n')

    def test_production_gate_accepts_only_validated_git_results(self):
        good = {'application': 'qualified', 'packageProvenance': 'git-immutable', 'immutablePackageRevisions': 'passed', 'staticAdoption': 'passed'}
        self.assertEqual(foundation.immutable_revision_errors([good]), [])
        for delta in [{'packageProvenance': 'workspace-unpublished'}, {'immutablePackageRevisions': 'pending'}, {'staticAdoption': 'pending'}]:
            self.assertTrue(foundation.immutable_revision_errors([{**good, **delta}]))


if __name__ == '__main__':
    unittest.main()
