# OpenTelemetry Collector #16236 — R8 metadata-integrity engineering

**Mission:** `AXG-OTEL-16236-R8-LEGACY-ENGINEERING-20261114`  
**Engineering result:** **`R8_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`**  
**Overall upstream compatibility and merge gate:** **`REVISE / BLOCKED`**  
**Internal draft:** [PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), unmerged. This is not an independent AETHER TEST ARCHITECT R8 verdict.

## Source identity

- Upstream source: `open-telemetry/opentelemetry-collector` pinned to `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`, baseline `persistent_queue.go` SHA-256 `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- R7 candidate source before changes: SHA-256 `4b362e244ec5365ee6bfd5e5499bcba4be03078339fc3733943e2c8f71060d93`.
- **R8 code successfully executed** at exact internal HEAD `1065e0870fbc8acf9db963cd38ed90f07f13b94e`. The [candidate](../r2/persistent_queue_candidate.go) SHA-256 is **`200cb460efa44879827f9074edb911276a3ff1f7ca2f51a4d44c2f5ba844506c`**.
- [New R8 test](axg_metadata_presence_test.go) SHA-256 `8431c66f8d8745e7e13a134151f7542619c735762b91924eecbb98aed7ce28cf`.
- **Unchanged independent R7 regression fixture:** `tests/opentelemetry/16236/r7/independent/axg_ta_r7_independent_test.go` SHA-256 `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`.
- **Unchanged independent R6 regression fixture:** SHA-256 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`. Upstream tests were never patched.
- Actual runner environment: Ubuntu 24.04, Go 1.26.0, published Contrib `file_storage v0.165.0` and bbolt 1.5.0 with real persistent database files.

## Narrow R8 remediation and behavior

The R7 independent review found three fail-closed defects. R8:
1. Uses `storage.Walker` when available to distinguish absent legacy `ri/wi/di` keys from present-but-empty keys before treating a storage client as a genuinely new queue.
2. Rejects orphan numeric payload keys if there is no usable legacy index metadata rather than overwriting keys after startup. This is proven only for clients implementing `storage.Walker`, notably the actual Contrib `file_storage`. When `Walker` is unavailable the old new-store ambiguity remains possible; **no all-backend guarantee is made**.
3. Validates the encoded `di` count and payload byte length exactly **before allocation**, rejecting trailing garbage and unsupported oversized counts. A valid zero-count representation continues returning a **nil slice** to preserve the upstream API/test contract.

These checks do not certify orphan detection when plausible-but-incorrect `qmv0` or valid `ri/wi` metadata is present, nor atomicity of every possible storage backend. A `Walker` scan on the legacy fallback path has startup-cost implications that require review for large persisted stores.

## Actual RED → REVISE → GREEN execution

| Stage, exact tested HEAD | Real result | Machine verdict |
| --- | --- | --- |
| [RED #43541773685](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541773685), HEAD `25a5b10e2973a524b19013553d8237d26aa478a9` | Original 3 TA R7 adverse findings reproduced; R8 added 3 more negative cases; unchanged old original package also failed the two known qmv0 leaves | `R8_EXPECTED_RED` |
| [First amended #43541879283](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541879283), HEAD `d8d6777cf5ba12e68cc8cdd6303477f98cc02512` | TA R7 **PASS**; new R8 controls **PASS**; historical R5/R6/R7 controls **PASS**. Original package still had one **additional** unanticipated `TestItemIndexArrayMarshaling/#elements:[]` failure because of nil-vs-empty slice behavior | **`R8_REVISE`** — not passed, fixed without changing tests |
| [Final R8 GREEN #43542074773](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43542074773), HEAD `1065e0870fbc8acf9db963cd38ed90f07f13b94e` | Original TA R7 adversarial cases **PASS, exit 0**. R8 added actual Contrib tests **PASS, exit 0**. R5/R6 targeted **PASS, exit 0**. Previous R6/R7 controls **PASS, exit 0**. **Full original Go queue package still exit 1 with exactly two known qmv0 subtests + parent** | **`R8_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`** |

**The original upstream failures remain explicitly unchanged**: `TestPersistentQueue_CorruptedData/corrupted_metadata`, `.../corrupted_everything` and their parent. They expect legacy reset-to-empty startup on corrupt `qmv0`, while the experimental policy refuses startup to protect persisted data. No maintainer policy approval has been received; do **not** delete/skip/alter original tests to conceal this conflict.

## Evidence and integrity

[Mutually linked original R8 evidence index](evidence/EVIDENCE_INDEX.md) includes **all three complete original runner job logs**, original machine `result.json` and original 18-entry SHA256SUMS files, committed byte-for-byte with independently verified Git blob SHA. **All three original ZIP artifacts were downloaded and unpacked, with 18/18 SHA-256 member hashes verified in each**. The complete ZIP originals contain the full per-command Go logs; the runner job console logs are preserved in Git. ZIP artifacts expire under GitHub Actions retention; individual ZIP members are not all independently preserved as Git files.

### Hard exclusions and decision

No new independent R8 Test Architect requalification, no upstream maintainer decision, no real disk exhaustion, power-loss durability, online compaction, non-Walker backend safety, external exactly-once exporter delivery or full Collector distribution proof. These remain open research/engineering gates, not implicit PASS.

**Decision:** **keep internal PR #22 Draft and unmerged**. Send the amended fixed SHA and full RED/REVISE/GREEN evidence to AETHER TEST ARCHITECT for a fresh independent R8 run; separately obtain a human maintainer decision on the `qmv0` contract before any external publication or merge.
