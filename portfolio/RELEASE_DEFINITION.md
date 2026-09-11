# Majestic Made Release Definition

A product counts toward the seven-product launch gate only when every required item below is
recorded as passing for a release candidate on `dev`. A README, mockup, waitlist page, simulator-only
demo, or unverified feature claim does not count as complete.

## Product and Experience

- The promised primary workflow works end to end on every launch platform.
- Empty, loading, offline, denied-permission, error, restore, and destructive-action states work.
- Accessibility labels, text scaling, keyboard/focus behavior where applicable, and contrast pass.
- A founder completes and records a clean-device physical-device acceptance run.

## Data, Privacy, and Security

- The product's local, optional-cloud, or required-cloud model is stated in plain language.
- Data inventory, data-flow diagram, retention, export, deletion, and backup/restore are verified.
- Client builds contain no server secrets; authentication and server authorization fail closed.
- A repository security review has no unresolved critical or high-severity finding.
- Store privacy/data-safety answers and website claims match the release build exactly.

## Quality and Operations

- Formatting, static analysis, tests, release build, and dependency audit pass in CI.
- Crash recovery, upgrade/migration, backup restore, and rollback or feature-disable paths pass.
- Support can reproduce the build and has a monitored support address and troubleshooting runbook.
- Required monitoring is privacy-minimized; cost and reliability alerts are configured for cloud use.

## Commercial and Legal

- Store products, trial/renewal language, restore purchase, cancellation, and entitlement loss pass.
- Privacy policy, terms, and support pages describe actual behavior and have launch approval.
- Per-user unit economics include store fees, hosting, storage, egress, email, support, and taxes.
- Pricing leaves an approved margin at expected use and at the documented high-usage limit.

## Portfolio Launch Gate

- Seven products independently satisfy this definition.
- Shared website and legal pages describe the same seven release candidates accurately.
- Signing, store, domain, payment, email, backup, incident, and rollback owners are assigned.
- Products may enter private internal testing before this gate; no public product deployment occurs
  until both founders record launch approval.
