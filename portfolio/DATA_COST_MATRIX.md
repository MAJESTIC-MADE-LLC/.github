# Data and Cost Matrix

Review this file before adding any SDK, hosted feature, background job, or externally stored field.
Dollar budgets must be approved by both founders before external testing because provider prices can
change. Free features must have a bounded worst-case cost.

<!-- BEGIN GENERATED: data-cost-matrix -->
| Product | Default data location | Remote services | Paid boundary | Mandatory guardrails |
| --- | --- | --- | --- | --- |
| Apiary | Encrypted SQLite and app-private files | Apple purchase processing only | One-time permanent unlock | No automatic upload; manual encrypted backup; no analytics |
| ReachMe | SQLite/browser storage | Optional Cloudflare D1 links; Apple/RevenueCat purchases | More profiles, links, and premium styling | Field-by-field publish consent; 10-link cap; 12-month expiry; revoke/delete; request limits |
| RideBinder | Local SQLite and files | Optional Supabase Auth/Postgres/Storage/Functions, RevenueCat, NHTSA, and optional OpenAI extraction | Cloud backup/sync/share and remote extraction | Remote flags off by default; 1 GB/user storage cap; five-link cap; AI rate cap; 90-day post-Pro purge |
| RoutineCue | Supabase account data with small local caches | Supabase, RevenueCat, Firebase/APNs | Plus/Pro household features | Private proof bucket; Free 7-day, Plus 90-day, Pro 12-month proof retention; daily cleanup; device/session limits |
| Paws | AES-256-GCM encrypted app-private vault; key/verifier in platform secure storage | RevenueCat and store purchase processing only | Creating pets and health records | No account/backend/analytics; single-device v1; Android backup and transfer disabled; on-device PDF export |
| Almanac | Encrypted on-device vault | RevenueCat and store purchase processing only | Creating inventory/tastings and encrypted note import/share | No account/backend/analytics; single-device v1; encrypted single-note transfer; no remote valuation |
| Use By | Encrypted on-device inventory | RevenueCat and store purchase processing only | Adding inventory items | No account/backend/database/analytics; single-device v1; manual CSV export; suggested dates remain editable |
| Hub/waitlists | Browser plus Supabase submissions | Supabase and hosting | Business overhead | Collect email and product only; consent copy; deletion process; abuse/rate limits |
<!-- END GENERATED: data-cost-matrix -->

## Approval Checklist for Any Remote Feature

- List every transmitted and retained field, processor, region if material, purpose, and retention.
- Define authentication, authorization, encryption, export, deletion, incident, and provider-exit paths.
- Set per-user quotas, endpoint rate limits, storage lifecycle rules, and a remote kill switch.
- Record fixed monthly cost, cost per active free user, cost per paid user, and a high-usage scenario.
- Configure spend alerts before real users; investigate at 50%, 75%, and 90% of the approved budget.
- Charge for recurring-cost features at a margin that survives store fees and the high-usage scenario.
- Update privacy, terms, support, store disclosures, tests, and marketing before enabling the feature.
