# Data and Cost Matrix

The [shared foundation standard](STACK_STANDARD.md) is implemented across the seven current
consumer apps. Local analysis/tests and both native release builds pass; physical-device, native-store
and immutable-package qualification remain pending before any app release.

Updated November 3, 2026. Current columns describe implemented behavior; concept rows remain
planning only. The approved-direction column includes continuing constraints and explicit deferrals.
Archived cloud/subscription code and dated reports are historical evidence, not the active mobile
operating model. Static PWA browser storage is explicitly distinct from encrypted native storage.

<!-- BEGIN GENERATED: data-cost-matrix -->
| Product | Current data location | Current remote services | Commercial direction | Approved product direction | Guardrails / remaining work |
| --- | --- | --- | --- | --- | --- |
| Skepbook | Shared encrypted SQLite and encrypted app-private attachments | Explicit native Apple/Google store actions; cached ownership loads locally | Native one-time permanent unlock implemented; established pricing preserved | Keep the existing encrypted offline logbook, manual encrypted backups, no account or analytics, and permanent unlock. | No automatic record upload or analytics; owner-encrypted backups; physical/store/provenance qualification pending |
| Ridelore | Shared encrypted SQLite and encrypted attachments; processing stays on device | Explicit native store actions and optional user-requested identity/recall lookup | Native permanent local premium unlock implemented; pricing/store transaction QA pending | Local motorcycle binder and user-controlled encrypted backups; permanent local premium unlock; on-device processing; optional user-owned sync later. | Hosted provider source archived; preserve encrypted owner recovery; no managed sync, hosted binder or remote AI in this release; disclose optional lookup |
| Paws | Shared encrypted SQLite containing authenticated legacy pet-vault envelopes | Explicit native Apple/Google store actions; cached ownership loads locally | Native permanent local premium unlock implemented; store/pricing QA pending | Local pet records and user-controlled PDF/backup exports; permanent local premium unlock; no veterinary diagnosis or required account. | No mandatory hosted account or analytics; native backup exclusions; local PDF and complete encrypted owner recovery; physical/store/provenance qualification pending |
| Pantry Clock | Shared encrypted SQLite containing authenticated legacy inventory envelopes | Explicit native Apple/Google store actions; cached ownership loads locally | Native permanent local premium unlock implemented; store/pricing QA pending | Local food inventory and editable date suggestions; user-controlled exports/recovery and permanent local premium unlock; no required catalog service. | No mandatory hosted account or analytics; local CSV plus complete encrypted owner recovery; editable dates; physical/store/provenance qualification pending |
| Fine Notes | Shared encrypted SQLite containing authenticated legacy tasting-vault envelopes | Explicit native Apple/Google store actions; cached ownership loads locally | Native permanent local premium unlock implemented; store/pricing QA pending | Keep wine, whiskey, coffee, and cigars in one local tasting app; deliberate encrypted sharing, manual valuations, and permanent local premium unlock. | Selected-note encrypted sharing and complete encrypted owner recovery; no remote valuation; physical/store/provenance qualification pending |
| Namefold | Native shared encrypted SQLite; separate static PWA uses unencrypted browser drafts/JSON backups | Native store actions only in wallet; initial static-site download for PWA; no hosted contact/link API | Native permanent-unlock integration implemented; PWA is free/account-free; store/pricing QA pending | Encrypted native contact wallet with QR/vCard exchange and owner backups; separate free static PWA with unencrypted browser drafts/JSON backups; managed links deferred. | Native encrypted recovery differs from unencrypted browser backup; old Worker/D1 source archived; managed links deferred, user-owned hosting later; publication paused |
| Daymerit | Shared encrypted SQLite on parent/shared tablet; no required hosted household account | Explicit native Apple/Google store actions; local reminders/proofs do not require a record server | Native permanent local premium unlock implemented; store/pricing QA pending | Local parent/shared-tablet chores and allowance records; permanent local premium unlock; no managed storage of child records; user-owned family sync only later. | Parent PIN boundaries, bounded authenticated owner recovery and local child board implemented; hosted source archived; user-owned family sync later; physical/store/provenance qualification pending |
| Turnstamp | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | On-device job evidence and deliberate client PDF exports; permanent local premium unlock; no mandatory location upload or job server. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| What We Own | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | One local home-and-move inventory with user-controlled backups and claim-oriented exports; on-device entry assistance; permanent local premium unlock. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Creelmark | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Private local fishing journal; omit locations and photo metadata from exports by default unless selected; optional user-owned hosting later. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Campsake | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Local camping/RV trip journal with deliberate recap exports and user-controlled backup; no required trip server. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Tender Days | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | On-device baby-care journal; deliberate caregiver summaries; optional local-network or user-owned sharing only after verification. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Divefolio | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Offline dive logbook and selected exports; no dive-computer replacement, live safety decision, or certification-acceptance promise. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Brassmark | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Separate encrypted local firearm/range records, maintenance counts, and deliberate exports; no centralized registry or compliance claim. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Object Lore | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Local specialist collection records, manual value history, user-controlled recovery and exports; no required valuation feed. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Quiet Arcade | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Offline puzzles and device-local progress, with no game server, accounts, advertisements, or analytics. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Lockbox | No implemented application; planning only | No implemented application services | Target: permanent local premium unlock | Encrypted on-device estate documents and explicit encrypted export/handoff; no autonomous delivery promise or mandatory managed vault. | Verify encryption, recovery, selective export, and accurate disclosures before release |
| Hub/waitlists | Cloudflare D1 form implementation; publication paused | Cloudflare Pages/Functions/D1 and anti-abuse tooling; no relaunch authorized | Business overhead | Keep website publication paused; any future waitlist is a minimal, disclosed business-contact flow separate from consumer app records. | Consent, bounds, retention, deletion, bot/rate controls; preserve the 2026-10-24 website pause |
<!-- END GENERATED: data-cost-matrix -->

## Portfolio defaults

- Native consumer records remain encrypted on-device; exports happen through deliberate user
  actions. Namefold's separate static PWA keeps browser drafts/JSON backups unencrypted. No app
  requires a hosted record account or Majestic-operated record storage.
- Optional customer-owned servers may be offered later, with tested installation, pairing,
  encryption, access, recovery, and upgrade behavior. Running a server in Majestic's account is
  company hosting, not customer self-hosting. Self-hosting is not an implemented portfolio promise.
- Native permanent-unlock integration is implemented across all seven apps; keep Skepbook's
  established SKU/pricing. Existing records and basic export remain accessible. Disclose native
  Apple/Google billing metadata; RevenueCat source is archived and is not an active mobile service.
- Encrypted owner backup/recovery is implemented across all seven native apps with documented
  bounds and retained legacy readers where applicable. Validate physical-device, cancellation,
  cross-platform and large-vault behavior before release. Reports, CSVs and selected-note sharing are separate
  export capabilities and do not by themselves establish restorable full-vault recovery.
- Network lookups, public contact publishing, website forms, and remote AI each require their own
  field-level explanation. Prefer on-device processing and user-triggered export. Defer managed
  public links, hosted binders, child proof storage, and remote document AI in local release targets.
- Keep the October 24 website pause. The Hub's current form implementation is Cloudflare D1,
  distinct from consumer records; legacy Supabase form descriptions are superseded.

## Before enabling any remote capability

- Document transmitted fields, purpose, recipient/server owner, retention, deletion, and consent.
- Verify access controls, encryption, export/recovery, endpoint limits, outage behavior, and the
  user's ability to stop using the service without losing local records.
- Record per-user cost and high-usage limits for any company service; configure quotas and spend
  alerts before real data. Do not create paid plans, accounts, or infrastructure in a docs pass.
- Reconcile actual binaries, support, privacy/legal pages, and store disclosures before release.
