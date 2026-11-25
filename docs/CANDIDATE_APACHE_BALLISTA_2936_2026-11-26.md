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
