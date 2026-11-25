# AETHER X GLOBAL — OpenTelemetry Collector #16236 — R10 engineering result

**Mission:** AXG-OTEL-16236-R10-QMV0-PENDING-REQUALIFICATION-20261114  
**Precise engineering verdict:** **R10_QMV0_PARTIAL_PASS_THREE_INDEPENDENT_BLOCKERS**.  
**Overall data-integrity / all-backend / merge verdict:** **REVISE / BLOCKED**.  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) — Draft and unmerged; no external upstream PR or comment.

## Immutable executed source

- **R10 actually tested HEAD:** \`8c82c3a6ff9be73b2698eaf011d676414accae68\`.
- Upstream Collector pinned to \`572057cde7e9bbe3aed6e5e3e8f16290d487f7d0\`, original queue source SHA-256 \`c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4\`.
- Amended [experimental candidate](../r2/persistent_queue_candidate.go) SHA-256 **\`5b1df085d3db0e91a2c0e8f5aef529087985b3cd102d725a206697cbdc3df176\`**.
- Added [R10 real file_storage inventory tests](axg_qmv0_inventory_test.go) SHA-256 \`ea7a616757b2ccc9db28c7513566d404feb15640ee0237700e2beacbcf00671c\`.
- **Unmodified independent R9 Test Architect fixture** Git blob \`da58cdec582045b1506a5b992bca7132105ba84c\`. All prior independent R8, R7, R6 fixtures remained unchanged.
- Environment: GitHub Actions ubuntu-24.04, Go 1.26.0, actual Contrib \`file_storage v0.165.0\`, actual bbolt v1.5.0.

## Targeted fix and its exact limits

The independently observed \`qmv0\` corruption had plausible metadata \`ReadIndex=0, WriteIndex=3\` with physical item keys 0 and 2 present, key 1 absent. R9 checked *only the first indexed payload*, so startup incorrectly proceeded.

R10 changes \`loadQueueMetadata\` to validate **every undispatched index** in \`[ReadIndex, WriteIndex)\` *before* the existing recovery writes:
- When \`storage.Walker\` is available, scans actual storage keys without allocating an array proportional to possibly malicious metadata length; counts strictly canonical present and nonempty physical pending payloads and requires the count equal the metadata pending range length. Any missing middle/last key or empty value rejects startup.
- Without Walker, reads every pending key and rejects empty or missing bytes. The \`Get\`-only fallback is *not* a physical presence oracle for empty keys, and cannot provide a transactional snapshot or ownership proof. R10 does not claim non-Walker safety.
- No metadata is silently reset on failed verification; original raw persisted payloads remain untouched in the specifically tested negative cases.
- This scan incurs **O(number of stored keys)** on the Walker path, or **O(number of pending requests)** Get calls without Walker; large-database startup latency has **NOT** been independently characterized. Cross-writer updates between scan and use are not made atomic by this change.

## Executed tests — success AND failure

**[Actual GitHub Actions R10 run #43583939265](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43583939265)**, job \`132414326496\`, source HEAD \`8c82c3a6ff9be73b2698eaf011d676414accae68\`.

| Actual command suite | Exit | Meaning |
| --- | ---: | --- |
| R10 new qmv0 integrity tests (missing middle, missing last, noncanonical alias, missing-middle non-Walker, huge false write index; valid subrange control) | **0** | **PASS_SCOPED**, five negative controls and valid control |
| Earlier R9 engineering fixtures | **0** | PASS_SCOPED |
| Historical R5–R8 plus earlier independent checks | **0** | PASS_SCOPED |
| **Unchanged TA R9 independent adversarial tests** | **1** | **3 cases still FAIL; exactly one previously failing missing-middle-qmv0 case now PASS** |
| Full original upstream Go queue assertions in package test run | **1** | Original \`TestPersistentQueue_CorruptedData/corrupted_metadata\` and \`.../corrupted_everything\` plus parent **still FAIL** |

**Three unchanged, still independently failing TA R9 cases:**
1. \`TestAXGTAR9NonWalkerEmptyPresentNumericSlotMustNotOverwrite\` — non-Walker \`Get\` cannot distinguish absent key from physically present zero-byte key;
2. \`TestAXGTAR9NonWalkerPresentEmptyLegacyMarkersMustReject\` — same absence/presence ambiguity for empty legacy \`ri/wi\` markers;
3. \`TestAXGTAR9ConcurrentWriterSharedNamespaceMustNotLoseRequest\` — two queue instances write the same namespace via Get-then-Batch without shared exclusion or CAS; a request can be overwritten.

**These are NOT regression fixes**: R10 did not address or reclassify them. Their original independent test source remains unchanged.

**Unresolved upstream contract:** original corrupt \`qmv0\` test expectations reset to empty versus experimental fail-closed semantics. No genuine maintainer decision was obtained, and neither original test was edited or skipped.

## Architectural blocker and recommended contract

The published \`storage.Client\` contract explicitly permits \`Set\` overwrites and \`Get\` returning nil for missing keys; it provides no conditional creation/CAS, key-presence proof for zero-byte values, durable ownership token, or transactionally enforced fencing across independent clients. Merely adding a mutex to a single \`persistentQueue\` or another \`Get\` cannot fix shared-namespace concurrent writers.

**Recommended engineering design gate before claiming general safety:**
1. **Prefer backend-verified exclusive queue ownership with fencing** across opens and writers, or a storage capability offering a true atomic conditional write/transaction. Any such capability must have deterministic acquisition, revocation, restart and concurrent-writer failure tests. Use the actual file_storage implementation and verify the transaction guarantee rather than relying on a wrapper's name.
2. **Fail closed** for backends that cannot prove the required ownership and key-existence semantics; do not silently market them as lossless. Such a restriction would alter currently accepted non-Walker startup behavior and upstream tests, so requires an explicit compatibility decision and fresh independent contract tests. A generic \`Client\` has no proof of an empty namespace.
3. Verify \`qmv0\` scan cost at meaningful queue sizes and adversarial metadata extremes, plus real disk exhaustion, crash/power-failure and reopened ownership before any broad guarantees.

**This is a decision/design record, not a claimed implementation of these three remaining safeguards.** Do not change independently authored tests to make the old assumptions appear green.

## Evidence, integrity and disposition

The [R10 evidence index](evidence/EVIDENCE_INDEX.md) is linked bidirectionally. Actual full original runner log, byte-identical original machine result and byte-identical SHA256SUMS manifest are committed on GitHub. The original [24-member GitHub Actions artifact #14109457993](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43583939265/artifacts/14109457993) was downloaded and independently checked: **24/24 original member SHA-256 digests matched**, ZIP SHA-256 \`0d41e593b1044e10f5b57355883716a021d23a0ad3879c564f867ed370b335a4\`. Individual full command logs in the ZIP are time-limited; original full job console, machine result and SHA-256 manifest remain durable. No broader claims.

**Next gate:** a distinct Test Architect cold-start R10 review, plus engineering/maintainer decision on mandatory backend owner/CAS capability and corrupt-qmv0 upstream contract. **Internal PR #22 stays Draft/unmerged; external publication and production are blocked.**
