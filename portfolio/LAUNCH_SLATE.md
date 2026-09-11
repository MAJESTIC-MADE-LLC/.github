# Seven-Product Launch Slate

Locked on September 11, 2026. Changing the slate requires both founders to record the reason,
replacement, cost impact, and schedule impact.

| Order | Product | Current evidence | Next release milestone | Main concern |
| --- | --- | --- | --- | --- |
| 1 | Apiary | Full Flutter implementation, automated tests, iOS simulator build | Physical iPhone QA, purchase sandbox, store/legal assets | Local trial can reset on reinstall; acceptable only if documented |
| 2 | ReachMe | Flutter app and Cloudflare web/PWA implementation | Physical iPhone QA and hosted-link abuse/recovery test | Published fields are public; D1 retention and recovery must stay reliable |
| 3 | RideBinder | Substantial local-first app and optional cloud backend | Finish release checklist with cloud flag off first | Cloud sync, document storage, and AI fallback greatly expand cost/risk |
| 4 | RoutineCue | Substantial Flutter/Supabase implementation and test suite | Production-like backend, deletion, notifications, and family-device QA | Child data, photo proof, and required cloud operations are high trust |
| 5 | Paws | Product specification only | Build offline-first iPhone MVP from shared template | Pet health copy must not become medical advice |
| 6 | Almanac | Product specification only | Build offline-first notebook without remote valuation in v1 | Remote valuation would add cost and collection privacy questions |
| 7 | Use By | Product specification only | Build single-device offline inventory before partner sync | Barcode/vision coverage and multi-device sync can expand scope quickly |

## Recommended Execution

1. Finish Apiary and ReachMe physical-device, purchase, legal, and store gates.
2. Ship a local-only RideBinder release candidate before enabling paid cloud modules.
3. Validate RoutineCue against a production-like backend with synthetic family data.
4. Build Paws, Almanac, and Use By on the offline-first template, one at a time.
5. Keep Chat Armor in research and keep all non-slate concepts out of the critical path.

The slate optimizes for reuse and low operations cost. It is a planning decision, not a statement
that any product is currently available.
