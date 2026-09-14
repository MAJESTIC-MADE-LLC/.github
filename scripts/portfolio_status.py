#!/usr/bin/env python3
"""Render and validate Majestic Made's canonical portfolio status."""

from __future__ import annotations

import argparse
import errno
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
import uuid
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "portfolio" / "REPOSITORIES.json"
STATUS_PATH = REPO_ROOT / "portfolio" / "STATUS.md"

ROLE_COUNTS = {"release-candidate": 7, "concept": 10, "shared": 6}
REQUIRED_REPOSITORY_FIELDS = {
    "name",
    "displayName",
    "role",
    "status",
    "next",
    "concern",
    "localCheckout",
}
CONCEPT_REMOTE_ALLOWLIST = {
    ".github/dependabot.yml",
    ".github/workflows/concept-governance.yml",
    ".gitignore",
    "README.md",
    "docs/IMPLEMENTATION_READINESS.md",
    "project-status.json",
    "scripts/validate_concept_repo.py",
}
REPOSITORY_NAME_PATTERN = re.compile(r"(?!-)[A-Za-z0-9._-]{1,100}\Z")
GITHUB_OWNER_PATTERN = re.compile(
    r"(?!.*--)[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z"
)
GITHUB_REPOSITORY_LIMIT = 1000
MARKDOWN_ESCAPES = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "|": "&#124;",
    "[": "&#91;",
    "]": "&#93;",
    "(": "&#40;",
    ")": "&#41;",
    "`": "&#96;",
    "!": "&#33;",
    "\\": "&#92;",
    "\r": "&#13;",
    "\n": "&#10;",
}


class PortfolioError(RuntimeError):
    """Raised when the canonical portfolio data or a generated artifact is invalid."""


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise PortfolioError(f"{field} must be a non-empty string")
    if any(
        unicodedata.category(character) in {"Cc", "Cf", "Cs", "Zl", "Zp"}
        for character in value
    ):
        raise PortfolioError(f"{field} must not contain control characters")
    return value


def validate_repository_name(value: Any, field: str = "repository name") -> str:
    name = require_text(value, field)
    if name in {".", ".."} or not REPOSITORY_NAME_PATTERN.fullmatch(name):
        raise PortfolioError(f"{field} is not a safe GitHub repository name")
    return name


def validate_github_owner(value: Any) -> str:
    owner = require_text(value, "GitHub owner")
    if not GITHUB_OWNER_PATTERN.fullmatch(owner):
        raise PortfolioError("GitHub owner is not a valid account or organization name")
    return owner


def validate_relative_path(value: Any, field: str) -> str:
    relative_path = require_text(value, field)
    posix_path = PurePosixPath(relative_path)
    windows_path = PureWindowsPath(relative_path)
    if (
        posix_path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
        or "\\" in relative_path
        or ":" in relative_path
        or any(part in {"", ".", ".."} for part in relative_path.split("/"))
    ):
        raise PortfolioError(f"{field} must be a normalized relative path")
    return relative_path


def markdown_text(value: str) -> str:
    """Encode manifest text so it remains text in generated Markdown."""
    return "".join(MARKDOWN_ESCAPES.get(character, character) for character in value)


def safe_external_text(value: str) -> str:
    """Make untrusted subprocess and API text safe for one diagnostic line."""
    return json.dumps(value, ensure_ascii=True)[1:-1]


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise PortfolioError(
                f"JSON contains duplicate key {safe_external_text(key)}"
            )
        value[key] = item
    return value


def decode_json(raw: str, description: str, expected_type: type[Any]) -> Any:
    try:
        value = json.loads(raw, object_pairs_hook=reject_duplicate_json_keys)
    except json.JSONDecodeError as error:
        raise PortfolioError(f"{description} returned invalid JSON") from error
    if not isinstance(value, expected_type):
        raise PortfolioError(
            f"{description} must return a {expected_type.__name__} JSON value"
        )
    return value


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    try:
        raw_manifest = path.read_text(encoding="utf-8")
        manifest = decode_json(raw_manifest, f"Manifest {path}", dict)
    except OSError as error:
        raise PortfolioError(f"Unable to load {path}: {error}") from error
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest, dict):
        raise PortfolioError("manifest must be an object")
    if manifest.get("schemaVersion") != 1:
        raise PortfolioError("schemaVersion must be 1")
    require_text(manifest.get("evidenceDate"), "evidenceDate")
    require_text(manifest.get("evidenceSummary"), "evidenceSummary")

    repositories = manifest.get("repositories")
    if not isinstance(repositories, list):
        raise PortfolioError("repositories must be a list")

    names: list[str] = []
    for index, repository in enumerate(repositories):
        if not isinstance(repository, dict):
            raise PortfolioError(f"repositories[{index}] must be an object")
        missing = REQUIRED_REPOSITORY_FIELDS - repository.keys()
        if missing:
            raise PortfolioError(
                f"repositories[{index}] is missing: {', '.join(sorted(missing))}"
            )
        name = validate_repository_name(
            repository["name"], f"repositories[{index}].name"
        )
        names.append(name)
        for field in ("displayName", "status", "next", "concern"):
            require_text(repository[field], f"{name}.{field}")
        if not isinstance(repository["localCheckout"], bool):
            raise PortfolioError(f"{name}.localCheckout must be a boolean")
        role = require_text(repository["role"], f"{name}.role")
        if role not in ROLE_COUNTS:
            raise PortfolioError(f"{name} has unsupported role {role!r}")
        if role in {"release-candidate", "concept"}:
            for field in ("stage", "focus"):
                require_text(repository.get(field), f"{name}.{field}")
        if role == "release-candidate":
            require_text(repository.get("launchEvidence"), f"{name}.launchEvidence")
        required_paths = repository.get("requiredPaths")
        if required_paths is not None and not isinstance(required_paths, list):
            raise PortfolioError(f"{name}.requiredPaths must be a list")
        if repository["localCheckout"] and not required_paths:
            raise PortfolioError(f"{name} is missing requiredPaths")
        for path_index, relative_path in enumerate(required_paths or []):
            validate_relative_path(
                relative_path, f"{name}.requiredPaths[{path_index}]"
            )

    if len(names) != len(set(names)):
        duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
        raise PortfolioError(f"duplicate repositories: {', '.join(duplicates)}")

    role_counts = Counter(repository["role"] for repository in repositories)
    if dict(role_counts) != ROLE_COUNTS:
        raise PortfolioError(
            f"repository role counts must be {ROLE_COUNTS}, found {dict(role_counts)}"
        )

    repository_names = set(names)
    launch_order = manifest.get("launchOrder")
    if not isinstance(launch_order, list) or len(launch_order) != 7:
        raise PortfolioError("launchOrder must contain exactly seven repositories")
    for index, name in enumerate(launch_order):
        validate_repository_name(name, f"launchOrder[{index}]")
    if len(launch_order) != len(set(launch_order)):
        raise PortfolioError("launchOrder contains duplicates")
    release_candidates = {
        repository["name"]
        for repository in repositories
        if repository["role"] == "release-candidate"
    }
    if set(launch_order) != release_candidates:
        raise PortfolioError("launchOrder must contain every release candidate exactly once")

    product_lineup = manifest.get("productLineup")
    if not isinstance(product_lineup, list) or len(product_lineup) != 17:
        raise PortfolioError("productLineup must contain exactly seventeen products")
    for index, name in enumerate(product_lineup):
        validate_repository_name(name, f"productLineup[{index}]")
    if len(product_lineup) != len(set(product_lineup)):
        raise PortfolioError("productLineup contains duplicates")
    product_repositories = {
        repository["name"]
        for repository in repositories
        if repository["role"] in {"release-candidate", "concept"}
    }
    if set(product_lineup) != product_repositories:
        raise PortfolioError(
            "productLineup must contain every concept and release candidate exactly once"
        )

    data_matrix = manifest.get("dataMatrix")
    if not isinstance(data_matrix, list) or len(data_matrix) != 8:
        raise PortfolioError("dataMatrix must contain the seven launch apps and Hub/waitlists")
    if any(not isinstance(row, dict) for row in data_matrix):
        raise PortfolioError("every dataMatrix row must be an object")
    matrix_fields = {
        "product",
        "repository",
        "defaultDataLocation",
        "remoteServices",
        "paidBoundary",
        "guardrails",
    }
    for row in data_matrix:
        missing = matrix_fields - row.keys()
        if missing:
            raise PortfolioError(
                f"dataMatrix row {row.get('product', '<unknown>')} is missing: "
                f"{', '.join(sorted(missing))}"
            )
        product = require_text(row["product"], "dataMatrix.product")
        validate_repository_name(row["repository"], f"dataMatrix[{product}].repository")
        for field in (
            "defaultDataLocation",
            "remoteServices",
            "paidBoundary",
            "guardrails",
        ):
            require_text(row[field], f"dataMatrix[{product}].{field}")
        if row["repository"] not in repository_names:
            raise PortfolioError(
                f"dataMatrix references unknown repository {row['repository']}"
            )
    matrix_repositories = [row["repository"] for row in data_matrix]
    if len(matrix_repositories) != len(set(matrix_repositories)):
        raise PortfolioError("dataMatrix contains duplicate repositories")
    expected_matrix = release_candidates | {"Majestic-Made-Hub"}
    if set(matrix_repositories) != expected_matrix:
        raise PortfolioError(
            "dataMatrix must contain every release candidate and Majestic-Made-Hub"
        )


def repositories_by_name(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {repository["name"]: repository for repository in manifest["repositories"]}


def generated_block(identifier: str, body: str) -> str:
    return (
        f"<!-- BEGIN GENERATED: {identifier} -->\n"
        f"{body.rstrip()}\n"
        f"<!-- END GENERATED: {identifier} -->"
    )


def render_status(manifest: dict[str, Any]) -> str:
    rows = [
        "| Repository | Status | What should happen next | Problems or concerns |",
        "| --- | --- | --- | --- |",
    ]
    for repository in manifest["repositories"]:
        rows.append(
            "| {displayName} | {status} | {next} | {concern} |".format(
                **{
                    field: markdown_text(repository[field])
                    for field in ("displayName", "status", "next", "concern")
                }
            )
        )

    counts = Counter(repository["role"] for repository in manifest["repositories"])
    summary = (
        f"The organization has {len(manifest['repositories'])} repositories: "
        f"{counts['release-candidate']} functional release candidates, "
        f"{counts['concept']} concept-only product repositories, and "
        f"{counts['shared']} shared, governance, legal, website, template, or "
        "infrastructure repositories. The implementation count is seven; the shared "
        "public-release gate is not complete."
    )
    body = "\n".join(
        [
            "# Organization repository status",
            "",
            "This file is generated from `portfolio/REPOSITORIES.json`. Do not edit its table by hand.",
            "",
            generated_block(
                "repository-status",
                "\n".join(
                    [
                        f"Evidence captured {markdown_text(manifest['evidenceDate'])}: "
                        f"{markdown_text(manifest['evidenceSummary'])}",
                        "",
                        summary,
                        "",
                        *rows,
                    ]
                ),
            ),
            "",
            "Run `python3 scripts/portfolio_status.py --check` after changing the manifest. "
            "Use `--workspace-root .. --verify-github MAJESTIC-MADE-LLC` for the full local and "
            "organization inventory audit.",
            "",
        ]
    )
    return body


def render_launch_table(manifest: dict[str, Any]) -> str:
    repositories = repositories_by_name(manifest)
    rows = [
        "| Order | Product | Current evidence | Next release milestone | Main concern |",
        "| --- | --- | --- | --- | --- |",
    ]
    for order, name in enumerate(manifest["launchOrder"], start=1):
        repository = repositories[name]
        rows.append(
            f"| {order} | {markdown_text(repository['displayName'])} | "
            f"{markdown_text(repository['launchEvidence'])} | "
            f"{markdown_text(repository['next'])} | "
            f"{markdown_text(repository['concern'])} |"
        )
    return generated_block("launch-slate-status", "\n".join(rows))


def render_profile_table(manifest: dict[str, Any]) -> str:
    repositories = repositories_by_name(manifest)
    rows = [
        "| Product | Focus | Stage |",
        "| --- | --- | --- |",
    ]
    for name in manifest["productLineup"]:
        repository = repositories[name]
        rows.append(
            f"| {markdown_text(repository['displayName'])} | "
            f"{markdown_text(repository['focus'])} | "
            f"{markdown_text(repository['stage'])} |"
        )
    return generated_block("product-lineup", "\n".join(rows))


def render_data_matrix(manifest: dict[str, Any]) -> str:
    rows = [
        "| Product | Default data location | Remote services | Paid boundary | Mandatory guardrails |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in manifest["dataMatrix"]:
        rows.append(
            f"| {markdown_text(row['product'])} | "
            f"{markdown_text(row['defaultDataLocation'])} | "
            f"{markdown_text(row['remoteServices'])} | "
            f"{markdown_text(row['paidBoundary'])} | "
            f"{markdown_text(row['guardrails'])} |"
        )
    return generated_block("data-cost-matrix", "\n".join(rows))


def replace_generated_block(contents: str, identifier: str, replacement: str) -> str:
    start_marker = f"<!-- BEGIN GENERATED: {identifier} -->"
    end_marker = f"<!-- END GENERATED: {identifier} -->"
    if contents.count(start_marker) != 1 or contents.count(end_marker) != 1:
        raise PortfolioError(f"missing or duplicate generated markers for {identifier}")
    start = contents.find(start_marker)
    end = contents.find(end_marker, start + len(start_marker))
    if end == -1:
        raise PortfolioError(f"missing or invalid generated markers for {identifier}")
    end += len(end_marker)
    return contents[:start] + replacement + contents[end:]


def repository_relative_path(path: Path) -> Path:
    absolute_path = Path(os.path.abspath(path))
    try:
        relative_path = absolute_path.relative_to(REPO_ROOT)
    except ValueError as error:
        raise PortfolioError(f"Generated path escapes repository: {path}") from error
    if not relative_path.parts:
        raise PortfolioError("Generated path must name a repository file")
    return relative_path


@contextmanager
def open_repository_parent(path: Path) -> Iterator[tuple[int, str]]:
    relative_path = repository_relative_path(path)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory_fd = os.open(REPO_ROOT, directory_flags)
    try:
        for part in relative_path.parts[:-1]:
            next_fd = os.open(
                part,
                directory_flags | nofollow,
                dir_fd=directory_fd,
            )
            os.close(directory_fd)
            directory_fd = next_fd
        yield directory_fd, relative_path.name
    except OSError as error:
        raise PortfolioError(f"Unsafe generated path {relative_path}: {error}") from error
    finally:
        os.close(directory_fd)


def read_repository_text(path: Path, *, missing_ok: bool = False) -> str | None:
    with open_repository_parent(path) as (directory_fd, filename):
        try:
            file_fd = os.open(
                filename,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=directory_fd,
            )
        except FileNotFoundError:
            if missing_ok:
                return None
            raise PortfolioError(f"Generated file is missing: {path}")
        except OSError as error:
            raise PortfolioError(f"Unable to open generated file {path}: {error}") from error
        file_status = os.fstat(file_fd)
        if not stat.S_ISREG(file_status.st_mode):
            os.close(file_fd)
            raise PortfolioError(f"Generated path must be a regular file: {path}")
        try:
            with os.fdopen(file_fd, encoding="utf-8") as generated_file:
                return generated_file.read()
        except (OSError, UnicodeError) as error:
            raise PortfolioError(f"Unable to read generated file {path}: {error}") from error


def atomic_write_repository_text(path: Path, contents: str) -> None:
    with open_repository_parent(path) as (directory_fd, filename):
        try:
            original_status = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            original_status = None
        if original_status is not None and not stat.S_ISREG(original_status.st_mode):
            raise PortfolioError(f"Refusing to replace non-regular generated path: {path}")

        temporary_name = f".{filename}.{uuid.uuid4().hex}.tmp"
        temporary_fd: int | None = None
        try:
            temporary_fd = os.open(
                temporary_name,
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
                | getattr(os, "O_NOFOLLOW", 0),
                0o600,
                dir_fd=directory_fd,
            )
            mode = stat.S_IMODE(original_status.st_mode) if original_status else 0o644
            os.fchmod(temporary_fd, mode)
            with os.fdopen(temporary_fd, "w", encoding="utf-8") as temporary_file:
                temporary_fd = None
                temporary_file.write(contents)
                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            try:
                current_status = os.stat(
                    filename, dir_fd=directory_fd, follow_symlinks=False
                )
            except FileNotFoundError:
                current_status = None
            original_identity = (
                (original_status.st_dev, original_status.st_ino)
                if original_status
                else None
            )
            current_identity = (
                (current_status.st_dev, current_status.st_ino) if current_status else None
            )
            if current_identity != original_identity:
                raise PortfolioError(f"Generated path changed during write: {path}")

            os.replace(
                temporary_name,
                filename,
                src_dir_fd=directory_fd,
                dst_dir_fd=directory_fd,
            )
            os.fsync(directory_fd)
        except OSError as error:
            if error.errno == errno.ELOOP:
                raise PortfolioError(f"Refusing symbolic-link generated path: {path}") from error
            raise PortfolioError(f"Unable to write generated file {path}: {error}") from error
        finally:
            if temporary_fd is not None:
                os.close(temporary_fd)
            try:
                os.unlink(temporary_name, dir_fd=directory_fd)
            except FileNotFoundError:
                pass


def synchronize_file(path: Path, identifier: str, replacement: str, write: bool) -> None:
    try:
        current = read_repository_text(path)
    except PortfolioError as error:
        raise PortfolioError(f"Unable to read {path}: {error}") from error
    assert current is not None
    expected = replace_generated_block(current, identifier, replacement)
    if expected == current:
        return
    if write:
        atomic_write_repository_text(path, expected)
        return
    raise PortfolioError(
        f"{path.relative_to(REPO_ROOT)} is stale; run "
        "python3 scripts/portfolio_status.py --write"
    )


def synchronize_documents(manifest: dict[str, Any], write: bool) -> None:
    expected_status = render_status(manifest)
    current_status = read_repository_text(STATUS_PATH, missing_ok=True) or ""
    if current_status != expected_status:
        if write:
            atomic_write_repository_text(STATUS_PATH, expected_status)
        else:
            raise PortfolioError(
                "portfolio/STATUS.md is stale; run "
                "python3 scripts/portfolio_status.py --write"
            )

    synchronize_file(
        REPO_ROOT / "portfolio" / "LAUNCH_SLATE.md",
        "launch-slate-status",
        render_launch_table(manifest),
        write,
    )
    synchronize_file(
        REPO_ROOT / "profile" / "README.md",
        "product-lineup",
        render_profile_table(manifest),
        write,
    )
    synchronize_file(
        REPO_ROOT / "portfolio" / "DATA_COST_MATRIX.md",
        "data-cost-matrix",
        render_data_matrix(manifest),
        write,
    )


def verify_workspace(manifest: dict[str, Any], workspace_root: Path) -> None:
    try:
        workspace_root = workspace_root.resolve(strict=True)
    except OSError as error:
        raise PortfolioError(f"Unable to resolve workspace root: {error}") from error
    if not workspace_root.is_dir():
        raise PortfolioError("workspace root must be a directory")
    failures: list[str] = []
    for repository in manifest["repositories"]:
        if not repository["localCheckout"]:
            continue
        name = validate_repository_name(repository["name"])
        checkout = (workspace_root / name).resolve(strict=False)
        if not checkout.is_relative_to(workspace_root):
            raise PortfolioError(f"{name}: checkout escapes workspace root")
        git_path = checkout / ".git"
        if not checkout.is_dir() or not git_path.exists() or git_path.is_symlink():
            failures.append(f"{name}: missing safe git checkout at {checkout}")
            continue
        branch = run_command(
            ["git", "-C", str(checkout), "branch", "--show-current"],
            f"read branch for {name}",
        ).strip()
        if branch != "dev":
            failures.append(f"{name}: expected dev branch, found {branch!r}")
        required_paths = repository.get("requiredPaths")
        if not isinstance(required_paths, list) or not required_paths:
            raise PortfolioError(f"{name}.requiredPaths must be a non-empty list")
        for path_index, relative_path in enumerate(required_paths):
            relative_path = validate_relative_path(
                relative_path, f"{name}.requiredPaths[{path_index}]"
            )
            evidence_path = (checkout / relative_path).resolve(strict=False)
            if not evidence_path.is_relative_to(checkout):
                raise PortfolioError(f"{name}: evidence path escapes checkout")
            if not evidence_path.exists():
                failures.append(f"{name}: missing {relative_path}")
    if failures:
        raise PortfolioError("workspace evidence failed:\n- " + "\n- ".join(failures))


def verify_github(manifest: dict[str, Any], owner: str) -> None:
    owner = validate_github_owner(owner)
    raw_repositories = run_command(
        [
            "gh",
            "repo",
            "list",
            "--limit",
            str(GITHUB_REPOSITORY_LIMIT),
            "--json",
            "name",
            "--",
            owner,
        ],
        f"list repositories for {owner}",
    )
    repository_items = decode_json(raw_repositories, "GitHub repository list", list)
    if len(repository_items) >= GITHUB_REPOSITORY_LIMIT:
        raise PortfolioError("GitHub repository list reached its safety limit")
    remote_name_list: list[str] = []
    for index, item in enumerate(repository_items):
        if not isinstance(item, dict) or "name" not in item:
            raise PortfolioError(f"GitHub repository list item {index} is malformed")
        remote_name_list.append(
            validate_repository_name(item["name"], f"GitHub repository list item {index}.name")
        )
    if len(remote_name_list) != len(set(remote_name_list)):
        raise PortfolioError("GitHub repository list contains duplicate names")
    remote_names = set(remote_name_list)
    expected_names = {
        validate_repository_name(repository["name"])
        for repository in manifest["repositories"]
    }
    if remote_names != expected_names:
        missing = sorted(expected_names - remote_names)
        unexpected = sorted(remote_names - expected_names)
        details = []
        if missing:
            details.append(
                "missing from GitHub: "
                + ", ".join(safe_external_text(name) for name in missing)
            )
        if unexpected:
            details.append(
                "missing from manifest: "
                + ", ".join(safe_external_text(name) for name in unexpected)
            )
        raise PortfolioError("GitHub inventory drift: " + "; ".join(details))

    failures: list[str] = []
    for repository in manifest["repositories"]:
        if repository["role"] != "concept":
            continue
        repository_name = validate_repository_name(repository["name"])
        raw_tree = run_command(
            [
                "gh",
                "api",
                f"repos/{owner}/{repository_name}/git/trees/dev?recursive=1",
            ],
            f"read dev tree for {owner}/{repository_name}",
        )
        tree_payload = decode_json(raw_tree, "GitHub tree", dict)
        if tree_payload.get("truncated") is not False:
            raise PortfolioError(f"{repository_name}: GitHub tree response is incomplete")
        tree = tree_payload.get("tree")
        if not isinstance(tree, list):
            raise PortfolioError(f"{repository_name}: GitHub tree is malformed")
        files: set[str] = set()
        for index, item in enumerate(tree):
            if not isinstance(item, dict):
                raise PortfolioError(f"{repository_name}: tree item {index} is malformed")
            path = item.get("path")
            item_type = item.get("type")
            if not isinstance(path, str) or not isinstance(item_type, str):
                raise PortfolioError(f"{repository_name}: tree item {index} is malformed")
            if item_type == "blob":
                files.add(path)
        unexpected = sorted(files - CONCEPT_REMOTE_ALLOWLIST)
        if "README.md" not in files or unexpected:
            details = []
            if "README.md" not in files:
                details.append("README.md is missing")
            if unexpected:
                details.append(
                    "implementation evidence found: "
                    + ", ".join(safe_external_text(path) for path in unexpected)
                )
            failures.append(f"{repository_name}: {'; '.join(details)}")
    if failures:
        raise PortfolioError(
            "concept classifications have drifted:\n- " + "\n- ".join(failures)
        )


def run_command(command: list[str], description: str) -> str:
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        stderr = getattr(error, "stderr", "")
        detail = stderr.strip() if stderr else str(error)
        raise PortfolioError(
            f"Unable to {description}: {safe_external_text(detail)}"
        ) from error
    return result.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="verify that generated documents match the manifest (default)",
    )
    mode.add_argument(
        "--write",
        action="store_true",
        help="update generated documents from the manifest",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        help="verify expected dev checkouts and evidence paths under this directory",
    )
    parser.add_argument(
        "--verify-github",
        metavar="OWNER",
        help="use the authenticated GitHub CLI to verify repository inventory and concept trees",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        synchronize_documents(manifest, write=args.write)
        if args.workspace_root:
            verify_workspace(manifest, args.workspace_root)
        if args.verify_github:
            verify_github(manifest, args.verify_github)
    except PortfolioError as error:
        print(f"portfolio status validation failed: {error}", file=sys.stderr)
        return 1
    action = "updated" if args.write else "validated"
    print(f"Portfolio status {action} for {len(manifest['repositories'])} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
