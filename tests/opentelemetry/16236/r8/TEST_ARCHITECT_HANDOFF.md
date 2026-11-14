# AETHER TEST ARCHITECT — R8 independent metadata-integrity requalification handoff

**Mission:** `AXG-OTEL-16236-R8-INDEPENDENT-METADATA-REQUALIFICATION-20261114`  
**Repository:** `AETHERXGLOBAL/aether-x-open-contributions` · [Internal Draft PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22)  
**Exact R8 engineering execution HEAD:** `1065e0870fbc8acf9db963cd38ed90f07f13b94e`  
**Experimental candidate SHA-256:** `200cb460efa44879827f9074edb911276a3ff1f7ca2f51a4d44c2f5ba844506c`  
**Pinned upstream:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.  
**Unchanged independent TA R7 SHA-256:** `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`.  
**Unchanged independent TA R6 SHA-256:** `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.  
**New R8 engineering regression SHA-256:** `8431c66f8d8745e7e13a134151f7542619c735762b91924eecbb98aed7ce28cf`.

## Separate independent cold-start task

Verify **actual latest PR HEAD**, exact code blobs and test hashes before testing. Review the R8 source diff and rerun, independently, on real Contrib `file_storage v0.165.0` / bbolt 1.5.0, Go 1.26.0, Ubuntu:

1. Every **unchanged independent R7 adversarial test**, especially both zero-length but present legacy index keys; malformed `di` with trailing garbage; orphan numeric request with all metadata absent. Check no deletion, reindexing, new `qmv0`, or lost physical payload.
2. Existing R6 TA negative regression unchanged, existing R7 engineering matrix, R5/R6 crash and real Contrib persistence, and new R8 orphan key=1024, zero-length `di`, zero-count-plus-garbage, and legitimate initialized empty `qmv0` control.
3. Falsify R8's use of `storage.Walker`: direct storage clients without Walker support, errors returned by Walk, very large databases / unbounded startup scanning, scoped namespace collisions, and plausible-but-wrong metadata. Distinguish improvements proven for **actual `file_storage`** from nonexistent all-backend guarantees.
4. **Run the original unmodified upstream Go queue package without skips.** It still fails `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything`. Do not silently update upstream tests or falsely report original package PASS. Record full exit code and remaining failure list; maintainer-approved semantics are NOT obtained.
5. Produce a separately executed, evidence-backed `PASS_SCOPED` or `REVISE` on the exact source and test tree; include original stdout/stderr, negative findings, counts, HEAD, SHA-256 inventory and bidirectional report/evidence links within the SAME existing internal PR #22. Preserve every failure and state exclusions.

## Source evidence to challenge

- [R8 engineering report](R8_ENGINEERING_RESULT.md) ↔ [original R8 evidence index](evidence/EVIDENCE_INDEX.md).
- [Actual baseline RED #43541773685](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541773685) at HEAD `25a5b10e2973a524b19013553d8237d26aa478a9`.
- [Initial R8 code compatibility REVISE #43541879283](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541879283), HEAD `d8d6777cf5ba12e68cc8cdd6303477f98cc02512`.
- [Targeted R8 engineering GREEN #43542074773](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43542074773), frozen tested HEAD `1065e0870fbc8acf9db963cd38ed90f07f13b94e`. **18/18 SHA-256 checks on each of the three downloaded original raw ZIPs passed**; internal original package still exits 1.

**Hard restrictions:** No new project/branch/PR, no merge, no external OpenTelemetry comments or PRs, no cloud spend or production operations. AETHER TEST ARCHITECT cannot be impersonated by an Engineering-authored result. Do not reclassify the upstream `qmv0` contract conflict as resolved without actual maintainer direction.

**Status:** `HANDOFF_PREPARED_ONLY`. A separate specialist has **NOT** executed independent R8 tests by virtue of publishing this file.
