# AETHER TEST ARCHITECT — separate R9 independent requalification handoff

**Mission:** `AXG-OTEL-16236-R9-INDEPENDENT-NONWALKER-QMV0-REQUALIFICATION-20261114`  
**Existing internal PR:** [AETHERXGLOBAL/aether-x-open-contributions #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), must remain Draft/unmerged.  
**Frozen R9 ENGINEERING-tested HEAD:** `d290913250985480e9fab08222a82642ee55bf67`. Verify current HEAD and exact source blobs independently before running; subsequent evidence/report commits are not new tests.  
**Candidate SHA-256:** `74a66d85a4e2000a3292aeed1ec2e3cfe59e1de9b9c873fb07c5620a6158469c`.  
**R9 engineering test SHA-256:** `81eaf422d0063bb38d9e38f13ca34d066970b75fa3b1d35d4eb88717838631d4`.  
**Unchanged independent R8 fixture SHA-256:** `2a5ea725923b3a36a4a00af06bf05a21d45eb37cc2718d4a549bd9e2c8eaf3c8`.  
**Unchanged R7:** `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`.  
**Unchanged R6:** `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.  
**Pinned upstream HEAD:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.  
**Engineer's prior verdict:** `R9_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`, **NOT independent approval**.

## Independent adversarial gates

Execute *new* cold-start tests on original Collector + actual Contrib file_storage v0.165.0/bbolt v1.5.0 under Go 1.26.0:

1. Re-run **unchanged** R8 independent tests, especially the two non-Walker wrapped clients that previously overwrote persisted request 11 with 41 and the plausible valid protobuf qmv0 with absent physical key. Verify no loss, no silent startup, no unauthorized mutation.
2. Fresh independently authored negative controls: non-Walker orphan at index 0 and at a future write slot (including key 3, key 1024), empty-but-present ri/wi keys, an occupied zero-byte numeric key, multiple concurrent queue writers sharing a namespace, and injected `Get` errors during the per-Offer collision probe. **Do not overstate a Get-then-Batch read as atomic CAS**. Differentiate any scope that is unsafe and fails.
3. Challenge qmv0: missing first pending payload versus missing *middle* pending payload; single and multiple pending requests; dispatched-only metadata; plausible but inconsistent index values. Record whether first-key check is intentionally incomplete, not all-inventory proof. Ensure valid qmv0 with physical data and clean non-Walker new queue still work.
4. Measure `Walker` startup scan in seeded 256+ keys (R8), characterize startup cost without claiming big-data performance. Check real file_storage namespace isolation. Keep original R5–R8 historical fault/SIGKILL/ack tests unchanged.
5. Execute **entire original upstream Go queue package unmodified and without skips** on the amended candidate. The original old `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` remain FAIL due to unresolved reset-vs-fail-closed contract. **No broad PASS until legitimate upstream maintainer decision**, no silent test rewrites or waivers.

## Primary evidence

[Engineering technical report](R9_ENGINEERING_RESULT.md) ↔ [permanent original evidence index](evidence/EVIDENCE_INDEX.md). Original GitHub Actions runs [RED #43545600682](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545600682), [REVISE #43545705820](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545705820), [scoped GREEN #43545871406](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545871406). Their full runner logs, original machine decisions, original SHA-256 manifests are committed; all three original ZIPs were downloaded and verified **19/19 each**, total **57/57**. The physical ZIP members expire on GitHub Actions retention.

Publish the **distinct** Test Architect result with immutable tested HEAD, actual commands/exits/complete logs, negative findings, SHA256 bundle and two-way report/evidence links on **same PR #22**, without modifying Engineering's candidate or prior independent tests. A successful classifier is not proof the original upstream package passed.

**Handoff state: PREPARED ONLY; distinct Test Architect R9 is NOT executed by creating this document.** No new project, branch, PR, external issue comment, merge, Founder-only approval change, or production use authorized.
