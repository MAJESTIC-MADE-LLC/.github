# Portfolio Alignment — November 3, 2026

## Approved direction

Majestic Made builds affordable apps whose useful core works with encrypted on-device records.
Exports are initiated by the user. Optional customer-owned hosting may follow; it is not the same
as a server operated by Majestic and is not currently supported across the portfolio. Avoid
required accounts, automatic record uploads, recurring hosting cost, and cloud-only value where
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

- What We Own owns one home-and-moving inventory. Claim Crate contributes PCS/box/QR, condition,
  damage, and claim-export requirements. The separate steward landing page belongs in the shared
  Hub/What We Own marketing plan. These decisions do not move files, users, links, or signups yet.
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

## Naming and operating rules

Use current repo/product names in active planning: Ridelore, Namefold, Daymerit, Brassmark,
What We Own, Claim Crate, and Object Lore. Old names such as RideBinder, ReachMe, RoutineCue, Range,
Steward, Convoy, and Trove may remain in dated records, compatibility identifiers, and historical
artifacts; do not blindly replace them or imply that app/store identity migration is complete.
No additional repository renames or archives follow from this standard. Foundation code lives in the maintained App-Template packages; keep app-specific identities and compatibility adapters.

Native permanent local premium-unlock integration is now present in all seven apps; Skepbook's
established SKU/pricing is preserved. Store product setup, prices and real transaction/restore QA
remain pending. Keep existing record access and basic export available. Verify encrypted full-vault
backup/restore, not just reports.

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
  `productLineup` also includes research/consolidating product ideas without giving them a slot.
- `dataMatrix.productId` references the physical repo name or virtual id. It includes every queued
  product and Hub/waitlists, with separate current and target data-model text.
- `localCheckout` and `requiredPaths` describe local evidence, not release readiness. `sourceRef`
  defaults to `dev`; `main` is used for legacy repos that do not yet have remote `dev` branches.

Change the manifest first, then run `python3 scripts/portfolio_status.py --write` and `--check`.
Generated tables must not be edited by hand. Counts derive from inventory; dated app test/build
results remain historical until actually rerun. Documentation-only concept notes do not become
app implementation evidence.
