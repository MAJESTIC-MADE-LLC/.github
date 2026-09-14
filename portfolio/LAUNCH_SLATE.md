# Seven-Product Launch Slate

Locked on September 11, 2026. Changing the slate requires both founders to record the reason,
replacement, cost impact, and schedule impact.

<!-- BEGIN GENERATED: launch-slate-status -->
| Order | Product | Current evidence | Next release milestone | Main concern |
| --- | --- | --- | --- | --- |
| 1 | Apiary | Full offline-first iPhone implementation with encrypted SQLite, automated tests, backup checks, and iOS build validation. | Run physical-device and accessibility QA, then configure App Store signing and the purchase product. | The local trial can reset after reinstall and must remain explicitly documented; release still needs owner legal approval. |
| 2 | ReachMe | Functional local contact wallet, Cloudflare link service, web/PWA, automated tests, and CI validation. | Run provider-sandbox end-to-end tests plus hosted-link abuse, expiry, revoke, and recovery tests. | Published fields are public, and the optional D1 link service creates recurring security, retention, and cost obligations. |
| 3 | RideBinder | Substantial local-first implementation with automated tests, encrypted backup checks, and Android/iOS release builds. | Run physical-device backup, import, PDF, purchase, and store-signing QA with cloud flags off first. | Optional sync, document storage, sharing, and AI extraction materially expand cost and security scope. |
| 4 | RoutineCue | Substantial Flutter/Supabase implementation with automated mobile/backend tests, local database smoke checks, and mobile release builds. | Apply and test the reviewed backend in a non-production Supabase project, configure purchases/notifications, and run family-device QA. | Child data and photo proof require high-trust cloud operations, strict retention, and continuing provider cost controls. |
| 5 | Paws | Functional encrypted local-vault implementation, automated tests, release configuration, PDF checks, and mobile release builds. | Resolve the trademark/name decision and run physical-device, accessibility, purchase, and store QA. | Full-vault recovery is not implemented, and product copy must remain recordkeeping rather than veterinary advice. |
| 6 | Almanac | Functional encrypted local-vault implementation, automated tests, release configuration, and mobile release-build checks. | Complete full-vault recovery plus physical-device, purchase, accessibility, and store QA. | Full-vault recovery is not implemented; client-side entitlement checks are a soft commercial gate. |
| 7 | Use By | Functional single-device encrypted inventory, automated tests, release configuration, export checks, and mobile release builds. | Complete date/time-zone, food-safety copy, recovery, physical-device, purchase, and store QA. | Suggested dates are user-editable defaults, not food-safety advice; full-vault recovery is not implemented. |
<!-- END GENERATED: launch-slate-status -->

## Recommended Execution

1. Finish Apiary and ReachMe physical-device, purchase, legal, and store gates.
2. Ship a local-only RideBinder release candidate before enabling paid cloud modules.
3. Validate RoutineCue against a production-like backend with synthetic family data.
4. Keep Paws, Almanac, and Use By local-only while completing recovery and device/store QA.
5. Keep Chat Armor in research and keep all non-slate concepts out of the critical path.

The slate optimizes for reuse and low operations cost. It is a planning decision, not a statement
that any product is currently available.
