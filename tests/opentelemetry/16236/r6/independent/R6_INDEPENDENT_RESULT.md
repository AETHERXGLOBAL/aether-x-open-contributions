# AETHER TEST ARCHITECT — R6 Independent Requalification

**Mission:** AXG-OTEL-16236-R6-INDEPENDENT-REQUALIFICATION-20261114  
**Date:** 2026-11-14 UTC  
**Repository / PR:** [AETHERXGLOBAL/aether-x-open-contributions #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) (internal Draft; unmerged)  
**Execution branch:** `evidence/otel-queue-recovery-16236-r1-20261113`  
**Exact independently executed internal HEAD:** `ca1eaadfe041685754cd4acfd3d0c848c7ac5c20`  
**Git tree:** `9aa29c999961ba686af4ca803dce83b95acedcb7`  
**Pinned original upstream HEAD:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`  
**Earlier engineering R6 HEAD:** `b42bb0aeefd4ac30a4d10a9b82f2308563c6a0f6` (not a separate independent signoff).

## Verdict: REVISE — NOT MERGE READY

The R6 safety improvements passed the bounded cold-start cases on real Contrib `file_storage`; **the entire unmodified original upstream test package still fails** and a new independent adversarial case demonstrated unsafe handling of *corrupted legacy read-index metadata*. These failures are not waived. No upstream publication, merger approval, production durability assurance, human-independent assurance or exactly-once exporter guarantee is implied.

## Actual independent execution

- [Independent GitHub Actions run #43536954950](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536954950), [job #132268165104](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536954950/job/132268165104): **workflow SUCCESS as truthful REVISE classifier**, not a software PASS.
- Environment: `ubuntu-24.04`, `go1.26.0 linux/amd64`, published Contrib `file_storage v0.165.0`, `bbolt v1.5.0`, `FSync=true`; all on isolated temporary directories.
- Candidate SHA-256 `52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446`; unchanged engineering R6 fixture SHA-256 `c09f2f0a72b5c49da3d4812b68ad2a1212f31c7522c29b04b5d12919158d4a1b`; independently authored regression fixture SHA-256 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.
- Cold rerun of real Contrib R5/R6 focused tests: **exit 0**. This covers the previously authored committed Batch/SIGKILL, injected pre/post-commit errors, capacity, qmv0/legacy, acknowledgment and corruption checks, not a novel independent oracle for each.
- Entire original upstream queue package, with all original test cases retained: **exit 1**; the only failing leaves were `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` (plus parent `TestPersistentQueue_CorruptedData`). This is a maintainer-contract conflict, **not a green original test suite**.
- Independent positive/negative-control suite: **exit 0**. Truly new empty queue initialized/reopened; actual Contrib qmv0 and legacy stores reopened five times each, yielding **10/10 reproducible fresh-reopen cycles**, each with logical queue size 3, zero dangling in-flight references and exactly `[11,22,33]` in physical numeric storage keys.
- Independent corrupted-legacy regression: **exit 1, expected failure revealing a defect**. A genuine `file_storage` instance containing an invalid two-byte legacy read index, valid legacy write index and durable request `11` was reopened. `initClient` returned **nil** (accepted corruption), the malformed old read-index key was **deleted**, while physical payload `[11]` remained. This violates fail-closed startup/preservation semantics and risks logically orphaning a physically persisted request. The test deliberately fails when unsafe behavior is observed.

### Minimal defect reproduction

Run from an exact pinned, isolated Go checkout as in [independent workflow](../../../.github/workflows/otel-16236-r6-independent.yml); the independent test source is [axg_ta_r6_independent_requalification_test.go](../axg_ta_r6_independent_requalification_test.go). In the real Contrib fixture: create a legacy `ri` key with `01 02` bytes, valid `wi=1`, numeric request key `0=11`; close the extension; reopen, attempt queue initialization; then independently inspect legacy key and physical request inventory. Expected: refuse startup and leave both legacy metadata and payload intact. Actual: `initClient` succeeded and the legacy read-index metadata was removed; request remained physically present.

### Execution integrity and negative runs

- Initial independent [run #43536555597](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536555597): **FAIL** at test formatting preflight before execution. Reviewer harness problem; preserved, not a product finding.
- Second [run #43536743345](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536743345): R5/R6 focused rerun succeeded, but novel tests failed setup because the temporary Contrib storage directory was absent; an exact-name classifier also retained trailing whitespace. **FAIL**. Both reviewer-harness problems corrected without altering candidate source.
- Final [run #43536954950](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536954950): cold-source verification succeeded; independently authored controls passed; legacy finding reproduced; full original package remains red.

### Untested / excluded boundaries

Actual filesystem ENOSPC, hardware/power-loss or torn-write durability, non-atomic backend Batch semantics, online compaction, complete Collector distribution, external exporter acknowledgments, and exactly-once delivery are **NOT_RUN**. The known postcommit error is injected *after* an actual Contrib Batch commit; it is not an arbitrary hardware/storage fault. Historical [R4 independent decision](../../r4/TEST_ARCHITECT_R4_RESULT.md) covers an older candidate only. The upstream issue currently has **no maintainer decision resolving corrupt-metadata recovery expectations**.

## Evidence, provenance and next gate

See the mutually linked [independent evidence index](evidence/EVIDENCE_INDEX.md) for the exact raw GitHub job log, original machine result with a byte-verified SHA-256, original artifact SHA-256 manifest, archived complete original test-log artifact, and limitations of artifact retention. The original artifact was downloaded and SHA-256 checked: **17/17 constituent files matched**; original ZIP SHA-256 `b3a21653fa0573a2e58dd867c321607938ed30b7a0e070aeabca555419c32cba`.

**Engineering next action:** narrowly address invalid legacy metadata without dropping/reindexing durable payloads; separately obtain actual upstream maintainer guidance about corrupt qmv0 reset-vs-fail-closed contract. Then rerun the complete original package and these independent regressions on a newly frozen exact source HEAD, preserving all failures. No candidate source, upstream PR or merge was modified/authorized by this review. This is independently executed automated test evidence, **not a separate human assurance statement**.

[Return to evidence index](evidence/EVIDENCE_INDEX.md).
