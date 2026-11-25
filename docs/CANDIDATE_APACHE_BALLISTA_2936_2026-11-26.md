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
