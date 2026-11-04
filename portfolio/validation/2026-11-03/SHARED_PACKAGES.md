# Shared-package local software qualification

Recorded 2026-11-04T14:12:56.498447+00:00. Current cohort fingerprint: `a2b53fd8ebd38f5dbc0f56348c406e590a9a04cb749a052dd206c38258da0842`.

All eight maintained packages have clean local analyzers and 90 tests passing on the patched Flutter 3.47.8 / Dart 3.13.7 toolchain. This records local analysis/unit-test execution only. It does not qualify physical iOS/Android privacy, store transactions, published immutable package revisions or public release.

| Package | Tests | Analysis artifact / SHA-256 | Test artifact / SHA-256 |
| --- | --- | --- | --- |
| majestic_app | 5 passed | [Analysis](logs/shared-app-analysis.log) / `759f7e230dc8530e95a6b330297191df8f9f2400b08e4f25fddd14a8c941fda3` | [Tests](logs/shared-app-tests.log) / `8344095ad36cda5b11a8c28c2887edba1c190d587be08c6305eb17b00fe54c61` |
| majestic_privacy | 13 passed | [Analysis](logs/shared-privacy-analysis.log) / `2a279c30b6d71a1d8e5ce38a11809b62e651c83b784fb5bb7e4878f980fef7c1` | [Tests](logs/shared-privacy-tests.log) / `3f68e92d29d5d9b433ffde6d8cab4da9547b0cd40e36b1f434ff548f24b3733f` |
| majestic_purchases | 17 passed | [Analysis](logs/shared-purchases-analysis.log) / `d7bce145aab9537af4acb9b809a1ace0856b37ea0651984dc0a219e585cbf006` | [Tests](logs/shared-purchases-tests.log) / `429742340cb2e6f2e38ea67340733852cc458e6dce24cea9e01d575557f3716c` |
| majestic_storage | 49 passed | [Analysis](logs/shared-storage-analysis.log) / `d4fa56386d99138bb03ef669069f6fa9f802b1e13e0e5a2a59b90da606644f78` | [Tests](logs/shared-storage-tests.log) / `0c11ea3016590eda5df7d71021b67fe418934c8a0e00201af905e7469095fa40` |
| majestic_media | 2 passed | [Analysis](logs/shared-media-analysis.log) / `9a3132b2001bb6a9b32eaa954d52708883dbc8c7dd9048a7818957ab0a001a6d` | [Tests](logs/shared-media-tests.log) / `2bb2bcc3f348556e766f52009f310b74d7df4173fbf461581f95ed0fb44f5b4e` |
| majestic_reports | 1 passed | [Analysis](logs/shared-reports-analysis.log) / `f138f2f1d8a7a0fe98fd5ffbe7045da3a3dfc1ec1e5abeea26f6b2c167a84eaf` | [Tests](logs/shared-reports-tests.log) / `fbfeea1868d463f8142fc3f401e0ce17a0dd207f702d68817c0e566671925f90` |
| majestic_reminders | 1 passed | [Analysis](logs/shared-reminders-analysis.log) / `e1d79a34dd53f257b7c943c67c0541d23e3ab019d061c42e341b79f67eeffcd5` | [Tests](logs/shared-reminders-tests.log) / `662b3e9e8e7b70ae4ca9eb9a92f89dedb600c2b5c0f357a0850d9d0e3000b3ed` |
| majestic_qr | 2 passed | [Analysis](logs/shared-qr-analysis.log) / `10f3f4d99c310288fdcbafb4b15a014ff36eec32c66522ad4e13e5d88d34e656` | [Tests](logs/shared-qr-tests.log) / `6acf619a4689e735da42c1b581fa1aeb89c7679c527996e3694a50d73a731d5a` |
