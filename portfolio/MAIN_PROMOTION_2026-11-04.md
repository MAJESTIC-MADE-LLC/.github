# Main promotion and repository metadata — November 4, 2026

The owner authorized promotion of reviewed portfolio work to `main`, plus accurate READMEs, GitHub
descriptions and naming. All 26 included repositories were reviewed. Dossier and OffRecord remain
excluded; their names and descriptions were left unchanged.

## Result

- Reviewed source is promoted directly to `main`, with `dev` synchronized to the same commit.
  Local checkouts return to `dev`. Pushes update both branches atomically without force or pull requests.
- All 26 GitHub descriptions match current product/supporting roles. The 28 technical names match
  canonical inventory and are retained; README headings clarify the branded products.
- Twenty-three repositories needed README commits. Corrections distinguish implemented local apps,
  concept/research plans, retained marketing/legal drafts, and retired/deferred server roles.
- Namefold managed links and Lockbox timed delivery remain deferred. What We Own combines planned
  home/moving requirements; Claim Crate and Steward retain their repositories. Kinwall has no release slot.
- Immutable shared source remains `d2895cba9ac5bc121369a409fb1e528071a98a2d`. No runtime,
  schema, key namespace, backup reader, entitlement or pricing changed in this review.

The [promotion record](validation/2026-11-04/main-promotion/promotion-results.json) contains verified
branch pairs for the other 25 repositories; the containing governance commit defines its own SHA.
Final remote verification for all 26 is retained at
`/tmp/majestic-main-promotion-20261104/final-status.json` in the shared workspace.
[Metadata review](validation/2026-11-04/main-promotion/metadata-review.json) and
[README commits](validation/2026-11-04/main-promotion/readme-commits.json) retain exact changes.

## Validation and boundaries

The 69 governance tests, 28-repository portfolio check, eight-consumer foundation software/source
checks, ten concept validators and legal-page validator pass. All checked relative README links
resolve. CI-only upstream ancestry is preserved; all 24 source workflows remain main-only.
Some clones previously fetched only `dev`; their fetch configuration now also includes `main`,
so local tracking reflects both remote branches. Lockbox and Steward now also have remote `dev`
branches and canonical metadata uses `dev` consistently.

[Local check records](validation/2026-11-04/main-promotion/governance-tests.log),
[foundation result](validation/2026-11-04/main-promotion/foundation-check.json),
[link check](validation/2026-11-04/main-promotion/readme-links.json), and
[workflow review](validation/2026-11-04/main-promotion/workflow-policy.json) preserve scope.
Existing 698 app tests, 90 shared-package tests and both-platform build evidence remain valid;
README/metadata edits do not change those software inputs. No redundant native builds were required.

Main pushes may run existing validation workflows; none performs website publication, store upload
or infrastructure activation. Paused web repositories have GitHub Pages disabled, no repository
webhooks, and no linked Majestic Cloudflare Pages Git project in the checked account. No provider
settings, live records, deployments or stores were changed. The website pause remains.

Hosted Actions are optional. Mobile workflows currently lack cross-repository read credential setup
for the private App-Template dependency, so hosted resolution may fail even when authenticated local
checks pass. No credential provisioning or manual CI reruns were performed. A hosted run snapshot is
an observation, not a passed build record.

Four representative physical-device/privacy and actual native-store checks remain pending.
Promotion records accepted source, not public app release approval. Product QA and the exact
17-product release order are unchanged, starting with Skepbook.
