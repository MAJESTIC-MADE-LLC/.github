# Portfolio Alignment — updated November 4, 2026

## Approved direction

Majestic Made builds affordable apps whose useful core works with encrypted on-device records.
Exports are initiated by the user. Future optional sync requires explicit destination/collection
enrollment and standing authorization; no sync is implemented by this design approval.
Customer-owned hosting is not the same as a server operated by Majestic and is not currently
supported across the portfolio. Avoid
required accounts, default or unauthorized record uploads, recurring hosting cost, and cloud-only value where
local software can solve the workflow. Store/billing metadata and minimal website business-contact
forms remain separate disclosed flows.

The [shared stack standard](STACK_STANDARD.md) now requires the template and all seven existing
consumer apps to adopt and qualify the maintained foundation before **any** app release, with iOS
and Android in each first release. This supersedes the earlier incremental-adoption assumption.
Implementation and local checks are present across the cohort; physical/store and immutable-package
qualification remain pending. The gate covers shared contracts/builds and representative device/store boundaries,
not every product's complete domain/release QA. After qualification, complete each product's own
[release gates](RELEASE_DEFINITION.md) in the unchanged [canonical queue](LAUNCH_SLATE.md).
Current evidence and target changes remain separate in [status](STATUS.md) and the
[data matrix](DATA_COST_MATRIX.md).

## Consolidation and boundaries

- What We Own now owns one home/moving/claims product specification, including Claim Crate's
  PCS/box/QR, condition, damage and claim-export requirements. Original Claim Crate source and
  provenance are preserved in What We Own, and the redundant remote/local repository was deleted
  on November 4 after a verified Git backup. Old website routes resolve to What We Own in source;
  publication remains paused. Steward source/signup migration remains separate and unperformed.
- Keep specialist experiences separate where their real workflows justify them: motorcycle
  ownership, firearm/range records, pet care, beekeeping, tasting notes, diving, and fishing. Use the maintained
  shared storage, backup, lock, billing, and export packages without combining private data.
- Object Lore needs collector provenance/value-history/category workflows to justify a separate
  app. Fine Notes remains one tasting app across wine, whiskey, coffee, and cigars. Outdoor apps
  share infrastructure but retain their distinct records rather than becoming a generic journal.
- Daymerit's account-free local parent/shared-tablet implementation is present with native permanent
  unlock, encrypted recovery and parent/child controls. Namefold implements native encrypted QR/vCard
  exchange and a separate static PWA with unencrypted browser drafts/backups. Their hosted source is
  archived; managed links, family sync and user-owned hosting remain deferred. Ridelore uses local
  processing and encrypted records, with explicit optional identity/recall lookup separately disclosed.
  Physical/store/provenance qualification remains pending across the cohort.
- Lockbox's late queue scope is a local document vault and explicit encrypted handoff. Autonomous
  time-release/dead-man delivery has no reliable device-only guarantee and is deferred.
- Kinwall remains research only. Dossier is explicitly excluded from this pass; Off Record remains
  paused/excluded experimental work. Quiet Arcade is a Hub-only concept and has no repo yet.

## Future optional user-owned hosting — November 4, 2026

The approved [hosting architecture and adoption roadmap](USER_OWNED_HOSTING.md) extends the
local foundation with a future Mac/Windows host, host-managed accounts, scoped collection sharing
and end-to-end encrypted sync. The storage daemon stores ciphertext; authorized clients keep record keys and
perform readable-data processing. Pairing requires client/recovery authority, not server-admin
access alone. Use a LAN or user-configured private network/VPN for remote connections. An optional
minimal Majestic push bridge carries opaque update hints and routing metadata, never records or keys.

This pass documents contracts only. Current mobile graphs, package pins, storage/recovery behavior,
foundation prerequisites and the public release order stay unchanged. Future reference clients prove
the protocol first, Pantry Clock pilots it, Daymerit/Paws follow, Skepbook/Ridelore/Fine Notes follow
later and Namefold receives selective native-wallet sync. This engineering roadmap adds no launch
blocker or implementation claim. Public publishing and Kinwall platform access remain separate.

The resolved hosting design distinguishes the ciphertext daemon from an independently enrolled
trusted desktop coordinator that can read selected collections. It adopts explicit background
services, current publication permits, atomic storage/crypto journals, disconnected restore/rejoin
and verified app-specific workspace grants. Shared Daymerit financial actions await confirmation.
Both the optional push bridge and purchase/grant verifier are disclosed metadata-only exceptions;
neither receives app records or decryption keys. Runtime implementation remains future work.

## Naming and operating rules

Use current repo/product names in active planning: Ridelore, Namefold, Daymerit, Brassmark,
What We Own and Object Lore. Claim Crate is now a former product/workflow within What We Own.
Old names such as RideBinder, ReachMe, RoutineCue, Range,
Steward, Convoy, and Trove may remain in dated records, compatibility identifiers, and historical
artifacts; do not blindly replace them or imply that app/store identity migration is complete.
No further repository renames or deletions follow from this decision. Foundation code lives in the maintained App-Template packages; keep app-specific identities and compatibility adapters.

New core app access is subscription-only at the [approved monthly/annual prices](PRICING.md).
One-time purchases may cover optional extras, never a permanent core unlock. Most current apps
still implement permanent adapters and need a qualified migration. Skepbook's monthly/yearly subscription
source is present; store setup and actual store acceptance remain pending. Preserve
verified legacy ownership, existing record reading/export and full encrypted backup/recovery after
expiration. Historical evidence does not qualify changed billing or configure store products.

Preserve existing work on local `dev` branches. Local validation supplies release evidence;
GitHub Actions are optional and may run only for allowed main-branch events. No commits, pushes,
CI triggers, store submissions, deployments, paid services, or infrastructure changes are authorized
by this standard alone. On November 4 the owner separately authorized logical local `dev` commits,
shared App-Template publication and immutable-source adoption/validation. Other repository pushes,
main promotion and public releases are outside that action. The October 24, 2026 website publication
pause remains in force.

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
