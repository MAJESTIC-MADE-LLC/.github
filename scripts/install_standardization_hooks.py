#!/usr/bin/env python3
"""Install local portfolio Git guards without replacing existing custom hooks."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess

from check_standardization import ROOT, git, repositories


def install(workspace: Path) -> list[str]:
    hook_path = (workspace / '.github/.githooks').resolve()
    for name in ('pre-commit', 'pre-push'):
        path = hook_path / name
        if not path.is_file() or not path.stat().st_mode & 0o111:
            raise ValueError(f'missing/executable hook: {path}')
    repos = repositories(workspace)
    # Preflight every repository before modifying any configuration.
    for repo in repos:
        existing = subprocess.run(['git', '-C', str(repo), 'config', '--get', 'core.hooksPath'],
                                  capture_output=True, text=True,
                                  env={k: v for k, v in os.environ.items() if not k.startswith('GIT_')})
        if existing.returncode not in (0, 1):
            raise ValueError(f'{repo.name}: cannot inspect hook configuration')
        if existing.stdout.strip():
            current = Path(existing.stdout.strip()).expanduser()
            if not current.is_absolute():
                current = repo / current
            if current.resolve() != hook_path:
                raise ValueError(f'{repo.name}: existing core.hooksPath retained; integrate its hooks explicitly')
        else:
            default = Path(git(repo, 'rev-parse', '--git-path', 'hooks').decode().strip())
            if not default.is_absolute():
                default = repo / default
            if default.is_dir() and any(p.is_file() and not p.name.endswith('.sample') for p in default.iterdir()):
                raise ValueError(f'{repo.name}: existing repository hooks retained; integrate explicitly')
    for repo in repos:
        git(repo, 'config', '--local', 'core.hooksPath', str(hook_path))
    return [p.name for p in repos]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-root', type=Path, default=ROOT.parent)
    args = parser.parse_args()
    try:
        installed = install(args.workspace_root.resolve())
        print(f'Installed pre-commit/pre-push standardization guards in {len(installed)} local repositories.')
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'{error}\n')
