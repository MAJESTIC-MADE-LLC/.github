from __future__ import annotations

import copy
import json
import plistlib
import unittest

import test_foundation_git as fixtures

foundation = fixtures.foundation
NAMES = ('majestic_hosting', 'majestic_sync', 'majestic_sync_crypto')


class HostingAdoptionTest(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.GitSourceTests('runTest')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        for name in NAMES:
            package = f.provider / 'packages' / name
            (package / 'lib').mkdir(parents=True)
            (package / 'lib' / f'{name}.dart').write_text('const scope = 1;\n')
            spec = f'name: {name}\nversion: 0.1.0\n'
            if name == 'majestic_hosting':
                spec += 'dependencies:\n  majestic_sync:\n    path: ../majestic_sync\n  majestic_sync_crypto:\n    path: ../majestic_sync_crypto\n'
            (package / 'pubspec.yaml').write_text(spec)
        fixtures.git(f.provider, 'add', '.')
        fixtures.git(f.provider, 'commit', '-m', 'qualified product hosting')
        self.revision = fixtures.git(f.provider, 'rev-parse', 'HEAD')
        mirror = f.cache / 'git/cache' / ('App-Template-' + fixtures.hashlib.sha1(fixtures.URL.encode()).hexdigest())
        fixtures.git(mirror, 'fetch', str(f.provider), 'dev')
        checkout = f.cache / 'git' / ('App-Template-' + self.revision)
        fixtures.git(f.provider, 'clone', str(mirror), str(checkout))
        fixtures.git(checkout, 'checkout', '--detach', self.revision)
        consumer, policy, matrix = f.consumer_fixture()
        consumer.update(id='Pantry-Clock', kind='application')
        caps = {'user_owned_hosting': 'required'}
        matrix = {'consumers': [{'id': consumer['id'], 'capabilities': caps}]}
        self.configs = {name: {'path': f'App-Template/packages/{name}', 'version': '0.1.0',
                               'capabilities': ['user_owned_hosting'],
                               'git': {'url': fixtures.URL, 'ref': self.revision, 'path': f'packages/{name}'}}
                        for name in NAMES}
        policy['optionalSharedPackages'] = copy.deepcopy(self.configs)
        policy['hostingPolicy'] = {'capability': 'user_owned_hosting', 'packages': list(NAMES),
                                   'approvedConsumers': ['Pantry-Clock'], 'dependencyPins': {}}
        manifest = foundation.read_json(f.app / 'foundation.json')
        manifest.update(application=consumer['id'], capabilities=caps)
        for name, config in self.configs.items():
            manifest['packages'][name] = {'version': config['version'], 'git': config['git']}
        (f.app / 'foundation.json').write_text(json.dumps(manifest))
        spec = (f.app / 'pubspec.yaml').read_text()
        additions = ''.join(f'  {name}:\n    git:\n      url: {fixtures.URL}\n      ref: {self.revision}\n      path: packages/{name}\n' for name in NAMES)
        (f.app / 'pubspec.yaml').write_text(spec.replace('hooks:\n', additions + 'hooks:\n'))
        lock = (f.app / 'pubspec.lock').read_text()
        lock += ''.join(f'  {name}:\n    description:\n      path: packages/{name}\n      url: {fixtures.URL}\n      ref: {self.revision}\n      resolved-ref: {self.revision}\n    source: git\n    version: "0.1.0"\n' for name in NAMES)
        (f.app / 'pubspec.lock').write_text(lock)
        config = foundation.read_json(f.app / '.dart_tool/package_config.json')
        config['packages'] += [{'name': name, 'rootUri': (checkout / f'packages/{name}').as_uri(), 'packageUri': 'lib/'} for name in NAMES]
        (f.app / '.dart_tool/package_config.json').write_text(json.dumps(config))
        (f.app / 'lib/main.dart').write_text(''.join(f"import 'package:{name}/{name}.dart';\n" for name in ('majestic_app', *NAMES)))
        (f.app / 'android/app/src/main').mkdir(parents=True)
        (f.app / 'android/app/src/main/AndroidManifest.xml').write_text('<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.INTERNET" /></manifest>')
        (f.app / 'ios/Runner').mkdir()
        (f.app / 'ios/Runner/Info.plist').write_bytes(plistlib.dumps({'NSLocalNetworkUsageDescription': 'Connect to the selected household host.'}))
        self.args = consumer, policy, matrix

    def inspect(self):
        return foundation.inspect_consumer(*self.args, self.fixture.workspace)

    def test_approved_hosting_uses_actual_immutable_git_cache_and_keeps_core_revision(self):
        result = self.inspect()
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['immutablePackageRevisions'], 'passed')
        revisions = {row['package']: row['ref'] for row in result['verifiedPackageSources']}
        self.assertEqual(revisions['majestic_app'], self.fixture.revision)
        self.assertTrue(all(revisions[name] == self.revision for name in NAMES))
        self.assertEqual(result['foundationEvidence'], 'pending')

    def test_optional_hosting_mutable_refs_overrides_and_cache_substitution_fail_closed(self):
        f = self.fixture
        cases = [
            ('pubspec.yaml', lambda text: text.replace(self.revision, 'dev')),
            ('pubspec.lock', lambda text: text.replace('resolved-ref: ' + self.revision, 'resolved-ref: ' + 'b' * 40)),
            ('pubspec.yaml', lambda text: text + '\ndependency_overrides:\n  majestic_sync:\n    path: ../App-Template/packages/majestic_sync\n'),
            ('.dart_tool/package_config.json', lambda text: text.replace('App-Template-' + self.revision, 'App-Template-' + f.revision)),
        ]
        for name, transform in cases:
            path = f.app / name
            original = path.read_text()
            with self.subTest(name=name):
                path.write_text(transform(original))
                result = self.inspect()
                self.assertEqual(result['immutablePackageRevisions'], 'pending')
                self.assertTrue(result['errors'])
            path.write_text(original)

    def test_missing_capability_or_package_cannot_partially_adopt_hosting(self):
        f = self.fixture
        original = (f.app / 'foundation.json').read_text()
        manifest = json.loads(original)
        manifest['capabilities'] = {}
        self.args[2]['consumers'][0]['capabilities'] = {}
        (f.app / 'foundation.json').write_text(json.dumps(manifest))
        self.assertTrue(any('requires declared user_owned_hosting' in error for error in self.inspect()['errors']))
        (f.app / 'foundation.json').write_text(original)
        self.args[2]['consumers'][0]['capabilities'] = {'user_owned_hosting': 'required'}
        manifest = json.loads(original)
        del manifest['packages']['majestic_sync_crypto']
        (f.app / 'foundation.json').write_text(json.dumps(manifest))
        self.assertTrue(any('complete approved package set' in error for error in self.inspect()['errors']))

    def test_default_template_and_other_apps_reject_even_valid_hosting_sources(self):
        consumer, policy, matrix = self.args
        for identifier, kind in [('App-Template', 'template'), ('Paws', 'application')]:
            with self.subTest(identifier=identifier):
                consumer.update(id=identifier, kind=kind)
                manifest = foundation.read_json(self.fixture.app / 'foundation.json')
                manifest['application'] = identifier
                (self.fixture.app / 'foundation.json').write_text(json.dumps(manifest))
                matrix['consumers'][0]['id'] = identifier
                self.assertTrue(any('not approved for this consumer' in error for error in self.inspect()['errors']))

    def test_native_network_permission_and_disclosure_are_required(self):
        f = self.fixture
        (f.app / 'android/app/src/main/AndroidManifest.xml').write_text('<manifest />')
        (f.app / 'ios/Runner/Info.plist').write_bytes(plistlib.dumps({'NSBonjourServices': ['_unreviewed._tcp']}))
        errors = self.inspect()['errors']
        self.assertIn('hosting requires an explicit Android INTERNET permission', errors)
        self.assertIn('hosting requires an explicit iOS local-network purpose', errors)
        self.assertIn('manual hosting pairing must not declare unused Bonjour discovery', errors)


if __name__ == '__main__':
    unittest.main()
