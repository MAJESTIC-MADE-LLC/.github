# Inventory and portfolio refresh — November 6, 2026

## Changes

- The concept inventory audit recognizes only the preserved Claim Crate subtree in What We Own,
  pinned to Git tree `6cf2806181232be46a022606307bfa9a14f91446`. Changed/missing history and
  implementation outside that exact archive still fail. The original history is unchanged.
- Current portfolio/product docs describe all seven native subscription implementations and the
  template, plus published optional hosting adoption by Pantry Clock, Paws and Daymerit.
- Hub source includes reconciled product pages and the Lockbox concept/waitlist source. Migration
  `0005_lockbox_waitlist.sql` is included and tested locally, not applied to a live database.
- Daymerit private household record deletion is still unfinished; implemented shared-proof
  deletion does not satisfy that task. The 17-product queue and website publication pause remain.

## Local validation

Run from the workspace root unless otherwise noted. Hub checks use its pinned Node 26.13.0.

| Command | Result |
| --- | --- |
| `python3 .github/scripts/portfolio_status.py --check --workspace-root . --verify-github MAJESTIC-MADE-LLC` | Passed: all 27 GitHub repositories, local evidence and concept classifications |
| `python3 -m unittest discover -s .github/tests -v` | 120 tests passed, including archive preservation/change/missing/boundary cases |
| `python3 .github/scripts/check_standardization.py` | Passed: 25 local repositories, template plus seven apps, 22 main-only workflows |
| `python3 .github/scripts/install_standardization_hooks.py` | Tracked pre-commit/pre-push guards installed in all 25 local repositories |
| Hub: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` | Passed: 201 tests and production static export, including Lockbox migration preservation/failure behavior |
| `git diff --check` in each modified checkout | Passed |
| `python3 .github/scripts/check_foundation.py --release-gate` | Expected pending/nonzero: immutable package revisions and static adoption pass; current source-bound cohort evidence, physical iOS/Android privacy and actual native-store acceptance remain pending |

No native implementation changed in this refresh and native suites/builds were not rerun. The
November 5 source-specific hosting records retain their original scope; no qualification manifest
or historical evidence was restamped. Hosted CI is optional and is not claimed as passed here.

## Branch and publication boundary

The owner authorized logical dev commits/pushes followed by direct main promotion. Preflight
fetched all 25 managed remotes: all local heads matched remote dev, 23 dev branches were ahead of
main, and none were behind. Excluded Dossier/OffRecord are outside this promotion. Exact before/
after refs are retained under `.archives/validation/portfolio-refresh-2026-11-06/` in the workspace.
Branch promotion approves source; it does not publish websites, migrate live signup data, deploy
services, provision store products or approve an app release.
