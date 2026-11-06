# Portfolio Alignment — reconciled November 6, 2026

## Current implementation and approved direction

Majestic Made builds affordable apps with useful core workflows and encrypted on-device records.
Exports are deliberate user actions. Optional sync uses explicit destination/collection enrollment
as scoped standing authorization. Pantry Clock, Paws and Daymerit implement selected-record
user-owned hosting in their pre-launch regular builds; service, licensing and physical/store
qualification remain pending. Other products adopt separately. No company-operated record backend
is required. Native billing, optional disclosed lookups and minimal website business-contact forms
are separate network flows.

The [shared stack standard](STACK_STANDARD.md) requires the template and all seven existing apps
to adopt and qualify the maintained foundation before **any** app release, with iOS and Android in
each first release. Implementation and dated local validation exist; current source-bound cohort
qualification and representative physical/store checks remain pending. Passing dependency alignment
does not refresh historical evidence. The gate covers shared contracts/builds and representative
boundaries, rather than every product's complete domain/release QA. After qualification, finish
each product's [release gates](RELEASE_DEFINITION.md) in the unchanged [queue](LAUNCH_SLATE.md).

All seven apps and the template implement monthly/annual subscription source and a separate
non-billing 14-day local trial. Preserve authentic legacy ownership and existing reading, exports,
deletion and authenticated encrypted recovery after expiry. Daymerit's remaining general deletion
workflow stays separate from implemented shared-proof deletion and must be completed before release. Store product setup and actual transactions remain pending.
See [pricing](PRICING.md), [status](STATUS.md) and the [data matrix](DATA_COST_MATRIX.md).

## Consolidation and boundaries

- What We Own owns the combined home/moving/claims concept, including Claim Crate's PCS/box/QR,
  condition, damage and claim-export requirements. Claim Crate source/provenance is preserved in
  What We Own; its redundant remote/local repository was deleted November 4 after verified backup.
- Steward marketing and fresh What We Own signup use Hub routes. The former Next.js source is
  preserved with checksums in Steward's November 5 archive. The offline review importer preserves
  original one-launch-email/founding-rate permission; live export/count reconciliation, subscriber
  transfer and domain cutover remain unperformed. Ongoing updates require fresh consent.
- Keep specialist experiences and their private databases, keys, branding and recovery formats
  independent while reusing maintained common modules. Fine Notes remains one tasting app across
  wine, whiskey, coffee and cigars. Object Lore requires collector-specific workflows to justify
  its separate scope.
- Daymerit's local parent/shared-tablet household stays independent of explicitly enrolled family
  hosting. Namefold has an encrypted native wallet and a separate static PWA with unencrypted
  browser drafts/backups; managed public links remain deferred. Ridelore's optional user-requested
  NHTSA VIN/model-year decoding requires its own disclosure; recall status stays manual.
- Lockbox remains a concept for local documents and explicit encrypted handoff. Autonomous
  time-release/dead-man delivery remains deferred. Kinwall is research-only; Dossier and Off Record
  are excluded. Quiet Arcade is a Hub-only concept without a repository.

## Published optional hosting

The [hosting architecture](USER_OWNED_HOSTING.md) distinguishes the ciphertext-only storage daemon
from an independently enrolled desktop coordinator trusted to read selected collections. The
published optional modules at `f74c7e709730b75e073a01bfcb7ef07100819a79` are deliberately adopted by
Pantry Clock, Paws and Daymerit; core/report/media/reminder pins remain unchanged. Shared scope and
workspace engines provide pairing, encrypted journals, verified grants and disconnected recovery;
product-specific DTOs, rules, private vaults and legacy readers remain independent.

Daymerit implements isolated parent/child/proof groups, signed global allocation, confirmed-only
financial effects, proof inventory/deletion and recoverable enrollment/source staging. November 5
published-source checks record 223 Daymerit, 196 Paws and 188 Pantry Clock app tests, shared/runtime
checks and rebuilt native artifacts. See the [current source-specific evidence](https://github.com/MAJESTIC-MADE-LLC/Daymerit/blob/dev/docs/validation/2026-11-05/hosting-family/RESULTS.md).
These checks do not qualify physical devices, signed Mac/Windows service installers, OS credential
provisioning, live licensing or actual native-store transactions. The metadata-only verifier remains
undeployed and the optional opaque push bridge remains unimplemented. Hosting adds no local-launch
prerequisite and changes neither prices nor public release order.

## Naming and operating rules

Use current product/repository names. Historical names and identifiers may remain in dated
records, compatibility formats and archives; do not blindly replace them or imply identity/store
migration. No further rename, deletion or consolidation follows from this document.

Normal work stays on `dev`; promotion directly to `main`, publication and deployments each require
explicit owner instruction. Reviewed November 4 source was promoted, followed by later November 5
work pushed on `dev`. Later source adoption does not imply another main promotion. Existing
main-only optional CI, reproducible local validation and the October 24 website publication pause
remain in force. This document authorizes no commit, push, store submission or infrastructure action.

## Canonical metadata contract

`REPOSITORIES.json` schema version 2 separates physical repository inventory from product ideas:

- `repositories` contains all physical repos, including inventory-only excluded entries. `role`
  describes current implementation category; `disposition` describes active, support, research,
  consolidating, or excluded work. Consolidating entries declare an active `consolidatesInto` target.
- `virtualProducts` records a concept without a repo, with its `id`, source repository, and source
  path. Quiet Arcade uses `quiet-arcade` and the Hub concept catalog; no checkout is invented.
- `launchOrder` contains every active physical/virtual product exactly once, across stages.
  `productLineup` also includes research product ideas without giving them a slot. Claim Crate is
  absent after consolidation and deletion; its history is recorded separately.
- `dataMatrix.productId` references the physical repo name or virtual id. It includes every queued
  product and Hub/waitlists, with separate current and target data-model text.
- `localCheckout` and `requiredPaths` describe local evidence, not release readiness. `sourceRef`
  defaults to `dev`; `main` is used for legacy repos that do not yet have remote `dev` branches.

Change the manifest first, then run `python3 scripts/portfolio_status.py --write` and `--check`.
Generated tables must not be edited by hand. Counts derive from inventory; dated app test/build
results remain historical until actually rerun. Documentation-only concept notes do not become
app implementation evidence.
