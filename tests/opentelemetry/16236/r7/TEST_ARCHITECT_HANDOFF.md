# AETHER TEST ARCHITECT — Independent R7 requalification handoff

**Mission:** `AXG-OTEL-16236-R7-INDEPENDENT-LEGACY-REQUALIFICATION-20261114`  
**Source of Truth:** `AETHERXGLOBAL/aether-x-open-contributions`, internal Draft [PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22).  
**Engineering R7 tested HEAD:** `1188a18cb42dc3938337e2bd7ee06a0680224360`; verify live HEAD and code/test diff before executing.  
**Upstream pinned Collector HEAD:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.  
**Exact amended candidate SHA256:** `4b362e244ec5365ee6bfd5e5499bcba4be03078339fc3733943e2c8f71060d93`.  
**Exact R7 regression test SHA256:** `363c77238fc49c7148a4b575521a3ccaca4b13beaa979f5ae8e6f54023f87305`.  
**Original independent R6 defect regression SHA256 (must remain unchanged):** `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.

## Independent instructions

Execute a separate cold-start qualification, not a restatement of Engineering's GREEN. Re-run the original R6 independent `TestAXGTAR6CorruptLegacyMustFailClosedWithoutOrphaning` unchanged; ensure malformed two-byte `ri` forces a startup error, retains exact bytes, does not create `qmv0`, and preserves request 11 physically. Independently challenge corrupt `wi`, partially missing `ri/wi`, out-of-order `ri > wi`, trailing garbage, orphan `di` without indices, and valid new/legacy controls. Use the **actual published Contrib `file_storage` extension and its real bbolt database**, not a mock alone.

Stress historical R5/R6 crash, injection, duplicate physical inventory, and capacity tests. Consider additional counterexamples: empty-but-present legacy keys, untrusted oversized `di` array encoding, restart interrupted between qmv0 creation and legacy cleanup, and missing all metadata with on-disk numeric payloads. Clearly separate newly tested cases from untested limitations.

**Crucial non-waivable remaining blocker:** execute the unchanged original upstream Go queue package in full; the expected remaining `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` cases still FAIL under the proposed qmv0 fail-closed policy, and upstream maintainers have **not** approved changing that contract. No broad PASS, ready-for-review, merge or external PR should be claimed.

## Evidence to audit

- [R7 engineering report](R7_ENGINEERING_RESULT.md) ↔ [R7 evidence index](evidence/EVIDENCE_INDEX.md).
- Before-fix [actual RED](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538751874), tested HEAD `7c15dd3bdcfc9c6bd76efee9a65e1ffc830b78b8`.
- Compile error [negative run](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538804092), tested HEAD `afb6346de405233c4d5f934cd1350a58550310d0`.
- Amended code [actual GREEN](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538951873), tested HEAD `1188a18cb42dc3938337e2bd7ee06a0680224360`.
- Original RED and GREEN ZIP artifacts, source/fixture SHA256, actual original machine-classified results and permanent full runner console logs. The two ZIPs were downloaded and verified **19/19 and 19/19 SHA256**; the individual ZIP contents are time-limited and not all individually stored in Git.

Publish an independently reproduced result with exact new tested HEAD, actual original stdout/stderr, exit codes, negative cases, SHA256 manifest and mutually linked report on **same existing internal PR #22**. Do not alter engineering candidate or the original TA R6 test, impersonate an independent human reviewer, open new PRs, contact upstream, merge or publish.

**Handoff status: PREPARED ONLY. Distinct AETHER TEST ARCHITECT independent R7 execution NOT performed by Engineering.**
