# Organization repository status

This file is generated from `portfolio/REPOSITORIES.json`. Do not edit its table by hand.

<!-- BEGIN GENERATED: repository-status -->
Evidence captured 2026-09-14: Live GitHub organization inventory plus local dev-branch checkouts for implemented and shared repositories.

The organization has 23 repositories: 7 functional release candidates, 10 concept-only product repositories, and 6 shared, governance, legal, website, template, or infrastructure repositories. The implementation count is seven; the shared public-release gate is not complete.

| Repository | Status | What should happen next | Problems or concerns |
| --- | --- | --- | --- |
| .github | Active organization governance with generated portfolio controls and CI validation. | Founder-review the release policy and resolve branch-protection issue #1. | Private-repository branch protection remains unavailable on the current GitHub plan. |
| Almanac | Functional local-first Flutter release candidate with automated tests and release-build checks. | Complete full-vault recovery plus physical-device, purchase, accessibility, and store QA. | Full-vault recovery is not implemented; client-side entitlement checks are a soft commercial gate. |
| Apiary | Functional offline-first iPhone release candidate with encrypted SQLite, exports, backups, and CI. | Run physical-device and accessibility QA, then configure App Store signing and the purchase product. | The local trial can reset after reinstall and must remain explicitly documented; release still needs owner legal approval. |
| App-Template | Reusable Flutter scaffold for local-only, local-first, and Supabase-backed products, with CI. | Complete a final baseline review, tag it, and enable GitHub template-repository mode. | It is a scaffold rather than a launch product; provider-backed modes still require per-product security review. |
| Bivy | README-only product concept on dev. | Define the trip and campsite schema plus recap-export requirements, then scaffold with CI. | No implementation, tests, roadmap, or automated checks exist. |
| Chat Armor | README-only research concept on dev. | Resolve platform feasibility, consent, and the privacy model before scaffolding. | The concept involves highly sensitive child and message data; beta-style claims must not imply an implemented product. |
| Convoy | README-only product concept on dev. | Define the evidence and claim-export model, then scaffold with CI. | No implementation or automated checks exist. |
| Cradle | README-only product concept on dev. | Define the event model and caregiver-sharing boundary before scaffolding. | The product would handle sensitive child data; sharing and recovery remain unresolved. |
| Deep Six | README-only product concept on dev. | Define the dive and certification schema plus export requirements, then scaffold with CI. | No implementation or automated checks exist. |
| Hook | README-only product concept on dev. | Define encrypted photo and location storage plus recovery, then scaffold with CI. | Sensitive location data and device-loss recovery behavior remain unresolved. |
| Majestic-Made-Hub | Implemented static Next.js portfolio and waitlist site pinned to Node 24, with web CI. | Keep product claims synchronized and complete owner and legal review before publishing. | The site is not deployed; waitlist submissions add Supabase retention, deletion, and abuse-control obligations. |
| Paws | Functional encrypted local-vault Flutter release candidate with on-device PDF reports and CI. | Resolve the trademark/name decision and run physical-device, accessibility, purchase, and store QA. | Full-vault recovery is not implemented, and product copy must remain recordkeeping rather than veterinary advice. |
| Range | README-only product concept on dev. | Define the MVP and security architecture before scaffolding. | The proposed firearm and license data is particularly sensitive; no implementation or CI exists. |
| ReachMe | Functional Flutter app plus Cloudflare worker and web/PWA release candidate with CI. | Run provider-sandbox end-to-end tests plus hosted-link abuse, expiry, revoke, and recovery tests. | Published fields are public, and the optional D1 link service creates recurring security, retention, and cost obligations. |
| RideBinder | Functional local-first Flutter release candidate with optional cloud modules and CI. | Run physical-device backup, import, PDF, purchase, and store-signing QA with cloud flags off first. | Optional sync, document storage, sharing, and AI extraction materially expand cost and security scope. |
| RoomProof | README and gitignore only; no application implementation on dev. | Define photo, signature, time, and location retention, then scaffold Flutter with CI. | Evidence media and location metadata need an explicit privacy and deletion model before implementation. |
| RoutineCue | Functional Flutter and Supabase collaborative release candidate with mobile, backend, and local database checks. | Apply and test the reviewed backend in a non-production Supabase project, configure purchases/notifications, and run family-device QA. | Child data and photo proof require high-trust cloud operations, strict retention, and continuing provider cost controls. |
| Steward | README-only product concept on dev. | Specify encryption, export, and recovery before scaffolding. | Insurance and home data is sensitive; cloudless device-loss behavior remains unresolved. |
| Trove | README-only product concept on dev. | Define the schema plus import, export, and recovery, then scaffold with CI. | No implementation or CI exists; portability and recovery are undefined. |
| Use By | Functional encrypted local-vault Flutter release candidate with CSV export and CI. | Complete date/time-zone, food-safety copy, recovery, physical-device, purchase, and store QA. | Suggested dates are user-editable defaults, not food-safety advice; full-vault recovery is not implemented. |
| app-legal | Public legal and support site with draft coverage and automated structural validation for all seven release candidates. | Have both founders and qualified counsel review the pages against final binaries and store disclosures. | Automated checks can verify completeness and consistency, but cannot establish legal adequacy. |
| wolfe-server-apps | Validated hardened Docker/Next.js deployment template; apps/ intentionally contains no deployable product. | Keep deferred until a server-backed product has an approved deployment need. | This is infrastructure scaffolding, not a deployed service or launch product. |
| wolfe-server-infra | Substantial server hardening, deployment, monitoring, and backup-readiness automation with CI. | Configure scheduled off-site backups on the target host and complete a documented restore drill. | Production readiness still depends on host-specific configuration, credentials, alert delivery, and a successful restore test. |
<!-- END GENERATED: repository-status -->

Run `python3 scripts/portfolio_status.py --check` after changing the manifest. Use `--workspace-root .. --verify-github MAJESTIC-MADE-LLC` for the full local and organization inventory audit.
