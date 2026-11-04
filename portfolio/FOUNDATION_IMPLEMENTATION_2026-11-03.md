# Consumer foundation implementation — November 3, 2026

This is the historical qualification record before authorized Git publication. See
[the November 4 Git adoption follow-up](GIT_SOURCE_ADOPTION_2026-11-04.md) for subsequent commits,
published sources and refreshed checks. Remaining-gate and no-commit statements below describe that earlier phase.

Final local validation: **November 4, 2026**. All eight consumers pass their recorded local software checks; all seven products pass final Android and unsigned iOS release builds. **The production foundation gate and public release approval remain pending.**

## Implemented

- All seven implemented consumer apps use Flutter/Dart, Riverpod, go_router and maintained App-Template foundation packages. The template includes a capability-selecting generator and optional reports, reminders, media and QR packages.
- Common Drift/native SQLite3MultipleCiphers storage, encrypted attachments/thumbnails where applicable, native privacy controls, protected lifecycle boundaries, authenticated archives and native permanent-unlock billing replace the active cloud/subscription infrastructure. Paws, Pantry Clock and Fine Notes deliberately retain their validated legacy product envelopes inside the encrypted SQLite container as a compatibility stage.
- Legacy IDs, file/key namespaces, backup readers and existing-record access are preserved. Paws also retains support for valid large version-one backups; new archives support 20 MiB encoded / 16 MiB clear, while the original reader keeps its 16 MiB encoded cap.
- Native billing startup reads cached ownership only. Catalog/purchase/restore actions are explicit. The owner confirmed **test purchases only and no public customers**; unverified old subscription flags do not grant permanent ownership. Exact permanent prices remain product work; Skepbook's established pricing is preserved.
- Namefold now has an offline native wallet and a static local-sharing PWA. Managed public links and their hosted code are archived. Browser drafts/backups are explicitly unencrypted; the native wallet has its own encrypted boundary.
- Daymerit now has an account-free local household, parent PIN controls, shared child board, routines, approvals, rewards/points, manual allowance, optional local proofs/reminders, legacy JSON import and complete bounded encrypted owner backups. Locked in-place recovery requires an immutable private authority from the current household's authenticated backup, before a new generation is selected.
- Lock covers preserve forms, routes and pending native-picker callbacks while excluding hidden focus, pointer input, semantics and tickers. Regression checks cover lost-camera selections, late authentication, protected startup and focused-dialog cleanup.

## Validation record

| Consumer | Current complete app tests | Android / unsigned iOS release builds |
|---|---:|---|
| Skepbook | 133 | Passed / passed |
| Ridelore | 207 | Passed / passed |
| Paws | 72 | Passed / passed |
| Pantry Clock | 73 | Passed / passed |
| Fine Notes | 97 | Passed / passed |
| Namefold | 47 | Passed / passed |
| Daymerit | 69 | Passed / passed |

The app suites total **698 tests**, with clean analyzers. Shared packages total **90 tests**. Additional validation includes the generated/reference apps, Namefold PWA, governance/concept/link checks, native QR decoding and a real native encrypted `SQLITE_FULL` rollback/restart contract. The [validation ledger](validation/2026-11-03/LOCAL_VALIDATION.md) and [source/log snapshot](validation/2026-11-03/source-log-snapshot.json) retain exact final evidence. Earlier binaries remain preliminary where a later source change affected them.

Qualified tooling: **Flutter 3.47.8 / Dart 3.13.7**, Android AGP 9.1.0 / KGP 2.4.0 / Gradle 9.3.1, Java/Kotlin bytecode target 17; the observed Gradle runtime is Android Studio JBR 21.0.8. Local Apple builds use **Xcode 27.2 (27B52)**. iOS device release builds are unsigned; simulator runs and owned API 30/36 emulators are separate evidence. No CI runs were triggered.

## Remaining gates

- Physical iPhone/Android privacy, device-backup, locking, permission and native-boundary qualification. The owner authorized simulators/emulators for now; those are not physical-device evidence.
- Actual native store test purchase/restore/offline qualification on both platforms.
- Publish/review immutable shared-package Git revisions and qualify actual Git-source resolution in the checker after separately authorized commits/pushes. Current dependencies honestly identify unpublished workspace paths; the production checker fails closed on that provenance.
- Each product's later store signing, accessibility, security, legal/support, pricing and owner release approval. Daymerit's archive capacity and reminder horizon are explicit bounded capabilities, not unbounded-history/background-scheduling promises.

The first public release requires the common foundation gate. Independent product completion then follows the unchanged [17-product queue](LAUNCH_SLATE.md), starting with **Skepbook**. Dossier and OffRecord remain excluded; concept apps inherit the standard when built.

## Work preservation and boundaries

All 26 checkouts remain on `dev` at their original commits. [The preservation audit](validation/2026-11-03/PRESERVATION.md) confirms all 265 relocated originals survive byte for byte, including 109 preexisting dirty/untracked files. Historical validation reports retain their scope and dates.

No commits, pushes, repository renames/merges, deployments, live provider/customer changes or publication occurred. The website pause and main-only CI policy remain. See the [stack standard](STACK_STANDARD.md), [native baseline](NATIVE_DEPENDENCY_BASELINE.md) and [portfolio alignment](ALIGNMENT.md).
