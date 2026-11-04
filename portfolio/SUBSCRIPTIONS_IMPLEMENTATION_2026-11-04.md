# Subscription implementation and repository promotion — November 4, 2026

The seven implemented native apps now support the approved monthly/annual plans and a separate
14-day local trial that never starts billing. Store activation and real-store/physical-device
acceptance remain pending. Concept repositories retain approved planning prices without billing
implementations. The release queue and website publication pause are unchanged.

## Implemented native plans

| App | Monthly USD | Annual USD | Local test evidence |
| --- | ---: | ---: | --- |
| Skepbook | $2.99 | $24.99 | 265 full-suite tests; clean analysis/formatting |
| Ridelore | $2.99 | $19.99 | 325 full-suite tests; clean analysis; retained exact-source native/build evidence |
| Paws | $1.99 | $14.99 | 135 full-suite tests; clean analysis/formatting |
| Pantry Clock | $0.99 | $9.99 | 136 full-suite tests; clean analysis/formatting |
| Fine Notes | $2.99 | $19.99 | 160 full-suite tests; clean analysis/formatting |
| Namefold | $1.99 | $14.99 | 108 full-suite tests plus 2 focused final regressions; clean analysis/formatting |
| Daymerit | $2.99 | $24.99 | 130 full-suite tests plus 8 focused import regressions; clean analysis/formatting |

Annual amounts are the total billed yearly. Purchase controls use localized store-returned prices;
the table records approved US targets, not configured live inventory. Pantry Clock's possible later
$14.99 annual price is not implemented. Fine Notes covers all tasting categories; Daymerit covers
one household with no per-child charge. Namefold's free browser PWA remains separate.

The local trial starts on meaningful record use or an explicit trial action, requires no payment
details, and does not restart through plan switching or record backup recovery. Native purchases
require separate consent. No new permanent core unlock is sold; authentic verified historical
ownership remains compatible and restore-only.

Creation, editing and new-record imports require current access at mutation boundaries. Existing
records, exports and authenticated encrypted backup/recovery remain available after expiry.
Implemented deletion paths remain independent of billing. Daymerit has no record-deletion UI/API;
that remains an explicit product requirement before release, rather than a completed workflow.

Offline subscription authorization is bounded. Apple term/grace evidence additionally bounds access;
Google Play's client purchased state supplies a bounded lease rather than an invented exact annual
expiration. Unknown responses do not manufacture permanent access. Tests cover clock rollback and
malformed state, renewal/expiry, restore, revocation, unknown/pending results, duplicate-plan
preflight, persistence before native acknowledgment, and expired recovery rights.

## Validation scope

The qualified toolchain is Flutter 3.47.8 / Dart 3.13.7. The machine restarted during excessive
parallel build load; saved commits/source survived, and unfinished checks were rerun with low
concurrency and serialized native builds. Successful earlier Ridelore evidence retains its original
source scope; an earlier real-account Apple sync timeout remains unqualified.

Android release and unsigned iOS release builds pass across all seven apps. Paws, Pantry Clock,
Fine Notes and Daymerit use development certificates for Android engineering validation; Namefold
and Skepbook report unsigned Android artifacts. These are not distribution-ready signing claims.
Namefold's Simulator XCTest target compiles for arm64/x86_64; Daymerit and Skepbook compile for
arm64. Those three native targets were not executed. Ridelore's earlier native fixture/helper
results retain their stated scope and real-account timeout.

App-specific commands, source fingerprints, build signing distinctions, logs, hashes and pending
store/device checks are recorded in each app's `docs/validation/2026-11-04/subscriptions/RESULTS.md`.
Namefold's commands run from `app/`; its report lives in repository-level `docs/validation`.
Native compilation does not prove signed store transactions or physical-device behavior.

Other local checks passed: 69 governance tests, 156 Hub tests plus lint/typecheck/static build,
29 legal tests and the legal-page validator, and all nine concept validators. Changed repository
whitespace checks pass. The hosting reference has separate sync/MLS/TLS/UI/generator/verifier checks
and explicit service/store/device limits in App-Template's `docs/HOSTING_IMPLEMENTATION.md`.

## Commits and promotion

Changes are split into logical subscription runtime/tests, formatting where required, pricing and
validation documentation, portfolio/legal/catalog consolidation, preserved Skepbook field logging,
and optional hosting contract/runtime/reference/packaging groups. The already-saved hosting work
was included after its other chat was interrupted; this does not enable consumer sync or install
services. No credentials or production store products were provisioned, and no production deployment was performed.

All 23 changed repositories were committed on `dev` and promoted directly to `main`, preserving
existing upstream work. All 25 local checkouts are left clean on `dev`, matching `main`; Turnstamp
and brand-assets already matched and needed no new commit. No force push or pull request was used. Existing main-only CI may run on
main pushes; no development-branch CI or manual workflow run was introduced. Local evidence is
recorded independently of Actions billing availability.

## Required before public sale

Provision exact monthly/annual products and approved localized periods/prices. Qualify real-store
purchase, interruption, pending payment, restore, renewal, cancellation, grace/hold and refunds on
physical devices, plus offline expiry and complete data/recovery rights. Finish each app's existing
privacy, accessibility, signing and product gates, including Daymerit deletion. Keep public app and
website publication separate from source promotion.

## Repository tips

The governance row is this report’s commit; other tips identify the promoted source and evidence.

| Repository | dev/main tip | Outcome |
| --- | --- | --- |
| .github | `this report commit` | Committed and promoted |
| App-Template | `8b2ca8d` | Committed and promoted |
| Brassmark | `9c5b7f9` | Committed and promoted |
| Campsake | `b1e4af1` | Committed and promoted |
| Creelmark | `994a4a3` | Committed and promoted |
| Daymerit | `808f677` | Committed and promoted |
| Divefolio | `553dc73` | Committed and promoted |
| Fine-Notes | `ab1e440` | Committed and promoted |
| Kinwall | `bfbca9e` | Committed and promoted |
| Majestic-Made-Hub | `dd9de95` | Committed and promoted |
| Namefold | `9547ab7` | Committed and promoted |
| Object-Lore | `74cd92c` | Committed and promoted |
| Pantry-Clock | `b610cd3` | Committed and promoted |
| Paws | `e9dbb7b` | Committed and promoted |
| Ridelore | `b5d570b` | Committed and promoted |
| Skepbook | `a08152c` | Committed and promoted |
| Tender-Days | `d438943` | Committed and promoted |
| Turnstamp | `3f85372` | Already matched; no changes |
| What-We-Own | `227920d` | Committed and promoted |
| app-legal | `995148e` | Committed and promoted |
| brand-assets | `532b256` | Already matched; no changes |
| lockbox | `0235390` | Committed and promoted |
| steward | `cf17236` | Committed and promoted |
| wolfe-server-apps | `7091858` | Committed and promoted |
| wolfe-server-infra | `7354200` | Committed and promoted |
