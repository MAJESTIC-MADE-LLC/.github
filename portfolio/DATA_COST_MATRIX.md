# Data and Cost Matrix

Review this file before adding any SDK, hosted feature, background job, or externally stored field.
Dollar budgets must be approved by both founders before external testing because provider prices can
change. Free features must have a bounded worst-case cost.

| Product | Default data location | Remote services | Paid boundary | Mandatory guardrails |
| --- | --- | --- | --- | --- |
| Apiary | Encrypted SQLite and app-private files | Apple purchase processing only | One-time permanent unlock | No automatic upload; manual encrypted backup; no analytics |
| ReachMe | SQLite/browser storage | Optional Cloudflare D1 links; Apple/RevenueCat purchases | More profiles, links, and premium styling | Field-by-field publish consent; 10-link cap; 12-month expiry; revoke/delete; request limits |
| RideBinder | Local SQLite and files | Optional Supabase Auth/Postgres/Storage/Functions, RevenueCat, NHTSA, optional OpenAI extraction | Cloud backup/sync/share and remote extraction | Remote flags off by default; 1 GB/user storage cap; five-link cap; AI rate cap; 90-day post-Pro purge |
| RoutineCue | Supabase account data with small local caches | Supabase, RevenueCat, Firebase/APNs | Plus/Pro household features | Private proof bucket; Free 7-day, Plus 90-day, Pro 12-month proof retention; daily cleanup; device/session limits |
| Paws | Planned local database and files | Store purchase processing only for v1 | To be approved before build | No cloud/account in v1; manual export/backup; no medical analytics SDK |
| Almanac | Planned local database and files | Store purchase processing only for v1 | To be approved before build | No remote valuation in v1; no collection upload; manual export/backup |
| Use By | Planned local database and files | Store purchase processing only for v1 | To be approved before build | Single-device v1; no hosted inventory; barcode data bundled/cached where licensing permits |
| Hub/waitlists | Browser plus Supabase submissions | Supabase and hosting | Business overhead | Collect email and product only; consent copy; deletion process; abuse/rate limits |

## Approval Checklist for Any Remote Feature

- List every transmitted and retained field, processor, region if material, purpose, and retention.
- Define authentication, authorization, encryption, export, deletion, incident, and provider-exit paths.
- Set per-user quotas, endpoint rate limits, storage lifecycle rules, and a remote kill switch.
- Record fixed monthly cost, cost per active free user, cost per paid user, and a high-usage scenario.
- Configure spend alerts before real users; investigate at 50%, 75%, and 90% of the approved budget.
- Charge for recurring-cost features at a margin that survives store fees and the high-usage scenario.
- Update privacy, terms, support, store disclosures, tests, and marketing before enabling the feature.
