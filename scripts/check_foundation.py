#!/usr/bin/env python3
"""Read-only adoption and qualification checks for Majestic's mobile foundation.

This never resolves dependencies, writes evidence, builds apps, or runs hosted CI.
Static adoption is deliberately distinct from the source-bound qualification gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote as uri_unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
STANDARD_PATH = REPO_ROOT / "portfolio/STACK_STANDARD.json"
STATUSES = {"pending", "adopting", "verified"}
GIT_REF = re.compile(r"[0-9a-f]{40}\Z")
SOURCE_FINGERPRINT_POLICY_VERSION = 2
GENERATED_SOURCE_FILES = {
    "ios/Runner/GeneratedPluginRegistrant.h",
    "ios/Runner/GeneratedPluginRegistrant.m",
    "ios/Flutter/Generated.xcconfig",
    "ios/Flutter/flutter_export_environment.sh",
    "ios/Flutter/.last_build_id",
    "android/local.properties",
    "android/app/src/main/java/io/flutter/plugins/GeneratedPluginRegistrant.java",
}
GENERATED_SOURCE_DIRECTORIES = {"ios/Flutter/ephemeral"}
IGNORED_PARTS = {
    ".git", ".dart_tool", "build", "Pods", ".symlinks", "node_modules",
    ".gradle", ".idea", "xcuserdata", "DerivedData", ".plugin_symlinks",
    ".build",
}


class FoundationError(ValueError):
    pass


def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FoundationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict[str, Any]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    except (OSError, json.JSONDecodeError) as error:
        raise FoundationError(f"unable to read {path.name}: {error}") from error
    if not isinstance(result, dict):
        raise FoundationError(f"{path.name} must contain an object")
    return result


def within(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise FoundationError("expected a relative workspace path")
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise FoundationError(f"path escapes workspace: {relative!r}")
    return candidate


def unquote(value: str) -> str:
    return value.split(" #", 1)[0].strip().strip("\"'")


def parse_pubspec(text: str) -> dict[str, Any]:
    """Parse the ordinary block-mapping pubspec subset used by this workspace.

    Unsupported dependency shapes are retained and fail the relevant exact/path
    checks instead of silently being interpreted as an approved dependency.
    """
    result: dict[str, Any] = {"dependencies": {}, "dev_dependencies": {}, "dependency_overrides": {}}
    section = ""
    package = ""
    nested = ""
    top_keys: set[str] = set()
    detail_keys: set[str] = set()
    for line in text.splitlines():
        top = re.match(r"^([A-Za-z_]\w*):\s*(.*)$", line)
        if top:
            section, scalar = top.groups()
            if section in top_keys:
                raise FoundationError(f"duplicate pubspec section: {section}")
            top_keys.add(section)
            package = ""
            nested = ""
            if section in {"name", "version"}:
                result[section] = unquote(scalar)
            continue
        if section == "environment":
            sdk = re.match(r"^  sdk:\s*(.*)$", line)
            if sdk:
                result["dartConstraint"] = unquote(sdk.group(1))
        if section not in {"dependencies", "dev_dependencies", "dependency_overrides"}:
            continue
        dependency = re.match(r"^  ([A-Za-z_]\w*):\s*(.*)$", line)
        if dependency:
            package, scalar = dependency.groups()
            nested = ""
            detail_keys = set()
            if package in result[section]:
                raise FoundationError(f"duplicate pubspec dependency: {package}")
            result[section][package] = {"version": unquote(scalar)}
        elif package:
            detail = re.match(r"^    ([A-Za-z_][\w-]*):\s*(.*)$", line)
            if detail:
                key, value = detail.groups()
                if key in detail_keys:
                    raise FoundationError(f"duplicate dependency descriptor: {package}.{key}")
                detail_keys.add(key)
                nested = key if key == "git" and not value.strip() else ""
                result[section][package][key] = {} if nested else unquote(value)
            elif nested:
                child = re.match(r"^      ([A-Za-z_][\w-]*):\s*(.*)$", line)
                if child:
                    key, value = child.groups()
                    descriptor = result[section][package][nested]
                    if key in descriptor:
                        raise FoundationError(f"duplicate Git descriptor: {package}.{key}")
                    descriptor[key] = unquote(value)
    hooks = re.search(r"(?ms)^hooks:\s*\n(.*?)(?=^\S|\Z)", text)
    result["encryptedSqliteHook"] = bool(hooks and re.search(
        r"(?m)^\s+sqlite3:\s*\n\s+source:\s*[\"']?sqlite3mc[\"']?\s*$", hooks.group(1)
    ))
    return result


def parse_lock(text: str) -> dict[str, dict[str, str]]:
    result = {}
    for match in re.finditer(r"(?ms)^  ([A-Za-z_]\w*):\n(.*?)(?=^  [^ ]|^sdks:|\Z)", text):
        name, block = match.groups()
        if name in result:
            raise FoundationError(f"duplicate lockfile package: {name}")
        row = {}
        for field, pattern in {
            "version": r"(?m)^    version:\s*(.*)$",
            "source": r"(?m)^    source:\s*(.*)$",
            "path": r"(?m)^      path:\s*(.*)$",
            "url": r"(?m)^      url:\s*(.*)$",
            "ref": r"(?m)^      ref:\s*(.*)$",
            "resolved-ref": r"(?m)^      resolved-ref:\s*(.*)$",
        }.items():
            values = re.findall(pattern, block)
            if len(values) > 1:
                raise FoundationError(f"duplicate lockfile descriptor: {name}.{field}")
            if values:
                row[field] = unquote(values[0])
        result[name] = row
    return result


def git_descriptor(value: Any) -> dict[str, str]:
    """Accept only the approved explicit HTTPS/full-commit/subdirectory form."""
    if not isinstance(value, dict) or set(value) != {"url", "ref", "path"}:
        raise FoundationError("Git source must have exactly url, ref and path")
    url, revision, subdir = (value[key] for key in ("url", "ref", "path"))
    if not all(isinstance(item, str) for item in (url, revision, subdir)):
        raise FoundationError("Git source fields must be strings")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or any(ord(c) < 33 for c in url)):
        raise FoundationError("Git source requires a credential-free HTTPS repository URL")
    if not GIT_REF.fullmatch(revision):
        raise FoundationError("Git source ref must be the approved full lowercase 40-character commit")
    if (not subdir or PurePosixPath(subdir).is_absolute()
            or not all(re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9._-]*", part)
                       for part in subdir.split("/"))):
        raise FoundationError("Git package path must be a normalized repository subdirectory")
    return {"url": url, "ref": revision, "path": subdir}


def git_read(repository: Path, *arguments: str) -> bytes:
    # Read Git objects directly; never invoke checkout, fetch, hooks, filters,
    # external diff drivers or a filesystem-monitor command.
    environment = {**os.environ, "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0"}
    result = subprocess.run(
        ["git", "--no-pager", "--no-replace-objects", "-c", "core.fsmonitor=false",
         "-C", str(repository), *arguments], capture_output=True, check=False, env=environment,
    )
    if result.returncode:
        raise FoundationError(f"Git source verification failed ({arguments[0]})")
    return result.stdout


def git_package_content(repository: Path, source: dict[str, str]) -> str:
    """Verify every tracked package byte against the qualified commit.

    Generated build/pub files may coexist with a package. Extra source/assets,
    symlinks, missing files, changed modes and replaced Git objects fail closed.
    The returned digest has no checkout/cache location in it.
    """
    revision, subdir = source["ref"], source["path"]
    actual = git_read(repository, "rev-parse", "--verify", f"{revision}^{{commit}}").decode().strip()
    if actual != revision:
        raise FoundationError("qualified Git commit is absent from the source repository")
    git_read(repository, "fsck", "--strict", "--no-reflogs", revision)
    raw = git_read(repository, "ls-tree", "-r", "-z", "--full-tree", revision, "--", subdir)
    package = repository / subdir
    if not package.is_dir():
        raise FoundationError("qualified package directory is absent")
    for candidate in [package, *package.parents]:
        if candidate == repository.parent:
            break
        if candidate.is_symlink():
            raise FoundationError("qualified package path contains a symlink")
    tracked: set[str] = set()
    digest = hashlib.sha256()
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        try:
            header, raw_name = entry.split(b"\t", 1)
            mode, kind, object_id = header.decode("ascii").split()
            name = raw_name.decode("utf-8")
            relative = PurePosixPath(name).relative_to(subdir).as_posix()
        except (ValueError, UnicodeDecodeError) as error:
            raise FoundationError("unsupported package Git-tree entry") from error
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise FoundationError("qualified packages cannot contain symlinks or submodules")
        candidate = package / relative
        if candidate.is_symlink() or not candidate.is_file():
            raise FoundationError(f"qualified package file missing or symlinked: {relative}")
        for parent in candidate.parents:
            if parent == package:
                break
            if parent.is_symlink():
                raise FoundationError("qualified package source directory is symlinked")
        data = candidate.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != object_id:
            raise FoundationError(f"qualified package content differs from commit: {relative}")
        if bool(candidate.stat().st_mode & 0o111) != (mode == "100755"):
            raise FoundationError(f"qualified package file mode differs: {relative}")
        tracked.add(relative)
        digest.update(mode.encode() + b" " + relative.encode() + b"\0" + bytes.fromhex(blob))
    if "pubspec.yaml" not in tracked:
        raise FoundationError("qualified Git package has no tracked pubspec")
    generated_files = {".DS_Store", ".packages", ".flutter-plugins", ".flutter-plugins-dependencies", "pubspec.lock"}
    for current, directories, names in os.walk(package, followlinks=False):
        for name in [*directories, *names]:
            if (Path(current) / name).is_symlink():
                raise FoundationError("qualified package contains an untracked symlink")
        directories[:] = [name for name in directories if name not in IGNORED_PARTS]
        for name in names:
            candidate = Path(current) / name
            relative = candidate.relative_to(package).as_posix()
            if relative not in tracked and not (candidate.parent == package and name in generated_files):
                raise FoundationError(f"unqualified extra package file: {relative}")
    return digest.hexdigest()


def package_config_roots(app_root: Path) -> dict[str, Path]:
    path = app_root / ".dart_tool/package_config.json"
    config = read_json(path)
    if config.get("configVersion") != 2 or not isinstance(config.get("packages"), list):
        raise FoundationError("package_config must be a resolved version-2 package map")
    result: dict[str, Path] = {}
    for row in config["packages"]:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str) or row["name"] in result:
            raise FoundationError("duplicate or malformed package_config entry")
        raw_uri = row.get("rootUri")
        if not isinstance(raw_uri, str):
            raise FoundationError("package_config rootUri must be a string")
        uri = urlsplit(raw_uri)
        if uri.scheme not in {"", "file"} or uri.netloc or uri.query or uri.fragment:
            raise FoundationError("package_config package roots must be local file URIs")
        raw_path = uri_unquote(uri.path)
        if not raw_path or "\0" in raw_path:
            raise FoundationError("invalid package_config rootUri")
        base = Path(raw_path) if uri.scheme == "file" else path.parent / raw_path
        if row.get("packageUri", "lib/") != "lib/":
            raise FoundationError("package_config must map package imports to lib/")
        result[row["name"]] = base.resolve()
    return result


def qualified_git_package(name: str, config: dict[str, Any], root: Path,
                          workspace: Path, *, verify_provider_worktree: bool = True) -> dict[str, Any]:
    # Dart Pub's GitSource clones URL-hashed bare mirrors into revision caches:
    # https://github.com/dart-lang/pub/blob/master/lib/src/source/git.dart
    source = git_descriptor(config.get("git"))
    cache = (Path(os.environ.get("PUB_CACHE", str(Path.home() / ".pub-cache"))).expanduser().resolve() / "git")
    repo_name = re.sub(r"[^a-zA-Z0-9._-]", "_", urlsplit(source["url"]).path.rstrip("/").split("/")[-1].removesuffix(".git"))[:50]
    checkout = cache / f"{repo_name}-{source['ref']}"
    expected_root = checkout / source["path"]
    if root != expected_root or not root.is_dir():
        raise FoundationError(f"{name} package_config does not identify the resolved Pub Git cache package")
    actual_checkout = Path(git_read(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if actual_checkout != checkout or git_read(checkout, "rev-parse", "HEAD").decode().strip() != source["ref"]:
        raise FoundationError(f"{name} cache checkout is not at the qualified immutable commit")
    mirror = cache / "cache" / f"{repo_name}-{hashlib.sha1(source['url'].encode()).hexdigest()}"
    origin = Path(git_read(checkout, "config", "--get", "remote.origin.url").decode().strip())
    if not origin.is_absolute() or origin.resolve() != mirror:
        raise FoundationError(f"{name} cache origin does not match Pub's approved URL mirror")
    if git_read(mirror, "config", "--get", "remote.origin.url").decode().strip() != source["url"]:
        raise FoundationError(f"{name} cache mirror URL differs from the approved repository")
    content = git_package_content(checkout, source)
    provider = within(workspace, config["path"])
    provider_repository = Path(git_read(provider, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if provider != provider_repository / source["path"]:
        raise FoundationError(f"{name} provider inventory path differs from its Git subdirectory")
    if verify_provider_worktree and git_package_content(provider_repository, source) != content:
        raise FoundationError(f"{name} provider and resolved Git package content differ")
    if not verify_provider_worktree:
        # Ordinary shared-source development may precede a new published pin.
        # Verify the provider's immutable tree object while consumer-cache bytes
        # remain strictly checked above. Release qualification retains the
        # stronger default worktree comparison.
        if git_read(provider_repository, 'ls-tree', '-r', source['ref'], '--', source['path']) != git_read(checkout, 'ls-tree', '-r', source['ref'], '--', source['path']):
            raise FoundationError(f'{name} provider immutable tree differs from resolved source')
    return {"identity": f"git:{source['url']}@{source['ref']}:{source['path']}",
            "contentSha256": content, "source": source, "root": root}


def provider_is_prohibited(name: str, standard: dict[str, Any]) -> bool:
    return name in standard["prohibitedProviderPackages"] or any(
        name.startswith(prefix) for prefix in standard["prohibitedProviderPrefixes"]
    )


def check_workflow(text: str) -> list[str]:
    errors = []
    event_block = re.search(r"(?ms)^on:\s*\n(.*?)(?=^\S|\Z)", text)
    if not event_block:
        return ["unsupported/missing explicit on mapping"]
    events = re.findall(r"(?m)^  ([\w-]+):", event_block.group(1))
    if not events or set(events) - {"push", "workflow_dispatch"}:
        errors.append("only main push and workflow_dispatch events are allowed")
    if "push" in events:
        push = re.search(r"(?ms)^  push:\s*\n(.*?)(?=^  \S|\Z)", event_block.group(1))
        if not push or not re.search(r"(?m)^    branches:\s*\[\s*['\"]?main['\"]?\s*\]\s*$", push.group(1)):
            errors.append("push must be filtered to branches: [main]")
        if push and re.search(r"(?m)^    (tags|branches-ignore|tags-ignore):", push.group(1)):
            errors.append("alternate push branch/tag filters are forbidden")
    if re.search(r"(?m)^\s+inputs:", event_block.group(1)):
        errors.append("workflow dispatch inputs are outside the allowed policy")
    jobs = re.search(r"(?ms)^jobs:\s*\n(.*)\Z", text)
    if not jobs:
        errors.append("workflow has no jobs mapping")
    else:
        for job in re.finditer(r"(?ms)^  ([\w-]+):\s*\n(.*?)(?=^  \S|\Z)", jobs.group(1)):
            header = re.split(r"(?m)^    (?:steps|uses):", job.group(2), maxsplit=1)[0]
            guard = re.search(r"(?m)^    if:\s*(.*)$", header)
            expression = re.sub(r"\s+", " ", guard.group(1).strip()) if guard else ""
            expression = expression.removeprefix("${{").removesuffix("}}").strip()
            expression = expression.replace('"', "'")
            allowed_guards = {
                "github.ref == 'refs/heads/main'",
                "github.ref == 'refs/heads/main' && (github.event_name == 'push' || github.event_name == 'workflow_dispatch')",
            }
            if expression not in allowed_guards:
                errors.append(f"job {job.group(1)} lacks a main-ref execution guard")
    if re.search(r"(?m)^\s+ref:", text):
        errors.append("checkout/ref overrides are not allowed")
    return errors


def android_toolchain_errors(app_root: Path, baseline: dict[str, Any]) -> list[str]:
    errors = []
    settings = (app_root / "android/settings.gradle.kts").read_text()
    wrapper = (app_root / "android/gradle/wrapper/gradle-wrapper.properties").read_text()
    build = (app_root / "android/app/build.gradle.kts").read_text()
    for name, plugin in [("agp", "com.android.application"), ("kotlin", "org.jetbrains.kotlin.android")]:
        match = re.search(r'id\("' + re.escape(plugin) + r'"\) version "([^"]+)"', settings)
        if not match or match.group(1) != baseline[name]:
            errors.append(f"Android {name} must be {baseline[name]}")
    match = re.search(r'gradle-([\d.]+)-(?:all|bin)\.zip', wrapper)
    if not match or match.group(1) != baseline["gradle"]:
        errors.append(f"Android Gradle wrapper must be {baseline['gradle']}")
    target = str(baseline["jvmTarget"])
    for name in ["sourceCompatibility", "targetCompatibility"]:
        if not re.search(r'(?m)^\s*' + name + r'\s*=\s*JavaVersion\.VERSION_' + target + r'\s*$', build):
            errors.append(f"Android {name} must be JVM {target}")
    if not re.search(r'(?m)^\s*jvmTarget\s*=\s*(?:org\.jetbrains\.kotlin\.gradle\.dsl\.)?JvmTarget\.JVM_' + target + r'\s*$', build):
        errors.append(f"Android Kotlin target must be JVM {target}")
    return errors


def flutter_ci_version_errors(text: str, version: str) -> list[str]:
    if not re.search(r'uses:\s*subosito/flutter-action@', text):
        return []
    pins = re.findall(r'(?m)^\s+flutter-version:\s*(.*?)\s*$', text)
    if not pins:
        return ["Flutter CI action must pin the approved SDK version"]
    for pin in pins:
        value = unquote(pin)
        variable = re.fullmatch(r'\$\{\{\s*env\.([A-Z_]+)\s*\}\}', value)
        if variable:
            found = re.search(r'(?m)^\s*' + re.escape(variable.group(1)) + r':\s*(.*?)\s*$', text)
            value = unquote(found.group(1)) if found else ""
        if value != version:
            return [f"Flutter CI SDK must be {version}"]
    return []


def source_fingerprint(app_root: Path, package_roots: list[Path], workspace: Path,
                       qualified_packages: dict[Path, dict[str, Any]] | None = None) -> str:
    qualified_packages = qualified_packages or {}
    files: set[Path] = set()
    for base in [app_root, *package_roots]:
        if base in qualified_packages:
            continue
        for relative in ["lib", "test", "integration_test", "ios", "android", "scripts", "tool", "assets"]:
            directory = base / relative
            if directory.is_dir():
                for current, directories, names in os.walk(directory, followlinks=False):
                    directories[:] = [name for name in directories if name not in IGNORED_PARTS
                                      and not (Path(current) / name).is_symlink()
                                      and (Path(current) / name).relative_to(base).as_posix()
                                      not in GENERATED_SOURCE_DIRECTORIES]
                    files.update(Path(current) / name for name in names
                                 if not (Path(current) / name).is_symlink()
                                 and (Path(current) / name).relative_to(base).as_posix()
                                 not in GENERATED_SOURCE_FILES)
        for relative in ["pubspec.yaml", "pubspec.lock", ".flutter-version", "analysis_options.yaml"]:
            if (base / relative).is_file():
                files.add(base / relative)
    digest = hashlib.sha256()
    digest.update(f"majestic-foundation/source-fingerprint/v{SOURCE_FINGERPRINT_POLICY_VERSION}\0".encode())
    for path in sorted(files, key=lambda item: str(item.relative_to(workspace))):
        digest.update(str(path.relative_to(workspace)).encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    for package in sorted(qualified_packages.values(), key=lambda item: item["identity"]):
        digest.update(package["identity"].encode() + b"\0")
        digest.update(bytes.fromhex(package["contentSha256"]))
    return digest.hexdigest()


def evidence_errors(evidence: Any, required: list[str], root: Path, fingerprint: str) -> list[str]:
    if not isinstance(evidence, dict):
        return ["evidence must be an object"]
    errors = []
    for name in required:
        record = evidence.get(name)
        if not isinstance(record, dict) or record.get("status") != "passed":
            errors.append(f"{name}: pending")
            continue
        try:
            artifact = within(root, record.get("record", ""))
            if not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest() != record.get("sha256"):
                raise FoundationError("evidence file missing or hash differs")
            datetime.fromisoformat(str(record.get("recordedAt", "")).replace("Z", "+00:00"))
            if record.get("sourceFingerprint") != fingerprint:
                raise FoundationError("evidence belongs to another source fingerprint")
            if name.startswith(("physical_", "native_store_")) and not record.get("recordedBy"):
                raise FoundationError("representative physical/store evidence needs recordedBy")
        except (OSError, ValueError) as error:
            errors.append(f"{name}: {error}")
    return errors


def selected_shared_packages(standard: dict[str, Any], manifest: dict[str, Any], pubspec: dict[str, Any], lock: dict[str, Any]) -> dict[str, Any]:
    """Select maintained optional modules only when this consumer actually declares/resolves them."""
    selected = dict(standard["packages"])
    for name, config in standard.get("optionalSharedPackages", {}).items():
        if name in lock or name in manifest.get("packages", {}) or name in pubspec["dependencies"]:
            selected[name] = config
    return selected


def inspect_consumer(consumer: dict[str, str], standard: dict[str, Any], matrix: dict[str, Any], workspace: Path, *, enforce_dev: bool = True, verify_provider_worktree: bool = True) -> dict[str, Any]:
    app_root = within(workspace, consumer["path"])
    errors: list[str] = []
    manifest = read_json(app_root / "foundation.json")
    if manifest.get("schemaVersion") != 1 or manifest.get("application") != consumer["id"]:
        errors.append("foundation manifest identity/schema mismatch")
    if manifest.get("foundationVersion") != standard["foundationVersion"] or manifest.get("status") not in STATUSES:
        errors.append("foundation version/status mismatch")
    if manifest.get("toolchain") != standard["toolchain"]:
        errors.append("manifest toolchain differs from approved baseline")
    if (app_root / ".flutter-version").read_text().strip() != standard["toolchain"]["flutter"]:
        errors.append(".flutter-version does not match exact approved Flutter SDK")
    expected_caps = next((x["capabilities"] for x in matrix["consumers"] if x["id"] == consumer["id"]), None)
    if manifest.get("capabilities") != expected_caps:
        errors.append("capability applicability differs from canonical matrix")
    provenance = manifest.get("packageProvenance")
    if provenance not in {"workspace-unpublished", "git-immutable"}:
        errors.append("package provenance must be workspace-unpublished or git-immutable")
    if provenance != standard.get("packageProvenance"):
        errors.append("package provenance differs from the approved production baseline")
    pubspec = parse_pubspec((app_root / "pubspec.yaml").read_text())
    overrides_path = app_root / "pubspec_overrides.yaml"
    if overrides_path.exists():
        extra = parse_pubspec(overrides_path.read_text())["dependency_overrides"]
        pubspec["dependency_overrides"].update(extra)
    if pubspec.get("dartConstraint") != standard["toolchain"]["dartConstraint"]:
        errors.append("Dart SDK constraint differs from approved exact minimum")
    if not pubspec.get("encryptedSqliteHook"):
        errors.append("consumer must select the sqlite3mc encrypted SQLite build hook")
    lock = parse_lock((app_root / "pubspec.lock").read_text())
    selected_packages = selected_shared_packages(standard, manifest, pubspec, lock)
    for name, config in selected_packages.items():
        if name in standard.get("optionalSharedPackages", {}) and not any(
            manifest.get("capabilities", {}).get(capability) == "required" for capability in config["capabilities"]
        ):
            errors.append(f"{name} lacks an applicable declared capability")
    package_roots: list[Path] = []
    qualified_packages: dict[Path, dict[str, Any]] = {}
    immutable_sources: list[dict[str, str]] = []
    resolved_roots = package_config_roots(app_root)
    for name, version in standard["coreDependencies"].items():
        if lock.get(name, {}).get("version") != version:
            errors.append(f"resolved {name} must be {version}")
    for name, config in standard["optionalDependencies"].items():
        if name in lock and lock[name].get("version") != config["version"]:
            errors.append(f"resolved optional {name} must be {config['version']}")
    for name, version in standard.get("compatibilityDependencies", {}).items():
        if name in lock and lock[name].get("version") != version:
            errors.append(f"resolved compatibility dependency {name} must be {version}")
    for name, version in standard.get("resolvedPlatformDependencies", {}).items():
        if name in lock and lock[name].get("version") != version:
            errors.append(f"resolved platform implementation {name} must be {version}")
    prohibited = sorted(name for name in lock if provider_is_prohibited(name, standard))
    if prohibited:
        errors.append("prohibited provider SDKs in lockfile: " + ", ".join(prohibited))
    first_party = [(app_root, pubspec)]
    imports: set[str] = set()
    for name, config in selected_packages.items():
        declaration = manifest.get("packages", {}).get(name, {})
        entry = lock.get(name, {})
        try:
            if declaration.get("version") != config["version"] or entry.get("version") != config["version"]:
                raise FoundationError("manifest/lock package version differs from the approved version")
            expected = resolved_roots.get(name)
            if expected is None:
                raise FoundationError("package is absent from package_config")
            if provenance == "git-immutable":
                approved = git_descriptor(config.get("git"))
                if set(declaration) != {"version", "git"} or git_descriptor(declaration.get("git")) != approved:
                    raise FoundationError("manifest Git descriptor differs from the approved source")
                direct = pubspec["dependencies"].get(name, {})
                if (set(direct) - {"version", "git"} or git_descriptor(direct.get("git")) != approved
                        or direct.get("version") not in {"", config["version"]}):
                    raise FoundationError("direct Git dependency differs from the approved source")
                if name in pubspec["dependency_overrides"]:
                    raise FoundationError("shared-package overrides are forbidden in immutable Git mode")
                if (entry.get("source") != "git" or any(entry.get(key) != value for key, value in approved.items())
                        or entry.get("resolved-ref") != approved["ref"]):
                    raise FoundationError("lock Git URL/ref/path/resolved-ref differs from the approved source")
                qualified = qualified_git_package(name, config, expected, workspace, verify_provider_worktree=verify_provider_worktree)
                qualified_packages[expected] = qualified
                immutable_sources.append({"package": name, **approved, "contentSha256": qualified["contentSha256"]})
            else:
                provider = within(workspace, config["path"])
                if (set(declaration) != {"version", "path"}
                        or (app_root / declaration.get("path", "")).resolve() != provider):
                    raise FoundationError("manifest workspace source differs from the approved provider")
                effective = pubspec["dependency_overrides"].get(name, pubspec["dependencies"].get(name, {}))
                if effective.get("path") is None or (app_root / effective["path"]).resolve() != provider:
                    raise FoundationError("effective workspace dependency differs from the approved provider")
                if (entry.get("source") != "path" or (app_root / entry.get("path", "")).resolve() != provider
                        or expected != provider):
                    raise FoundationError("lock/package_config workspace path differs from the approved provider")
            if not (expected / "pubspec.yaml").is_file():
                raise FoundationError("resolved package pubspec is absent")
        except (FoundationError, ValueError, TypeError) as error:
            errors.append(f"{name}: {error}")
            continue
        package_roots.append(expected)
        package_spec = parse_pubspec((expected / "pubspec.yaml").read_text())
        if package_spec.get("name") != name or package_spec.get("version") != config["version"]:
            errors.append(f"{name} source identity/version mismatch")
        first_party.append((expected, package_spec))
    for base, spec in first_party:
        for section in ["dependencies", "dev_dependencies", "dependency_overrides"]:
            for name, dependency in spec[section].items():
                if provider_is_prohibited(name, standard):
                    errors.append(f"prohibited first-party dependency {name}")
                approved = (standard["coreDependencies"].get(name) or standard.get("compatibilityDependencies", {}).get(name)
                            or standard.get("resolvedPlatformDependencies", {}).get(name))
                optional = standard["optionalDependencies"].get(name)
                if optional:
                    approved = optional["version"]
                    if manifest.get("capabilities", {}).get(optional["capability"]) != "required":
                        errors.append(f"{name} requires declared {optional['capability']} capability")
                if approved and dependency.get("version") != approved:
                    errors.append(f"first-party {name} constraint must be exact {approved}")
                if name in standard["networkPackages"]:
                    if consumer["kind"] == "template" or manifest.get("capabilities", {}).get("network_lookup") != "required" or not manifest.get("networkLookups"):
                        errors.append(f"direct {name} requires an app-specific disclosed network lookup; forbidden in the default template")
        for path in (base / "lib").rglob("*.dart"):
            imports.update(re.findall(r"(?:import|export)\s+['\"]package:(majestic_\w+)/", path.read_text()))
    for name in selected_packages:
        if name not in imports:
            errors.append(f"no first-party import/export adopts {name}")
    for platform in standard["toolchain"]["platforms"]:
        if not (app_root / platform).is_dir():
            errors.append(f"missing first-release {platform} platform source")
    errors.extend(android_toolchain_errors(app_root, standard["androidToolchain"]))
    repository = app_root.parent if consumer["id"] == "Namefold" else app_root
    branch = subprocess.run(["git", "-C", str(repository), "branch", "--show-current"], capture_output=True, text=True, check=False)
    if enforce_dev and (branch.returncode or branch.stdout.strip() != "dev"):
        errors.append("foundation adoption work must remain on dev")
    for workflow in sorted((repository / ".github/workflows").glob("*.y*ml")):
        workflow_text = workflow.read_text()
        errors.extend(f"{workflow.name}: {error}" for error in check_workflow(workflow_text))
        errors.extend(f"{workflow.name}: {error}" for error in flutter_ci_version_errors(workflow_text, standard["toolchain"]["flutter"]))
    fingerprint = source_fingerprint(app_root, package_roots, workspace, qualified_packages)
    checks = standard["templateChecks"] if consumer["kind"] == "template" else standard["consumerChecks"]
    pending = evidence_errors(manifest.get("evidence", {}), checks, app_root, fingerprint)
    return {"application": consumer["id"], "declaredStatus": manifest.get("status"),
            "sourceFingerprintPolicyVersion": SOURCE_FINGERPRINT_POLICY_VERSION,
            "packageProvenance": provenance,
            "immutablePackageRevisions": "passed" if provenance == "git-immutable" and len(immutable_sources) == len(selected_packages) and not errors else "pending",
            "verifiedPackageSources": immutable_sources,
            "staticAdoption": "passed" if not errors else "pending", "errors": sorted(set(errors)),
            "sourceFingerprint": fingerprint, "foundationEvidence": "passed" if not pending else "pending",
            "pendingEvidence": pending}


def immutable_revision_errors(results: list[dict[str, Any]]) -> list[str]:
    return [f"{row['application']}: immutable_package_revisions pending (requires actual approved Git resolution/cache/provider verification)"
            for row in results if row.get("packageProvenance") != "git-immutable"
            or row.get("immutablePackageRevisions") != "passed" or row.get("staticAdoption") != "passed"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=REPO_ROOT.parent)
    parser.add_argument("--app", action="append", help="inspect a named consumer; repeat as needed")
    parser.add_argument("--release-gate", action="store_true", help="also require foundation evidence and representative qualification; not full product release QA")
    args = parser.parse_args()
    try:
        standard = read_json(STANDARD_PATH)
        matrix = read_json(REPO_ROOT / "portfolio/CAPABILITY_MATRIX.json")
        consumers = standard["consumers"]
        if args.app:
            unknown = set(args.app) - {item["id"] for item in consumers}
            if unknown:
                raise FoundationError("unknown/excluded consumer: " + ", ".join(sorted(unknown)))
            consumers = [item for item in consumers if item["id"] in args.app]
        results = []
        for consumer in consumers:
            try:
                results.append(inspect_consumer(consumer, standard, matrix, args.workspace_root.resolve()))
            except (FoundationError, OSError, KeyError, TypeError) as error:
                results.append({"application": consumer["id"], "staticAdoption": "pending", "errors": [str(error)], "foundationEvidence": "pending"})
        cohort = hashlib.sha256("\n".join(f"{x['application']}:{x.get('sourceFingerprint', 'unavailable')}" for x in results).encode()).hexdigest()
        qualification = read_json(REPO_ROOT / "portfolio/FOUNDATION_QUALIFICATION.json")
        qualification_pending = evidence_errors(qualification.get("evidence", {}), standard["qualificationChecks"], REPO_ROOT, cohort)
        complete_cohort = not args.app or {x["id"] for x in consumers} == {x["id"] for x in standard["consumers"]}
        static_ok = all(x["staticAdoption"] == "passed" for x in results)
        development_ok = complete_cohort and static_ok and all(x["foundationEvidence"] == "passed" for x in results) and not qualification_pending
        immutable_pending = immutable_revision_errors(results)
        gate_ok = development_ok and not immutable_pending
        report = {"foundationVersion": standard["foundationVersion"], "results": results,
                  "sourceFingerprintPolicyVersion": SOURCE_FINGERPRINT_POLICY_VERSION,
                  "cohortFingerprint": cohort, "qualificationPending": qualification_pending,
                  "immutablePackageRevisions": "passed" if not immutable_pending else "pending", "productionPending": immutable_pending,
                  "developmentQualification": "verified" if development_ok else "pending",
                  "foundationGate": "verified" if gate_ok else "pending",
                  "productReleaseQA": "separate; this checker cannot approve publication"}
        print(json.dumps(report, indent=2))
        return 0 if (gate_ok if args.release_gate else static_ok) else 1
    except (FoundationError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"foundationGate": "pending", "error": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
