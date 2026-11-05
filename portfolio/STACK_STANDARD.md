# Shared mobile foundation standard

Approved 2026-11-03. This replaces the earlier incremental-adoption assumption. **The template and
all seven existing consumer apps must adopt and qualify the same maintained foundation before any
app release.** The 17-product queue remains unchanged after this foundation gate. Qualification is
currently **pending**; files, dependency declarations and earlier product tests do not establish it.

## Architecture and supported releases

- Use Flutter/Dart for the consumer mobile portfolio, with iOS **and** Android in the first release.
  Pin Flutter 3.47.8 in `.flutter-version`; it supplies Dart 3.13.7. Use the app SDK constraint
  `>=3.13.7 <4.0.0`, exact approved first-party dependency versions and committed resolved lockfiles.
- Use Material 3, Riverpod and `go_router`, with feature-owned repositories and testable service
  boundaries. Keep domain models, user interface/branding, data identities and app permissions
  product-specific. Familiarity and shared maintenance must not combine unrelated private data.
- Use the maintained packages in `App-Template/packages`: `majestic_app`, `majestic_privacy`,
  `majestic_storage` and `majestic_purchases`, initially version 0.1.0. Applications must actually
  integrate their applicable contracts; adding unused dependencies or a verified label is not adoption.
- Use encrypted relational storage, app-private encrypted attachments where applicable, versioned
  authenticated full backups, app-specific keys/identifiers and deliberate exports. Verify existing
  database/archive migration and restore contracts; never replace a user's vault as incidental cleanup.
- Select SQLite3MultipleCiphers through the `sqlite3` build hook (`source: sqlite3mc`). Existing
  SQLCipher databases require tested compatibility settings/migrations, not an assumed format match.
- Target native auto-renewable monthly/annual subscriptions for core access, at the approved
  [product prices](PRICING.md). One-time purchases may cover optional extras only; no new permanent
  core unlocks. The reference/shared non-consumable adapter is current implementation, not the
  approved commercial target, and needs qualified subscription support before adoption for new offers.
  Keep existing records, basic export and backup/recovery available without an active entitlement.
- Ship no Supabase, Firebase, Sentry, RevenueCat or hosted-AI provider SDKs in current mobile dependency graphs.
  Do not initialize a backend or remote telemetry merely because a prior template supported it.
- Generic network libraries are forbidden in the default template's first-party dependencies.
  A particular application may declare a necessary, user-triggered public lookup with an explicit
  capability and disclosure (for example Ridelore's existing NHTSA lookup). This does not authorize
  automatic record uploads, cloud sync, remote analytics or a general personal-data service.

`STACK_STANDARD.json` is the machine-readable version/dependency policy. `CAPABILITY_MATRIX.json`
records applicability, not delivered features. Optional camera, contacts, location, widgets, reminders,
PDF and QR libraries must be justified by the application's capability; they are not mandatory UI
features for every app. Do not add permissions or new product scope to satisfy a generic checklist.

The owner confirmed on 2026-11-03 that there are no public customers and all prior purchases
are tests. Preserve existing test records, durable IDs and verified legacy purchase compatibility.
The November 4 subscription decision supersedes earlier permanent-core pricing: Skepbook's targets
are $24.99/year or $2.99/month; current source includes both choices, with store setup and qualification pending. Do not grant
ownership from unverified legacy test state. Real product configuration and store test evidence
remain separate, pending checks. Historical signed-off evidence does not qualify changed billing.

The release baseline includes the patched Flutter 3.47.8 / Dart 3.13.7 SDK, required by the
[publisher's TLS advisory](https://github.com/dart-lang/sdk/security/advisories/GHSA-frr6-h895-5pxp).
The earlier 3.47.3 build logs remain dated preliminary evidence. The common Android build tuple
is AGP 9.1.0, Kotlin Gradle Plugin 2.4.0, Gradle 9.3.1, and Java/Kotlin source/bytecode target 17, matching
[Flutter 3.47's verified matrix](https://flutter.dev/blog/whats-new-in-flutter-3-47#android-dependency-matrix).
The checker verifies source pins and CI SDK versions; actual patched-SDK builds and device/store
evidence are still required. Installing or editing a version pin does not qualify an app.

## Package ownership and provenance

Maintain the common implementation once in the four base packages; do not keep copied competing app
implementations of those same responsibilities. Retain app-specific adapters where old data formats,
native configuration or domain behavior require them, and test the boundary against the shared core.

The seven products and reference consume version 0.1.0 through immutable Git revision
`d2895cba9ac5bc121369a409fb1e528071a98a2d` in App-Template. `foundation.json` records `git-immutable`
provenance and each package's exact URL, full commit and repository-relative subdirectory. Pubspecs,
resolved lockfiles and actual cached package source must agree. Ordinary Git credentials provide
private-repository access; never embed tokens in URLs. Local paths/ignored overrides are explicit
development modes and do not satisfy production qualification. Shared updates require deliberate
adoption and validation, rather than following `dev` or another moving ref.

Optional maintained modules are selected only where applicable: `majestic_reports` for PDF,
`majestic_reminders` for reminders, `majestic_media` for camera/attachment processing and
`majestic_qr` for native camera QR scanning. Their source/version pins, real adoption,
capability declarations and validation fingerprints follow the same rules as the base packages.
QR display alone uses `qr_flutter`; it does not require camera/scanner dependencies.

Native platform implementations also use an exact compatibility baseline, recorded in
`resolvedPlatformDependencies`. The checker applies it only where a package is present.
The shared privacy/purchase/storage pubspecs pin their critical native implementations.
Consumers of `file_picker` use explicit root `dependency_overrides` for its platform packages,
so an older lock cannot retain a different recovery picker. Generated apps copy those pins.
`file_selector` 1.1.0 remains a supported product adapter where already used (including Paws
and Pantry Clock); do not add a second picker just for uniform naming. See
[NATIVE_DEPENDENCY_BASELINE.md](NATIVE_DEPENDENCY_BASELINE.md) for the resolution audit.

## Foundation gate versus product release gates

The shared gate covers the template and seven existing apps: Skepbook, Ridelore, Paws, Pantry Clock,
Fine Notes, Namefold and Daymerit. It requires:

1. Static adoption: exact toolchain/dependencies, real shared-package imports/resolution, encrypted
   SQLite selection, applicable capability declarations, both native platform sources, `dev` work
   and the existing main-only CI restrictions.
2. Source-bound local analysis/tests, both platform release builds and integration/migration contract
   evidence for each app; the template also needs a generated-template smoke run.
3. Shared-package tests and representative **physical iOS/Android privacy and native-store boundary**
   qualification. Simulator results are not physical-device or actual store-purchase evidence.

This does **not** require every app to finish all domain/accessibility/security/legal/store-submission
QA before the first app can release. After the foundation qualifies, each product completes its own
[release definition](RELEASE_DEFINITION.md) in the original [queue](LAUNCH_SLATE.md).

The checker is read-only:

```bash
python3 scripts/check_foundation.py --workspace-root ..
python3 scripts/check_foundation.py --workspace-root .. --app Skepbook
python3 scripts/check_foundation.py --workspace-root .. --release-gate
python3 -m unittest discover -s tests -v
```

The default exits nonzero for static adoption drift. `--release-gate` also requires the complete
cohort and recorded foundation qualification; it cannot approve a product release or publication.
JSON output distinguishes `staticAdoption`, `foundationEvidence` and `foundationGate`, and reports
source/cohort fingerprints. Missing or stale evidence keeps the gate pending even if a manifest
claims verified. Creating a manifest or running this checker is not a test/build/device result.

Each evidence entry in a consumer's `foundation.json` identifies the actual `record`, its `sha256`,
`recordedAt`, `sourceFingerprint` and `status: passed`. Global representative qualification records
live in `FOUNDATION_QUALIFICATION.json`, reference files inside this governance repo and bind to the
reported `cohortFingerprint`; physical/store records also identify `recordedBy`. Preserve real logs
or dated manual observations. Do not fill evidence fields for checks that have not occurred.

## Planned optional hosting extension — November 4, 2026

The [user-owned hosting design](USER_OWNED_HOSTING.md) and
[template extension contracts](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/USER_OWNED_HOSTING.md)
approve future optional Mac/Windows ciphertext hosting, host-managed identities, scoped collection
sharing and direct sync over a LAN/user private network. Authorized clients hold keys and perform
readable-data processing; local encrypted storage and recovery remain usable without a host.
Opt-in sync enrollment grants scoped standing transfer authorization, separate from manual exports.

Shared enrollment, atomic encrypted journals, source-built MLS, separate storage/coordinator roles,
reference clients and an explicitly selected reference generator now have optional implementations.
The [implementation report](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_IMPLEMENTATION.md)
records reference limits and qualification. Default production consumer synchronization remains disabled;
Pantry Clock's separately registered development pilot is under qualification.
The consumer machine-readable baseline, app capability declarations and immutable package revisions
remain unchanged. Future sync and push need explicit optional capabilities, reviewed provider-policy
exceptions where applicable, exact dependency pins and renewed source-bound qualification; neither
is an implicit public-lookup exception or permission to initialize a backend in default scaffolds.

The approved optional Majestic notification bridge may relay authenticated opaque update hints
through Apple/Google. It receives routing metadata, not record content/keys; developer push secrets
stay out of household installers. Push does not establish private-network reachability or guarantee
background execution. Disabling it must preserve direct sync and offline work.

This is future expansion outside current launch work, not another foundation prerequisite. Prove
generated reference clients, then pilot Pantry Clock before later product adoption in the roadmap.
The 17-product public release queue, existing qualification scope and independent approvals remain.

### Resolved hosting extension contracts — November 4, 2026

The [hosting roadmap](USER_OWNED_HOSTING.md) links four detailed template contracts that resolve
all seven review findings. Optional reference pins (OpenMLS 0.9.2, matching Flutter Rust Bridge
2.13.0, Rust 1.99.1) are isolated from this standard's current consumer machine baseline. The Rust ciphertext daemon has no record keys. A separately authorized headless Dart
coordinator reuses product rules and may decrypt selected collections, with independent role TLS
trust/credentials. Prove the native service, transaction/MLS and grants contracts with generated
clients before app adoption. Current dependency policy, package SHA and launch gates stay intact.

## Web, concepts and operations

Namefold's free semantic QR/vCard PWA, Hub's TypeScript/React surface and static legal pages may use
the appropriate web stack. Web/mobile share data contracts where needed, not a forced mobile UI or
database. Pin active Node projects to the exact current supported LTS baseline in the machine standard
(Node 26.13.0 as verified against the [official release index](https://nodejs.org/dist/index.json) on 2026-11-04). Steward's separate marketing surface
is consolidating into Hub; it is not a new consumer stack. Customer self-hosting remains a later
opt-in capability and no managed backend is required by this foundation.

New queued concepts use the qualified template when implementation starts. They must not acquire
placeholder apps simply to satisfy this existing-cohort gate. Kinwall remains research-only;
Dossier and OffRecord are excluded. Existing website publication pauses, owner release decisions,
main-only CI, local validation and explicit dev-to-main promotion remain in force. This standard adds
no workflow, CI trigger, deployment, commit or push.

The [standardization guard and local hooks](STANDARDIZATION.md) enforce these rules across active
native, web and optional-hosting source. Dependency declaration/lock updates and new app manifests
require a reviewed canonical registration. Hooks validate commit/push inputs as well as the worktree;
alignment does not refresh release evidence or authorize promotion/publication.

## Production package provenance

The checker validates actual immutable Git resolution: approved URL/full SHA/subdirectory in policy,
manifests and pubspecs; matching Git lockfile `resolved-ref`; and package configuration pointing to
matching, untampered cached Git source. Forged labels, path overrides, mutable refs and differing
package bytes fail closed. A clean generated consumer must also resolve the published revision and
pass local checks. This closes only the source-provenance requirement; physical-device and real-store
requirements remain independently pending. The checker never commits, pushes or resolves dependencies.

Java 17 denotes the minimum/source/bytecode target. The local Gradle 9.3.1 runtime actually used
Android Studio JBR 21.0.8, a supported runtime; the standard does not require rebuilding on JDK 17.

For source/log capture, use `python3 scripts/foundation_evidence_snapshot.py --output NEW.json`
before a qualification batch, then `--compare NEW.json --log Paws tests /path/to/tests.log`
afterward. It reports source drift and exact log hashes without editing manifests or interpreting
logs as passes. The owner records actual validation separately. Physical/store qualification is
never inferred from simulator or build output.

## Optional hosting source

The default template still has no record backend. Only explicitly approved consumers may add the
complete optional hosting/sync/crypto set, currently Pantry Clock and Paws at published Git
`f5942ed7a2b318e48ec7e47ce9f46ba531e02c31`. Both use the same native session engine; product
schemas and scopes stay separate. Core/report sources retain their existing immutable revisions.
See [drift enforcement](STANDARDIZATION.md) for exact manifest, lock, cache, capability and native
permission checks. Source adoption does not replace physical/store or signed-service qualification.
