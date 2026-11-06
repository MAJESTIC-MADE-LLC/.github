# Majestic Made portfolio and engineering guidance

Organization profile, repository inventory, product release queue, and shared consumer-app standards
for Majestic Made LLC. This repository supports the apps; it is not a consumer product.

Consumer records stay on-device by default, with deliberate owner exports and encrypted recovery.
Optional user-owned hosting has published reference/runtime source and regular-build integrations
in Pantry Clock, Paws and Daymerit; signed services, live licensing and physical qualification
remain pending. Native store billing communicates with Apple/Google;
product-specific network capabilities must be disclosed. Core app access is subscription-only for
new purchases; one-time purchases are limited to optional extras. See the approved
[monthly/annual prices and access policy](portfolio/PRICING.md).

- [Repository inventory and current status](portfolio/STATUS.md): current repositories, including the two exclusions.
- [Exact 17-product release order](portfolio/LAUNCH_SLATE.md): starts with Skepbook after foundation qualification.
- [Shared Flutter/Dart foundation](portfolio/STACK_STANDARD.md): iOS and Android, encrypted local storage,
  native privacy/recovery/billing, and deliberately adopted immutable shared-package revisions.
- [Enforced portfolio standardization](portfolio/STANDARDIZATION.md): one offline drift gate and
  tracked local commit/push hooks for native apps, web surfaces, optional hosting and main-only CI.
- [Optional user-owned hosting](portfolio/USER_OWNED_HOSTING.md): optional Mac/Windows ciphertext storage with a separately
  trusted selected-collection coordinator, private-network sharing and bounded workspace grants. Local-only
  releases of its adopted apps gain no additional hosting prerequisite; Skepbook’s approved combined
  release has a separate hosting requirement.
- [Independent product release requirements](portfolio/RELEASE_DEFINITION.md).
- [Current software qualification and formatting cleanup](portfolio/validation/2026-11-06/formatting-refresh/RESULTS.md).
- [November 4 software/source qualification](portfolio/GIT_SOURCE_ADOPTION_2026-11-04.md).
- [Main promotion and repository metadata review](portfolio/MAIN_PROMOTION_2026-11-04.md).

The seven implemented apps and template have current source-bound software evidence: analysis,
tests, both native builds and immutable package verification pass. Representative physical
iPhone/Android privacy and actual native-store purchase/restore qualification remain pending.
A promotion to `main` records accepted source; it does not establish store readiness or deploy a website.
The website publication pause remains in force. Dossier and OffRecord are excluded from this initiative.
Claim Crate's requirements and source documents are consolidated into What We Own, with no
independent app or subscription. Its redundant remote and local repository was deleted under the
owner's explicit November 4 instruction after verified preservation; see
[the consolidation record](portfolio/CLAIM_CRATE_CONSOLIDATION.md).
Steward marketing is consolidated in Hub, with its previous stack archived. Live signup-list
reconciliation and domain cutover remain pending. Kinwall remains research-only.

Normal work stays on `dev`. Promote directly to `main` only on explicit owner instruction, then sync
`dev` to the same commit. Open a pull request only if requested. GitHub Actions may run only for allowed
main-branch pushes or guarded manual main runs; development validation runs locally.

```bash
python3 scripts/portfolio_status.py --check
python3 scripts/check_standardization.py --workspace-root ..
python3 scripts/install_standardization_hooks.py --workspace-root ..
python3 scripts/check_foundation.py --workspace-root ..
python3 -m unittest discover -s tests -v
```

The checker reports a pending foundation gate honestly. `--release-gate` remains nonzero until the
missing representative physical/store evidence is recorded. No command here submits an app or provisions a backend.
