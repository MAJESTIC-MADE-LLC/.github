# Baseline preservation audit — 2026-11-03

Compared the 26 local repositories with the recorded `majestic-foundation-20261103-baseline` working-copy snapshot. All 26 remain on `dev`; every current `HEAD` and local `dev` reference equals its recorded baseline commit.

All **265 files removed from their original baseline paths have an exact SHA-256 match in the current repository archives**. This includes **109 originally dirty files**: files whose recorded working-copy bytes differed from their baseline commit, or which did not exist in that commit. No preservation exceptions remain.

| Repository with relocated baseline files | Exact copies retained | Originally dirty |
| --- | ---: | ---: |
| App-Template | 42 | 0 |
| Daymerit | 153 | 69 |
| Fine-Notes | 3 | 0 |
| Namefold | 34 | 21 |
| Pantry-Clock | 3 | 0 |
| Paws | 3 | 0 |
| Ridelore | 27 | 19 |
| **Total** | **265** | **109** |

The audit checked every baseline path for removal, compared removed files with existing tracked and untracked archive copies using SHA-256, and compared each removed file with its recorded commit to distinguish preexisting working-copy changes. Two initially missing Namefold working-copy files were copied exactly from the saved baseline into `legacy/native-cloud-2026-11-03` before the final clean audit.

The [machine-readable evidence](preservation-audit.json) records all 26 baseline/current commits and the original/archive paths and hashes for relocated files. It contains no user records or credentials.

This verifies file retention and branch/commit continuity. It does not validate runtime equivalence or claim that modified active files are byte-identical to the baseline. This audit performed no commits or pushes.
