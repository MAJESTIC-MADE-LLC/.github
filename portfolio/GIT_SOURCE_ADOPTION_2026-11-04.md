# Git source adoption — November 4, 2026

This records the Git-adoption phase before the owner subsequently authorized promotion to `main`.
See [the main-promotion and metadata review](MAIN_PROMOTION_2026-11-04.md) for the later branch/publication state.

The owner authorized review and logical `dev` commits of the current portfolio work, publication of
the shared foundation, immutable consumer references and local revalidation. Product repositories
remain separate. App-Template publication uses `dev`; other repository commits are local.

The maintained package/scaffold source is published in App-Template at
`d2895cba9ac5bc121369a409fb1e528071a98a2d`. Private Git dependencies require ordinary Git credentials,
without tokens in manifests or URLs. Package version remains 0.1.0. A later reference/docs commit
can adopt that source without changing the pinned package implementation.

The checker validates policy, manifest, pubspec, resolved lock and actual cached source, including
Git objects and package bytes. Workspace paths/ignored overrides remain development-only. Both
native release builds, analysis and tests are rerun against Git sources; previous dated runtime,
recovery, encryption and preservation evidence retains its original source/binary scope.

All 26 included repositories now have reviewed logical commits on `dev`. The App-Template source
revision and subsequent reference/documentation adoption are published to its `dev` branch; other
repositories remain local commits. Upstream main-only CI history was integrated into `dev` without
changing product behavior; no product repositories were combined or renamed.

| Validation | Result |
|---|---|
| Seven app suites | 698 tests; clean analysis |
| Shared packages, clean fetched source | 90 tests; eight clean analyzers |
| Reference / fresh Git-generated app / local generated app | 16 / 9 / 9 tests; clean analysis |
| Native release builds | All seven apps, reference and fresh Git-generated app pass Android and unsigned iOS |
| Governance | 69 tests; 28-repository inventory and 17-product queue checks pass |
| Actual immutable source checks | All eight consumers pass; 42 package selections use the same real published commit |
| Android binary parity | All seven APKs exactly match the earlier independently encryption-tested artifacts |

[Final checker output](validation/2026-11-04/git-foundation/final-checker.json),
[shared package evidence](validation/2026-11-04/git-foundation/SHARED_PACKAGES.md),
[authored-source preservation](validation/2026-11-04/git-foundation/authored-source-preservation.json),
[Android artifact parity](validation/2026-11-04/git-foundation/android-artifact-parity.json), and
[commit record](validation/2026-11-04/git-foundation/commits.json) retain exact scope and provenance.
Ten concept validators and supporting infrastructure checks also pass; their existing source and
dated historical records were preserved. Fresh generated Android locked startup passed on the
owned headless emulator; its unsigned artifact required a temporary QA-signed installation copy
with identical non-signature ZIP contents.

Source fingerprint policy **2** excludes seven precisely enumerated Flutter-generated files and
`ios/Flutter/ephemeral`, while retaining actual native sources, Podfile/lock and dependency manifests.
Every tracked shared-package byte/mode remains verified against Git objects. Earlier snapshots keep
their original policy. Namefold's old-policy harness stopped only on generated-file hash drift after
all real checks passed; its APK is unchanged byte for byte. No authored runtime/native/test input
changed during source adoption. This correction changes the checker, not the apps, and does not
require relabeling simulator observations as physical-device evidence.

The [release-gate check](validation/2026-11-04/git-foundation/release-gate-pending.json) correctly remains
nonzero for exactly four pending representative checks: physical privacy on iOS/Android and actual
native store purchase/restore on iOS/Android. Static adoption, all consumer software evidence, shared
software and actual immutable source qualification pass. Product release approval remains separate.
Physical-device privacy and real native-store purchase/restore checks remain pending. No public
release, main promotion, deployment, live provider/customer change or hosted CI run is authorized
by this phase. The website remains paused; Dossier and OffRecord are excluded.
