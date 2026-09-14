# Seven-Product Launch Slate

Locked on September 11, 2026. Changing the slate requires both founders to record the reason,
replacement, cost impact, and schedule impact.

<!-- BEGIN GENERATED: launch-slate-status -->
| Order | Product | Current evidence | Next release milestone | Main concern |
| --- | --- | --- | --- | --- |
| 1 | Apiary | Encrypted offline records, exports and backups, hardened lifecycle locking, native privacy controls, automated tests, and iOS release-build validation. | Run Face ID/passcode, screen-capture, physical-device, and accessibility QA, then configure App Store signing and the purchase product. | The local trial can reset after reinstall and must remain explicit; individual screenshots cannot be blocked on iOS, and release still needs owner legal approval. |
| 2 | ReachMe | Local contact wallet, explicit-field publishing, Cloudflare link service, PWA, 22 Flutter tests, four native tests, and iOS release-build validation. | Configure a Cloudflare staging environment and Cron, then run hosted-link abuse, expiry, revoke, recovery, and physical-device tests. | Published fields are public; D1 creates recurring security, retention, and cost obligations, while provider credentials and deployed staging require owner access. |
| 3 | RideBinder | Local-first records, encrypted backups, API-28 strong-biometric enforcement, stale-key cleanup, automated tests, and Android/iOS builds. | Run biometric hardware and physical-device QA, then configure production HTTPS callbacks and App/Universal Links before enabling cloud flags. | Optional sync, storage, sharing, and AI extraction expand cost/security scope; Android emulator images are missing and hardware enrollment-change behavior is unverified. |
| 4 | RoutineCue | Mobile workflows, reviewed Supabase authorization and retention logic, automated app/backend tests, local database validation, and Android/iOS release builds. | Apply the reviewed backend to a non-production Supabase project, configure purchases/notifications, and run multi-device family QA. | Child data and photo proof require high-trust cloud operations; staging credentials, push providers, retention operations, and cost alerts require owner-controlled services. |
| 5 | Paws | Encrypted local vault, device-bound authentication, native data protections, automated tests, PDF validation, and Android/iOS release builds. | Resolve the trademark/name and recovery decisions, then run biometric hardware, physical-device, accessibility, purchase, and store QA. | Full-vault recovery is not implemented, biometric enrollment changes need hardware validation, and copy must remain recordkeeping rather than veterinary advice. |
| 6 | Almanac | Encrypted local vault, enrollment-bound device authentication, native backup and screen-privacy controls, automated tests, and Android/iOS release-build checks. | Choose and implement full-vault recovery, then complete physical-device, purchase, accessibility, and store QA. | Full-vault recovery is not implemented; client-side entitlement checks remain a soft commercial gate, and biometric enrollment changes still need hardware validation. |
| 7 | Use By | Encrypted single-device inventory, device-bound authentication, native privacy controls, automated export tests, and signed Android/unsigned iOS release builds. | Choose recovery behavior, validate date/time-zone and food-safety copy, then run biometric hardware, physical-device, purchase, and store QA. | Suggested dates are not food-safety advice; full-vault recovery is absent, and biometric enrollment changes need hardware validation. |
<!-- END GENERATED: launch-slate-status -->

## Recommended Execution

1. Finish Apiary and ReachMe physical-device, purchase, legal, and store gates.
2. Ship a local-only RideBinder release candidate before enabling paid cloud modules.
3. Validate RoutineCue against a production-like backend with synthetic family data.
4. Keep Paws, Almanac, and Use By local-only while completing recovery and device/store QA.
5. Keep Chat Armor in research and keep all non-slate concepts out of the critical path.

The slate optimizes for reuse and low operations cost. It is a planning decision, not a statement
that any product is currently available.
