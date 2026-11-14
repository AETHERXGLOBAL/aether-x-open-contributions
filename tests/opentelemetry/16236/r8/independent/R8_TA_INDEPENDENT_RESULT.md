# AETHER X GLOBAL — AETHER TEST ARCHITECT independent R8 result

**Mission:** `AXG-OTEL-16236-R8-INDEPENDENT-METADATA-REQUALIFICATION-20261114`  
**Date:** 2026-11-14 UTC  
**Repository:** `AETHERXGLOBAL/aether-x-open-contributions`  
**Existing internal Draft PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22)  
**Independent executed HEAD:** `c79f031015244e0d5c7f6d653b36e71bcde4da42`  
**Pinned upstream:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`  
**Frozen R8 candidate SHA-256:** `200cb460efa44879827f9074edb911276a3ff1f7ca2f51a4d44c2f5ba844506c`  
**Unmodified independent R7 test SHA-256:** `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`  
**Unmodified independent R6 test SHA-256:** `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`  
**Independent R8 test SHA-256:** `2a5ea725923b3a36a4a00af06bf05a21d45eb37cc2718d4a549bd9e2c8eaf3c8`  
**Independent verdict: `REVISE`. Upstream original-suite/merge gate: `BLOCKED`.**

[**Bidirectionally linked permanent evidence index**](evidence/EVIDENCE_INDEX.md).

## Actual independent runs and test-oracle correction

1. Initial separate execution [#43543717153](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43543717153), HEAD `5df51a2a1bcd0804ebcac408da43888cbcca72b2`: genuine non-Walker overwrite reproduced, plus three false-positive **test-harness control failures**. Specifically, the custom Walk proxies used an unnamed Go callback type rather than `storage.WalkFunc`, so the interface type assertions did not dispatch the fault/scanning paths; an empty but present `qmv0` control incorrectly assumed nonempty bytes. These are **NOT product defects**.
2. Corrected cold-start [#43543925006](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43543925006), HEAD `c79f031015244e0d5c7f6d653b36e71bcde4da42`: fixed ONLY the separate independent test fixture. The R8 candidate, unchanged R6 and R7 independent tests, R7 engineering tests, and R8 engineering tests were not edited. Four positive controls then PASS; the two integrity test roots remain FAIL. Both original runs and their adverse evidence are preserved.

**Environment:** GitHub Actions Ubuntu 24.04, Go 1.26.0, actual published Contrib `file_storage v0.165.0`, bbolt 1.5.0, isolated temporary on-disk databases. No mocked-bbolt equivalence claim, skipped original tests or changes to product code.

| Executed test group on corrected run | Actual exit code | Observed |
| --- | --- | --- |
| Original unmodified upstream Go queue package with candidate source | **1** | `TestPersistentQueue_CorruptedData/corrupted_metadata`, `.../corrupted_everything` (plus their parent) FAIL; maintainer policy not decided |
| Historical R3–R6 bbolt crash and real Contrib persistence checks | **0** | PASS within tested scope |
| Unchanged R6/R7 independent plus R7/R8 engineering regressions | **0** | PASS within tested scope |
| New independently authored R8 adversarial suite | **1** | `TestAXGTAR8NonWalkerUnsafeOrphanAndEmptyMarkers` (2 failing subcases) and `TestAXGTAR8PlausibleButWrongQmv0RefusesStartup` FAIL; **4 named positive controls PASS** |

## Independently reproduced defects and controls

**TA-R8-01 — HIGH / actual durable payload overwrite for a non-Walker storage.Client.** On two separate real Contrib `file_storage` databases, wrap its client in a Go `storage.Client` interface that does not expose optional `Walker`. Fixture A has an orphan numeric request key 0; fixture B has present-but-empty legacy `ri` and `wi` markers with a request key 0. The queue incorrectly starts as new and permits `Offer(41)` to overwrite an existing **11** with **41**. Actual raw test output records `original=11 final="41"` for both cases. Expected oracle: reject unsafe startup and preserve durable bytes. **FAILED**. This is a validated limitation of **non-Walker** clients, not a demonstrated failure of Walker-capable normal Contrib operation.

**TA-R8-02 — MEDIUM / plausible but inconsistent `qmv0` accepted.** Inject a protobuf-valid `PersistentMetadata{ReadIndex:0, WriteIndex:1}` without persisted numeric request key 0. `initClient` returns success. An independent startup consistency/fail-closed oracle **FAILED**. The complete downstream effect and desired upstream recovery contract need Engineering and maintainer adjudication; a concrete payload overwrite was **not** shown in this particular test.

**Independent positive controls:** Non-Walker clean new store PASS; injected real `storage.Walker.Walk` error propagates and preserves payload/no new metadata PASS; startup Walk visited exactly **256/256** seeded non-queue keys PASS (shows linear enumeration, **not** acceptable large-store latency); isolated real Contrib exporter namespaces including present-but-empty `qmv0` PASS. These four controls passed only after the independently documented test-harness correction.

**Mutation/negative-control quality:** The historical unsafe-metadata scenarios were used as real known-bad counterexamples, with actual test failures. The first-run oracle false positives were corrected openly, and both original traces retained; this is not a blind mutation-score certification.

## Original raw evidence and integrity

Both GitHub Actions original ZIPs were separately downloaded and opened. The 17-file ZIP for the first execution has SHA-256 `6e60c9f78242e77a9b1d15084ede99d67343c20da677d25f273491f81950470c`; the 17-file ZIP for the corrected execution has SHA-256 `2998e09dcfac4e19fc4f78d26508ea903b87f6ab744c8552160e7734086c488a`. The original `SHA256SUMS.txt` inside **each** archive was independently checked against all 16 listed members: **16/16 PASS in each, zero mismatches**. Complete per-command Go stdout/stderr was printed to the runner console and the full original logs have been durably copied to this branch. Original ZIPs and contained original member manifests remain accessible subject to Actions retention.

[Evidence index, machine results, full original logs and source inventory](evidence/EVIDENCE_INDEX.md).

## Scope limitations and minimal disposition

**NOT RUN / NOT CERTIFIED:** actual physical disk exhaustion/ENOSPC, power-loss durability, massive database startup time or memory, every backend's `Batch` atomicity, all scoped collision combinations, full Collector distribution, external exactly-once delivery, upstream maintainer acceptance. The original upstream queue suite **still has exit 1**; it may not be relabeled PASS. The `qmv0` fail-closed versus historical reset-to-empty contract cannot be changed without maintainer guidance.

**Required next step:** keep existing PR #22 **Draft/unmerged**; deliver TA-R8-01 to Engineering to require a safe capability boundary or an equivalent existence oracle for non-Walker clients; adjudicate TA-R8-02 without assuming all missing-payload cases are recoverable; obtain genuine maintainer direction for original `qmv0` tests; re-run independent code-and-test evidence on a new exact HEAD only after targeted remediation. No new project, branch, PR, upstream comment, or merge authorized or performed.
