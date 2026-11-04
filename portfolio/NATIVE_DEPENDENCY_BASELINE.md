# Native dependency compatibility baseline — 2026-11-03

The same facade version previously resolved different native implementations from older app lockfiles. Foundation qualification must identify the implementation actually built; facade pins alone are insufficient. The selected exact versions are in `STACK_STANDARD.json` under `resolvedPlatformDependencies`, enforced only where present.

| Implementation | Earlier resolved variants | Approved baseline | Reason |
|---|---|---|---|
| `local_auth_android` | 2.0.10 / 2.3.0 | 2.3.0 | Common Kotlin/suspend implementation compatible with Flutter 3.47.8 |
| `local_auth_darwin` | 2.0.4 / 2.0.5 | 2.0.5 | Swift 6 actor/lifecycle fixes |
| `flutter_secure_storage_darwin` | 0.4.2 / 0.4.3 | 0.4.3 | Finds existing keys across accessibility levels |
| `flutter_secure_storage_platform_interface` | 2.1.0 / 2.1.1 | 2.1.1 | Avoids false pending-namespace data-loss reports |
| `in_app_purchase_storekit` | 0.4.13 / 0.4.16 | 0.4.16 | Current entitlement API and fixes since the older lock |
| `path_provider_android` | 2.2.23 / 2.3.1 | 2.3.1 | Consistent JNI implementation, including release-mode PathUtils fix |
| `native_toolchain_c` | 0.19.4 / 0.19.5 | 0.19.5 | Consistent native-asset compiler tooling; arm64e support |
| `android_file_picker` | 2.0.0 / 2.1.3 | 2.1.3 | Pending-picker, result-code and save SecurityException fixes |
| `jni` / `jni_flutter` | 1.0.3 / newer | 1.1.1 / 1.0.4+1 | Consistent JNI implementation, including suspend ProGuard rules |
| `image_picker_android` / `image_picker_ios` | +23 / +25; +7 / +14 | 0.8.13+25 / 0.8.13+14 | Bounded Android image decode and iOS 15/Swift picker implementation |
| `file_picker_darwin` | 2.0.0 / 2.4.2 | 2.4.2 | Picker cancellation/concurrency, duplicate temporary files and save-state fixes |
| `file_picker_platform_interface` | 4.0.0 / 4.2.0 | 4.2.0 | Matches selected Darwin options/interface |
| `file_picker_web` | 4.0.0 / 4.2.0 | 4.2.0 | Same resolved family where included by the facade |
| `file_picker_linux` | 2.0.0 / 2.0.3 | 2.0.3 | Same resolved family where included by the facade |

The first four are pinned by `majestic_privacy`, StoreKit by `majestic_purchases`, and Android path/native tooling by `majestic_storage`. Root `dependency_overrides` select file-picker variants only in apps/template that use `file_picker`, and image-picker drivers only where `image_picker` already applies. The QR module already uses `image_picker` and pins those same drivers. The media sanitizer remains a pure image-processing package; a file-only sanitizer does not acquire a photo-picker feature. Paws and Pantry Clock retain their existing official `file_selector` adapter, now exact 1.1.0; no second picker is imposed. Desktop/web packages appearing in federated lockfiles do not imply those platforms are release targets. iOS and Android remain the first release platforms.

Publisher changelogs/pubspec constraints were inspected in the locally resolved pub cache before selection. Public primary references: [local_auth_android](https://pub.dev/packages/local_auth_android/changelog), [local_auth_darwin](https://pub.dev/packages/local_auth_darwin/changelog), [secure storage Darwin](https://pub.dev/packages/flutter_secure_storage_darwin/changelog), [secure storage interface](https://pub.dev/packages/flutter_secure_storage_platform_interface/changelog), [StoreKit](https://pub.dev/packages/in_app_purchase_storekit/changelog), [path provider Android](https://pub.dev/packages/path_provider_android/changelog), [native compiler tooling](https://pub.dev/packages/native_toolchain_c/changelog), [Darwin picker](https://pub.dev/packages/file_picker_darwin/changelog).

The final SDK/build baseline is Flutter 3.47.8 / Dart 3.13.7 and AGP 9.1.0 / KGP 2.4.0 / Gradle 9.3.1 / JVM 17. This supersedes the earlier installed-SDK and mixed Android-toolchain choices, following the publisher TLS patch and official Flutter matrix. Dated earlier test/build reports remain historical.

App-specific capability adapters such as preferences, URL launchers and package-info integration may have differing resolved versions where the common baseline does not prescribe them. They remain product-owned adapters, not reasons to add unrelated features to other apps. Complete the one final eight-consumer dependency-diff audit and then freeze this platform baseline; further updates require a concrete failure or new evidence.

Consumer resolution and validation are separate. A selected version or successful `pub get` does not prove device behavior. Native builds and representative privacy/store evidence predating this baseline must be treated as earlier evidence; rerun applicable checks after the final source/dependency freeze. Physical device and store qualification remain pending until explicitly recorded.

## Final resolution audit

The [eight-consumer audit](dependency_audits/2026-11-03.json) records the verified patched SDK revisions and all 220 resolved packages. Every prescribed baseline version matched after all eight `pub get` runs. The 32 remaining version differences are outside the prescribed shared baseline: developer/code-generation transitives, standalone UI-package transitives, optional adapter interfaces, product-specific preferences/launchers/package information and desktop implementations. They are recorded explicitly rather than hidden by a blanket “all dependencies identical” claim. The dependency baseline is frozen; qualification builds/device/store tests remain separate.
