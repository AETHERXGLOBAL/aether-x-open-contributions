# Apache DataFusion Ballista #2936 — engineering candidate checkpoint

**AETHER X GLOBAL — 26 November 2026.** This is a candidate-only source checkpoint, not an accepted upstream contribution, test execution receipt, portfolio upgrade or merge authorization.

- [Upstream issue #2936](https://github.com/apache/datafusion-ballista/issues/2936): open, no assignee and no comments at the inspected snapshot. No directly matching open PR was found in the searches.
- [Previous contribution #2775](https://github.com/apache/datafusion-ballista/pull/2775): merged on 24 November; historical record unchanged.
- Upstream base: [a879ad07d204d26df702c681fcb8101dfa1e6c2c](https://github.com/apache/datafusion-ballista/commit/a879ad07d204d26df702c681fcb8101dfa1e6c2c); tree d570c1a59c7aaf8f5c69b598b3e72c58b6e8d941.
- [Engineering candidate branch](https://github.com/AETHERXGLOBAL/datafusion-ballista/tree/fix/2936-standalone-private-workdir), exact [HEAD 45a02407caf8ad7da232b1110d94f648a81461d4](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/45a02407caf8ad7da232b1110d94f648a81461d4), tree 8ba5fcd36b2d131f79db9f128667b52df17e9a81.
- [Initial regression source commit](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/ec3222a4e5f2925d3b3a72cc75dfa877f39d681b), followed by the API-aligned [original-bug control](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/bc9d2cc95c3ca9ff296b722179819fccea8e5d9c), tree fa6644f46cbaa7d98238482ce06100844706483e. The original defect remains in the control.
- [Fork-only exact-source qualification workflow](https://github.com/AETHERXGLOBAL/datafusion-ballista/blob/488b1a3bbff5aedde79f99422da6f8c164a53683/.github/workflows/ax-2936-qualification.yml). Not included in the upstream patch.
- [Complete candidate diff](https://github.com/AETHERXGLOBAL/datafusion-ballista/compare/a879ad07d204d26df702c681fcb8101dfa1e6c2c...45a02407caf8ad7da232b1110d94f648a81461d4): 3 commits, 5 Rust files. No change to either repository's main branch.

## Scope and evidence status

Shared TempDir ownership is attached to executor instances and Flight services/streams/readers, rather than the returning builder or a new global registry. The private-directory helper from #2775 is reused; invalid UTF-8 is returned as a configuration error. Flight startup in push mode is delayed until successful registration. No SessionContext-drop shutdown contract is claimed.

Regression source covers pull/push startup, real Flight range read, runtime shutdown, push registration rejection/cancellation, invalid UTF-8, and lazy stream lifetime. Permission tests check 0700; the workflow proposes executing under umask 022 and 077. Separate in-flight real shuffle-task cancellation and detached child writer behavior remain to be independently assessed. The existing stop channel semantics and runtime boundary are not newly defined by this patch.

| Gate | Status |
| --- | --- |
| GitHub source and branch verification | Verified |
| Rust RED run | NOT EXECUTED |
| Rust GREEN run | NOT EXECUTED |
| Format / Clippy / Cargo check | NOT EXECUTED |
| GitHub Actions | No run observed for exact candidate or qualification workflow |
| Independent Test Architect / Security / Assurance | Pending |
| Upstream issue claim / PR / maintainer approval / merge | Not performed |

**Status:** TEST_CANDIDATE_PREPARED / EVIDENCE_PENDING / NOT READY FOR FINAL ACCEPTANCE OR MERGE.

The qualification workflow records expected commands and pins both trees. It is not a substitute for actual run IDs, exit codes, logs and durable SHA-256 evidence manifests. Those remain pending. The upstream publication gate remains separate; no claim of Apache endorsement, accepted code or completed contribution is made.

## Follow-up checkpoint — dedicated runtime ownership

This checkpoint supersedes only the earlier candidate pointer above; historical candidate/control records are retained.

- [Issue #2936](https://github.com/apache/datafusion-ballista/issues/2936) is assigned to `aetherxeg-source` after the [Founder-authorized take comment](https://github.com/apache/datafusion-ballista/issues/2936#issuecomment-7177097210). No upstream PR is open for this candidate.
- Reverified upstream HEAD: `a879ad07d204d26df702c681fcb8101dfa1e6c2c`.
- [Revised candidate HEAD](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/2d04b04b405dc055108391ebd9b05a20e1730e93): `2d04b04b405dc055108391ebd9b05a20e1730e93`; tree `958441100c6a120556df452a2ab439ff54d4308b`.
- [Exact diff from upstream](https://github.com/AETHERXGLOBAL/datafusion-ballista/compare/a879ad07d204d26df702c681fcb8101dfa1e6c2c...2d04b04b405dc055108391ebd9b05a20e1730e93): 5 commits, 7 Rust source files, no workflow in upstream patch.
- [Original-bug control](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/bc9d2cc95c3ca9ff296b722179819fccea8e5d9c) unchanged.
- [Re-pinned fork-only qualification workflow](https://github.com/AETHERXGLOBAL/datafusion-ballista/blob/2311053a960d903966a1e08f8e19b17bd3229513/.github/workflows/ax-2936-qualification.yml).

Source review found that dedicated Tokio task runtimes can outlive an individual task during cancellation, including blocking descendants. The owner is now also retained across dedicated runtime destruction on pull and push paths. Added tests use the existing real passthrough ShuffleWriterExec cancellation fixture for two tasks, check caller-owned directories, and use a pending async task plus a blocking child to synchronize a shutdown-boundary regression. Runtime teardown is asynchronous relative to outer runtime drop; the standalone test now waits with a bounded deadline rather than assuming immediate cleanup.

The tests are source candidates only. The local execution environment has no rustc, Cargo, rustfmt, protoc, or GitHub CLI and cannot resolve github.com. Available connected tools do not expose workflow dispatch. No runtime, build, formatting, Clippy, CI success or independent review is claimed. The next stage is exact-source execution of the unchanged RED and revised candidate, confirmation of actual original-bug failure (not build failure), all candidate tests and lint, followed by independent review. No automatic PR submission, release or merge.

**Current status: TEST_CANDIDATE_PREPARED / EVIDENCE_PENDING / NOT READY FOR FINAL ACCEPTANCE OR MERGE.**

## First hosted CI execution and formatting delta

Fork Actions re-enabled by Founder; workflow dispatch verified against pinned SHAs:
- [RED run 45719905225](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719905225) at `bc9d2cc95c3ca9ff296b722179819fccea8e5d9c`.
- [Candidate run 45719911744](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719911744) at `2d04b04b405dc055108391ebd9b05a20e1730e93`.
- Both runs have unfinished build/test jobs. Lint failed in both; the candidate's [Lint log](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719911744/job/139575335979) specifically reports seven rustfmt diff hunks across four files, exit 1. Applied those exact hunks only in [formatting successor] (https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/0a9e79d484b912f72437f2ec14f95504d93ca7e6), tree `cba6666412ede92a2b95ee8d6dc824cb83b139ce`. Existing runs remain pinned to their original commits; their eventual results do not certify this successor. No RED regression outcome yet. No independent signoff or upstream PR.
- Qualification workflow re-pinned to successor, commit `bf193d42e92769f02868c6f7813530c800a1703e`.

Status: CI_STARTED / FORMAT_CORRECTED_UNVERIFIED / EVIDENCE_PENDING.

## Hosted RED/GREEN evidence and qualification harness repair

Verified job outcomes from official Ballista Rust CI, exact pinned commits retained:

- RED `bc9d2cc95c3ca9ff296b722179819fccea8e5d9c`: [linux crates job](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719905225/job/139575317659), [linux Ballista job](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719905225/job/139575317765). Both logs report the two intended panics: `standalone pull-staged removed its work directory during startup` and `standalone push-staged removed its work directory during startup`. Executor test result: 114 passed, 2 failed, exit 101. RED reproduced, not compilation failure. Lint failed separately.
- GREEN `2d04b04b405dc055108391ebd9b05a20e1730e93`: [linux crates](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719911744/job/139575336151), [linux Ballista](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719911744/job/139575336121), each successful; executor 123 passed, 0 failed. Named passes include standalone pull/push lifetime, registration cancellation/failure, caller-owned directory, multiple shuffle cancellation, and dedicated-runtime blocking child. Existing standalone push/pull integration tests passed. Cargo check, Clippy, benchmarks, Linux workspace, docs and ancillary jobs passed. macOS still in progress at observation. Lint failed; successor `0a9e79d484b912f72437f2ec14f95504d93ca7e6` is not yet qualified.
- [Fork-only qualification run 45720314297](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45720314297/job/139576706550) failed before tests at Git's dubious ownership check in the ephemeral container. No code failure established by that run. Harness repair [a28d1f283fe052a9bb3d5ae4ec259f3a6eac8e4a](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/a28d1f283fe052a9bb3d5ae4ec259f3a6eac8e4a) scopes safe.directory to the checked-out workspace only, retains exact candidate SHA/tree checks and read-only token; removes duplicate RED execution now supported by official logs. Candidate and RED branches unchanged by this harness repair. No new qualification success claimed.

Status: RED_PROVEN / GREEN_LINUX_R2_PROVEN / FORMAT_SUCCESSOR_QUALIFICATION_PENDING / INDEPENDENT_REVIEW_PENDING. No upstream PR or merge.

## Exact-source Linux success and macOS portability delta

- [Qualification run 45723518219](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45723518219/job/139587466114) completed successfully on source `0a9e79d484b912f72437f2ec14f95504d93ca7e6`, tree `cba6666412ede92a2b95ee8d6dc824cb83b139ce`: exact identity assertions, 123 passed/0 failed executor tests under umask 022, 4 passed/0 failed standalone tests under umask 077, rustfmt, git diff check, cargo check and Clippy all passed.
- [macOS candidate job](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719911744/job/139575335941) on `2d04b04b405dc055108391ebd9b05a20e1730e93`: 122 executor tests passed, one failed at fixture creation (`std::fs::create_dir`, OS error 92 Illegal byte sequence), before the intended path conversion. Both standalone lifecycle tests and cancellation tests passed. [macOS RED](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45719905225/job/139575317726): 114 passed/2 intended lifecycle failures.
- [Portable successor](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/85dabe6fde55ffa4685bc354be04808c5510aa07), tree `fbfea41229e7fb7bb2c1ebc0e0cd1853b383e9d6`: extracts existing path conversion without changing behavior, tests non-UTF-8 conversion independently of filesystem on Unix, retains real non-UTF-8 directory cleanup fixture on Linux. No unrelated changes. [Fork-only harness](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/4067ff419f5c1113ce09b786fcb52a21b206cffe) pins successor and runs Linux qualification plus macOS workspace tests using upstream test command. [Run 45724870888](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45724870888): in_progress, conclusion pending at observation.

Status: RED_PROVEN / GREEN_LINUX_PREDECESSOR_PROVEN / PORTABILITY_SUCCESSOR_QUALIFICATION_PENDING / INDEPENDENT_REVIEW_PENDING. No upstream PR or merge.

## Independent qualification gate — review handoff (READ_ONLY)

Review target: `85dabe6fde55ffa4685bc354be04808c5510aa07`, tree `fbfea41229e7fb7bb2c1ebc0e0cd1853b383e9d6`. Active hosted run [45724870888](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45724870888). Do not infer final candidate success from predecessor success. Preserve already established RED evidence; do not rerun accepted tests without a documented reason.

Required independent review decisions:

1. Test Architect: confirm exact-source CI, expected RED assertion failures, GREEN Pull/Push lifetime (including real Flight gRPC range reads), 0700 under both umasks, invalid path structured error and real Linux cleanup, registration rejection/cancellation, caller-owned directory preservation, concurrent real ShuffleWriterExec cancellation, dedicated-runtime blocking-child quiescence, and upstream real standalone SQL integration tests. Check whether the two regression controls are equivalent at the original failure boundary. Distinguish fixture data from real query integration evidence.
2. Security: inspect every owner and release boundary (Executor, dedicated runtime, Flight backend, do_get/do_action streams, blocking reads, detached child work, cleanup tasks); verify no use-after-delete/recreation window, no premature deletion of another executor's directory, unchanged externally supplied directory behavior and no public API/security weakening. Inspect failure/cancellation and scheduler stop semantics against upstream behavior.
3. Assurance: independently reconcile commit/tree identities, immutable hosted run/job records, full actual outcomes including macOS, and exact delta; report any unresolved scope or contradictory evidence. Confirm minimality of the patch and no hidden test exclusions beyond the documented filesystem-specific fixture. Final claims must be tied to exact candidate SHA.
4. Scope limits: current direct ownership test exercises do_action range stream; do_get ownership is implemented via the same wrapper but not directly established by the specific owner-drop test. Existing standalone SQL integration tests are separate from the lifecycle fixture. Direct multi-executor cleanup isolation and real shutdown while an in-flight Flight read and Shuffle write overlap have not been established as a combined end-to-end test. The directly tested standalone teardown boundary is runtime destruction, not an independently promised SessionContext-drop or StopExecutor RPC shutdown contract. Review these gaps for materiality; require a targeted falsifier if needed, not broad test repetition or speculative scope expansion.

No claim of completed independent review. Publication remains gated on evidence, review and separate Founder approval of the exact upstream PR. No merge authorized.

## Test Architect independent verdict received — consolidated closure gate

Received the Founder-supplied AETHER TEST ARCHITECT report dated 2026-11-26 for exact candidate `85dabe6fde55ffa4685bc354be04808c5510aa07`, tree `fbfea41229e7fb7bb2c1ebc0e0cd1853b383e9d6`. Report verdict: **NO_GO for final qualification/publication; original fix PASS_SCOPED; Linux PASS; test strength STRONG; macOS PENDING**. This records the submitted review, not an independently authenticated agent execution receipt. Commander rechecked [Linux job 139592053215](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45724870888/job/139592053215) and actual logs: exact SHA/tree match; 124 passed, 0 failed, 0 ignored under umask 022; 4 passed, 0 failed under umask 077; format, diff check, cargo check all targets and Clippy all successful. macOS remained in progress when checked. Prior RED remains proven and must not be repeated without cause.

### Open independent findings

| ID | Severity | Required falsifiable closure |
| --- | --- | --- |
| TA-B2936-01 | HIGH | Two independent executors A/B with distinct work directories; tear down A, assert only A directory disappears; demonstrate B can still read/write; then tear down B and prove cleanup. |
| TA-B2936-02 | HIGH | Deterministic synchronization barriers with Flight read and actual Shuffle write overlapping runtime teardown; assert directory remains until all real users release; assert final deletion and no recreation; verify task/child quiescence. |
| TA-B2936-03 | MEDIUM | Real Arrow IPC do_get stream; release service owner while stream is live; assert decoded values and directory lifetime across completion or cancellation, including outstanding blocking readers. |

These are coverage deficiencies, not three demonstrated implementation failures. Preserve architecture unless a targeted test or security review establishes a defect. Do not redefine SessionContext-drop or StopExecutor contracts merely to expand scope.

### Execution handoff — one consolidated delta

AETHER SECURITY: READ_ONLY independent review of exact pinned source, outstanding owner/cleanup/recreation boundaries, failure/cancellation and all three findings above. Return all material findings together; distinguish code defect, coverage gap, and pre-existing out-of-scope behavior. No code changes or repetition of accepted tests. The security report is to be consolidated with the Test Architect findings before Engineering closes the batch.

AETHER ENGINEERING: implement the minimum necessary targeted tests and any proven fixes on the existing candidate branch, in a single batch after consolidation. Use real executor/Flight/Shuffle paths, deterministic barriers, bounded timeouts, no fixed sleeps as synchronization, no production test hooks unless justified, no public API changes, no added dependency unless unavoidable and documented. Preserve prior RED and accepted evidence. Add targeted negative controls on separate test-only refs or isolated worktrees (remove the specific ownership protections), showing expected assertion failure rather than compile error, then restore and prove GREEN. Keep qualification-only files out of the upstream diff. Pin exact new SHA/tree; run impacted tests and applicable lint/build/platform gates, including macOS qualification of the final source. Record actual log/job links, test names, exit outcomes, source/negative-control identities and evidence SHA-256 manifest; retain raw logs or evidence artifacts under repository publication policy without exposing secrets. Do not claim tests executed without evidence. If a control or artifact cannot be produced, state the blocker. No upstream PR or merge.

AETHER TEST ARCHITECT and AETHER SECURITY: independent DELTA_ONLY re-review after engineering delivery. AETHER ASSURANCE: final evidence provenance and scope reconciliation, including independent review receipts and published evidence custody. Founder approval of exact upstream PR remains separate.

Status: **NO_GO_PUBLICATION / RED_PROVEN / LINUX_124_OF_124 / MACOS_PENDING / THREE_TECHNICAL_FINDINGS_OPEN / SECURITY_AND_ASSURANCE_PENDING / EVIDENCE_GATE_BLOCKED**.

## Consolidated independent review disposition — AX-OSS-APACHE-BALLISTA-2936-002

Founder supplied AETHER SECURITY review dated 2026-11-26 for candidate `85dabe6fde55ffa4685bc354be04808c5510aa07`, tree `fbfea41229e7fb7bb2c1ebc0e0cd1853b383e9d6`. Submitted verdict: NO_GO final security/publication; original fix PASS_SCOPED; ownership architecture ACCEPTABLE; zero newly introduced code defects identified by reviewer; engineering continuation GO. This records the supplied review, not authenticated independent execution receipts. Commander rechecked candidate identity and [run 45724870888](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45724870888): Linux success, macOS in progress at observation. Prior RED and accepted evidence retained.

### Authorized engineering batch D1–D5 (supersedes earlier handoff sequencing)

- D1 / TA-B2936-01: independently owned executor directories; A teardown deletes only A; B remains operational for real reads and writes; then B teardown cleans B.
- D2 / TA-B2936-02: deterministic overlap of real Shuffle writes, Flight reads and runtime shutdown; demonstrate quiescence, no premature deletion, no recreation following final cleanup.
- D3 / TA-B2936-03 and SEC-B2936-01: real Arrow IPC do_get ownership, decoded values and completion/cancellation; cover affected range, whole-file and sort-shuffle reads, including pending asynchronous filesystem/blocking operations. Do not substitute synchronous mock reads for actual I/O. Integrate cases where meaningful, document any remaining unproven boundary.
- D4: targeted ownership-removal negative controls in isolated test-only refs/worktrees; assert intended regression failure rather than build failure; preserve original RED evidence; positive controls on exact final source.
- D5: final source identity, impacted tests, Linux/macOS qualification, umasks 022/077, rustfmt, diff check, cargo check, Clippy and applicable upstream integration tests. Reuse accepted evidence only with explicit scope and delta justification. Store actual logs, commands, exit codes, test names, source identities and SHA-256 evidence manifest under publication policy; no secrets or unrelated security details.

Retain existing architecture unless a targeted falsifier demonstrates a defect. No broad rework, public API change, new dependency without justification, or change to pre-existing scheduler/Job cleanup contracts. Avoid sleeps as synchronization; bounded timeouts and deterministic barriers. Qualification-only files remain off upstream candidate diff. No external PR or merge. Any unrelated security matter must remain in separate confidential handling; no details or reproduction steps in this public repository. Do not claim broad platform security or guarantees beyond actual runtime lifecycle scope.

Engineering delivers a single pinned successor with actual code, tests and evidence, not another plan. Independent Test Architect and Security DELTA_ONLY re-review required; Assurance reconciles evidence integrity and review provenance. Final external publication requires exact-content Founder approval. No independent gate closed merely by this checkpoint.

Status: ENGINEERING_DELTA_GO / TECHNICAL_FINAL_NO_GO / SECURITY_FINAL_NO_GO / MACOS_PENDING / EVIDENCE_GATE_BLOCKED / UPSTREAM_PUBLICATION_BLOCKED.


## Engineering D1–D5 execution checkpoint — candidate source published; qualification in progress

AETHER X GLOBAL engineering implemented the authorized delta on the existing fork candidate branch without changing production implementation, main, the original RED baseline, upstream issue discussion, or creating a PR. This checkpoint is not an independent review or a completion receipt.

- [Pinned successor source](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/f6ddcb66d947b72ea8d1d6c592bbd19f98c12968): HEAD `f6ddcb66d947b72ea8d1d6c592bbd19f98c12968`, tree `d4da6c2c25325e29050b2a2a66096a9afaa95bcf`; remote branch re-read and both identities matched.
- [Delta from reviewed predecessor](https://github.com/AETHERXGLOBAL/datafusion-ballista/compare/85dabe6fde55ffa4685bc354be04808c5510aa07...f6ddcb66d947b72ea8d1d6c592bbd19f98c12968): 4 commits, 3 Rust test-containing files, 565 added lines, no production change or new dependency.
- [Fork-only pinned qualification workflow](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/ba9dde43be1df6fa4ecc3a6034398e1c868fbfaa), [actual push-triggered run 45726676278](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278). Workflow is separate from the proposed upstream source diff.

| Batch | Implemented source or runner action | Observed result |
| --- | --- | --- |
| D1 | `standalone_independent_work_dirs_survive_peer_shutdown`: distinct real pull/push standalone runtimes, actual ShuffleWriterExec writes and decoded gRPC Flight reads before and after peer teardown; bounded cleanup observation | SOURCE_PUBLISHED / EXECUTION_PENDING |
| D2 | `owned_shuffle_and_flight_overlap_runtime_shutdown`: actual pending ShuffleWriterExec, real lazy Flight byte read, dedicated runtime shutdown, input-poll notification, gated blocking descendant, join and final cleanup checks | SOURCE_PUBLISHED / EXECUTION_PENDING |
| D3 | `owned_ipc_do_get_completion_and_cancellation`, `owned_ipc_block_transport_pending_io`: actual Arrow IPC stream/file/sort fixtures, decoded values, byte equality, occupied blocking-pool barrier, completion and cancellation | SOURCE_PUBLISHED / EXECUTION_PENDING |
| D4 | Fork-only isolated worktree controls for runtime, decoded-response, blocking-reader, block-response owners; expected assertion marker and failed-test count plus exit 101; patch, command, log, exit and manifest artifact prescribed | RUN_STARTED / NO_CONTROL_RESULT_YET |
| D5 | Exact candidate checks and Linux/macOS delta tests under both umasks; Linux format, diff check, cargo check and Clippy configured | RUN_STARTED / NO_FINAL_RESULT_YET |

At observation, [Linux job 139598181218](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278/job/139598181218) was in progress at container initialization; [macOS job 139598180811](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278/job/139598180811) was in progress after successful candidate identity verification and setup. These are actual hosted job records, not completed tests. The predecessor's Linux qualification remains accepted within its own SHA; predecessor macOS [job 139592053603](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45724870888/job/139592053603) remains in progress. Original RED remains unchanged.

Important boundaries: D1 executes the real writer within each standalone runtime, not via scheduler task delivery. D2 signals entry into the real writer's pending input and verifies runtime cancellation/quiescence while a Flight response and separately gated blocking descendant overlap; the descendant gate is not a direct instrumentation of the actual writer's blocking file operation. D3's cancelled asynchronous Tokio filesystem operations are drained before final cleanup assertion; it does not establish that every cancelled OS read independently retains directory ownership after the response drops. Do not overstate these boundaries. The new test source has not yet been compiled or formatted in this session. Upstream integration evidence from predecessor is retained; fresh applicability to the successor and any remaining required integration run must be reconciled. D4 artifact generation and SHA-256 evidence manifest are configured, not observed; actual logs and durable evidence custody remain pending. Local environment lacks Cargo, rustc, rustfmt, protoc and GitHub network resolution; hosted CI is used instead.

**Status: ENGINEERING_SOURCE_PUBLISHED / EXACT_CANDIDATE_PINNED / HOSTED_CI_IN_PROGRESS / D1–D5_NOT_CLOSED / EVIDENCE_PENDING / INDEPENDENT_DELTA_REVIEW_PENDING / UPSTREAM_PUBLICATION_BLOCKED.** No external PR or merge. No independent gate changed. Next permitted action: inspect exact job logs, address concrete build/test/lint failures, preserve actual sanitized evidence and source identity, then route independent delta reviews and Assurance; exact-content Founder approval remains separate.

## D1–D5 hosted results and rustfmt-only successor

Commander verified [run 45726676278](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278) on pinned candidate `f6ddcb66d947b72ea8d1d6c592bbd19f98c12968`, tree `d4da6c2c25325e29050b2a2a66096a9afaa95bcf`. Linux GREEN tests (5 owned tests + 1 peer-isolation test per umask 022/077) passed. macOS ownership-delta qualification passed. D4 isolated controls all passed the intended failure gate: runtime AX2936_RUNTIME_OWNER, decoded response AX2936_RESPONSE_OWNER (sort), blocking AX2936_BLOCKING_OWNER (whole), block response AX2936_BLOCK_RESPONSE_OWNER (range); each actual test failed with one failed test and exit 101, not a build failure. [Linux log](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278/job/139598181218); [macOS log](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278/job/139598180811). Evidence artifact [15074857491](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45726676278/artifacts/15074857491), 7785 bytes, GitHub-reported digest `sha256:9ecbdf579a148dc932cf0bd6ac1614370700c8501785b7ab95f6689f863bcf97`; SHA256SUMS generated and upload successful. Artifact bytes and internal checksums have not been independently retrieved/recomputed; retention expires 2027-02-24. D2/D3 proof limitations remain as previously recorded. Format failed on 12 rustfmt hunks; Cargo check/Clippy skipped. Overall run failure is therefore not a functional test failure.

Applied exactly the 12 observed rustfmt hunks in three test files, preserving code tokens modulo whitespace and trailing commas. Verified successor [6831465ca3445bbc1ee612534cdefda533b25e41](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/6831465ca3445bbc1ee612534cdefda533b25e41), tree `fc4b732e26e56b8a171b70356ebab657992ee9fb`. Fork-only [workflow delta](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/7d39edec6c12faa362a11d900bd09c7557844b5a) checks exact successor identity, formatting delta, rustfmt, git diff check, cargo check and Clippy; [run 45727659655](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45727659655) started, not yet completed. Prior successful tests and mutations are retained as predecessor evidence with a formatting-only transfer rationale; no claim of rerunning them on successor. Predecessor workspace macOS job 139592053603 still in progress at observation; not confused with passing delta macOS job. No external PR or merge. Independent DELTA_ONLY review and final evidence custody remain required.

Status: D1–D5_POSITIVE_AND_MUTATION_TESTS_PROVEN_ON_PREDECESSOR / FORMAT_SUCCESSOR_CHECKS_PENDING / D2_D3_PROOF_LIMITS_OPEN / INDEPENDENT_REVIEW_PENDING / UPSTREAM_PUBLICATION_BLOCKED.

## Commander evidence custody verification and independent delta handoff

Downloaded original D4 artifact ID 15074857491 from GitHub Actions, run 45726676278, into the review environment. Recomputed archive SHA-256 `9ecbdf579a148dc932cf0bd6ac1614370700c8501785b7ab95f6689f863bcf97`, matching GitHub-reported digest; size 7785 bytes; ZIP CRC check passed; all 17 entries listed in SHA256SUMS matched actual extracted bytes. source.txt pins `f6ddcb66d947b72ea8d1d6c592bbd19f98c12968`, tree `d4da6c2c25325e29050b2a2a66096a9afaa95bcf`. Checked all four exit files (101) and actual log assertions, each 0 passed/1 failed: runtime AX2936_RUNTIME_OWNER; response AX2936_RESPONSE_OWNER: sort; blocking AX2936_BLOCKING_OWNER: whole; block_response AX2936_BLOCK_RESPONSE_OWNER: range. This is Commander custody verification, not independent Assurance approval. Artifact expiry remains 2027-02-24; preserve original archive outside expiring CI storage under evidence policy. No replacement or regeneration of original bytes.

Current review target: `6831465ca3445bbc1ee612534cdefda533b25e41`, tree `fc4b732e26e56b8a171b70356ebab657992ee9fb`. [Exact-source build delta job](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45727659655/job/139601475414): formatting-only comparison and rustfmt/diff check passed; cargo check in progress, Clippy pending at observation. Full predecessor macOS workspace job 139592053603 still in progress; the macOS delta tests on f6ddcb66 passed. No further rerun or source change initiated.

### Independent review assignment — DELTA_ONLY / READ_ONLY

Test Architect and Security: review current target vs reviewed 85dabe6f and test predecessor f6ddcb66. Validate D1 actual isolation, D2 synchronization and whether the separate gated blocking child sufficiently proves the real writer's release boundary, D3 completion/cancellation and residual Tokio filesystem lifetime limitation. Assess each D4 control's scope, assertion specificity and coverage, including whether further controls are materially necessary; do not infer proof of D1 or every D2/D3 boundary from four mutations alone. Assess formatting evidence transfer with exact diff (normalization comparison alone is not a semantic proof), complete current CI results, predecessor integration applicability, and necessity/minimality of tests. Decide each TA-B2936-01–03 and SEC-B2936-01 individually, distinguish actual defects vs gaps vs out-of-scope prior behavior. Return consolidated GO/NO_GO with exact SHA/tree and no code change. Independent Assurance after both verdicts: verify original artifact bytes/manifest, provenance, receipts, durable custody and scope, and final build/integration evidence. Final approval and external publication remain blocked pending these gates and explicit Founder authorization. No merge.

## Final Test Architect delta verdict received — narrow remaining closure

Founder supplied independent Test Architect report dated 2026-11-26 for exact candidate `6831465ca3445bbc1ee612534cdefda533b25e41`, tree `fc4b732e26e56b8a171b70356ebab657992ee9fb`. Report: NO_GO final qualification/publication; TA-B2936-01 CLOSED; TA-B2936-02 PARTIAL/OPEN; TA-B2936-03 CLOSED_SCOPED; D4 PASS (four targeted mutations); evidence integrity and formatting-only evidence transfer accepted within scope. 24 recorded successful executions (six selected tests x two umasks x two platforms), not 24 unique tests. No new production defect identified. These are supplied review findings; authenticated institutional review receipts remain a separate Assurance gate.

Commander independently rechecked [final build job 139601475414](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45727659655/job/139601475414): completed failure, exact-source/formatting-delta/rustfmt/diff check/cargo check all targets PASS, Clippy FAIL (exit 101), two actual `clippy::async_yields_async` diagnostics in executor.rs lines 746 and 758. Candidate HEAD/tree unchanged. Predecessor full macOS workspace job 139592053603 still in progress at observation; passing macOS delta remains accepted separately. Do not blindly await the nested handles: that would await a blocked child before release of its gate. Preserve handoff of child completion without suppressing lint or weakening synchronization.

### Remaining gate and next authorized action

AETHER SECURITY: independent READ_ONLY DELTA_ONLY review of exact current target; rule individually on TA-B2936-02 and residual SEC-B2936-01/D3 cancelled filesystem work; accept scoped closures only with rationale, identify any genuinely material remaining defect or proof gap, assess safe Clippy correction and negative-control applicability. Preserve D1, scoped TA-B2936-03, D4 and evidence transfer accepted by Test Architect; no re-execution of accepted tests without a documented reason. Return consolidated GO/NO_GO; unrelated security matters remain confidential and outside public ledger details.

After Security verdict, Engineering receives a single minimal closure delta: TA-B2936-02 direct deterministic synchronization at the actual writer's completion boundary (rather than using a separate blocking child as a proxy); TA-B2936-04 resolve both Clippy diagnostics while preserving cancellation/barrier semantics; residual D3 only if Security establishes necessity. Re-run changed D2 test and its runtime mutation control on the pinned successor, and applicable lint/check/platform gates; preserve unrelated accepted tests and mutations. If a direct boundary requires test instrumentation, justify narrowly scoped test-only seam and absence of production behavior changes. Full macOS workspace outcome and permanent original evidence custody remain open. No external PR or merge. Final independent delta approvals and Assurance required.

Status: D1_CLOSED / D2_OPEN / D3_CLOSED_SCOPED_WITH_SECURITY_RESIDUAL / D4_PASS_SCOPED / D5_CLIPPY_FAIL / EVIDENCE_TRANSFER_ACCEPTED / SECURITY_DELTA_PENDING / UPSTREAM_PUBLICATION_BLOCKED.
