# AETHER X GLOBAL — OpenTelemetry persistent-queue recovery #16236

**Mission:** `AXG-OTEL-PERSISTENT-RECOVERY-R1-20261113`  
**Issue:** https://github.com/open-telemetry/opentelemetry-collector/issues/16236  
**Baseline upstream HEAD:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0` (verified live GitHub)  
**Baseline upstream queue source SHA-256:** to be recorded by runner and compared to pinned commit.

## Exact, bounded initial scope

This mission is a **new independent diagnostic** for a *different* bug. It does NOT modify or claim PR #16404 / issue #16398 or the third-party issue #16236 reproduction and historic dataset.

We independently inspected upstream `exporter/exporterhelper/internal/queue/persistent_queue.go`: `enqueueNotDispatchedReqs` currently commits deletion of in-flight stored payload keys in one `Batch` before the new requests are committed in later `putInternal` calls. Under a transaction-capable backend, a crash **after the delete commit and before any replacement commit** leaves no recoverable copy for those requests. This is a source-based failure hypothesis from existing upstream code and aligns with the original reporter's independent historical experiments. A separate isolated test will validate it.

### Actual proposed test (not a patch)

[`axg_recovery_contract_test.go`](axg_recovery_contract_test.go) is copied into a pristine, exact upstream checkout **only inside GitHub Actions** to execute an independent Go test at the pinned HEAD. It uses a transactional *in-memory* `storage.Client` to inject a crash (Go panic) *immediately after commit of a transaction deleting old in-flight payload keys*. It deliberately does **not** claim a native process kill or an actual bbolt/fsync test.

The harness tests:
- **Positive control:** same 3 synthetic requests `11,22,33`, of which the first two are in flight; uninterrupted recovery must leave all three durable IDs.
- **Adversarial RED:** crash after the durable retirement cut, then fresh queue initialization must still preserve all IDs. The unpatched upstream baseline is expected to fail this invariant, with `AXG_LOSS_CONFIRMED`. Actual output, exit code and failure will determine whether the result is RED; no result is pre-certified.
- Counterfactual risk: a future fix may use a transaction for both writes/deletes, or copy-before-delete with duplicate-aware recovery; the test must not enforce a specific implementation. Any loss-free migration approach needs independent review and real file_storage integration.

### Independent evidence and publication gates

GitHub Actions will archive **real** Go stdout/stderr, exact tested upstream SHA and source SHA256, toolchain, exit codes, machine verdict, and SHA256 manifest. Link the final report and actual evidence in both directions. Preserve any unexpected failures. Do not mistake the intentionally failing bug-regression test for CI success.

**NOT yet done at authoring:** runtime execution, native bbolt recovery test, maintainer-approved design, engineering correction, GREEN-on-fix, Test Architect separate sign-off, upstream PR.

### Upstream AI authorship and scope

OpenTelemetry's `AGENTS.md` prohibits AI-authored upstream issue/PR comments and descriptions, and requires maintainer agreement on the proposed implementation approach before code is submitted. **No generated text may be copied as a purported human-authored upstream PR description.** This is an internal technical record; no external publication, attribution to the original reporter's work, or main merge is implied. `AGENTS.md` and AETHER governance remain authoritative.

## Verified R1 follow-up (2026-11-13)

The actual GitHub Go test run has now completed. The authoritative result is [R1_RESULT.md](r1/R1_RESULT.md), mutually linked to [permanent original SHA-256 evidence](r1/SHA256SUMS.txt) and the [raw original Go test output](r1/recovery_cut.log). **Verdict: `RED_REPRODUCED_SCOPED`**, not a patch or GREEN certification. Positive control 3/3 IDs survived; crash-cut test retained 1/3 IDs. The evidence is from synthetic transactional storage on actual Go baseline, not bbolt. No external PR/comment or independent Test Architect signoff has been performed.

## R2 internal candidate after R1 — 2026-11-14

An **internal experimental implementation** and independent-on-GitHub-runner (not an independently assigned reviewer) RED/GREEN exercise are now recorded in [R2_RESULT.md](r2/R2_RESULT.md). The [permanent actual job log](r2/evidence/github_actions_run_43518638054_job_132206964545.log), [exact result JSON](r2/evidence/result.json), [original SHA-256 manifest](r2/evidence/SHA256SUMS.txt), [candidate source](r2/persistent_queue_candidate.go) and [five passing focused Go cases](r2/evidence/candidate_focused_green.log) are linked there. The full existing queue package tests passed after addressing two prior R2 failures. **Native bbolt/process crash, broader backend compatibility, independent AETHER TEST ARCHITECT qualification, maintainer architecture agreement and any external PR remain NOT DONE.** Source tested was the candidate at internal HEAD `7ef6689935c199e120ad1823d6ad652ce9f5b044`, not this later evidence-only documentation commit.
