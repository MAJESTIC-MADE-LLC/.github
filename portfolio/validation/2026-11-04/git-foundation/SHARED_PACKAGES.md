# Published shared-package qualification — November 4, 2026

All eight maintained packages were fetched from App-Template at actual published commit
`d2895cba9ac5bc121369a409fb1e528071a98a2d`. Each package passed `flutter pub get --enforce-lockfile`,
`flutter analyze --no-pub` and `flutter test --no-pub` using Flutter 3.47.8 / Dart 3.13.7.

| Package | Tests |
|---|---:|
| majestic_app | 5 |
| majestic_media | 2 |
| majestic_privacy | 13 |
| majestic_purchases | 17 |
| majestic_qr | 2 |
| majestic_reminders | 1 |
| majestic_reports | 1 |
| majestic_storage | 49 |

Total: **90**. [Exact exit codes, durations and log hashes](shared/commands.json).
The clean fetched checkout retains the exact tracked package content at that commit. The checker
independently verifies the production consumers’ actual cached Git package content against the same
Git objects, source identities and provider package bytes.

Pub rejects commands run directly inside its cache. That initial rejected attempt is retained in
[its original log](shared/cache-operation-rejected.log); tests ran in the clean fetched checkout,
without changing Pub’s cached sources. This report records software checks, not physical-device
privacy or actual store transactions. Those four representative gates remain pending.
