# Keeping implemented applications aligned

The canonical versions and package sources live in `STACK_STANDARD.json`; capability applicability
lives in `CAPABILITY_MATRIX.json`. `STANDARDIZATION.json` registers active manifests, exact dependency
declaration/lock fingerprints, Node projects and the retained Steward marketing exception. It does
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
16.4.3 and React/React DOM 19.3.1. Steward is retained legacy marketing; company server Docker
scaffolding is separate operational material, not the consumer hosting/runtime template.

Software alignment passing does not mean physical-device/store acceptance, current foundation
evidence, signed installers or self-hosting product integration has been completed.

## Registered hosting development pilots

`Pantry-Clock/hosting_pilot` is the first explicit optional-hosting development composition. Its
local Pantry/shared-source bindings and dependency/lock fingerprints are registered in
`STANDARDIZATION.json`. The guard verifies those exact paths and all overlapping production/core
versions, and rejects hosting packages leaking into the production app graph. This permits source
implementation and native engineering builds before a new shared Git revision is published. It
does not relax production provenance or release qualification, or adopt a second product.

## Explicit optional hosting adoption

Pantry Clock’s regular app and thin integration harness now resolve the three optional modules
from published Git revision `3c81cd84da760e17ec358799156e66014a2651e4`. The four core pins remain
unchanged. `hostingPolicy` requires the complete package set, explicit `user_owned_hosting`
capability, approved consumer identity, exact transitive pins, native LAN permission/disclosure
and verified Git/cache provenance. A thin harness may use only its registered parent app as a
local source and must agree with its parent’s optional sources. Overrides and moving refs fail.

Only the two reviewed Pantry dependency fingerprints were updated. Existing qualification
records were not restamped. Native iOS linker configuration is covered by staged-input guards;
native binaries and generated provenance remain ignored. Each later product adopts deliberately.

## Shared session adoption

The three optional modules now resolve together from published Git
`f5942ed7a2b318e48ec7e47ce9f46ba531e02c31`. Only Pantry Clock and Paws are approved consumers.
Both delegate generic native hosting orchestration to `HostingSessionEngine`; typed product
models, selected-source adapters and portable archive schemas remain app-owned. Pantry's legacy
hosting namespace, selectors and proposal format remain compatible. Paws has an independent scope
and preserves private database, key and legacy backup identities.

Three reviewed dependency baselines advanced: Pantry regular app, its thin harness and Paws.
Only optional sources advance; core/report modules retain their original immutable pins. All
other products retain their current graph. Production qualification evidence remains separate.
