# OpenTelemetry Collector #16236 — R7 Legacy fail-closed engineering

**Mission:** `AXG-OTEL-16236-R7-LEGACY-ENGINEERING-20261114`  
**Engineering verdict:** **`R7_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`**  
**Full original upstream package acceptance:** **REVISE / BLOCKED**  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), Draft/unmerged. No new project, no upstream submission, no merge.

## Source of truth and exact identities

- Upstream `open-telemetry/opentelemetry-collector` baseline exact HEAD: `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`. Original persistent queue file SHA-256: `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- **Before fix source HEAD:** `7c15dd3bdcfc9c6bd76efee9a65e1ffc830b78b8`, candidate SHA-256 `52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446`.
- **First attempted amended source HEAD:** `afb6346de405233c4d5f934cd1350a58550310d0`, compile **FAIL** `undefined: err` in `loadLegacyMetadata`; corrected the variable declaration scope only, no test expectations changed. See [failed Actions run #43538804092](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538804092).
- **Successful amended code execution HEAD:** `1188a18cb42dc3938337e2bd7ee06a0680224360`, source SHA-256 **`4b362e244ec5365ee6bfd5e5499bcba4be03078339fc3733943e2c8f71060d93`**. Later reporting and raw-evidence commits do not by themselves qualify a later HEAD.
- Added [R7 Contrib fault-injection / legacy matrix](axg_legacy_fail_closed_test.go), SHA-256 `363c77238fc49c7148a4b575521a3ccaca4b13beaa979f5ae8e6f54023f87305`. The original **independently authored** [AETHER TEST ARCHITECT R6 regression](../r6/axg_ta_r6_independent_requalification_test.go), SHA-256 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`, was **re-executed without changing its file**.
- Runtime: Ubuntu 24.04, Go 1.26.0, actual Contrib `file_storage v0.165.0` extension with bbolt v1.5.0; isolated temporary persistent files. No production resources.

## Material flaw and narrow remediation

The independent Test Architect R6 finding established that malformed *legacy* read-index metadata (example two-byte `ri`) was silently interpreted as a fresh queue, which allowed cleanup of the corrupted marker while leaving request 11 only physically stored, not logically reachable.

The R7 [experimental candidate](../r2/persistent_queue_candidate.go) now:
- Treats both legacy `ri` and `wi` absent as potentially fresh, but rejects existing nonempty legacy `di` without indices.
- Rejects partially missing, malformed/non-exactly-eight-byte, or logically impossible `ri/wi` combinations **before any metadata migration, deletion or payload reindex**.
- Returns a concrete error instead of silently resetting indices, preserving old metadata bytes and physical request keys for later operator diagnosis.
- Preserves the existing valid Legacy migration and genuinely empty queue behavior.

This does **not** certify recovery when `ri/wi/di` and `qmv0` are all absent but orphaned numeric payloads remain, nor recovery from arbitrary plausible-but-wrong metadata, non-atomic storage backends or genuine power loss.

## Actual RED → GREEN evidence

| Executed test | Before-fix R7 | After-fix R7 |
| --- | --- | --- |
| Existing R5/R6 focused queue + actual Contrib extension | PASS, exit 0 | PASS, exit 0 |
| Six legacy-malformed cases with actual Contrib `file_storage` (bad read/write, half-missing, read>write, trailing garbage) | FAIL, exit 1 | **6/6 PASS**, exit 0 |
| New clean queue + intact legacy migration controls | PASS | PASS |
| Orphan legacy dispatched marker without indices | FAIL | **PASS** |
| Original AETHER TEST ARCHITECT independent legacy negative test, **unchanged** | FAIL, exit 1, original defect reproduced | **PASS, exit 0**, no original `ri` deletion, request 11 remains |
| Entire **unmodified** upstream queue package | **FAIL**, exit 1 | **FAIL**, exit 1 |

Actual runner: [before-fix run #43538751874](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538751874), job `132274052417`, classifier `R7_EXPECTED_LEGACY_RED`. Successful amended runner: [after-fix run #43538951873](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538951873), job `132274706426`, classifier `R7_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`.

The **only** old upstream failing *leaf* cases after the fix remain `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` (plus parent), which explicitly expect old reset-to-empty behavior on corrupted `qmv0`. **Do not classify the original suite as PASS or silently update those tests.** Maintainers have **not** approved the fail-closed policy as their new API/test contract.

## Evidence durability and limitations

[Mutually linked R7 evidence index](evidence/EVIDENCE_INDEX.md) includes:
- Complete original GitHub Actions runner stdout/stderr for the before-fix RED, the intermediate compile failure, and the final R7 GREEN, **all permanently committed**.
- Original RED + GREEN machine-readable `result.json` and **original SHA-256 `SHA256SUMS.txt`** manifests committed **byte-for-byte**; verified matching original git blob hashes.
- Original RED 20-file ZIP artifact (SHA-256 `38128930b45a79643985d251715618374b2c30b6b064720c57f424f2b245ffca`) and GREEN 20-file ZIP artifact (SHA-256 `9ac0b34c0c4f3179bf89c05766e78d2d078f86beccdc0231b3ce175540a8686c`). Both were actually downloaded, extracted, and validated against their original **19/19 SHA-256 entries** with zero mismatches.
- Entire original per-command log files remain in the expiring original artifact. The full GitHub Actions runner logs, exact classified results and original integrity manifests are durably committed; **not all 20 individual original archive files have been committed**.

**Important gate:** R7 engineering tests use a previously independent R6 regression, but **R7 has NOT received an independent AETHER TEST ARCHITECT requalification on its new HEAD**, nor any upstream maintainer decision. No actual ENOSPC, full distribution, power-failure or exactly-once external exporter guarantee has been proven.

**Decision:** maintain internal PR #22 in Draft/unmerged and external publication blocked. The pending next independent gate should challenge the amended exact source; the separate upstream `qmv0` contract must be resolved with actual maintainers. No public PR/comment is authorized by this document.
