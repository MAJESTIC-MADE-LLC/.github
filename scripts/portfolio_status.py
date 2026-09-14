#!/usr/bin/env python3
"""Render and validate Majestic Made's canonical portfolio status."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


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


class PortfolioError(RuntimeError):
    """Raised when the canonical portfolio data or a generated artifact is invalid."""


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PortfolioError(f"Unable to load {path}: {error}") from error
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schemaVersion") != 1:
        raise PortfolioError("schemaVersion must be 1")
    if not manifest.get("evidenceDate") or not manifest.get("evidenceSummary"):
        raise PortfolioError("evidenceDate and evidenceSummary are required")

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
        names.append(repository["name"])
        role = repository["role"]
        if role not in ROLE_COUNTS:
            raise PortfolioError(f"{repository['name']} has unsupported role {role!r}")
        if role in {"release-candidate", "concept"}:
            for field in ("stage", "focus"):
                if not repository.get(field):
                    raise PortfolioError(f"{repository['name']} is missing {field}")
        if role == "release-candidate" and not repository.get("launchEvidence"):
            raise PortfolioError(f"{repository['name']} is missing launchEvidence")
        if repository["localCheckout"] and not repository.get("requiredPaths"):
            raise PortfolioError(f"{repository['name']} is missing requiredPaths")

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
    matrix_repositories = [row.get("repository") for row in data_matrix]
    if len(matrix_repositories) != len(set(matrix_repositories)):
        raise PortfolioError("dataMatrix contains duplicate repositories")
    expected_matrix = release_candidates | {"Majestic-Made-Hub"}
    if set(matrix_repositories) != expected_matrix:
        raise PortfolioError(
            "dataMatrix must contain every release candidate and Majestic-Made-Hub"
        )
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
        if row["repository"] not in repository_names:
            raise PortfolioError(
                f"dataMatrix references unknown repository {row['repository']}"
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
            "| {displayName} | {status} | {next} | {concern} |".format(**repository)
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
                        f"Evidence captured {manifest['evidenceDate']}: {manifest['evidenceSummary']}",
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
            f"| {order} | {repository['displayName']} | {repository['launchEvidence']} | "
            f"{repository['next']} | {repository['concern']} |"
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
            f"| {repository['displayName']} | {repository['focus']} | {repository['stage']} |"
        )
    return generated_block("product-lineup", "\n".join(rows))


def render_data_matrix(manifest: dict[str, Any]) -> str:
    rows = [
        "| Product | Default data location | Remote services | Paid boundary | Mandatory guardrails |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in manifest["dataMatrix"]:
        rows.append(
            f"| {row['product']} | {row['defaultDataLocation']} | {row['remoteServices']} | "
            f"{row['paidBoundary']} | {row['guardrails']} |"
        )
    return generated_block("data-cost-matrix", "\n".join(rows))


def replace_generated_block(contents: str, identifier: str, replacement: str) -> str:
    start_marker = f"<!-- BEGIN GENERATED: {identifier} -->"
    end_marker = f"<!-- END GENERATED: {identifier} -->"
    start = contents.find(start_marker)
    end = contents.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise PortfolioError(f"missing or invalid generated markers for {identifier}")
    end += len(end_marker)
    return contents[:start] + replacement + contents[end:]


def synchronize_file(path: Path, identifier: str, replacement: str, write: bool) -> None:
    try:
        current = path.read_text(encoding="utf-8")
    except OSError as error:
        raise PortfolioError(f"Unable to read {path}: {error}") from error
    expected = replace_generated_block(current, identifier, replacement)
    if expected == current:
        return
    if write:
        path.write_text(expected, encoding="utf-8")
        return
    raise PortfolioError(
        f"{path.relative_to(REPO_ROOT)} is stale; run "
        "python3 scripts/portfolio_status.py --write"
    )


def synchronize_documents(manifest: dict[str, Any], write: bool) -> None:
    expected_status = render_status(manifest)
    if STATUS_PATH.exists():
        current_status = STATUS_PATH.read_text(encoding="utf-8")
    else:
        current_status = ""
    if current_status != expected_status:
        if write:
            STATUS_PATH.write_text(expected_status, encoding="utf-8")
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
    workspace_root = workspace_root.resolve()
    failures: list[str] = []
    for repository in manifest["repositories"]:
        if not repository["localCheckout"]:
            continue
        checkout = workspace_root / repository["name"]
        if not (checkout / ".git").exists():
            failures.append(f"{repository['name']}: missing git checkout at {checkout}")
            continue
        branch = run_command(
            ["git", "-C", str(checkout), "branch", "--show-current"],
            f"read branch for {repository['name']}",
        ).strip()
        if branch != "dev":
            failures.append(f"{repository['name']}: expected dev branch, found {branch!r}")
        for relative_path in repository["requiredPaths"]:
            if not (checkout / relative_path).exists():
                failures.append(f"{repository['name']}: missing {relative_path}")
    if failures:
        raise PortfolioError("workspace evidence failed:\n- " + "\n- ".join(failures))


def verify_github(manifest: dict[str, Any], owner: str) -> None:
    raw_repositories = run_command(
        [
            "gh",
            "repo",
            "list",
            owner,
            "--limit",
            "100",
            "--json",
            "name",
        ],
        f"list repositories for {owner}",
    )
    remote_names = {item["name"] for item in json.loads(raw_repositories)}
    expected_names = {repository["name"] for repository in manifest["repositories"]}
    if remote_names != expected_names:
        missing = sorted(expected_names - remote_names)
        unexpected = sorted(remote_names - expected_names)
        details = []
        if missing:
            details.append(f"missing from GitHub: {', '.join(missing)}")
        if unexpected:
            details.append(f"missing from manifest: {', '.join(unexpected)}")
        raise PortfolioError("GitHub inventory drift: " + "; ".join(details))

    failures: list[str] = []
    for repository in manifest["repositories"]:
        if repository["role"] != "concept":
            continue
        raw_tree = run_command(
            [
                "gh",
                "api",
                f"repos/{owner}/{repository['name']}/git/trees/dev?recursive=1",
            ],
            f"read dev tree for {owner}/{repository['name']}",
        )
        tree = json.loads(raw_tree).get("tree", [])
        files = {item["path"] for item in tree if item.get("type") == "blob"}
        unexpected = sorted(files - CONCEPT_REMOTE_ALLOWLIST)
        if "README.md" not in files or unexpected:
            details = []
            if "README.md" not in files:
                details.append("README.md is missing")
            if unexpected:
                details.append(f"implementation evidence found: {', '.join(unexpected)}")
            failures.append(f"{repository['name']}: {'; '.join(details)}")
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
        raise PortfolioError(f"Unable to {description}: {detail}") from error
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
