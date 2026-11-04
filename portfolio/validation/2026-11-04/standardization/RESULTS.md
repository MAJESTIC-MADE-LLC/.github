# Local standardization enforcement — November 4, 2026

This task changes local configuration/checks and web dependency pins. No commit, push, workflow
run, store provisioning, service installation, deployment or publication was performed.

## Completed checks

| Command / scope | Result |
| --- | --- |
| `python3 scripts/check_standardization.py` | Pass: 25 registered repositories, template + seven native applications, 23 active workflows, all registered dependency profiles and optional hosting |
| `python3 scripts/portfolio_status.py --check` | Pass: inventory of 27 repositories |
| `python3 -m unittest discover -s tests -q` in governance | 107 tests pass |
| `python3 -m unittest discover -s tool/tests -q` in App-Template | 23 hosting policy mutation tests pass |
| Hosting checker with `--consumer-standard ../.github/portfolio/STACK_STANDARD.json` | Pass; release qualification explicitly pending |
| Hub on Node 26.13.0 | Clean install, lint, typecheck and production static build pass; final rerun after concurrent UI edits passes all 161 tests |
| Namefold web on Node 26.13.0 | Clean install, lint, 9 unit + 10 static/service-worker tests, typecheck and production export/offline shell pass |
| Metadata verifier on Node 26.13.0 | 27 tests pass; no live vendor calls |
| Hub install under Node 24 | Correctly rejects incompatible engine with EBADENGINE |

Node 26.13.0 was installed in the user's nvm version directory without changing the machine
default. The official Node distribution index identifies this as the latest LTS as checked today.
Active web framework pins are Next 16.4.3, React/React DOM 19.3.1 and matching eslint-config-next.
Native toolchains, product runtime source and immutable foundation revisions were not upgraded.

## Enforcement and scope

The installer sets only repository-local `core.hooksPath` for all 25 registered local repositories.
It preflights and preserves existing custom hooks. Guards are tracked under governance `.githooks/`.
No hosted CI trigger or job was added or changed. Automated checks remain main-only.

All 25 local hook configurations were verified. Directly invoking the installed pre-commit wrapper
in Paws passes without making a commit. Invoking its pre-push wrapper with the local ref correctly
rejects the still-uncommitted governance policy, without contacting any remote or making a push.
The fresh foundation `--release-gate` returns the expected nonzero result: all eight static-adoption
checks pass, while old source evidence and physical/store qualification remain pending.

Tests cover version/lock mismatches, new dependencies, missing/new manifests, complete cohort
membership, strict npm engines, CI trigger/guard/permission/action-pin bypasses, partial staging,
pushing a different configuration snapshot, shared-import/native-permission changes, inherited Git
environment isolation, and preservation of existing hooks. Consumer Git cache verification remains
strict while maintained shared implementation can develop ahead of consumer pins. Release checks
retain their separate strict provider/source-bound evidence behavior.

This record is an engineering alignment result. It does not refresh old `foundation.json` evidence
or establish physical-device, native-store, product-release or self-hosting qualification. Skepbook's
QR capability now agrees with its implemented scanner/labels; no product feature was removed.
