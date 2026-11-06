# Optional user-owned hosting

Approved and review findings resolved November 4, 2026; runtime adoption updated November 6. **Shared source is published and Skepbook, Pantry Clock, Paws and Daymerit regular builds adopt it;
production service and physical/store qualification remain pending.** This extends the [shared foundation](STACK_STANDARD.md).
Current runtime dependencies, immutable package revisions and foundation qualification keep
their existing scope. Hosting adds no current-launch prerequisite. The
[17-product release order](LAUNCH_SLATE.md), approved base prices, website pause and independent
product approvals remain unchanged. Dossier and OffRecord remain excluded.

## Approved experience

- Encrypted local records remain primary. Useful local workflows require no host or Majestic
  account; existing trial/subscription rules still apply. A sleeping or unreachable computer
  delays sharing without deleting or blocking access to existing local records.
- First distribution: a simple **Mac/Windows control application**, guided installation/pairing
  and explicitly approved background services that continue after window close/logout and
  restart after reboot when disks and credentials are available. Sleep, power loss and disk
  preboot locking still interrupt availability. Linux/NAS/container packaging comes later.
- Owners explicitly select collections, recipients and destinations. Enrollment provides scoped
  standing authorization for background synchronization; manual export remains a separate action.
  Show who can decrypt, necessary metadata, pending changes and how to disconnect.
- Host-owned identities and native purchases remain separate. Pairing grants no billing ownership;
  purchasing/restoring grants no collection membership or keys. One computer can serve several
  products with independent app namespaces, keys, memberships and retention policies.
- Remote access uses the owner's configured private network/VPN. No automatic router opening,
  public record relay or universal remote-reachability promise. A chosen VPN may have its own
  account, coordination service and metadata disclosures.

## Trust and concrete technical direction

| Component | Selected direction and access |
| --- | --- |
| Desktop control UI | Existing qualified Flutter/Dart toolchain; guided setup/status and explicit administration. Closing the UI does not stop approved services. |
| Ciphertext storage daemon | Rust service; host-local SQLite routing metadata and immutable encrypted objects. No record/attachment/group/recovery private keys or readable product rules. |
| Trusted desktop coordinator client | Separately approved headless Dart service reusing product adapters and the shared Rust crypto bridge. Holds keys and readable projections only for selected collections; validates and orders shared decisions. |
| Mobile encryption | MLS 1.0 via maintained OpenMLS and a shared Rust/Dart bridge; separate groups for confidentiality scopes. Existing local database/attachment keys stay local. |
| Native transport | Separate per-role private TLS trust roots and pinned identities for storage and coordinator; normal certificate and hostname validation. LAN/private-network access only. |

The owner explicitly approved the **trusted desktop coordinator for selected collections**.
“Ciphertext-only host” applies to the storage process. A computer also running an enrolled
coordinator is an authorized plaintext endpoint for those collections. Its administrator or a
whole-machine compromise may expose them; process isolation does not remove that risk. Majestic,
the push bridge and entitlement verifier receive no record-decryption keys or app content.
Search/reports/processing occur on authorized clients, including the selected coordinator.
Readable processing by the storage daemon remains outside this design.
The first sync profile requires coordinator enrollment for selected shared collections; declining
that trust keeps them local. One workspace-wide membership/cap ledger prevents independent
collections from multiplying the included member/device allowance.

The optional reference pins OpenMLS **0.9.2**, Flutter Rust Bridge **2.13.0**, and Rust **1.99.1**,
with Flutter **3.47.8**/Dart **3.13.7**. These are isolated optional dependencies; default consumer
pins are unchanged. Recheck advisories and qualify source-built native libraries before adoption. Product support targets are macOS **15+**
and vendor-supported Windows **11 25H2+**, distributing only tested architectures. The
[desktop contract](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_DESKTOP_CONTRACT.md)
specifies service identities, unattended key access, signed installers, TLS lifecycle and local
network permission/denial behavior. Source-built native integration checks exist; signed service
installation and OS credential lifecycle still require operational qualification.

## Seven review findings and their resolutions

All seven are **resolved as design requirements**. Reference code and local evidence now exist;
[implementation status](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_IMPLEMENTATION.md)
separates completed checks from remaining qualification. Published source now includes generic
product-owned transactions and a workspace-wide allocation ledger; Daymerit composes isolated
parent/child/proof groups. These implemented contracts do not qualify signed services or live licensing.

| Finding | Required resolution | Detailed template contract |
| --- | --- | --- |
| 1. Backup serializers expose secrets or other members' records | Independent allowlisted/versioned sync DTOs; exclude recovery/PIN/private-key/purchase/legacy-export fields. Daymerit uses parent, per-child working and per-child proof key scopes. Preserve existing owner-backup readers. | [Security](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_SECURITY_CONTRACT.md) |
| 2. Signed old membership can be replayed | One explicitly trusted coordinator per collection serializes membership and content-bound single-use publication permits. New uploads require current authority; stale work stays local and rebases under a new operation identity. Suspected coordinator rollback requires quarantine and owner-reviewed authority recovery. | [Security](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_SECURITY_CONTRACT.md) |
| 3. Existing snapshot writes cannot atomically queue sync | One encrypted SQLite transaction/executor commits projection, journal, inbox/deduplication, cursor and staged MLS state. Introduce a qualified shared storage extension; never attach a second journal after a snapshot save. | [Sync/migration](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_SYNC_CONTRACT.md) |
| 4. Offline requests can overspend shared balances | Daymerit queues offline requests; approvals, reward debits, awards and manual allowance entries become final only after coordinator confirmation. Pantry uses exact fixed-point quantity operations, revision conflicts and visible underflow handling. | [Sync/migration](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_SYNC_CONTRACT.md) |
| 5. Old restores can resurrect deleted data or devices | Restore defaults to a disconnected fork; explicit rejoin uses a fresh device identity and current authenticated checkpoint. Terminal deletion markers and checkpoint-based deduplication prevent resurrection; stale devices rebase. | [Sync/migration](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_SYNC_CONTRACT.md) |
| 6. Invited members lack portable paid access | One verified owner subscription covers app-specific included members across iOS/Android. Minimal metadata-only verifier issues bounded signed workspace grants; no arbitrary host paid flag or per-child fee. | [Entitlements](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_ENTITLEMENT_CONTRACT.md) |
| 7. Host lifetime, platform and LAN trust were undefined | Explicitly approved OS services, separate coordinator, qualified OS floor/runtime, per-role private-CA pairing/rotation, permission repair and signed upgrade/rollback rules. | [Desktop](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_DESKTOP_CONTRACT.md) |

## Publication, consistency and recovery rules

One logical coordinator per collection serializes current membership and shared decisions.
An owner can record a revocation offline, but it is **pending** until that authority durably
commits the membership change and new epoch. Before new record/attachment ciphertext reaches
the storage daemon, obtain a fresh content-bound permit over the independently authenticated
coordinator connection. An old signed membership is insufficient. Reconcile the disposition of
ambiguous attempts before issuing a superseding operation; do not duplicate spending/quantity effects.

Revocation cannot erase previously decrypted copies, old keys or already-authorized past bytes.
A permit ordered before removal authorizes only its exact old content, even if delivery is delayed.
A rolled-back storage daemon cannot authorize new publication; a compromised/rolled-back trusted
coordinator is an endpoint failure with explicit quarantine/recovery, not automatically solved
by encryption. Owner-phone checkpoints detect witnessed regressions but cannot prove that an
unseen newer history never existed.

Local provisional work, host receipt and signed shared acceptance are different states. Keep
pending/conflicted/disconnected status visible. Synchronize records/operations, never live SQLite
files or whole-vault snapshots. [SQLite network guidance](https://sqlite.org/useovernet.html)
explains the file-sharing boundary. Product adapters own schemas, domain validation and conflict
resolution; a ciphertext daemon cannot validate an encrypted balance or care event.

Sync is not backup: authorized deletions can propagate. Preserve independently retained encrypted
archives and owner recovery material. Restore is disconnected by default; rejoining requires current
authorization and a verified checkpoint. Disconnect/export works without host availability and
explains retained remote/member copies. Missing keys/data cannot be reconstructed by Majestic.

A final shared decision requires the coordinator to durably retain the accepted command,
exact ciphertext, signed outcome and required attachment/repair state in its atomic projection,
authority and crypto journal before acknowledging success. A digest-only publication permit is
preauthorization, not finalization; losing the originating phone must not lose an accepted decision.

## Licensing and metadata services

Keep the [approved subscription prices](PRICING.md). Future hosting includes a bounded workspace
in the core offer: Pantry/Paws/Fine Notes up to **6** people including owner, Skepbook **3**,
Ridelore **4**, Daymerit **4 adult caregivers** with no per-child charge, Namefold one owner's
devices. Limits span collections rather than resetting per collection. No extra-seat fee or host
surcharge is introduced for the first hosting version. Larger-team pricing is a later decision.
The entitlement contract defines device capacity, scope, expiry and capacity repair.

Cross-platform invited access uses a separately disclosed **minimal Majestic entitlement verifier**
with store developer credentials retained only by Majestic. It sees necessary purchase and
pseudonymous workspace/grant metadata, not record contents or keys. Signed workspace grants are
bounded to at most seven days and verified paid-through/grace; expiry pauses authored work relying
on that workspace grant. Separately valid native personal/local entitlements remain effective;
reading, export, permitted deletion, backup/recovery and security updates stay available.
A child with a valid household grant does not need a separate purchase or personal trial.
Store compliance and actual cross-store acceptance still require qualification.

The separately opted-in **minimal Majestic push bridge** holds developer push credentials and
routes opaque update hints. It receives device tokens and necessary routing/IP/timing metadata,
with documented retention/abuse limits, but no names, records, proofs, commands or keys. Household
installers never contain APNs/FCM developer credentials. Generic notifications expose no child/task
content. Push is optional, best effort and never the durable sync channel; missed/disabled hints
are repaired by direct catch-up over the owner's reachable private network.
[Apple background-delivery guidance](https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app),
[FCM encryption guidance](https://firebase.google.com/docs/cloud-messaging/encryption).

The metadata-only verifier has undeployed source and injected-vendor tests; production store
attribution, credentials and operations remain unqualified. The push bridge is not implemented.
Both require privacy review, operating budgets and separate deployment authorization. Keep them outside today's default mobile dependency graph. No hosted
record service or Majestic app account is introduced by this design.

## Adoption roadmap and evidence

The [template guidance](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/USER_OWNED_HOSTING.md)
links the four detailed contracts. The optional reference now exports packages/APIs and a separate
reference generator; see its [runbook](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/dev/docs/HOSTING_REFERENCE_RUNBOOK.md)
and implementation report. Core consumer pins remain intact. The three optional modules are published together at
the full immutable revision approved in `STACK_STANDARD.json`, registered as an explicit capability and adopted
by Skepbook, Pantry Clock, Paws and Daymerit. All use the maintained scope engine for native lifecycle, pairing,
membership, journaled mutations and rollback-safe recovery. Its former pilot is a thin harness over the regular implementation. Policy rejects
mutable refs, unapproved consumers, source overrides and mismatched harness dependencies.
A source commit, passing unit test or simulator build does not qualify signed service installation,
physical devices, live-store grants or product migrations.

Daymerit additionally composes a shared multi-scope workspace session: one parent group and
independent child/proof groups, with signed global principal allocations and four adult seats
excluding children. Typed commands preserve confirmed-only financial decisions; selected source
staging, interrupted enrollment and authenticated disconnected family recovery retain durable
boundaries. Product/native/server tests use real TLS, MLS and the ciphertext daemon. Its implementation
does not qualify signed desktop service packaging or production licensing operations.

| Phase / status | Products | Scope / remaining work |
| --- | --- | --- |
| Reference source implemented; operational qualification pending | App-Template generated clients and desktop services | Local coordinator, atomic storage/MLS, role-separated TLS, grant and generated-client tests exist. Complete source-bound release evidence, signed service/credential lifecycle and physical-device qualification. |
| First pilot adopted in regular build | Pantry Clock | Shared household inventory, staged snapshot migration, exact quantity/deletion/conflict semantics and preserved legacy backups; operational/device/store qualification remains pending. |
| Implemented development adoption | Skepbook; Daymerit; Paws | Skepbook selected typed apiaries and field logs with one common workspace roster; Daymerit isolated parent/child/proof data, household grants and confirmed ledger rules; Paws distinct pet/care events. Production operational/device/store qualification remains pending. |
| Later | Ridelore; Fine Notes | Selected vehicle binders and tasting collections; preserve relationships, attachment access and authorship. |
| Selective | Namefold | Private native-wallet sync only. Public profiles/links and the browser-local PWA remain separate architecture/consent decisions. |
| Later own-device adoption | Turnstamp | After reference-client/Pantry Clock qualification, sync selected property/job collections among the solo cleaner's own approved devices. Preserve original photographs, report versions and complaint/re-clean links; review concurrent edits and deletion conflicts. Explicitly enroll the trusted coordinator for selected plaintext access while keeping the storage daemon ciphertext-only. No helpers, client accounts/portals or hosted client report links; no first-release prerequisite or new pricing. |
| Inherit when built | Future concepts | Adopt only when workflows benefit; sharing/accounts are not mandatory template features. |
| Separate feasibility | Kinwall | Hosting conveys legitimately obtained records; it cannot grant iPhone Messages/call-history access. No new release slot or implementation claim. |

These are hosting implementation/qualification phases, separate from public release positions. The `wolfe-server-*`
repositories remain company operational references, not the customer desktop kit. No repository
creation/rename/merge, service restoration, application migration or new launch dependency follows.

Turnstamp's approved [product scope](https://github.com/MAJESTIC-MADE-LLC/Turnstamp/blob/main/docs/ENHANCEMENTS.md)
and [own-device design](https://github.com/MAJESTIC-MADE-LLC/Turnstamp/blob/main/docs/USER_OWNED_HOSTING.md)
remain concept requirements at public release position 8. Its product hosting notes predate the
trusted-coordinator refinement: the latest shared contracts govern implementation, and
“ciphertext-only” applies to the storage daemon rather than the entire enrolled desktop computer.
Report export selections do not determine sync scope; enrollment must separately disclose original
photos/private notes and coordinator access. Hosting does not turn the solo offer into a team tier
or change its approved $9.99/month or $79.99/year base price.

For each deliberate adoption and before releasing hosting, record source-bound evidence for the contracts:

- Source-built reference interoperability and release artifacts on both mobile platforms; independent
  database/attachment encryption, DTO disclosure checks and existing archive/ID/key compatibility.
- Crash injection across projection/outbox/inbox/ratchet transactions; duplicates, reorder, storage
  pressure, attachment interruption, offline quantity conflicts and no shared double spend.
- Malicious/rolled-back daemon, publication-versus-revocation races, stale permits, coordinator
  quarantine/recovery, old backups, retired devices, checkpoint compaction and no deleted-data resurrection.
- Signed Mac/Windows setup, background operation, key isolation, logout/reboot/disk unlock, TLS
  expiry/rotation, LAN denial/revocation, VPN outage, signed updates and incompatible downgrade.
- Owner/member cross-store access, limits, refund/expiry/outage/clock handling, content-free metadata
  services and recovery/export without any paid grant or host.

Local source tests now cover real TLS/MLS/storage traffic, atomic quantities/migration, grant
rejection and disconnected recovery in the reference, Skepbook, Pantry Clock, Paws and Daymerit. Daymerit
adds isolated parent/child/proof scopes, confirmed financial effects, proof deletion and bounded
encrypted family recovery; its [November 5 evidence](https://github.com/MAJESTIC-MADE-LLC/Daymerit/blob/dev/docs/validation/2026-11-05/hosting-family/RESULTS.md)
records published-source app/network checks and native builds. Paws also covers
real two-device care-event exchange, genuine first-owner selected-source publication and parent
deletion races while preserving private SQLite bytes/keys. Regular native-build evidence is
recorded separately from earlier foundation/pilot evidence. Signed services, live
store attribution and physical-device qualification are still pending; local fixtures do not
qualify those operational boundaries. Physical-device, native-store and individual product approvals remain required.

## Native hosting and private deletion — November 6, 2026

Skepbook now composes the maintained hosting engine with its typed apiary, hive,
field-log, reminder and photo models on an independent encrypted executor. One
owner-approved workspace roster covers every explicitly selected apiary; the
three-person cap includes the owner. The separately approved coordinator can read
shared data. Sensitive location/access/free-text/revenue fields and individual
photos require explicit selection. Private drafts, keys and recovery stay separate.

Daymerit provides active-parent private deletion even after paid access expires.
Selected records, child activity and all-record deletion have explicit confirmation;
linked content and the raw legacy import are removed together. Minimal redacted
ledger amounts preserve surviving balances. Local proof/thumbnail and retired-copy
cleanup has a durable retry marker. Existing exports, old backups and hosted copies
cannot be recalled; authenticated restoration of an older backup can reintroduce
its contents. This makes no forensic-erasure claim.

See the [current software dossier](validation/2026-11-06/host-packaging/RESULTS.md).
Signed services and remaining OS lifecycle acceptance, production licensing, physical
privacy checks and real native-store acceptance remain separate. Release order,
pricing and the website publication pause remain unchanged.

## Host packaging and credential qualification

Desktop packaging and protected Windows credential provisioning are implemented and locally component-tested. The [current qualification dossier](https://github.com/MAJESTIC-MADE-LLC/.github/blob/dev/portfolio/validation/2026-11-06/host-packaging/RESULTS.md) separates passed engineering/component checks from publisher signing, actual Mac daemon/approval, interactive Windows owner IPC, logout/reboot, production licensing and physical/store acceptance. Earlier dated evidence retains its original scope. No website was published.
