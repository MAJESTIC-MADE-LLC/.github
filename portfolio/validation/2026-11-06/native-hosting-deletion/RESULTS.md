# Native hosting and private deletion — November 6, 2026

Current-source software qualification passes. This does not approve a product release or qualify physical devices, actual stores, signed host installation or production licensing.

## Implemented

- Skepbook: explicit native pairing/enrollment and reviewed recipient/device removal; one common workspace roster for every selected apiary (three people including owner); typed field/batch edits and permitted deletion; pending/conflict/local-draft review; selected photos; independent encrypted recovery, local erasure and shared/private photo export. Location, access instructions, free text, revenue and photos require explicit inclusion. Private data, keys, drafts and legacy recovery stay independent.
- Shared foundation: authenticated roster authors and one encrypted product/journal executor; atomic rollback; create-only immutable staging fast path and covering index; bounded opt-in transfer budget (default240, hard ceiling16384 requests/address/minute); sealed/closed-executor product-file cleanup. Existing consumers retain default behavior.
- Daymerit: active-parent private record/child/all-record deletion after paid access expires; linked content/raw legacy-source removal; hashed anti-regeneration identities; minimal redacted surviving balances; durable proof/retired-local-copy cleanup and retry. Existing exported backups and hosted copies remain independent; explicit authenticated restoration can reintroduce older records. No forensic-erasure claim.

## Actual validation

| Consumer | Current full-suite tests | Native builds |
| --- | ---: | --- |
| Skepbook | 306 | Android release-mode; unsigned iOS |
| Daymerit | 242 | Android release-mode; unsigned iOS |
| Paws | 196 | Android release-mode; unsigned iOS |
| Pantry-Clock | 188 | Android release-mode; unsigned iOS |

Pantry’s thin harness adds13 tests. The affected applications and harness total **945 Dart tests**, plus5 retained backend tests. All11 maintained packages passed independent analysis and **250 tests**; see [shared commands](shared-commands.json). Hub lint/typecheck,201 tests and static export passed; [Hub records](hub/results.json) also check the generated product copy.

Skepbook’s supported20MiB photo completed all640 encrypted chunks, actual TLS/MLS publication, a fresh native viewer checkpoint, verified photo read, encrypted backup, disconnected restore and local erasure in **235.14 seconds**. The coordinator served7789 requests with HTTP200 responses and no clock bypass. The explicit test storage quota is256MiB; a16MiB daemon quota cannot hold this supported transfer. This is local engineering timing, not physical-phone performance acceptance.

Both product CLI entries compile and run as macOS engineering bundles; [CLI proof](https://github.com/MAJESTIC-MADE-LLC/Skepbook/blob/dev/docs/validation/2026-11-06/native-hosting-deletion/cli/README.md) records exact commands and native assets. APK/Runner inspections check both Android Rust ABIs, ELF machine/export symbols, packaged native code against source-built copies, iOS bridge exports and complete bundle/Dart-AOT hashes. Skepbook’s APK is intentionally unsigned under its existing local build policy; the other APKs use the existing development certificate. No store signature is claimed.

Current optional Git source: `5e72d2e60f9c77ab713a671b05fdedd11e7ceb0a`. Core/report/media/reminder pins remain unchanged. Eight-consumer cohort: `b32d296ea025a0ba3da6115c5ea7156558efe65f08074d3dcebeb43d6c193c28`. Unchanged consumers retain their valid original source-specific records. Historical evidence remains unchanged; superseded initial materialization, earlier immutable revisions and documentation-race attempts retain their original scope.

## Release blockers remaining

- Representative physical iOS and Android privacy/lifecycle/device checks.
- Actual signed native-store transactions on both platforms: purchase, renewal, cancellation/refund, restore and offline expiry.
- Hosting operations: signed/notarized desktop service installers and lifecycle, qualified Windows credentials/ACL provisioning, production workspace licensing/verifier configuration and physical LAN/VPN qualification. The optional opaque push bridge remains unimplemented; synchronization is explicit/manual.
- Independent product QA/accessibility/artwork/store-listing and owner release approval in the unchanged17-product queue. The website publication pause remains in force.

GitHub Free protection limitations and billing-blocked optional CI remain accepted interim conditions; reproducible local results are recorded here.

See the [final foundation gate](foundation-gate.json), [portfolio alignment](standardization.json), [governance regressions](governance-tests.log), [live inventory audit](inventory.log), [historical evidence check](historical-evidence-check.json) and [existing dependency alert review](ALERT_REVIEW.md).
