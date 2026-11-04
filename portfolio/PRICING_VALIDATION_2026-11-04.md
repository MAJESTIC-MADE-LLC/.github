# Subscription documentation and consolidation validation

November 4, 2026. This work updates approved commercial direction and product documentation. It does not migrate native billing, configure store products, qualify a mobile release or lift the website publication pause. Existing unrelated Skepbook runtime edits were preserved.

## Changed scope

- Approved monthly/annual price pairs for all 17 queued products and provisional Kinwall match the portfolio, Hub and legal pricing matrices. Each physical app/concept has a pricing document; Quiet Arcade's plan lives in the Hub. Current app docs distinguish subscription targets from unchanged permanent adapters and pending store setup.
- New permanent core unlocks are prohibited; one-time purchases are limited to optional extras. Reading existing records, basic export, backup/recovery and deletion remain available after expiration. Genuine historical lifetime ownership remains a compatibility obligation, not a new sale.
- What We Own owns the combined home/moving/PCS/claims specification. Claim Crate was removed from independent catalogs and the active repository inventory; its seven tracked files and original Convoy README were copied with commit/checksum provenance before remote/local deletion. A complete verified Git bundle remains in the local workspace archive. See [the consolidation record](CLAIM_CRATE_CONSOLIDATION.md).
- The existing 17-position launch order is unchanged. Kinwall stays research-only; Dossier/Off Record stay excluded. Steward signup data and deployments remain untouched.

## Reproducible local checks

| Check | Result |
| --- | --- |
| `python3 scripts/portfolio_status.py --write` then `--check` in `.github` | Generated docs agree with the canonical 27-repository manifest |
| `python3 scripts/portfolio_status.py --check --workspace-root .. --verify-github MAJESTIC-MADE-LLC` | Local and GitHub inventories agree after Claim Crate deletion |
| `python3 -m unittest discover -s tests -v` in `.github` | 69 tests pass |
| Each of the nine retained concept repos' `python3 scripts/validate_concept_repo.py` | Pass; concepts remain unimplemented |
| Hub local tests, lint, typecheck and production static build on Node 24.22.1 | 156 tests / 20 files and all checks pass; final schema-only follow-up also passes typecheck/build and verifies 45 exported JSON-LD blocks contain no sales offers |
| Legal-site validator and Python tests | Validator and 29 tests pass |
| Changed repositories' `git diff --check` | Pass |
| Claim Crate source/archive SHA-256 checks and `git bundle verify` | Match captured source; bundle records complete Git history |
| Independent read-only pricing/consolidation review | All 18 price pairs match; no separate Claim Crate product or new permanent-core target |

The website tests cover the catalog consolidation and old legal aliases; archived one-time survey identifiers remain readable without appearing as new offerings. Dated foundation/device/store evidence remains unchanged. No CI was run, no documentation commit was created, and no branch was pushed.

## External operations actually completed

GitHub's repository settings confirmed successful deletion of `MAJESTIC-MADE-LLC/Claim-Crate` after owner authentication. Its clean local checkout was then removed. What We Own's repository description now reflects combined home/moving/claims scope; Skepbook's description no longer advertises permanent core sales. These metadata/deletion operations do not publish the uncommitted documentation changes.
