# Majestic Made Release Definition

Overview reconciled November 6, 2026; release policy approved November 3. Before **any** app release, the template and all seven existing consumer
apps must adopt and qualify the [shared foundation](STACK_STANDARD.md) on iOS and Android.
That foundation gate is pending. It does not require all seven products to finish every domain,
accessibility, legal or store-submission check simultaneously. After it qualifies, each product
satisfies this definition on `dev` in the unchanged [sequential queue](LAUNCH_SLATE.md).
A README, manifest label, mockup, simulator-only demo or historical report is not release evidence.

## Shared foundation prerequisite

- Run the read-only local foundation checker. All seven apps and the template use the approved SDK,
  dependency baseline and maintained shared packages, with their applicable capability contracts.
- Record actual analysis/tests, both native release builds and foundation/migration integration
  checks for the cohort, plus a generated-template smoke run and shared-package tests.
- Complete representative physical iOS/Android privacy and native-store boundary qualification.
  Preserve pending status for unavailable hardware/store checks; do not relabel simulators as hardware.
- Verify the approved immutable Git revision, resolved lock and actual cached package bytes.
  Development-only local paths do not qualify production provenance. No version tag or declaration
  substitutes for package integration or current source-bound qualification evidence.

## Product and experience

- The promised primary workflow works end to end on iOS and Android for the first release.
- Empty, loading, offline, denied-permission, error, restore, and destructive-action states work.
- Accessibility labels, text scaling, keyboard/focus behavior where applicable, and contrast pass.
- A founder completes and records a clean-device physical-device acceptance run.

## Data, privacy, and security

- State implemented behavior and remaining acceptance separately. Daymerit's account-free local
  app and Namefold's native local wallet/static PWA are implemented; physical/store/provenance
  qualification is pending. Namefold browser drafts/JSON backups are unencrypted, unlike its native vault.
- Default consumer records to encrypted on-device storage without a mandatory company account.
  Only deliberate user actions export records. Optional sync uses explicit destination/
  collection enrollment as scoped standing transfer authorization, separate from manual exports.
  The [approved hosting design](USER_OWNED_HOSTING.md) requires its own tested encryption, pairing,
  access, recovery, disconnect and provider-exit behavior before that feature releases. It is
  implemented in the Skepbook, Pantry Clock, Paws and Daymerit pre-launch builds; service, licensing and
  physical/store qualification remain pending. Hosting adds no prerequisite for local-app launches.
- Verify data inventory, data flows, retention, export, deletion, and encrypted backup/restore.
  A PDF/CSV or a single shared note is not a complete restorable vault backup. Do not rely on
  untested system backup or promise recovery of a key or passphrase Majestic does not hold.
- Billing metadata, store purchase processing, public website/contact forms, and optional network
  lookups are separate disclosed flows. Do not call a build network-free when these flows exist.
- Client builds contain no server secrets; authentication and any server authorization fail closed.
- A repository security review has no unresolved critical or high-severity finding.
- Store privacy/data-safety answers and website/legal claims match the final release build.

## Quality and operations

- Record reproducible formatting, static analysis, relevant tests, release builds, and dependency
  review. Preserve dated earlier evidence; report only checks actually rerun for the final change.
  Hosted CI is optional under the GitHub Free policy. Do not create or trigger non-main CI runs.
- Verify crash recovery, upgrade/migration, backup restore, offline purchase/entitlement behavior,
  and rollback or feature-disable paths on supported devices.
- Support can reproduce the build and has a monitored address and troubleshooting runbook.
- Any approved remote feature has minimal disclosed monitoring, bounded cost, retention/deletion,
  and tested outage behavior. Local work and access to existing records remain usable offline.

## Commercial and legal

- Use the approved [monthly/annual subscription prices](PRICING.md) for core access. No new
  permanent core-app unlocks; one-time purchases are limited to optional extras. All seven existing
  apps and the template implement monthly/annual subscription source and separate non-billing
  local trials. This does not establish actual store availability or signed-store acceptance.
- Verify subscription enrollment, renewal, cancellation through the paid-through date, expiration,
  grace/retry, refund/revocation, restore and bounded offline entitlement behavior. Preserve authentic
  legacy lifetime ownership separately from new sales and validate optional-extra restoration.
- Existing records, basic user export, encrypted backup/recovery and deletion remain accessible
  after expiration. A fourteen-day local trial never starts billing automatically. Store setup,
  changed-binary validation and actual transaction qualification remain pending release work.
- Privacy policy, terms, support, screenshots, and store forms describe actual behavior and have
  product-specific launch approval. Records/exports do not replace qualified professional advice.
- Unit economics include store fees, support, and any explicitly approved ongoing services. Do not
  enable recurring-cost features merely because the app previously contained provider code.

## Independent approval

- Record the product/version, passed checks, unresolved accepted limits, and owner launch decision.
- Assign signing/store, payment, support, data recovery, and rollback owners relevant to that app.
- The shared foundation must first qualify across the template and all seven current apps. After
  that, another product's unfinished domain/legal/store QA does not block the current product's
  independent approval. Do not silently skip the shared gate or require all product releases at once.
- Store submission, public deployment, provider provisioning, and paid-service changes are separate
  actions. The October 24, 2026 website pause remains until explicitly lifted by the owners.
