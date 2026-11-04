# Majestic Made portfolio and engineering guidance

Organization profile, repository inventory, product release queue, and shared consumer-app standards
for Majestic Made LLC. This repository supports the apps; it is not a consumer product.

Consumer records stay on-device by default, with deliberate owner exports and encrypted recovery.
Optional user-owned hosting is later work. Native store billing communicates with Apple/Google;
product-specific network capabilities must be disclosed. Existing local products target permanent
unlocks, with Skepbook's established pricing preserved.

- [Repository inventory and current status](portfolio/STATUS.md): all 28 repositories, including the two exclusions.
- [Exact 17-product release order](portfolio/LAUNCH_SLATE.md): starts with Skepbook after foundation qualification.
- [Shared Flutter/Dart foundation](portfolio/STACK_STANDARD.md): iOS and Android, encrypted local storage,
  native privacy/recovery/billing, and deliberately adopted immutable shared-package revisions.
- [Independent product release requirements](portfolio/RELEASE_DEFINITION.md).
- [Latest software/source qualification](portfolio/GIT_SOURCE_ADOPTION_2026-11-04.md).

The seven implemented apps and template pass their recorded software and immutable-source checks.
Physical iPhone/Android privacy and actual native-store purchase/restore checks remain pending.
A promotion to `main` records accepted source; it does not establish store readiness or deploy a website.
The website publication pause remains in force. Dossier and OffRecord are excluded from this initiative.
Claim Crate and Steward retain their repositories while their requirements consolidate into What We Own;
Kinwall remains research-only with no release slot. Current technical repository names are retained.

Normal work stays on `dev`. Promote directly to `main` only on explicit owner instruction, then sync
`dev` to the same commit. Open a pull request only if requested. GitHub Actions may run only for allowed
main-branch pushes or guarded manual main runs; development validation runs locally.

```bash
python3 scripts/portfolio_status.py --check
python3 scripts/check_foundation.py --workspace-root ..
python3 -m unittest discover -s tests -v
```

The checker reports a pending foundation gate honestly. `--release-gate` remains nonzero until the
missing physical/store evidence is recorded. No command here submits an app or provisions a backend.
