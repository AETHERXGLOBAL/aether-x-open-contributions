# AETHER X GLOBAL — AETHER TEST ARCHITECT — R7 Independent Requalification

**Mission:** `AXG-OTEL-16236-R7-INDEPENDENT-LEGACY-REQUALIFICATION-20261114`  
**Verdict:** **REVISE — independently reproduced new fail-closed defects; upstream contract still BLOCKED.**  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) (remain Draft/unmerged).  
**Exact execution-source HEAD:** `2318e42dc29e46968609ea7f82bb108e8997fd90` (subsequent evidence/report commits do **not** become tested source).  
**Original upstream Collector HEAD:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.  
**Candidate SHA-256:** `4b362e244ec5365ee6bfd5e5499bcba4be03078339fc3733943e2c8f71060d93`.  
**Unchanged R6 TA regression SHA-256:** `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.  
**Unchanged R7 engineering test SHA-256:** `363c77238fc49c7148a4b575521a3ccaca4b13beaa979f5ae8e6f54023f87305`.  
**Independent R7 fixture SHA-256:** `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`.

## New independent execution and fixed-source provenance

The separate [R7 independent GitHub Actions workflow](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/2318e42dc29e46968609ea7f82bb108e8997fd90/.github/workflows/otel-16236-r7-independent.yml) ran on **Ubuntu 24.04, Go 1.26.0**, actual published Collector Contrib `file_storage v0.165.0` with **bbolt v1.5.0**, isolated persistent bbolt files, the exact pinned upstream checkout, and unmodified previously published R5/R6/R7 fixture bytes. The only new tests are the independently authored [additive R7 tests](axg_ta_r7_independent_test.go). No product changes or upstream test changes were made.

**Completed independent run:** [Actions #43540293081](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43540293081), job `132279017927`. The GitHub job's success means the truthful classifier executed and reported **REVISE**; it does **not** mean the product or full suite passed. The initial [Actions #43540154139](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43540154139) was a **failed harness attempt**: an expected upstream exit code halted subsequent steps. The harness was corrected to capture nonzero test exits, without changing product or test expectations; the failed run remains visible.

| Actual executed suite | Captured exit | Outcome |
| --- | ---: | --- |
| Historical R5/R6 real file_storage reliability | `0` | **PASS** |
| Unchanged original R6 TA negative regression + R7 engineering controls | `0` | **PASS** |
| New independent TA R7 adversarial cases | `1` | **FAIL — defects independently reproduced** |
| Complete unchanged upstream Go queue package | `1` | **FAIL — qmv0 compatibility conflict** |

The original R6 malformed two-byte `ri` negative test passed unchanged: startup now fails closed, corrupt bytes remain, no `qmv0` is minted, and request `11` remains physically present. Previously exercised R5/R6 crash/fault/capacity scenarios were re-run and passed under the scoped suite.

## Independent adversarial observations

| Actual test | Result | Technical interpretation |
| --- | --- | --- |
| `TestAXGTAR7EmptyButPresentLegacyIndices/empty_ri` | PASS | One empty old index with other valid index rejects startup |
| `TestAXGTAR7EmptyButPresentLegacyIndices/empty_wi` | PASS | Symmetric case rejects startup |
| `TestAXGTAR7EmptyButPresentLegacyIndices/empty_both` | **FAIL** | Both legacy keys present but zero-length and an existing physical request: startup returns nil instead of refusing ambiguous state |
| `TestAXGTAR7OversizedDispatchCountFailClosed` | PASS | Untrusted impossible `di` array count rejected without allocation/rewrite |
| `TestAXGTAR7TrailingGarbageInDispatchArrayFailClosed` | **FAIL** | Valid `di` array followed by extra garbage is silently accepted instead of refusing malformed legacy metadata |
| `TestAXGTAR7OrphanNumericPayloadWithoutAnyMetadata` | **FAIL** | Physically stored request with missing `ri/wi/di/qmv0` is silently accepted as a fresh empty queue (a pre-existing acknowledged limitation, now reproduced) |
| `TestAXGTAR7RestartAfterConsolidatedMetadataBeforeLegacyCleanup` | PASS | Restart with `qmv0` plus leftover `ri/wi` retains logical and physical request `11` |

A failed test establishes the violated expected fail-closed contract on the specified fixture, not a claim of real-world exploitability or an upstream-approved intended behavior. Engineering should triage these three non-green leaf cases, including the known orphan-payload boundary, and retain the test evidence. In particular, distinguishing absent storage keys from present-but-empty keys may require an actual `storage.Walker` presence check rather than `len(Get/Batch.Value)==0`. Validate that against the published extension.

The **unchanged original upstream queue package still fails** `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` (with parent `TestPersistentQueue_CorruptedData`). These tests require historical reset-to-empty behavior for corrupt `qmv0`, contrary to candidate fail-closed policy. This **independent upstream-policy blocker is not waived or passed**; no maintainer decision is known.

## Integrity-backed persistent evidence (two-way linked)

[**Durable evidence index**](evidence/EVIDENCE_INDEX.md) and [**complete raw artifact archive**](evidence/AXG_OTEL_16236_R7_TA_INDEPENDENT_EVIDENCE.tar.xz) are committed to this **same internal PR #22**; the evidence index links back here. The archive contains all **17 raw artifact files**, including per-suite complete stdout/stderr, exit files, `result.json`, `source_hashes.sha256`, module versions, original run source HEAD, `SHA256SUMS.txt` and upstream HEAD. The original GitHub Actions ZIP is also [available while retained](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43540293081/artifacts/14091556616), but the Git-committed archive is the durable record.

- Git committed `.tar.xz` file: **6,596 bytes**, SHA-256 **`538aa8aea696528dc86397ee3d7a7e74f7385d1bdf918c75b77d988e598413da`**, Git blob **`71302e57f9348ee954a3416413e389e3680f78a4`**.
- Original Action ZIP: **10,532 bytes**, SHA-256 **`30015ff776977e80668fbea37297a503f6e11c37a89c16c2f297632dbc403f43`**.
- Original `SHA256SUMS.txt`: **16/16 internal source/output files verified**, zero mismatches. Its `result.json` is the primary machine-classified result, not the Actions green badge.
- Inspect and verify: `tar -xJf AXG_OTEL_16236_R7_TA_INDEPENDENT_EVIDENCE.tar.xz -C <empty-directory>`; then `cd <empty-directory> && sha256sum -c SHA256SUMS.txt`. Use the [pinned workflow](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/2318e42dc29e46968609ea7f82bb108e8997fd90/.github/workflows/otel-16236-r7-independent.yml) to reproduce Go commands and exact fixture setup; do not run the file against production data.

## Scope, limits, and required decision

Physical disk ENOSPC, actual power loss, non-atomic backend durability, end-to-end Collector exporter operation, and exactly-once external delivery are **NOT TESTED**. Neither this AI-operated testing nor a successful CI workflow is an independent **human** signoff. The current result does **not** authorize merge, ready-for-review, external PR, upstream communications, production deployment, or any source-policy waiver.

**Final Test Architect adjudication: `REVISE`**. Keep PR #22 **Draft/unmerged**. Engineering should address the independently reproduced fail-closed boundaries **without changing the original R6 TA regression or upstream tests**, then request a new independent execution at a precisely frozen amended HEAD. The `qmv0` contract must be resolved with legitimate upstream maintainers under separately authorized external engagement before any broad upstream acceptance claim.
