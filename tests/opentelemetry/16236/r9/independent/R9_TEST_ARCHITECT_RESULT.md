# AETHER X GLOBAL — AETHER TEST ARCHITECT — R9 independent adjudication

**Mission ID:** `AXG-OTEL-16236-R9-INDEPENDENT-NONWALKER-QMV0-REQUALIFICATION-20261114`  
**Independent technical verdict:** **`REVISE`** — four falsifying independent tests; original unmodified Upstream assertions still fail on two corrupt-qmv0 leaves.  
**Disposition:** PR #22 remains **Draft / unmerged**. No upstream issue, PR, release, production execution or repair-code edits authorized or performed.

## Immutable execution identity

| Dimension | Executed source |
|---|---|
| Repository / PR | `AETHERXGLOBAL/aether-x-open-contributions` / [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) |
| Existing branch | `evidence/otel-queue-recovery-16236-r1-20261113` |
| **Actual independent GitHub Actions execution HEAD** | `b18313bfa30ee098b0e6a2de074245589b7d90bf` |
| **Actual execution Git Tree** | `417ff03881ba814318a6027a33c93e7c5da162bb` |
| **Unchanged R9 engineering source HEAD** | `d290913250985480e9fab08222a82642ee55bf67` |
| **Candidate source SHA-256** | `74a66d85a4e2000a3292aeed1ec2e3cfe59e1de9b9c873fb07c5620a6158469c` |
| Pinned original Collector HEAD | `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0` |
| Environment | GitHub Actions Ubuntu 24.04, Go 1.26.0, actual Contrib file_storage v0.165.0, bbolt v1.5.0 |
| [Actual independent run](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43582341324) | `43582341324`; job `132409540943`; action conclusion **failure**, deliberately enforcing `REVISE` |
| [Original raw artifact](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43582341324/artifacts/14109425122) | ZIP SHA-256 `051abfd0776d2bfcda01a485c78ca3d0e8c4ea5120bb3788bb71114da7fe8761`; 18/18 content hashes independently verified |

This is a separate test suite and separate execution, not acceptance of Engineering's previous run. The original R5–R8 test fixtures were copied without alteration; candidate integrity was independently checked at execution.

## Run receipts, not assumed success

| Test operation | Actual exit | Result |
|---|---:|---|
| Original upstream queue package assertions, no skipped or modified upstream cases | `1` | **FAIL** |
| Historical R5–R8 and prior TA R6–R8 tests | `0` | PASS_SCOPED |
| Existing R9 Engineering tests, comparator only | `0` | PASS_SCOPED (not independent) |
| **New independently authored TA R9 tests** | `1` | **4 PASS, 4 FAIL, 0 SKIP** |

Full raw logs, exit files, original machine `result.json`, and preserved original `SHA256SUMS.txt` are permanently committed and mutually linked in [R9 independent evidence index](evidence/EVIDENCE_INDEX.md).

### Independent new probes — exact results

| Test / threat hypothesis | Result | Oracle |
|---|---|---|
| `TestAXGTAR9NonWalkerOrphanZeroPreserved` | PASS | First orphan rejects startup, physical bytes unchanged |
| `TestAXGTAR9NonWalkerOrphan1024CollisionPreserved` | PASS | Future occupied slot rejects Offer, original physical bytes remain `11` |
| `TestAXGTAR9NonWalkerEmptyPresentNumericSlotMustNotOverwrite` | **FAIL** | Actual file_storage Walker confirms a physically present but empty numeric `0` key; non-Walker startup incorrectly succeeds |
| `TestAXGTAR9Qmv0MissingMiddlePayloadMustRefuse` | **FAIL** | Valid protobuf `ReadIndex=0, WriteIndex=3`; keys 0 and 2 exist but 1 is missing; startup incorrectly succeeds |
| `TestAXGTAR9NonWalkerPresentEmptyLegacyMarkersMustReject` | **FAIL** | Walker verifies both empty legacy index keys exist; non-Walker startup incorrectly succeeds |
| `TestAXGTAR9GetErrorMustNotAdvanceDurableWrite` | PASS | Injected `Get` failure blocks Offer without changing qmv0/physical payload |
| `TestAXGTAR9ConcurrentWriterSharedNamespaceMustNotLoseRequest` | **FAIL** | Two writer clients both read empty slot before either Batch; both Offers return nil but only `[41]` remains, request `11` lost |
| `TestAXGTAR9ValidTwoPendingQmv0RestartControl` | PASS | Real file_storage restart retains two valid pending records |

Negative controls were not reclassified as passes. The concurrent test proves a **shared-namespace multi-writer counterexample**, not that file_storage violates a promised single-writer contract. The qmv0 and non-Walker empty-presence cases independently falsify broad fail-closed guarantees, but do not on their own establish actual loss of nonempty bytes. The `[41]` inventory in the concurrent case is a directly observed loss under the deliberately adversarial shared-writer arrangement.

## Defect register and targeted Engineering handoff

**TA-R9-01 — Present-empty numeric key is invisible to non-Walker `Get` (FAIL).**  
Reproduce `go test -run '^TestAXGTAR9NonWalkerEmptyPresentNumericSlotMustNotOverwrite$' -count=1 ./internal/queue` in the pinned workflow. Before treating a client with no `Walker` as a clean new queue, define a storage capability/ownership contract that can prove absence of numeric markers; absent proof, reject unsafe states. Avoid relying on `len(Get(key)) == 0` as a key-existence oracle.

**TA-R9-02 — qmv0 non-first missing pending payload undetected (FAIL).**  
Reproduce `-run '^TestAXGTAR9Qmv0MissingMiddlePayloadMustRefuse$'`. Current candidate checks physical `ReadIndex` only. Design an integrity predicate across *all* pending records, or fail closed where physical inventory cannot be established. Preserve existing data without silent reset. Distinguish a comprehensive validation design from the old limited first-key check.

**TA-R9-03 — Empty-but-present legacy markers under non-Walker (FAIL).**  
Reproduce `-run '^TestAXGTAR9NonWalkerPresentEmptyLegacyMarkersMustReject$'`. Presence of `ri`/`wi` cannot be inferred from empty `Get`; prohibit unsafe legacy migration / startup without a presence oracle. Keep Walker-capable storage and valid new-store controls functioning.

**TA-R9-04 — Two writers, one namespace, Get/Batch TOCTOU (FAIL).**  
Reproduce `-run '^TestAXGTAR9ConcurrentWriterSharedNamespaceMustNotLoseRequest$'`. The barrier holds both readers after `Get(0)`; both Offers succeed and durable inventory contains only `41`. Either enforce exclusive durable queue ownership/fencing (including startup and re-open) or require backend-specific conditional insert/transaction semantics. Mutex within one `persistentQueue` cannot protect another queue instance. If multi-writer is explicitly unsupported, prove and enforce that exclusion rather than imply a generic lossless guarantee.

**Upstream policy gate — independently reconfirmed FAIL.**  
Original `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` fail (and their parent reports FAIL) with no test rewrites, skips, or waiver. This is the unresolved reset-to-empty versus fail-closed `qmv0` contract. Requires authentic upstream maintainer design resolution before acceptance.

## Execution provenance and limits

Independent fixture: [axg_ta_r9_independent_test.go](axg_ta_r9_independent_test.go); invocation and source pinning: [R9 TA GitHub Actions workflow](../../../../../.github/workflows/otel-16236-r9-independent.yml). Its steps pin upstream and candidate hashes, run entire original tests first, add unchanged historical fixtures and distinct TA tests, and preserve every exit/log without treating failures as green.

The test run did **not** test all storage backends, genuine ENOSPC/power removal, full Collector exporter E2E, external exactly-once semantics, non-atomic implementations, or a maintainer-approved qmv0 contract. The earlier R8 Walker 256-key scan and real namespace isolation passed as historical regressions; no scalable throughput or latency SLA follows.

**Decision: `REVISE`**. Require Engineering repair/explicit enforceable backend capability restriction for the four failed cases, re-run unchanged historical and independent cases on a newly frozen exact source HEAD, and obtain upstream maintainer qmv0 contract decision. Do not merge or issue a comprehensive PASS.

**Two-way primary evidence link:** [R9 independent evidence index](evidence/EVIDENCE_INDEX.md).
