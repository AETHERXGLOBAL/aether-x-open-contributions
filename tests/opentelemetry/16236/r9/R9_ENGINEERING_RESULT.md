# AETHER X GLOBAL — OpenTelemetry Collector #16236 — R9 engineering

**Mission:** `AXG-OTEL-16236-R9-ENGINEERING-20261114`  
**Engineering verdict:** **`R9_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`**  
**Original upstream package:** **FAIL, exit 1** — unchanged corrupt-`qmv0` contract conflict; NOT merge-ready.  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), Draft/unmerged.

## Exact source

- **R9 tested code HEAD:** `d290913250985480e9fab08222a82642ee55bf67`. Any later evidence-only commit is not a new Go test.
- **Candidate:** [persistent_queue_candidate.go](../r2/persistent_queue_candidate.go) SHA-256 **`74a66d85a4e2000a3292aeed1ec2e3cfe59e1de9b9c873fb07c5620a6158469c`**.
- **R9 engineering fixture:** [axg_nonwalker_integrity_test.go](axg_nonwalker_integrity_test.go) SHA-256 `81eaf422d0063bb38d9e38f13ca34d066970b75fa3b1d35d4eb88717838631d4`.
- Original **unchanged independent TA R8** fixture SHA-256 `2a5ea725923b3a36a4a00af06bf05a21d45eb37cc2718d4a549bd9e2c8eaf3c8`. Independent TA R7 `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`; TA R6 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.
- Pinned upstream Collector HEAD `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`; original `persistent_queue.go` SHA-256 `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- Actual Ubuntu 24.04 / Go 1.26.0 / Contrib `file_storage v0.165.0` backed by bbolt v1.5.0. No production files.

## Change and proof

**TA-R8-01 — non-Walker durable overwrite.** The `storage.Client` API cannot enumerate arbitrary existing numeric keys without optional `storage.Walker`. The R9 candidate adds a read of numeric key 0 before treating missing legacy metadata as a new queue when Walker is unavailable. An orphaned first payload now refuses initialization instead of silently accepting an Offer that overwrites `11` with `41`. It also checks each prospective write slot for an existing **nonempty** payload **before** the in-memory count and durable Batch, preventing later non-Walker key collisions when encountered.

**TA-R8-02 — plausible qmv0, missing first pending payload.** Before declaring loaded consolidated metadata valid, R9 verifies that the physical record for `ReadIndex` exists when `ReadIndex < WriteIndex`. A protobuf-valid metadata record `ReadIndex=0, WriteIndex=1` with absent physical key 0 now refuses startup without writing or resetting stored metadata.

The code passes the *exact, unchanged* independent R8 adversarial root tests plus the new R9 controls, including a subsequent orphan at index 3 and valid clean non-Walker and qmv0 restarts. Historical R5–R8 targeted checks also pass. These are **bounded** properties; see caveats below.

## Actual RED → REVISE → GREEN

| Run / exact source HEAD | Actual observed | Classification |
| --- | --- | --- |
| [Expected RED #43545600682](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545600682), `dee14219def8c64e7c9a8f6f547dac055ded01d8` | TA R8 two non-Walker failure leaves + plausible-qmv0 failure; three new R9 negatives also failed; historical PASS; upstream original two corrupt-qmv0 leaves FAIL | **`R9_EXPECTED_RED`** |
| [Initial code REVISE #43545705820](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545705820), `3e9fa68bb270c8a1d75b08b13533ac56f3ef154d` | All original TA R8 cases now PASS, but R9 future orphan slot collision check FAIL; source had not yet enforced protection inside Offer; original suite still FAIL | **`R9_REVISE`** |
| [Final scoped GREEN #43545871406](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545871406), `d290913250985480e9fab08222a82642ee55bf67` | Exact independent TA R8 suite **exit 0**; R9 added scenarios **exit 0**; historical R5–R8 **exit 0**; **original unmodified upstream Go package exit 1**, with only its known two corrupt-`qmv0` subcases plus parent | **`R9_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`** |

The first R9 CI authoring attempts [#43545392585](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545392585) and [#43545565920](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545565920) incorrectly mixed new adversarial fixtures into the original-package step. The workflow was corrected before classifying the **true RED**; those failed runs are not falsely counted as original-suite comparisons.

## Critical boundaries — **not certified**

- **Non-Walker is not globally safe**. The interface has no key-enumeration or conditional create. The initial probe covers numeric key 0; a later per-Offer probe protects a **nonempty** occupied key *when encountered*, but the absence of arbitrary orphan records is not proven. Empty legacy markers without payload cannot be distinguished from absent ones by `Get` alone. The Get-then-Batch gap is **not cross-writer atomic**, so concurrent writers sharing a namespace or non-atomic backends remain unsafe/unqualified.
- **qmv0 consistency is NOT fully proven.** Only the first pending indexed physical payload is checked on startup. Missing later indices, plausible but incorrect metadata pointing at other keys, torn writes and on-disk corruption still require broader design and independent tests. This cannot be represented as complete physical-inventory certification.
- Historical original `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` **still fail unchanged** because they require reset-to-empty semantics while the candidate is fail-closed. Upstream maintainers have not accepted a revised contract.
- Actual disk ENOSPC, power loss, compaction, full Collector exporter round-trip, storage clients without transactional Batch, and external exactly-once delivery **NOT tested**. No independent R9 AETHER TEST ARCHITECT signoff.

## Evidence and disposition

[**Mutually linked R9 evidence index**](evidence/EVIDENCE_INDEX.md) contains complete original GitHub Actions runner logs for all three classified executions, original machine `result.json`, original 19-file SHA-256 manifest and ZIP artifact references. The three ZIPs were downloaded and independently unpacked with **19/19 SHA-256 digest matches each (57/57)**. Original ZIPs are time-limited; complete GitHub runner logs and original results/manifests are durably committed, but not every original ZIP member is individually preserved in Git.

**Decision:** keep internal PR #22 **Draft/unmerged**. Request a genuinely distinct R9 independent review on the amended exact candidate, and a separate human upstream maintainer design decision on qmv0/Backend capability contracts. No upstream public PR/comment, production release, or merge executed.
