# AETHER X GLOBAL — AETHER TEST ARCHITECT

## OpenTelemetry Collector #16236 — Independent native R3 requalification (R4 adversarial execution)

**Mission:** `AXG-OTEL-16236-R3-INDEPENDENT-NATIVE-REQUALIFICATION-20261114`  
**Independent technical verdict:** **`PASS_SCOPED`** for the stated **direct on-disk bbolt adapter + Go exporterhelper queue package**, subject to the material adverse finding and exclusions below.  
**Broader crash/data-integrity, release, merger and upstream-publication verdict:** **NOT APPROVED / BLOCKED**.  
**Internal Draft:** [PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), retained Draft/unmerged. No upstream publication.

### Frozen identity and independence boundary

| Input | Source identity |
| --- | --- |
| Original upstream Collector baseline | `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0` |
| Upstream queue implementation SHA-256 | `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4` |
| Internal candidate SHA-256 | `c9705f155cd3c143da236741947689120670d17817c0244e386a4d138f86afce` |
| Pre-existing R3 native fixture SHA-256 | `c461fc2ceceb4217bb8545562d3a6c43f10495566ee72e833591141c8667329a` |
| Newly authored independent Go fixture SHA-256 | `dfead9a31cc205ebdce9484f1e98442994b19fe0608348649d6d7a0629a4ec0d` |
| Successful independently authored/operated CI HEAD | **`77fe44a90775a9b46a5237db684ac8fb20e98bb4`** |
| Original engineering R3 run HEAD, for historical comparison | `5520dcf0fe3367f29b722ccececb7094d346f77a` |

All SHA-256 source commitments above were checked **on the independent GitHub Actions runner** before the tests. Later branch commits only publish evidence/report and do **not** constitute new tested executions. The source changed from original R3 only by adding the independent fixture and its workflow; the experimental queue implementation was not altered. This review was performed through a separately authored/tested suite by the connected AETHER TEST ARCHITECT workflow, **not** through an independent human auditor, and is not a self-certified full product guarantee.

### Real execution and negative controls

- **Successful run:** [GitHub Actions #43528322682](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528322682), job `132239471072`, **SUCCESS**, Ubuntu 24.04, `go1.26.0 linux/amd64`, `go.etcd.io/bbolt v1.5.0`. `NoSync=false` (fsync enabled) on the direct bbolt storage adapter. Real child processes are terminated by operating-system **SIGKILL immediately after a returned committed bbolt `DB.Update`**, then database files are reopened in a fresh process.
- **Original unpatched baseline RED:** `go test -count=1 -v -timeout=5m -run '^TestAXGBboltSIGKILLRecovery$/^qmv0_first_committed$' ./internal/queue` ⇒ **exit 1**, SIGKILL confirmed, recovered physical/logical request IDs **only [33]** instead of [11,22,33].
- **Experimental candidate native SIGKILL GREEN:** `go test -count=1 -v -timeout=5m -run '^TestAXG(Independent|BboltSIGKILLRecovery)' ./internal/queue` ⇒ **exit 0**, SIGKILL confirmed for all three committed-cut scenarios, new queue format first and second cuts and legacy first cut. All three recover **[11,22,33]**.
- **New independent deterministic crash-free restart regressions:** four sequential persisted reopen/recovery cycles for each `qmv0` and legacy, **8/8** observed, with **both logical and physical bbolt-bucket inventory** [11,22,33] each time, no second physical copy of the test IDs.
- **Independent pre-commit fault injection:** forced `storage.ErrStorageFull` rejection when recovery tries to retire the old in-flight key; initialization returns an error, the native bbolt DB is reopened without committed retirement, and all three items survive in both inventories. **This is injected write rejection, NOT physical ENOSPC.**
- **Whole queue package:** `go test -count=1 -timeout=6m ./internal/queue` ⇒ **exit 0** with native tests and independent regressions included. Observed CI package output is PASS, about 8.27 seconds. No fuzz seed; tests are deterministic.
- **Confirmed adverse characterization — corrupt `qmv0`:** with real durable physical payloads **11,22** in bbolt, intentionally writing invalid consolidated metadata permits `initClient` to silently reset read/write indices. Reopened logical queue becomes empty while both physical payloads remain. The regression logs `AXG_INDEPENDENT_ADVERSE_FINDING`. This behavior is in the **inherited upstream `loadQueueMetadata` error branch**, not proven to have been introduced by this experimental fix. It is explicitly **not** a PASS for corrupted metadata, and must be mitigated or consciously accepted under a separate product contract before any broad data-retention claim.

**First independent attempt retained:** [run #43528063602](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528063602), HEAD `212c018646af57db1cc6535bc36ec3b9e4833fbe`, outcome FAILED. The independent test file used a candidate-only `initClient` return signature and was mistakenly compiled into the baseline phase. The runner logged a baseline compile error (so the original baseline RED oracle was not reached), while candidate native and package tests passed. A narrowly scoped **workflow-only** repair isolated candidate-only tests to the candidate phase, yielding the valid successful run above. This failure is preserved; it was not relabeled as a successful baseline reproduction.

### Evidence permanence, exact raw receipts and bidirectional links

**Canonical permanent evidence/index:** [R4 evidence index](evidence/EVIDENCE_INDEX.md). The evidence index links back to this report and both full CI run logs. The PR review comment must link this report and index.

- [Successful run full original GitHub job log](evidence/github_actions_run_43528322682_job_132239471072.log), [raw classified machine `result.json`](evidence/result.json) and [original 13-entry `SHA256SUMS` manifest](evidence/ORIGINAL_ARTIFACT_SHA256SUMS.txt): preserved in this Git branch.
- [Success run original artifact #14086630995](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528322682/artifacts/14086630995); **ZIP SHA-256 `3ee44600e7f7e7a64c290edf005e84144b952e08c97dc5959d892e7855a5fd50`**, 5,183 bytes; **13/13 original entry SHA-256 matches independently rechecked**; expires approximately **2026-12-13**.
- [Failed original-run full GitHub job log](evidence/github_actions_run_43528063602_job_132238623112_INITIAL_REVISE.log), [failed original artifact #14085687895](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528063602/artifacts/14085687895); ZIP SHA-256 `e84bc24cc6c8afb948710f8730d599c5dc6b715201976a71c5e116ac7b2536f9`, **13/13 entry SHA-256 matches rechecked**. This negative attempt is part of the history.
- [Original engineering R3 source report](../r3/R3_RESULT.md) and [its original 16-entry checksum manifest](../r3/evidence/SHA256SUMS.txt) remain accessible for contrast.

**Evidence retention limitation:** the *complete 13 original individual raw files* for the new independent run reside inside the GitHub Actions ZIP and may expire; the **complete GitHub job log, machine decision, original checksum manifest and evidence index** are committed permanently. The full `baseline_red.log` and `independent_native.log` files have not individually been re-committed; beyond ZIP retention they may require rerunning this pinned workflow. No claim of an immutable perpetual raw ZIP is made.

### Unexecuted tests and material limits

| Area | State / risk |
| --- | --- |
| Direct disk-backed bbolt committed-process-kill recovery | **PASS_SCOPED**, verified three cuts |
| Eight repeated restarts, full Go queue package and pre-commit fault injection | **PASS_SCOPED**, observed |
| Corrupt consolidated metadata `qmv0` | **Adverse finding**, logical payload inaccessibility under corrupted metadata |
| Real OpenTelemetry Contrib `file_storage v0.165.0` extension instantiated and started | **NOT_RUN**; adapter only |
| Full Collector distribution, lifecycle, real exporter delivery/ack receipts | **NOT_RUN** |
| Real disk exhaustion, ambiguous post-commit write error, torn writes/power loss, online compaction | **NOT_RUN** |
| Fully saturated durable backlog, scale/soak, randomized fuzz and explicit mutation score | **NOT_RUN** |
| Non-atomic `storage.Client.Batch` backends and exactly-once external delivery | **NOT_RUN**; no universal guarantee |
| Upstream maintainer design acceptance, human-authored upstream PR/description | **NOT OBTAINED / NOT POSTED** |
| Internal corporate production use or PR merge | **BLOCKED**; Founder-only exact approval and project gates retained |

### Minimal next engineering action

Keep PR #22 **Draft/unmerged**. Engineering should address/define the inherited metadata-corruption behavior through a deliberate separately scoped fail-closed/recovery policy; test real extension client lifecycle, storage errors (including ENOSPC), online compaction and externally observable duplicate/ack semantics using pinned actual Contrib `file_storage`. Then request a new independent targeted gate against the new exact HEAD, with genuine raw evidence. Do not turn this narrow bbolt adapter success into product-level lossless or power-failure certification. Do not publish AI-generated OpenTelemetry upstream issue/PR comments; any upstream PR description must be human-authored consistent with upstream `AGENTS.md`.

**Technical decision:** **`PASS_SCOPED`** for native direct-bbolt recovery invariant only. **Broad release/merge decision: BLOCKED**. 
