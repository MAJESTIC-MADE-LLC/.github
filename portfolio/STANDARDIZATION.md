# Keeping implemented applications aligned

The canonical versions and package sources live in `STACK_STANDARD.json`; capability applicability
lives in `CAPABILITY_MATRIX.json`. `STANDARDIZATION.json` registers active manifests, exact dependency
declaration/lock fingerprints, Node projects. Steward’s former marketing application is archived; its buildless transition surface
has no active Node manifest or exception. This registry does
not qualify a release. The foundation's pending device/store/source-evidence gates remain unchanged.

## Local enforcement

Use Python 3.11+ and the approved Flutter SDK. Resolve each app's pinned packages before the first
check; ordinary private Git credentials are required. From the Majestic workspace:

```sh
python3 .github/scripts/check_standardization.py
python3 .github/scripts/install_standardization_hooks.py
```

The installer sets repository-local `core.hooksPath` to the governance repository's tracked hooks
in all 25 registered local repositories. It never changes global Git configuration or overwrites
custom hooks. Repeat it after moving/recloning the workspace or adding a repository. Keep the
governance checkout beside the products. A missing checker fails the hooks instead of passing.

Both pre-commit and pre-push run the complete offline portfolio drift check. It checks:

- All seven native apps plus the template, exact SDK/core/platform dependencies, real shared-package
  imports, encrypted SQLite selection, immutable Git resolution/cache bytes and capability declarations.
- Every registered active Dart/Node dependency declaration and resolved lockfile. New manifests,
  removed registered manifests and unregistered apps fail; archives and generated build trees are excluded.
- Common web framework versions, exact Node engines/version files, strict npm engines and deployment
  Node settings. Product-specific tooling such as TypeScript can have a deliberate registered profile.
- Optional hosting's common SDK/dependency agreement, Rust pins, complete manifest coverage,
  reference paths, verifier engine and isolation from the default consumer graph.
- Every active workflow's main-only triggers, job guards, minimal permissions, immutable actions
  and checkout restrictions. This creates no CI trigger, remote run or paid dependency.

Hooks also check the index/pushed tip against the checked worktree for governed configuration,
native permission inputs and shared-import changes. Stage complete changes to these files, then
use plain `git commit`; alternate-index commit modes are rejected. Ordinary unrelated product edits
can remain unstaged for logical commits. Before pushing dependent repositories, commit the reviewed
governance inputs first; an uncommitted policy cannot approve a dependency push.

Local hooks are cooperative safeguards: Git's explicit bypass switches and direct remote edits can
bypass them. Install on each workstation. Existing GitHub Free remote-protection limitations remain
accepted; no remote protection, publication or deployment is claimed.

## Deliberate updates

1. Work on `dev`. Before changing a dependency, capability, toolchain or platform contract, inspect
   the canonical policy and the affected products. Keep product databases, keys, branding and
   permissions separate. Reuse maintained foundation modules for common behavior.
2. Change the canonical version/capability entries and all applicable consumers together. Keep
   shared Git dependencies on a full immutable commit. New optional hosting capabilities remain
   separate until deliberately adopted; an implementation change alone does not enable them.
3. Review declaration and lockfile diffs. Print candidate fingerprints with
   `python3 .github/scripts/check_standardization.py --print-dependency-baseline`, then update only
   the reviewed entries in `STANDARDIZATION.json`. The command prints candidates; it never writes
   approval or evidence. Register new products/manifests and run the hook installer for new repos.
4. Run affected app/package tests and builds, then the complete portfolio guard and governance tests.
   Save actual validation separately. Never change an old source fingerprint or result to make a gate pass.
5. Commit logical changes on `dev` only when requested. Push/promote to `main` only when explicitly
   requested. No pull request, service installation, store setup or deployment follows from this process.

Maintained shared implementation can develop ahead of consumer pins: this local guard verifies the
published provider Git tree and actual consumer cache, without requiring the provider worktree's
implementation to remain frozen at the old pin. Dependency/configuration drift is still rejected.
`check_foundation.py --release-gate` retains strict provider-source and source-bound evidence checks.
After publishing a new reviewed foundation revision, deliberately migrate/resolve/validate its consumers.

## Current baseline

Flutter 3.47.8 / Dart 3.13.7 and the existing immutable foundation commit remain unchanged. Active
Node projects use 26.13.0, the latest LTS entry verified November 4 against the
[official Node release index](https://nodejs.org/dist/index.json). Hub and Namefold web use Next
16.4.3 and React/React DOM 19.3.1. Steward’s active marketing is consolidated into Hub; its old Next.js source is an archive. Company server Docker
scaffolding is separate operational material, not the consumer hosting/runtime template.

Passing software alignment does not complete physical-device/store acceptance, current foundation
evidence or signed installers. Pantry Clock, Paws and Daymerit have explicit
pre-launch integrations; their operational qualification remains separate.

## Optional hosting pilot and explicit adoption

`Pantry-Clock/hosting_pilot` began as the registered development composition and is now a thin
harness over Pantry Clock's regular implementation. The app and harness, Paws and Daymerit resolve
the complete optional module set from published Git
`f74c7e709730b75e073a01bfcb7ef07100819a79`. The core pins remain unchanged.

`hostingPolicy` requires the complete package set, explicit `user_owned_hosting` capability,
approved consumer identity, exact transitive pins, native LAN permission/disclosure and verified
Git/cache provenance. The harness may use only its registered parent app as a local source and
must agree with its parent's optional sources. Overrides and moving refs fail. Earlier local-source
pilot evidence retains its original scope and does not qualify later published artifacts.

Four reviewed dependency baselines advanced together: Pantry regular app, its harness, Paws and
Daymerit. Native iOS linker inputs are covered by staged-input guards; native binaries and generated
provenance remain ignored. Later products adopt deliberately. Signed service, live licensing,
physical-device/store and current foundation evidence gates remain separate.

## Shared session adoption

The three optional modules resolve together from the full immutable Git revision approved in
`STACK_STANDARD.json`. Pantry Clock, Paws and Daymerit are approved consumers.
Pantry Clock and Paws delegate generic native hosting orchestration to `HostingSessionEngine`; typed product
models, selected-source adapters and portable archive schemas remain app-owned. Pantry's legacy
hosting namespace, selectors and proposal format remain compatible. Paws has an independent scope
and preserves private database, key and legacy backup identities.

Daymerit composes `HostingWorkspaceSessionEngine` over the same maintained scope engine. Its
owner-signed global allocation, isolated parent/child/proof groups and recoverable enrollment/source
staging belong to the shared foundation; product rules and native consent remain app-owned.
Four reviewed dependency baselines advance together: Pantry regular app, its thin harness, Paws
and Daymerit. Only optional sources advance; core/report/media/reminder modules retain their original immutable pins. All
other products retain their current graph. Production qualification evidence remains separate.

## Validation efficiency — November 5, 2026

Standalone foundation checks and the portfolio guard now use the same workflow-policy parser.
The portfolio pass checks each workflow once while retaining each native consumer’s exact Flutter
CI pin check. Git object integrity checks are shared only within one invocation for each repository
and immutable revision; package files, modes and extra source are still inspected on every use.
Nothing is cached across invocations, and release qualification remains independent.
