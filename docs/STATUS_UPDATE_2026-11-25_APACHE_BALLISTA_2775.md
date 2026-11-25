# AETHER X GLOBAL — Apache DataFusion Ballista #2775 merged upstream

**Dated evidence:** 25 November 2026 (Africa/Cairo).  
**Verified classification:** `MERGED_AUTHORED_PR`; owner account `aetherxeg-source`.  
**Boundary:** AETHER X GLOBAL open-source contribution — **not** Apache/ASF endorsement, partnership, certification, downstream deployment or product approval.

## Verified upstream disposition

- [Apache DataFusion Ballista PR #2775](https://github.com/apache/datafusion-ballista/pull/2775), authored by `aetherxeg-source`, **merged** by upstream maintainer `andygrove` at **2026-11-24T23:54:56Z** (25 November, 01:54 Cairo).
- [Upstream merge commit `9c0e89fafe136973445072719198e0801f92b29d`](https://github.com/apache/datafusion-ballista/commit/9c0e89fafe136973445072719198e0801f92b29d).
- Final submitted head: [`69a66f0f6a8d9919ee7a2b81e7461af733e47738`](https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/69a66f0f6a8d9919ee7a2b81e7461af733e47738).
- [Maintainer final APPROVED review — 24 November 2026](https://github.com/apache/datafusion-ballista/pull/2775#pullrequestreview-6041830869); acknowledged the corrected guard-binding comment and test placement.
- [Original reported defect #2767](https://github.com/apache/datafusion-ballista/issues/2767).

## Accepted code scope

Exactly **one** file changed against the upstream PR base: `ballista/executor/src/executor_process.rs`. The accepted fix retains the default `TempDir` owner through the executor lifetime, explicitly enforces private Unix `0700` permissions without changing caller-specified directories, and adds a focused `#[cfg(unix)]` async regression in the existing `mod tests` to verify directory lifetime, permissions and cleanup.

## Verification and preserved negative results

- [Final Ballista Rust workflow in AETHER's fork](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45079848161): `COMPLETED / SUCCESS`; **13/13 jobs passed**, exact tested head `69a66f0f6a8d9919ee7a2b81e7461af733e47738`. Includes Linux, macOS, cargo check, Clippy and rustdoc.
- This was **manual `workflow_dispatch` in the fork**, **not an upstream required PR status check**. The upstream maintainer approval and actual merge are separately proved by Apache GitHub.
- The [previous fork run](https://github.com/AETHERXGLOBAL/datafusion-ballista/actions/runs/45077568489) had **10 success / 3 failure** on earlier head `acfa1dbf04b677f8b2b3d2b083ad4e0e92eb1cc8`, tracing to the upstream `ballista-chaos` executable lookup. The fix was incorporated from upstream `main` before the successful final run.
- Earlier R9/R10 exploratory engineering notes are preserved in company history. They describe a different, more complex candidate and are **not** acceptance evidence for the final minimal one-file upstream patch.

## Distinct prospective follow-up

Maintainer [issue #2936](https://github.com/apache/datafusion-ballista/issues/2936) concerns a similar standalone-executor defect. The maintainer explicitly welcomed follow-up work. It is **a separate open issue**, not a second authored/merged contribution.

## Register lineage and publication gate

This is a new **dated status observation** for the already-recorded external PR #2775. The original 3/4/5/10/17 November snapshots correctly reflected earlier OPEN/UNMERGED states and must remain unchanged. Do not count another participation link merely due to a status update. Current verified outcome is `MERGED_AUTHORED_PR`.

The record is staged on [AETHER X Open Contributions Draft PR #23](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/23), not yet published to `main`. Internal integration remains subject to repository `catalog-integrity`, review and Founder authorization for the **exact PR HEAD**, not a general automatic approval.
