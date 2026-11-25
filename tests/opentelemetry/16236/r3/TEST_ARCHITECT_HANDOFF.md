# AETHER TEST ARCHITECT — Independent R3 Native Recovery Requalification

**Mission:** `AXG-OTEL-16236-R3-INDEPENDENT-NATIVE-REQUALIFICATION-20261114`  
**Priority:** HIGH — crash-consistency, migration, data loss prevention  
**Lead:** AETHER TEST ARCHITECT (independent from the experimental implementation author)  
**Repository:** `AETHERXGLOBAL/aether-x-open-contributions`  
**Internal Draft PR:** https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22  
**Branch:** `evidence/otel-queue-recovery-16236-r1-20261113`  
**Exact tested baseline commit:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`  
**Exact internal R3 executable test HEAD:** `5520dcf0fe3367f29b722ccececb7094d346f77a`  
**Current PR HEAD:** Verify live at the moment of review. Later reports/evidence commits are not claims of new executed tests.

## Independent cold-start objectives

1. **Authenticate source and tested identity:** independently fetch PR #22 current HEAD, compare the experimental `tests/opentelemetry/16236/r2/persistent_queue_candidate.go` SHA-256 against `c9705f155cd3c143da236741947689120670d17817c0244e386a4d138f86afce`, the native R3 test source SHA-256 `c461fc2ceceb4217bb8545562d3a6c43f10495566ee72e833591141c8667329a` and upstream baseline file SHA-256 `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`. Verify no code drift rather than accepting narrative HEAD alone.
2. **Repeat native baseline and candidate:** independently execute or independently qualify GitHub Actions [run #43522401439](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522401439), confirming real OS-level `SIGKILL` after a committed `bbolt.DB.Update` operation on a persisted fsynced database. Original baseline MUST show missing IDs `11,22` (RED); internal candidate must preserve `11,22,33` across new format first and second committed move cuts and legacy first move cut.
3. **Re-run existing and new Go package tests** on isolated pinned upstream source with candidate, and ensure `-count=1`. Record exact command, Go version, module version, actual exit code, PASS/FAIL and source hash.
4. **Adversarial falsification:** challenge the transaction invariant with commit failures, read/unmarshal faults, fully populated durable backlog, disk-full or write failure, metadata corruption, repeated restarts, qmv0 vs legacy compatibility, and duplicate physical delivery behavior. A mock storage client is not a substitute for testing on an actual persistent backend when claiming a native result.
5. **Product boundary:** check the exact Contrib `file_storage v0.165.0` implementation and distinguish a direct bbolt-backed test adapter from an actual running extension. If actual file_storage extension and full Collector distribution have NOT been exercised, explicitly limit any PASS to native bbolt adapter + Go queue package. Do not infer end-to-end, fsync-on-power-loss, no-duplicates or data retention under all backends.
6. **Evidence permanence:** report actual run ID, SHA-256 manifest, original raw stdout/stderr, both negative and positive results, source commit identity, all discrepancies and a bidirectional report/manifest link on the same internal PR #22. Review [R3 report](R3_RESULT.md), [original all-files manifest](evidence/SHA256SUMS.txt), [baseline native RED log](evidence/baseline_native_red.log), [candidate native GREEN log](evidence/candidate_native_green.log), and [original full job log](evidence/github_actions_run_43522401439_job_132219684042.log). The 17 original text evidence files are committed; original raw ZIP artifact ID `14083676099` expires 2026-12-13.

## Decision boundaries

Produce an evidence-backed independent **`PASS_SCOPED` or `REVISE`**, plus exact exclusions. This is not a grant to merge or publish upstream. Identify defects that would prevent even a scoped native pass. No paid cloud, privileged AWS, external communication, public issue comments, or external PRs. OpenTelemetry upstream forbids AI-generated issue/PR comments and requires human-authored PR descriptions; preserve that boundary. Company main and external publication remain Founder-controlled.

**No AETHER TEST ARCHITECT run is claimed by the authoring of this task.** It becomes a genuine independent review only if the distinct specialist actually executes it with its own verifiable evidence.
