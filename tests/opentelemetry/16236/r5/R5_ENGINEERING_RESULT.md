# AETHER X GLOBAL — OpenTelemetry #16236 — R5 metadata-integrity engineering

**Mission:** `AXG-OTEL-16236-R5-QMV0-INTEGRITY-ENGINEERING-20261114`  
**Overall technical verdict:** **`R5_REVISE`**, not merge-ready.  
**Narrow actual Contrib extension result:** **`R5_ACTUAL_FILESTORAGE_PASS_SCOPED`** on three tests.  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), Draft/unmerged. No external OpenTelemetry PR or comment authorized by this report.

## Source identity

- Upstream Collector source pinned to `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`. Original `persistent_queue.go` SHA-256 `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- Previously independently reviewed R4 candidate SHA-256 `c9705f155cd3c143da236741947689120670d17817c0244e386a4d138f86afce`.
- New R5 candidate [`persistent_queue_candidate.go`](../r2/persistent_queue_candidate.go) SHA-256 **`52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446`**.
- New [bbolt metadata-integrity test](axg_qmv0_integrity_test.go) SHA-256 `c7140862be442c6cc436b4d261d6b3a18b52cefd710082b14faab953ec08829f`.
- New [actual Contrib file_storage integration test](axg_actual_filestorage_test.go) SHA-256 `11c87147d2862c6380e9333e0de03e0d318f10b8e5b36de3baaca22124e5fd44`.
- Go `1.26.0 linux/amd64`, native bbolt `v1.5.0`, Contrib `file_storage v0.165.0`, with `FSync=true` in actual extension integration tests.

## Falsifiable executed results

| Exact run / tested internal HEAD | Actually observed | Decision |
| --- | --- | --- |
| [R5 before fix #43530352324](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530352324), HEAD `18b47660b1ee0c2e681eba89e0e2d765247ab262` | Old candidate **failed** three new bbolt negative checks: corrupt `qmv0` returned nil instead of error; metadata read failure returned nil; read index past write index was accepted. Existing new-empty queue control passed. Focused exit **1**, full package exit **1**. | **`R5_EXPECTED_METADATA_RED`** |
| [R5 after fail-closed fix #43530527088](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530527088), HEAD `a876e1686e8c653c4a5cf92b8511558c44b5136a` | All **four targeted R5 tests PASS**: malformed `qmv0` fails closed with unchanged physical payloads and metadata bytes; manual restoration of original good metadata recovers IDs `11,22`; injected metadata read failure fails closed; impossible indices fail closed; fresh queue without metadata still initializes. Focused exit **0**. **BUT existing upstream full queue package failed, exit 1.** | **`R5_REVISE`** |
| [Actual Contrib extension #43530894477](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530894477), HEAD `178e00c5acba5fb254b96000b4a7f1be89bb6572` | Instantiated the **real published Contrib** `filestorage.NewFactory` and called `Start`, `GetClient`, `Close`, `Shutdown` on persistent files. Qmv0 two-dispatched-items restart and independent physical inventory passed; legacy `ri/wi/di` migration passed; corrupt `qmv0` refused initialization and preserved physical records until manual restoration. **3/3 PASS**, focused exit 0. | **`R5_ACTUAL_FILESTORAGE_PASS_SCOPED`** |

### Material incompatibility: two untouched upstream tests

The full upstream `exporter/exporterhelper/internal/queue` suite fails **exactly two existing test cases** in `TestPersistentQueue_CorruptedData`:

- `corrupted_metadata`
- `corrupted_everything`

The upstream test explicitly expects **successful initialization of an empty queue with Size=0** after corrupting metadata; R5 refuses startup instead. This is an intentional **fail-closed contract change**, not a test harness malfunction or an acceptable green suite. The original upstream tests **were not altered, skipped, suppressed or reclassified as PASS**. They require maintainer agreement on intended data-loss/metadata-recovery semantics, with an independently reviewed test-contract change if approved. No such approval exists.

### Exact behavior of the proposed R5 change

1. Keep normal missing `qmv0` behavior (`errValueNotSet`): initialize a new queue or try legacy format.
2. Treat a present-but-unreadable `qmv0` (invalid protobuf or storage read error) as **fatal startup error**: no reset to `ReadIndex=WriteIndex=0`; no write to durable storage from that path.
3. Reject a successfully decoded but impossible metadata state with `ReadIndex > WriteIndex`.
4. Preserve the earlier R2/R3 per-item transactional copy + metadata + retirement model unchanged.

**This is NOT general corruption recovery:** a protobuf that decodes to *plausible but wrong indices* cannot be reliably identified by only the current metadata bytes. Lost or absent `qmv0`, non-atomic storage, actual full-disk/ENOSPC, compaction, power loss and producer/consumer duplicate external deliveries require separate contracts/tests.

## Evidence and permissions

The [R5 permanent original evidence index](evidence/EVIDENCE_INDEX.md) is mutually linked with this report. It links **three full raw original GitHub Actions job logs**, three byte-for-byte restored original JSON result files, **three byte-for-byte restored original SHA256 manifests**, and three complete original archived ZIPs. Independently downloaded every ZIP and validated all manifest entries: **15/15, 15/15, 12/12**. ZIP artifacts expire; the original full job logs/results/manifests and this index remain in Git history. Complete individual original ZIP contents are not claimed to be permanently committed.

**Remaining gates:** overall `R5_REVISE` until upstream maintainers agree the metadata policy and the two original tests' contract is resolved without hiding regressions; full Collector distribution, power-loss/compaction/ENOSPC tests and fresh **AETHER TEST ARCHITECT** independent qualification on a new exact HEAD remain NOT DONE. No external issue comments, upstream PR, production claims, or internal merge executed.

**Decision:** **KEEP PR #22 DRAFT AND UNMERGED.** The original independently approved R4 narrow result does not automatically extend to R5's new candidate. Await design/contract decision before classifying broad suitability.
