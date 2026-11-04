# Local foundation validation — 2026-11-03

This ledger records local checks and their limits. The [implementation report](../../FOUNDATION_IMPLEMENTATION_2026-11-03.md) tracks the seven product apps. No hosted CI, physical-device test, store purchase, published package revision, or release approval is inferred from these records.

## Environment

- Isolated Flutter 3.47.8, framework `737ba8f885dc774b53b442759999a312c9461e4e`; Dart 3.13.7; engine `cf636b1dfb818dd6a3ff16e390e93b1a036969c8`.
- SDK: `/Users/bespin-starter/.cache/majestic/flutter/3.47.8`. The machine-wide Homebrew SDK was retained.
- Android: AGP 9.1.0 / Kotlin 2.4.0 / Gradle 9.3.1. Java source/bytecode target 17; local Gradle runtime Android Studio JBR 21.0.8.
- Apple: Xcode 27.2, build 27B52. Device release builds use `--no-codesign`; simulator runs are separate.
- Owned Android runtime: headless `Medium_Phone`, API 36, serial `emulator-5556`. The interrupted AVD was restarted without wiping its data. No TV device was used.
- Owned Apple runtime: headless `Majestic Foundation QA`, iOS 27.1, UDID `1B0369BA-E416-414F-B12F-DB0C489AF64B`. Simulator Face ID notifications exercise native LocalAuthentication; they do not qualify physical biometrics or hardware key protection.

## Repository checks

| Check | Actual result | Local evidence |
| --- | --- | --- |
| Foundation static adoption | All eight consumers pass | [Static result](logs/foundation-static.json) |
| Governance Python suite | 51 tests pass | [51-test log](logs/governance-tests.log) |
| Repository inventory / launch order | 28 repositories validated; original 17-position queue retained | [Inventory log](logs/portfolio-inventory.log) |
| Concept-only governance | All ten owned concept repositories pass | [Concept log](logs/concept-governance.log) |
| Dependency resolution | All eight lockfiles match prescribed versions; 220 packages audited, 32 documented product/transitive version differences | [Resolution audit](../../dependency_audits/2026-11-03.json) |
| Source preservation | See independent exact-byte baseline audit | [Preservation evidence](PRESERVATION.md) |

Local link checks cover active Markdown file targets and local counterparts of canonical GitHub source links. They do not assert publication or availability of an unpublished remote branch. The completed ledger check resolves 562 active local/source-counterpart links with zero missing targets; see the [link result](logs/active-links.json).

## Product and shared checks

All seven complete product suites pass (698 tests), with clean analyzers and both local release builds. These are compilation/test results; product release approval and native-store qualification remain separate.

| Product | Analysis | Tests | Android / unsigned iOS |
| --- | --- | --- | --- |
| Skepbook | [Clean](logs/skepbook-analysis.log) | [133 passed](logs/skepbook-tests.log) | [Android](logs/skepbook-android.log) / [iOS](logs/skepbook-ios.log) |
| Ridelore | [Clean](logs/ridelore-analysis.log) | [207 passed](logs/ridelore-tests.log) | [Android](logs/ridelore-android.log) / [iOS](logs/ridelore-ios.log) |
| Paws | [Clean](logs/paws-analysis.log) | [72 passed](logs/paws-tests.log) | [Android](logs/paws-android.log) / [iOS](logs/paws-ios.log) |
| Pantry Clock | [Clean](logs/pantry-analysis.log) | [73 passed](logs/pantry-tests.log) | [Android](logs/pantry-android.log) / [iOS](logs/pantry-ios.log) |
| Fine Notes | [Clean](logs/fine-analysis.log) | [97 passed](logs/fine-tests.log) | [Android](logs/fine-android.log) / [iOS](logs/fine-ios.log) |
| Namefold | [Clean](logs/namefold-analysis.log) | [47 passed](logs/namefold-tests.log) | [Android](logs/namefold-android.log) / [iOS](logs/namefold-ios.log) |
| Daymerit | [Clean](logs/daymerit-analysis.log) | [69 passed](logs/daymerit-tests.log) | [Android](logs/daymerit-android.log) / [iOS](logs/daymerit-ios.log) |

All eight shared packages have clean analyzers and 90 tests passing:

| Package | Analysis | Tests |
| --- | --- | --- |
| majestic_app | [Clean](logs/shared-app-analysis.log) | [5 passed](logs/shared-app-tests.log) |
| majestic_privacy | [Clean](logs/shared-privacy-analysis.log) | [13 passed](logs/shared-privacy-tests.log) |
| majestic_purchases | [Clean](logs/shared-purchases-analysis.log) | [17 passed](logs/shared-purchases-tests.log) |
| majestic_storage | [Clean](logs/shared-storage-analysis.log) | [49 passed](logs/shared-storage-tests.log) |
| majestic_media | [Clean](logs/shared-media-analysis.log) | [2 passed](logs/shared-media-tests.log) |
| majestic_reports | [Clean](logs/shared-reports-analysis.log) | [1 passed](logs/shared-reports-tests.log) |
| majestic_reminders | [Clean](logs/shared-reminders-analysis.log) | [1 passed](logs/shared-reminders-tests.log) |
| majestic_qr | [Clean](logs/shared-qr-analysis.log) | [2 passed](logs/shared-qr-tests.log) |

The [unassessed source/log snapshot](source-log-snapshot.json) records current source fingerprints and SHA-256 hashes of the retained evidence; the [retained-file index](evidence-files.json) hashes every saved log/JSON artifact. It does not create passed manifest entries, infer a purchase/physical-device result, or approve production provenance. The [production gate result](logs/production-gate.json) correctly remains pending and the command exits 1, including the immutable-package-revision gate.

## Reviewed machine records

The maintained template now records its five completed software checks as passed, using its current source fingerprint and repo-owned artifact hashes; see the [template qualification report](../../../../App-Template/docs/validation/2026-11-03/foundation/GENERATED_TEMPLATE_SMOKE.md). The global [shared-package software record](SHARED_PACKAGES.md) records eight clean analyzers and 90 tests against the current cohort hash. All seven products also record their completed local software and compatibility reviews. The checker accepts software evidence for all eight consumers with no per-consumer evidence pending. These are reviewed local software/emulator/simulator results. Physical privacy, native-store transactions and immutable package provenance remain pending; the global foundation status is unchanged.

## Reference and generator

The maintained reference uses the shared content boundary, preserving route/form state across native dialogs while removing hidden focus, semantics, pointer access and ticking. Its secret-dialog controllers live with their route. A real native recovery attempt also exposed Android picker results arriving before `resumed`; recovery now waits for the foreground transition before requesting owner credentials. The regression test verifies that authorization does not run while inactive.

Reference analysis is clean and all 16 tests pass. The fresh generated fixture has clean analysis and nine tests passing. Both current applications build for Android release and unsigned iOS device release:

| Application | Analysis / tests | Android release | Unsigned iOS release |
| --- | --- | --- | --- |
| Maintained reference | [Clean analysis](logs/reference-analysis.log), [16 tests](logs/reference-tests.log) | [61.3 MB](logs/reference-android.log) | [21.1 MB](logs/reference-ios.log) |
| Fresh all-capabilities fixture | [Clean analysis](logs/generated-analysis.log), [9 tests](logs/generated-tests.log) | [71.0 MB](logs/generated-android.log) | [25.9 MB](logs/generated-ios.log) |

These logs include the picker correction. Earlier `/tmp/majestic-final-boundary-*` reference/generated logs remain preliminary. The Paws release build in that batch used `test/fixtures/release/app_config.production.json`; its production source was unaffected by the reference correction.

A fresh all-capabilities fixture was generated at `/tmp/majestic-foundation-picker-qualification-20261103` with PDF, reminders, camera and QR selected. Scaffold creation is recorded in `/tmp/majestic-reference-picker-generated-scaffold-20261103.log`. The completed native results are linked above; runtime evidence is recorded below.

The generator's immutable-Git mode rejects local path dependencies inside selected shared packages. The current maintained packages use portable hosted dependencies. Actual immutable Git resolution remains pending authorized commits/publication; no production commit SHA was invented. See [Git package provenance](../../../../App-Template/docs/GIT_PACKAGE_PROVENANCE.md).

## Runtime evidence and limits

- Fresh final generated Android release startup was observed for 25 seconds with no store action. The [new process log](logs/generated-cached-startup.log) and [summary](logs/generated-cached-startup-summary.json) contain no BillingClient, CCT transport or fatal-error matches. This is a bounded process-log observation, not packet capture or a universal no-network claim. Shared adapter tests separately require zero store-client calls during default cached-only initialization.
- The final Android reference release passes [owner-encrypted export → save a changed record → native picker/PIN → authenticated decrypt → confirmed replacement](logs/reference-owner-roundtrip.log) and [cold-process persistence](logs/reference-cold-persistence.log), each with a terminal instrumentation pass. The exported backup also [decodes independently](logs/reference-export-independent-decode.log) to the intended synthetic fixture.
- [Release reference database inspection](logs/reference-database-inspection.log) reads ciphertext/header only through a same-certificate QA instrumentation helper: opaque header, no plaintext SQLite signature and no synthetic record marker. No key or secure-store value was read. The helper was uninstalled after qualification. Only scratch copies of the release APKs were signed with the existing development certificate for installation; production signing was unchanged.
- The fresh generated fixture passes [iOS simulator native UI save, encrypted attachment roundtrip and locking](logs/ios-simulator-write.log), followed by [a second process that loads the existing saved note and locks again](logs/ios-simulator-cold.log). Both invocations use `--no-uninstall`; the second run does not recreate the fixture. Native LocalAuthentication remains enabled and is exercised with the owned simulator's simulated Face ID. Test-only harness setup re-enrolls that simulator after its authentication daemon starts; no production unlock policy is replaced.
- Independent host inspection [after the write](logs/ios-simulator-write-file-inspection.json) and [after the cold run](logs/ios-simulator-cold-file-inspection.json) finds opaque SQLite headers, rejection by unkeyed SQLite, absent synthetic plaintext markers, and the encrypted attachment envelope. These are actual simulator files. The reference has no attachment UI; the temporary native integration harness exercises the shared attachment API. Simulator debug execution and unsigned iOS device release compilation are distinct checks, with physical qualification still pending.
- Android accessibility `ACTION_SET_TEXT` did not reliably update the actual Flutter record. Failed harness attempts were not recorded as recovery passes. Final recovery checks use normal synthetic touch/key input and native OS credentials/document pickers, with no fake purchase grant.

Physical Android/iOS privacy and recovery checks, native store product/transaction testing, and immutable shared-package adoption remain pending. The [qualification record](../../FOUNDATION_QUALIFICATION.json) and production revision gate retain that status. Product-specific release QA follows the foundation gate.
