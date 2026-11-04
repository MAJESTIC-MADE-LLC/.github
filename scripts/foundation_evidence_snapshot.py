#!/usr/bin/env python3
"""Capture current source fingerprints and log hashes without approving any check.

Run before/after local qualification commands. This never edits foundation
manifests, interprets a log as a pass, or marks physical/store evidence complete.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import check_foundation as foundation


def file_record(path: Path) -> dict[str, Any]:
    path = path.resolve(strict=True)
    if not path.is_file():
        raise foundation.FoundationError(f"log is not a file: {path}")
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
            "modifiedAt": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()}


def compare_sources(previous: dict[str, Any], current: dict[str, Any]) -> list[str]:
    before = {row["application"]: row["sourceFingerprint"] for row in previous["consumers"]}
    after = {row["application"]: row["sourceFingerprint"] for row in current["consumers"]}
    return sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=foundation.REPO_ROOT.parent)
    parser.add_argument("--log", nargs=3, action="append", default=[], metavar=("APPLICATION", "CHECK", "PATH"))
    parser.add_argument("--compare", type=Path, help="prior snapshot; report source drift")
    parser.add_argument("--output", type=Path, help="new snapshot file; refuses to overwrite")
    args = parser.parse_args()
    try:
        standard = foundation.read_json(foundation.STANDARD_PATH)
        matrix = foundation.read_json(foundation.REPO_ROOT / "portfolio/CAPABILITY_MATRIX.json")
        consumers = []
        for consumer in standard["consumers"]:
            result = foundation.inspect_consumer(consumer, standard, matrix, args.workspace_root.resolve())
            consumers.append({"application": result["application"], "sourceFingerprint": result["sourceFingerprint"],
                              "staticAdoption": result["staticAdoption"], "errors": result["errors"]})
        cohort = hashlib.sha256("\n".join(f"{row['application']}:{row['sourceFingerprint']}" for row in consumers).encode()).hexdigest()
        record = {"schemaVersion": 1, "capturedAt": datetime.now(timezone.utc).isoformat(),
                  "foundationVersion": standard["foundationVersion"], "toolchain": standard["toolchain"],
                  "consumers": consumers, "cohortFingerprint": cohort, "logs": [],
                  "assessment": "Unassessed source/log snapshot. Owner review records actual checks separately; physical/store qualification is never inferred."}
        fingerprints = {row["application"]: row["sourceFingerprint"] for row in consumers}
        allowed_checks = set(standard["consumerChecks"] + standard["templateChecks"] + standard["qualificationChecks"])
        for application, check, path in args.log:
            if application not in fingerprints and application != "cohort":
                raise foundation.FoundationError(f"unknown application: {application}")
            if check not in allowed_checks:
                raise foundation.FoundationError(f"unknown check: {check}")
            record["logs"].append({"application": application, "check": check,
                                   "sourceFingerprint": cohort if application == "cohort" else fingerprints[application],
                                   **file_record(Path(path))})
        if args.compare:
            record["sourcesChangedSincePriorSnapshot"] = compare_sources(foundation.read_json(args.compare), record)
        output = json.dumps(record, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as destination:
                destination.write(output)
            print(f"Unassessed snapshot written: {args.output}")
        else:
            print(output, end="")
        return 0
    except (OSError, KeyError, ValueError) as error:
        print(json.dumps({"error": str(error), "assessment": "unassessed"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
