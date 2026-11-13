# AETHER X GLOBAL — R3 independent requalification / stop-duplicate decision

**Mission:** `AXG-OTEL-QUEUE-BATCH-PERSISTENCE-R3`  
**Date:** 2026-11-13  
**Company internal Draft:** [PR #20](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/20) (unmerged)  
**Original issue:** [open-telemetry/opentelemetry-collector #16398](https://github.com/open-telemetry/opentelemetry-collector/issues/16398)  
**Third-party implementation:** [PR #16404](https://github.com/open-telemetry/opentelemetry-collector/pull/16404), authored by upstream maintainer `iblancasa`; **not authored by AETHER X GLOBAL**.

## Change of external circumstances

At the R1/R2 selection and test run, no identical upstream implementation PR was found in searched results. Subsequently, PR #16404 was opened on **2026-11-13 at 15:26:08 UTC**. Its patch rejects a processor using a persistent queue from being reused in multiple pipelines carrying the same signal and provides an actionable validation error. The original issue reporter `braydonk` commented that this is acceptable while a robust enabling fix is unavailable. This is **a fail-closed configuration rejection**, *not* support for safely sharing a persistent queue between pipelines.

**Nonduplication decision: STOP implementing or claiming the same upstream fix.** The issue has an assigned maintainer and an already-open authored PR. The original reporter and PR author retain their respective credit; AETHER retains only its independently executed diagnostics and truthful internal evidence.

## Actual independent R3 tests (third-party exact candidate)

- **Exact external PR #16404 head:** `f5fda3c98612c41e9a505aaeaefdcdecb460dc82`.
- **Exact internal workflow source head tested:** `d65bfa19928fbf2c8a04a916ad94f5cdd48d7880`.
- **Source provenance:** cloned and verified the external PR commit SHA on a fresh Ubuntu 24.04 GitHub runner; source-file SHA-256 entries are in the artifact.
- **Toolchain:** Go 1.26.0 linux/amd64.
- **Graph test:** `go -C /tmp/otel-pr16404/service test -count=1 -timeout=8m -run '^TestProcessorPersistentQueueSharedByPipelines$' ./internal/graph` → exit **0**, PASS.
- **Exporterhelper test:** `go -C /tmp/otel-pr16404/exporter/exporterhelper test -count=1 -timeout=6m -run '^TestBaseExporterPersistentQueueEnabled$' ./internal` → exit **0**, PASS.
- The upstream author's graph test table includes shared persistent storage rejection, unique named instances, single pipeline, shared without storage, and a case where an opaque wrapper is deliberately not detected. These are **upstream-authored test cases**, not new AETHER-authored regression tests.
- **R3 verdict:** `TARGETED_PASS_SCOPED` for *independent execution* of two third-party-authored targeted Go tests. No general regression suite, full runtime binary with PR patch, storage migration, or production test claimed.

## Links to source, raw execution and integrity proof

1. [Actual GitHub Actions execution](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43508856744).
2. [Original 10-file raw artifact](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43508856744/artifacts/14076903525). The artifact has **30-day retention**, due to expire 2026-12-13.
3. Original artifact ZIP **SHA-256**: `0f9b5863217dcef1fb4be1083d4f1ff871d60aaebafc7f0dc9e5ca14afac5e0e`. The ZIP was downloaded, digest independently calculated, and its nine manifest entries all verified against extracted file contents.
4. [Permanent full original runner job log](pr16404-run43508856744-job132173525902.log), fetched from GitHub job `132173525902` and committed to this internal PR.
5. [Original machine-readable verdict](r3_result.json) and [original SHA-256 manifest](R3_SHA256SUMS.txt), retained byte-for-byte as text, linked here. Full original output remains obtainable from artifact #14076903525 while retained.
6. [R2 independently reproduced failing original configuration](../r2/R2_RESULT.md), including raw run logs, original failure and three healthy controls, for comparison.

### Negative findings and limitations

- **Potential blind spot — opaque wrapper:** the upstream test `shared_with_storage_opaque_wrapper` expects no validation error, because the new interface probe checks a directly returned component. This is a known scoped limitation in the external candidate, **not a newly proven exploit or defect**. Do not claim it fixes all third-party wrapped processors.
- **No green runtime proof:** R3 executes targeted Go tests on the external PR. No rebuilt contrib distribution including the PR was used in a live multi-pipeline storage integration test.
- **No functional per-pipeline storage solution:** the external patch rejects conflicting configurations. Developing a deterministic per-pipeline namespace with a provably safe old-backlog migration is a separate technical proposal, subject to explicit maintainer agreement and human-authored discussion.
- **Upstream checks:** inspection of the PR's checks showed a separate Windows workflow failure at the inspected commit. Do not infer that all upstream required CI passed from these two local scoped tests.
- **Authorship and authority:** no external comments, external PR, company merge or maintainer endorsement for AETHER was performed. OpenTelemetry AGENTS.md prohibits AI-written issue/PR discussions and PR descriptions. AETHER TEST ARCHITECT has not independently signed off this R3 report; its tests were executed by GitHub Actions and the evidence is preserved.

## Final decision and forward path

**Stop duplicate implementation; keep internal PR #20 as a Draft evidence-only record pending Founder merge/closure decision.** There is no defensible claim that AETHER wrote or fixed #16398. Focus any prospective contribution on a **distinct unclaimed issue** or a maintainer-requested follow-on gap, with a fresh priority/duplication check and independent test-architect review. No new project, external PR or GitHub public issue comment is authorized by this document.
