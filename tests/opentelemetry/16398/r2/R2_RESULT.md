# AETHER X GLOBAL — OpenTelemetry #16398 R2 native reproduction evidence

**Mission:** AXG-OTEL-QUEUE-BATCH-PERSISTENCE-R2  
**Original upstream issue:** https://github.com/open-telemetry/opentelemetry-collector/issues/16398  
**Internal Draft PR:** https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/20  
**Exact executed internal PR head:** c6957d5e25a89e197ae70c32ec982edb89735ffa  
**Pinned upstream source HEAD:** 6d43df6a97f2806bbda92c6bce0e1b63440985dc  
**Run ID:** 43440549340  
**Runner job:** 131936727684  
**UTC execution:** 2026-11-13 14:12:37–14:15:01

## Verified R2 result

**Verdict: RED_REPRODUCED_SCOPED.** The reported multi-pipeline persistent queue startup failure is independently reproduced on published OpenTelemetry Collector **contrib v0.165.0**. Three negative-control configurations reach the collector readiness log line. This is not an engineering fix, no GREEN-on-patch result, no restart/recovery test, and no independent sign-off.

| Actual execution | Exit/condition | Observed |
| --- | --- | --- |
| Same queue_batch ID in two logs pipelines + file_storage | exit 1 in 1.27 s | **RED_REPRODUCED**: failed to start \"queue_batch\" processor: timeout |
| Single logs pipeline + file_storage | readiness marker; intentionally terminated by harness after 30.14 s | CONTROL_READY |
| Same queue_batch ID in two logs pipelines, without persistent storage | readiness marker; intentionally terminated after 30.15 s | CONTROL_READY |
| Two differently named queue_batch IDs + file_storage | readiness marker; intentionally terminated after 30.20 s | CONTROL_READY |

The three exit codes -9 are **test-harness process kills after a deliberate observation interval**, not application failures. The controls show readiness only, **not** preservation of queued telemetry during restart or proof of exact-once delivery.

## Test evidence and integrity

- **GitHub Actions run:** https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43440549340
- **Exact 28-file raw evidence bundle:** https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43440549340/artifacts/14045827550
- **Archive SHA-256 (verified after download):** 3dd5b979bd27723881f71713f2bd672bec115061a2be54d3115edf75b06c8ee1
- **Manifest of original 27 evidence-file SHA-256 checks:** [SHA256SUMS.txt](SHA256SUMS.txt). All 27 entries verified against the ZIP after download with sha256sum --check.
- **Original raw runtime-result JSON, byte-for-byte verified via Git blob SHA:** [runtime_results.json](runtime_results.json) (blob SHA b34c33ddf433aaa261f6550af143ba578fabc58e).
- **Permanent full upstream GitHub Actions job log:** [github_actions_run_43440549340_job_131936727684.log](github_actions_run_43440549340_job_131936727684.log).
- **Actual fixture harness:** [runtime_probe.py](../runtime_probe.py) and [test_runtime_probe.py](../test_runtime_probe.py).
- **Actual GitHub Actions workflow:** [.github/workflows/otel-16398-r2.yml](../../../../.github/workflows/otel-16398-r2.yml).

The original GitHub Actions ZIP expires **2026-12-13** under the 30-day retention setting. This report, permanent job log, SHA manifest and exact runtime results remain in the internal Git branch; the temporary artifact link must not be represented as permanently retained.

## Independently checked source and Go tests

- Pinned source clone: exact upstream HEAD above.
- Code source file processor/queuebatchprocessor/processor.go SHA-256 e6ba727ed0ae6b366202ca7bb0ea78d716c8217676c9c5e6d9ecadc15f41f3fd.
- Go 1.26.0 installed on ubuntu-24.04 linux/amd64. Go package test command: go -C /tmp/otel-upstream/processor/queuebatchprocessor test -count=1 -timeout=7m ./...
- Actual test exit code **0**, three listed Go packages **ok**, no failures.
- Python harness fixture tests **5/5 PASS**, actual stdout is included in the runner log and evidence ZIP.
- Image tag otel/opentelemetry-collector-contrib:0.165.0, resolved image digest sha256:e40d61f10c9a617cca1ffd1be4d7e2b3a4b0f0001798ff07e58cabe82e618cea. The Docker release image is **not** the binary compiled from the exact pinned upstream commit. Never merge those two evidence scopes.

## Cause hypothesis / compatibility guard

The graph creates separate processor instances for each pipeline but processor.Settings.ID is the same configured component ID. The queuebatch processor forwards that ID as exporter.Settings.ID, then the persistent queue calls storageID.GetStorageClient with component.KindExporter and the shared owner ID plus signal. The pipeline identity is not included in that storage namespace call on the inspected HEAD. This source path supports the observed identifier collision; it is **not a complete root-cause adjudication** until a candidate implementation is tested.

A naive renaming of exporter.Settings.ID could alter observability identity or orphan old persistent queue files after upgrade. The eventual implementation needs a deterministic, stable per-pipeline namespace, explicit legacy migration rules, and a test for nonempty pre-upgrade persistent queues. The reporter owns original issue authorship; AETHER owns only the tests and internal records it actually authored.

## Gate and publication policy

**R2 reproduction and scoped controls: PASS_SCOPED.**  
**Patch constructed: NO. GREEN tests: NO. Durable queue migration: UNTESTED. Independent Test Architect sign-off: NOT YET. Upstream PR: NONE. External comment: NONE. Internal PR #20: Draft / unmerged.**

Upstream AGENTS.md forbids AI-generated issue comments, PR comments, and AI-generated PR descriptions. A human contributor must write the discussion and PR description personally and mark the human-authorship checkbox themselves. The technical packet here is factual evidence only. Seek maintainer alignment on ID/migration semantics before code proposals. External publication or company merge requires the applicable authorizations.
