# Portfolio standardization

- Read `portfolio/STACK_STANDARD.json`, `portfolio/CAPABILITY_MATRIX.json` and
  `portfolio/STANDARDIZATION.md` before changing shared standards or registered application dependencies.
- Run `python3 scripts/check_standardization.py --workspace-root ..` and the governance tests for
  policy/validator changes. Install tracked local hooks with `scripts/install_standardization_hooks.py`.
- Update applicable products with a deliberate canonical baseline change; do not bypass a failing
  guard, relax it for one app, or re-stamp historical evidence to claim current qualification.
- Keep local alignment checks separate from source-bound release, physical-device and real-store gates.
- Preserve dev-first work and existing main-only CI. Do not commit, push, publish, deploy or create
  a pull request unless the user's instruction authorizes that action.
