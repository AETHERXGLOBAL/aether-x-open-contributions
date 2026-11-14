# AETHER TEST ARCHITECT — R6 independent requalification handoff

**Mission:** AXG-OTEL-16236-R6-INDEPENDENT-REQUALIFICATION-20261114  
**Repository:** AETHERXGLOBAL/aether-x-open-contributions  
**Internal Draft:** https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22  
**Engineering execution HEAD:** b42bb0aeefd4ac30a4d10a9b82f2308563c6a0f6  
**Upstream pinned HEAD:** 572057cde7e9bbe3aed6e5e3e8f16290d487f7d0  
**Experimental candidate SHA-256:** 52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446  
**R6 fixture SHA-256:** c09f2f0a72b5c49da3d4812b68ad2a1212f31c7522c29b04b5d12919158d4a1b

## Independence and requested tests

The authored R6 workflow is ENGINEERING evidence, not an AETHER TEST ARCHITECT independent judgment. The separate specialist must obtain live current PR HEAD, verify that candidate and fixture bytes have not drifted, execute its own cold-start checks and archive its own original evidence.

Assess independently:
- Actual Contrib file_storage v0.165.0 factory lifecycle + bbolt FSync and real post-commit subprocess SIGKILL; no handcrafted client substitution.
- Precommit injected storage.ErrStorageFull and a postcommit error where underlying Contrib Batch already committed: evidence of durable physical and logical inventory after fresh reopen, no phantom duplicate keys.
- Durable at-capacity recovery, acknowledged vs unacknowledged request replay, deterministic repeated starts, legacy and qmv0 compatibility.
- Explicitly classify all untested boundaries: real disk exhaustion, power loss, non-atomic storage, compaction, full Collector and exactly-once exporter delivery.
- Run **the entire original upstream package without skipping or modifying tests**. Original cases TestPersistentQueue_CorruptedData/corrupted_metadata and /corrupted_everything currently FAIL by design-contract conflict. Do not issue broad PASS while they fail; identify alternative design or a genuine maintainer-approved test-contract change.
- Report independent PASS_SCOPED / REVISE only within exact proven boundaries. Do not claim upstream maintainer acceptance, merge, public contribution or production readiness.

## Source evidence to falsify

- [R6 engineering report](R6_ENGINEERING_RESULT.md).
- [R6 evidence index](evidence/EVIDENCE_INDEX.md), with complete original job log, byte-exact original JSON result, SHA256 manifest and original exit codes.
- [Original R6 GitHub Actions run](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43534103589) at tested HEAD b42bb0aeefd4ac30a4d10a9b82f2308563c6a0f6, SUCCESS for scoped classifier.
- Original full suite exit **1**. Original focused test exit **0**. The original remaining failures are a current BLOCK.
- [Prior independent R4 outcome](../r4/TEST_ARCHITECT_R4_RESULT.md) applied to the older experimental source and **does not approve R5/R6**.

**Publication contract:** separate reviewer should publish actual independent raw stdout/stderr and material results with tested HEAD, SHA256 manifest and mutually linked report on the same existing internal PR #22. Do not open a new project or PR, modify candidate source, post external comments, authorize merge, waive original failures, or claim that this handoff itself constitutes an independent execution.

**CURRENT STATUS: HANDOFF_PREPARED, NOT EXECUTED BY THE DISTINCT SPECIALIST.**
