#!/usr/bin/env python3
"""Offline portfolio drift gate. Passing is not release or device qualification."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

if sys.version_info < (3, 11):
    sys.exit('Portfolio standardization requires Python 3.11+ (including the standard-library TOML reader).')

import check_foundation as foundation
import workflow_policy

ROOT = Path(__file__).resolve().parents[1]
SKIP = foundation.IGNORED_PARTS | {
    "legacy", "docs", ".archives", ".next", "out", ".venv", "venv",
    "assets", "vendor", "target", ".playwright-cli",
}


def repositories(workspace: Path) -> list[Path]:
    inventory = foundation.read_json(workspace / '.github/portfolio/REPOSITORIES.json')
    return [foundation.within(workspace, row['name']) for row in inventory['repositories']
            if row.get('localCheckout') and row.get('disposition') != 'excluded']


def discover_manifests(repos: list[Path], workspace: Path) -> set[str]:
    found = set()
    for repo in repos:
        for current, directories, files in os.walk(repo, followlinks=False):
            directories[:] = [d for d in directories if d not in SKIP and not (Path(current) / d).is_symlink()]
            for name in {'pubspec.yaml', 'package.json'} & set(files):
                found.add((Path(current) / name).relative_to(workspace).as_posix())
    return found


def dependency_baseline(path: Path) -> dict[str, str]:
    if path.name == 'pubspec.yaml':
        parsed = foundation.parse_pubspec(path.read_text())
        declarations = {key: parsed[key] for key in ('dependencies', 'dev_dependencies', 'dependency_overrides')}
        lock = path.with_name('pubspec.lock')
    else:
        parsed = foundation.read_json(path)
        declarations = {key: parsed.get(key, {}) for key in
                        ('dependencies', 'devDependencies', 'optionalDependencies', 'overrides', 'engines')}
        lock = path.with_name('package-lock.json')
    digest = hashlib.sha256(json.dumps(declarations, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = {'declarationsSha256': digest}
    # All registered packages in this portfolio commit their resolved lockfiles,
    # including independently validated hosting/reference and shared packages.
    result['lockSha256'] = hashlib.sha256(lock.read_bytes()).hexdigest()
    return result


def cohort_errors(standard: dict, matrix: dict) -> list[str]:
    errors = []
    consumers = standard['consumers']
    expected_ids = set(standard['gate']['requiredApps']) | {standard['gate']['requiredTemplate']}
    if (len(consumers) != len(expected_ids) or {c['id'] for c in consumers} != expected_ids
            or {c['id'] for c in matrix['consumers']} != expected_ids
            or len(matrix['consumers']) != len(expected_ids)):
        errors.append('native consumer inventory must match the complete foundation gate and capability matrix')
    for consumer in consumers:
        expected_path = 'Namefold/app' if consumer['id'] == 'Namefold' else consumer['id']
        expected_kind = 'template' if consumer['id'] == standard['gate']['requiredTemplate'] else 'application'
        if consumer['path'] != expected_path or consumer['kind'] != expected_kind:
            errors.append(f"{consumer['id']}: canonical consumer path/kind differs")
    return errors


def check_node(root: Path, policy: dict, framework: bool) -> list[str]:
    errors = []
    version = policy['nodeExact']
    package = foundation.read_json(root / 'package.json')
    lock = foundation.read_json(root / 'package-lock.json')
    if (root / '.nvmrc').read_text().strip() != version:
        errors.append(f'.nvmrc must equal {version}')
    if (root / '.node-version').exists() and (root / '.node-version').read_text().strip() != version:
        errors.append(f'.node-version must equal {version}')
    if package.get('engines', {}).get('node') != version:
        errors.append(f'package engines.node must equal {version}')
    if lock.get('lockfileVersion') != 3 or lock.get('packages', {}).get('', {}).get('engines', {}).get('node') != version:
        errors.append('lockfile root must use the approved exact Node engine and lockfile v3')
    strict = [line.strip() for line in (root / '.npmrc').read_text().splitlines()
              if line.strip() and not line.lstrip().startswith(('#', ';'))]
    if [line for line in strict if line.split('=', 1)[0].strip() == 'engine-strict'] != ['engine-strict=true']:
        errors.append('.npmrc must enable engine-strict=true exactly once')
    for section in ('dependencies', 'devDependencies', 'optionalDependencies'):
        if package.get(section, {}) != lock.get('packages', {}).get('', {}).get(section, {}):
            errors.append(f'lockfile root {section} differs from package.json')
    if framework:
        for name, expected in policy['sharedDependencies'].items():
            actual = package.get('dependencies', {}).get(name, package.get('devDependencies', {}).get(name))
            resolved = lock.get('packages', {}).get('node_modules/' + name, {}).get('version')
            if actual != expected or resolved != expected:
                errors.append(f'{name} declaration and resolution must equal {expected}')
    wrangler = root / 'wrangler.json'
    if wrangler.exists():
        config = foundation.read_json(wrangler)
        settings = [config, *config.get('env', {}).values()]
        if any(s.get('vars', {}).get('NODE_VERSION', version) != version for s in settings):
            errors.append('Wrangler NODE_VERSION differs from the approved baseline')
    return errors


def check(workspace: Path) -> dict:
    governance = workspace / '.github'
    standard = foundation.read_json(governance / 'portfolio/STACK_STANDARD.json')
    policy = foundation.read_json(governance / 'portfolio/STANDARDIZATION.json')
    matrix = foundation.read_json(governance / 'portfolio/CAPABILITY_MATRIX.json')
    errors = cohort_errors(standard, matrix)
    repos = repositories(workspace)
    for repo in repos:
        if not repo.is_dir() or not (repo / '.git').exists():
            errors.append(f'{repo.name}: required repository checkout missing')
    declared = set(policy['dependencyBaselines'])
    exceptions = policy['manifestExceptions']
    extra_roots = [p for p in workspace.iterdir() if p.is_dir() and not p.is_symlink()
                   and p.name not in SKIP and p not in repos
                   and p.name not in standard['excludedRepositories']]
    discovered = discover_manifests(repos + extra_roots, workspace)
    registered_node = {p['path'] + '/package.json' for p in policy['nodeProjects']}
    if registered_node != {p for p in declared if p.endswith('/package.json')}:
        errors.append('active Node manifest coverage differs from nodeProjects')
    for relative in sorted(discovered - declared - set(exceptions)):
        errors.append(f'{relative}: unregistered application/package; review and register its stack first')
    for relative in sorted(declared - discovered):
        errors.append(f'{relative}: registered manifest is missing or outside active source')
    for relative, reason in exceptions.items():
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f'{relative}: exceptions require a reason')
    for relative, expected in policy['dependencyBaselines'].items():
        try:
            actual = dependency_baseline(foundation.within(workspace, relative))
            if actual != expected:
                errors.append(f'{relative}: dependency declarations/lock changed; review the coordinated baseline update')
            if relative.endswith('/pubspec.yaml'):
                parsed = foundation.parse_pubspec((workspace / relative).read_text())
                if parsed.get('dartConstraint') != standard['toolchain']['dartConstraint']:
                    errors.append(f'{relative}: Dart SDK differs from the canonical baseline')
        except (OSError, ValueError, TypeError, KeyError) as error:
            errors.append(f'{relative}: {error}')
    native = []
    for consumer in standard['consumers']:
        try:
            row = foundation.inspect_consumer(consumer, standard, matrix, workspace, enforce_dev=False, verify_provider_worktree=False)
            native.append({'application': consumer['id'], 'staticAdoption': row['staticAdoption'],
                           'foundationEvidence': row['foundationEvidence']})
            errors.extend(f"{consumer['id']}: {error}" for error in row['errors'])
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f"{consumer['id']}: {error}")
    for project in policy['nodeProjects']:
        try:
            root = foundation.within(workspace, project['path'])
            errors.extend(f"{project['path']}: {e}" for e in check_node(root, standard['webPolicy'], project['framework']))
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f"{project['path']}: {error}")
    workflow_count = 0
    for repo in repos:
        for workflow in sorted((repo / '.github/workflows').glob('*.y*ml')):
            workflow_count += 1
            errors.extend(f'{repo.name}/{workflow.name}: {e}' for e in workflow_policy.check_workflow(workflow.read_text()))
    try:
        spec = importlib.util.spec_from_file_location('hosting_policy', workspace / 'App-Template/tool/check_hosting.py')
        hosting = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hosting)
        errors.extend('hosting: ' + e for e in hosting.check(workspace / 'App-Template', governance / 'portfolio/STACK_STANDARD.json'))
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f'hosting: {error}')
    return {'standardization': 'failed' if errors else 'passed', 'repositories': len(repos),
            'workflowCount': workflow_count, 'native': native, 'errors': sorted(set(errors)),
            'releaseQualification': 'separate; run check_foundation.py --release-gate; no evidence is refreshed'}


def git(repo: Path, *args: str) -> bytes:
    # Git exports GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE inside hooks. Clear them
    # for cross-repository reads; retain GIT_INDEX_FILE for the caller's commit
    # snapshot by passing it explicitly in snapshot_errors below.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(['git', '-c', 'core.fsmonitor=false', '-C', str(repo), *args],
                          check=True, capture_output=True, env=env).stdout


def governed(relative: str) -> bool:
    parts = Path(relative).parts
    if set(parts) & SKIP:
        return False
    return (Path(relative).name in {'pubspec.yaml', 'pubspec.lock', 'pubspec_overrides.yaml',
                                  'package.json', 'package-lock.json', '.nvmrc', '.node-version',
                                  '.npmrc', '.flutter-version', 'foundation.json', 'standard.json',
                                  'wrangler.json', 'Cargo.toml', 'Cargo.lock', 'rust-toolchain.toml',
                                  'AndroidManifest.xml', 'Info.plist'}
            or relative.startswith(('.github/workflows/', '.githooks/'))
            or relative in {'portfolio/STACK_STANDARD.json', 'portfolio/CAPABILITY_MATRIX.json',
                            'portfolio/STANDARDIZATION.json', 'portfolio/REPOSITORIES.json'}
            or relative.startswith('scripts/') and relative.endswith('.py')
            or relative == 'tool/check_hosting.py'
            or relative.startswith('android/') and relative.endswith(('.gradle', '.kts', '.properties')))


def snapshot_errors(repo: Path, revision: str | None) -> list[str]:
    """Do not validate a good worktree while committing/pushing older bad config."""
    # diff without a revision compares worktree with index, including partial staging.
    args = ['diff', '--name-only', '-z'] + ([revision] if revision else []) + ['--']
    changed = git(repo, *args).decode().split('\0')
    untracked = git(repo, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
    protected = []
    for p in sorted(set(changed + untracked)):
        if not p:
            continue
        needs_match = governed(p)
        if not needs_match and p.endswith('.dart') and 'lib' in Path(p).parts and not set(Path(p).parts) & SKIP:
            try:
                previous = git(repo, 'show', f'{revision or ""}:{p}').decode()
            except subprocess.CalledProcessError:  # New file, absent in the prior snapshot.
                previous = ''
            current = (repo / p).read_text() if (repo / p).is_file() else ''
            pattern = r"(?:import|export)\s+['\"]package:(majestic_\w+)/"
            needs_match = set(re.findall(pattern, previous)) != set(re.findall(pattern, current))
        if needs_match:
            protected.append(f'{repo.name}/{p}: governed input must match {revision or "the index"}; stage/commit its complete change first')
    return protected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-root', type=Path, default=ROOT.parent)
    parser.add_argument('--hook', choices=['commit', 'push'])
    parser.add_argument('--repository', type=Path)
    parser.add_argument('--print-dependency-baseline', action='store_true', help='print candidates for human diff review; does not approve/write them')
    args = parser.parse_args()
    workspace = args.workspace_root.resolve()
    try:
        if args.print_dependency_baseline:
            baseline = {p: dependency_baseline(workspace / p) for p in sorted(discover_manifests(repositories(workspace), workspace))
                        if p != 'steward/package.json'}
            print(json.dumps(baseline, indent=2))
            return 0
        extra = []
        if args.hook:
            if not args.repository:
                raise ValueError('--repository is required in hook mode')
            repo = args.repository.resolve()
            if repo not in repositories(workspace):
                raise ValueError('hook repository is outside the registered portfolio')
            if args.hook == 'commit':
                # An alternate index is used by git commit --only/-a. Reject it
                # rather than accidentally checking the ordinary index instead.
                if os.environ.get('GIT_INDEX_FILE'):
                    ordinary = git(repo, 'rev-parse', '--git-path', 'index').decode().strip()
                    supplied = Path(os.environ['GIT_INDEX_FILE']).resolve()
                    expected = (repo / ordinary).resolve()
                    if supplied != expected:
                        raise ValueError('stage the intended files and use plain git commit; alternate indexes are not validated')
                extra = snapshot_errors(repo, None)
            else:
                # Dependency changes must not be pushed against a policy that
                # exists only as unstaged/uncommitted work in a sibling checkout.
                extra.extend(snapshot_errors(workspace / '.github', 'HEAD'))
                for line in sys.stdin:
                    fields = line.split()
                    if len(fields) != 4 or not re.fullmatch(r'[0-9a-f]{40}', fields[1]):
                        raise ValueError('invalid pre-push ref input')
                    if fields[1] != '0' * 40:  # Deleting a ref carries no code.
                        extra.extend(snapshot_errors(repo, fields[1]))
        # Hook-local Git environment must not redirect foundation Git reads.
        for key in list(os.environ):
            if key.startswith('GIT_'):
                del os.environ[key]
        report = check(workspace)
        report['errors'] = sorted(set(report['errors'] + extra))
        if report['errors']:
            report['standardization'] = 'failed'
        print(json.dumps(report, indent=2))
        return int(bool(report['errors']))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'standardization': 'failed', 'error': str(error)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
