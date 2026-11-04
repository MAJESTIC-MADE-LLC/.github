# Sequential Product Release Queue

Updated November 3, 2026 from the approved portfolio review. This replaces the September 11
seven-product launch slate and the requirement to finish seven products before the first release.
First standardize the template and all seven current apps under the [shared foundation gate](STACK_STANDARD.md),
with iOS and Android first releases. The gate is pending and must qualify before any app release.
Then complete each application's remaining product work in the order below. A queue entry is a
priority decision, not a readiness claim, release date, or authorization to publish.

<!-- BEGIN GENERATED: launch-slate-status -->
| Order | Product | Recorded implementation evidence | Next release milestone | Main concern |
| --- | --- | --- | --- | --- |
| 1 | Skepbook | Current shared-foundation analysis/tests and Android/unsigned iOS release builds pass; real local record/photo persistence is recorded separately from pending physical/store qualification. | Finish shared physical-device/store qualification, then validate Skepbook recovery, accessibility, signing and final store/legal copy for its first release. | The local trial can reset after reinstall; iOS cannot block individual screenshots. Physical-device/store tests and owner release approval remain pending. |
| 2 | Ridelore | Current shared-foundation analysis/tests, Android/unsigned iOS release builds and native OCR qualification pass; existing records and encrypted backups remain local. | Finish physical recovery/privacy, native store qualification, then product-specific import/PDF/accessibility/signing QA. Managed sync, hosted binders and remote AI remain deferred. | Optional user-requested vehicle lookup and native store metadata are remote flows; do not claim universal zero network. Physical devices, store transactions and product release approval remain pending. |
| 3 | Paws | Current shared-foundation analysis/tests and Android/unsigned iOS release builds pass; legacy IDs, key namespaces and large version-one recovery compatibility are preserved. | Finish physical recovery/privacy, native store qualification, then pet-report/accessibility/signing/store QA and naming review. | Physical-device/reliability and store transactions remain pending. Recordkeeping and exports do not provide veterinary diagnosis. |
| 4 | Pantry Clock | Current shared-foundation analysis/tests and Android/unsigned iOS release builds pass; legacy inventory and backup readers remain compatible. | Finish physical recovery/privacy, native store qualification, then validate dates/time zones, editable suggestions, accessibility, signing and store copy. | Physical-device/store qualification remains pending. Suggested dates are editable defaults, not food-safety advice; CSV export is distinct from full encrypted recovery. |
| 5 | Fine Notes | Current shared-foundation analysis/tests and Android/unsigned iOS release builds pass; original encrypted-note and full-vault readers are retained. | Finish physical recovery/privacy, native store qualification, then large-collection, selected-sharing, accessibility, signing and store QA. | Large/low-memory vault and physical-device reliability, store transactions and release approval remain pending; no remote valuation or diagnosis is provided. |
| 6 | Namefold | Current native analysis/tests and Android/unsigned iOS release builds pass. Static PWA export, local VCF/PNG/SVG/JSON workflows, offline reload and backup restore pass local validation. | Finish physical camera/privacy/recovery, native store qualification. Keep website publication paused; managed public links remain deferred and user-owned hosting is later work. | Browser drafts and JSON backups are unencrypted and can be cleared by browser storage deletion. Physical/store qualification is pending; no managed public-link service is part of this release. |
| 7 | Daymerit | Current local app analysis, 69 tests and Android/unsigned iOS release builds pass; real local parent/child workflow and bounded owner-backup validation are recorded separately. | Finish physical parent/child/privacy/recovery, native store qualification, then product accessibility/signing/store QA. User-owned family sync remains deferred. | Physical/store qualification is pending. Archive capacity and reminder horizon are bounded; family synchronization and managed child-record hosting are not implemented release features. |
| 8 | Turnstamp | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Build a solo-cleaner workflow with local checklists, before/after photos, selected signatures, and owner-reviewed PDF exports; defer teams, dispatch, billing, and hosted portals. | Evidence media and location metadata need an explicit privacy and deletion model before implementation. |
| 9 | What We Own | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Combine Claim Crate requirements and steward marketing into this product plan; design one belongings dataset across home and moves, with verified backup/recovery. | The product is still a concept; consolidation is a documentation decision, not a completed repo/content/sign-up migration. |
| 10 | Creelmark | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Define local catch/spot records, encrypted backup/restore, and location-redacted exports; avoid social feeds, uploaded fishing spots, and required species APIs. | Sensitive location data and device-loss recovery behavior remain unresolved. |
| 11 | Campsake | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Build the local trip/campsite journal, packing lists, and recap exports; defer campground discovery, booking, and live map services. | No application implementation or product tests and build checks exist. |
| 12 | Tender Days | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Design fast local care logging and tested recovery first; define consent and secure local partner handoff before collaboration; avoid medical predictions. | The product would handle sensitive child data; sharing and recovery remain unresolved. |
| 13 | Divefolio | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Define local dive logs, certifications, buddy signatures, backup/restore, and portable exports; defer unsupported computer imports and safety algorithms. | No application implementation or product tests and build checks exist. |
| 14 | Brassmark | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Keep an isolated local firearm/ammo/range vault; design encrypted recovery and selective exports before scaffolding; avoid managed ownership databases. | The proposed firearm and license data is particularly sensitive; no implementation or product validation exists. |
| 15 | Object Lore | Concept-only repository with implementation-readiness guardrails and local governance validation and main-only CI configuration. | Define collector-specific provenance, value history, and category fields before building a separate app; reuse inventory primitives without coupling private databases. | Separate launch is justified only by collector workflows beyond the combined home inventory; valuation feeds, marketplace features, imports, and recovery are not implemented. |
| 16 | Quiet Arcade | Concept in the Hub catalog; no standalone repository, app, or validated game set. | After Object Lore, choose a small puzzle set with deterministic local daily boards, no ads or analytics, local saves, and a permanent unlock. | No new repository or game implementation is created by this alignment; game quality, content rights, and recovery remain unverified. |
| 17 | Lockbox | Planning/handoff documents exist; no application code or product validation. | Build only after earlier products; narrow v1 to local document organization and explicit encrypted handoff. Defer autonomous time-release/dead-man delivery. | A device-only app cannot guarantee future unattended delivery; inheritance access and recovery require deliberate design and testing. |
<!-- END GENERATED: launch-slate-status -->

## How to use the queue

- First pass the [shared foundation adoption and qualification gate](STACK_STANDARD.md). Then finish
  and record the current product's applicable [release gates](RELEASE_DEFINITION.md)
  before moving to the next app. Record any owner/device/service blocker; do not silently skip or
  reorder the queue. Support and documentation work may unblock the current app.
- After the common foundation qualifies across the template and all seven existing apps, each app
  can receive its own product release approval. The foundation gate is not a requirement for all
  seven products to finish every domain/legal/accessibility/store-submission check. Publication and
  paid-service changes remain separate owner-controlled actions.
- All seven apps implement the shared local foundation and pass local tests/both native builds.
  Daymerit is account-free/local; Namefold's native wallet is encrypted and its separate static PWA
  stores browser drafts/backups unencrypted. Hosted source/reports remain archived/historical.
  Physical recovery/privacy, native-store acceptance and immutable-package provenance remain pending.
- Consumer records stay on-device by default. Exports are deliberate user actions. Optional
  user-owned hosting is a later capability, not an existing portfolio-wide feature. Company-hosted
  storage is not equivalent to customer self-hosting.
- Native permanent-unlock integration is implemented across all seven apps. Keep Skepbook's
  established SKU/pricing; verify each app's store products, prices and transaction/restore behavior,
  preserving existing record access and basic export.
- Quiet Arcade is a Hub concept without a repo. Its slot does not authorize repository creation.
  Lockbox's autonomous time-release/dead-man delivery is deferred; the queued scope is a document
  vault and explicit encrypted handoff.

## Work without an independent launch slot

| Repository or product | Decision |
| --- | --- |
| Claim-Crate | Consolidate moving/PCS, boxes, condition/damage evidence, and claim exports into What We Own. Keep the repo and requirements until migration is separately implemented. |
| steward | Consolidate the legacy landing page into Hub/What We Own; plan URLs, consent, and signup migration before any archival or relaunch. |
| Kinwall | Research only; no app build until platform feasibility and a transparent consent-based local model are resolved. |
| dossier | Excluded from this alignment and release work at the owner's request; inventory entry only. |
| off-record | Paused experimental work; excluded from the consumer release queue. |
| .github, App-Template, Majestic-Made-Hub, app-legal, brand-assets | Shared support work for the current app; no independent consumer-app slot. |
| wolfe-server-apps, wolfe-server-infra | Separate operational scaffolding; defer consumer hosting work until a specific customer-owned hosting requirement is approved. |

The website pause recorded October 24, 2026 remains in force: app-legal Pages/DNS and Hub
Cloudflare publication stay disabled. This queue authorizes no publishing, renames, archives,
commits, pushes, or infrastructure changes.
