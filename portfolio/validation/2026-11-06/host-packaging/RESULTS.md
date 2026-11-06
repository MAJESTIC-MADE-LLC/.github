# Current host packaging and foundation evidence — November 6, 2026

The shared host implementation is published at immutable provider
`fd310cecc7dae52a9cb3adf44ed603d59a0eb7ac`, deliberately adopted by all four hosting apps and
Pantry's independent pilot. No SDK or dependency versions changed; the exact three Git revisions
and equivalent resolver YAML quoting are the only lock movements. Core packages remain at d289.

| Scope | Current result |
| --- | --- |
| Skepbook | 306 tests; clean format/analysis; Android and unsigned iOS builds |
| Daymerit | 243 tests; clean format/analysis; Android and unsigned iOS builds |
| Paws | 196 tests; clean format/analysis; Android and unsigned iOS builds |
| Pantry Clock / pilot | 188 + 13 tests; clean format/analysis; regular Android and unsigned iOS builds |
| Shared packages | Eleven analyzers and 264 tests passed |
| Template | 86 tests; Android/unsigned iOS builds; default generated app analysis + 73 tests |
| Host reference | Rust 6 MLS + 16 storage contracts; control 2/reference 10 tests; verifier 27 tests |
| Packaging / policy | 62 Python regressions; four complete Mac arm64 package manifests |
| Windows credentials/services | 44 actual SCM/DPAPI checks; 6 native factory checks; reinstall/TLS negative checks |
| Mac helpers/lifecycle components | Seven isolated checks; arm64 and x64 helper compilation |

Every current consumer passes static adoption, immutable provider/cache provenance and current-source
software evidence. The cohort fingerprint is
`ec81075d82b0c298c2de59e27d4efc53ec668296bdfa0e48e5684b83656fe287`.
The [shared command records](shared-commands.json), [consumer records](consumer-records.json),
[canonical source binding](source-current.json), [adoption check](standardization-after-docs.json)
and [release gate](current-release-gate.json) retain exact hashes and source scopes.

Both Android Rust ABIs, bridge exports and packaged native code were inspected against the selected
source-built libraries; unsigned iOS Runner/AOT/full bundle hashes are retained in each app's new
`docs/validation/2026-11-06/host-packaging` dossier. Skepbook's APK remains intentionally unsigned;
the other engineering APKs use their existing development certificate. These are not store builds.
The [host component dossier](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/validation/2026-11-06/host-packaging/RESULTS.md)
contains exact Mac/Windows component logs, source comparisons and all four host package manifests.

## Release blockers

The global foundation gate still has exactly four unperformed checks: physical iOS privacy,
physical Android privacy, real iOS store transactions and real Android store transactions.

Desktop release also needs the real publisher identities and signed/notarized installation,
actual Mac system-daemon Keychain/approval, interactive Windows owner IPC, signed product-native
execution, minimum-OS/architecture and logout/reboot acceptance. Production store/workspace
licensing, private-network/certificate/recovery operations and independent product release approval
remain separate. Current software/component passes do not satisfy those gates.

A later unsigned Windows AOT fixture was blocked by Application Control; the original-source AOT
pass is retained in its original scope and the new source's native SQLite behavior passed under the
existing trusted Dart VM. No protection was weakened, toolchain installed, certificate imported,
firewall opened, reboot performed, or personal record accessed.

All test SCM registrations/processes/directories on odom-pc were removed. Windows still holds seven
captured temporary service profiles, totaling 5,386,787 bytes (5.14 MiB). Their exact paths/SIDs and
safe-cleanup status are preserved in the component dossier; no force unload or personal-profile
cleanup was attempted. No task-created outputs modified the checked existing graph/build/cache.

Earlier dated evidence remains unchanged. The 27-repository inventory, 17-product queue, accepted
GitHub Free risks and main-only CI policy are unchanged. Website publication remains paused.
