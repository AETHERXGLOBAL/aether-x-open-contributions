# AETHER X GLOBAL — OpenTelemetry #16398 R1 source-only qualification

**Mission:** `AXG-OTEL-QUEUE-BATCH-PERSISTENCE-R1`  
**Date:** 2026-11-13  
**Upstream:** `open-telemetry/opentelemetry-collector` issue [#16398](https://github.com/open-telemetry/opentelemetry-collector/issues/16398)  
**Pinned upstream main HEAD:** `6d43df6a97f2806bbda92c6bce0e1b63440985dc`  
**Examined upstream file:** `processor/queuebatchprocessor/processor.go` (SHA-256 `e6ba727ed0ae6b366202ca7bb0ea78d716c8217676c9c5e6d9ecadc15f41f3fd`).

## Evidence-backed finding

`exporterSettings(set processor.Settings)` copies `set.ID` into `exporter.Settings.ID` without deriving a per-pipeline namespace in that function. The traces, metrics, logs and profiles constructors all call `exporterSettings(set)`. This supports the **static source-code hypothesis** in upstream issue #16398; it does **not** establish that `persistent_queue` collisions occur at runtime, nor that any proposed remapping preserves persisted data across restarts.

## Exactly what was run

A source-only checker, with SHA-256 pinning to the fetched upstream file:

```sh
python3 source_contract_check.py processor.go \
  --expected-sha256 e6ba727ed0ae6b366202ca7bb0ea78d716c8217676c9c5e6d9ecadc15f41f3fd
```

The actual checker source and captured JSON stdout are included next to this record; see `SHA256SUMS.txt` for fingerprints. The upstream file was read with the connected GitHub source tool and tested locally; upstream code is not redistributed in this evidence package. Result: **`SOURCE_STATIC_MATCH`**. This is **not** an upstream suite PASS, integration proof, security finding, or proof of a finished patch.

## Required R2 implementation gate (NOT EXECUTED)

1. Retrieve a complete clean upstream checkout at the pinned commit and read the current queuebatch, exporterhelper persistent queue, pipeline graph and storage extension implementations and tests.
2. Run upstream #16398's two-pipeline `queue_batch` + `file_storage` reproducer with a local throwaway file-storage directory. Capture full stdout/stderr, exact binary build/tool versions and exit status. RED must fail **for the reported reason**.
3. Confirm the intended lifetime / identity of each pipeline processor instance before changing API contracts. A proposed ID must be stable across restart, distinct between pipelines, not derived from nondeterministic runtime values, and migration-safe for existing persisted queue data. Preserve existing `set.ID` for observability unless approved by maintainers.
4. Test at least: two pipelines sharing one configured processor ID; single pipeline backward compatibility; restart/recovery of already-persisted data; independent persistence and cancellation; pipeline reorder; traces/metrics/logs/profiles applicability; unchanged metrics identity. Explicitly test for accidental orphaning or replay of legacy storage data.
5. Discuss implementation direction with upstream maintainers using a **human-authored** comment *before code is proposed*. Upstream AGENTS.md forbids posting AI-generated issue/PR comments and prohibits an AI-authored PR description or AI-checked human attestation. Keep upstream PR unpublished pending human authorship and review.
6. Publish genuine RED/GREEN logs, tested HEAD, test implementation, integrity hashes, and linked technical report. Request independently run technical/security qualification. A completed static code check cannot be promoted to runtime qualification.

## Novelty/provenance boundary

Original bug report and its reproducer belong to the upstream issue author. Search of upstream PR titles/bodies on 2026-11-13 found no linked PR for #16398 or obvious queue_batch multi-pipeline storage-ID collision fix; this is a **time-bounded search result**, not a guarantee of priority or acceptance. No upstream comment, PR or merge has been submitted by AETHER for this mission. No maintainer endorsement or independent reviewer approval is claimed.

## Environment limitations

The execution container had Go `1.23.2`, while the upstream guide states Go `1.25.x`, and it had no working DNS access to GitHub for a complete checkout. The present results therefore **must not** be described as a native OpenTelemetry execution or an integration fix. Do not patch upstream on an old/runtime-incompatible checkout. This mission's status is `SOURCE_STATIC_MATCH / RUNTIME_NOT_RUN / PATCH_NOT_PREPARED / UPSTREAM_NOT_CONTACTED`.

## Subsequent evidence (R2; do not retroactively replace R1 finding)

A separate native reproduction and controls were completed on 2026-11-13 after this R1 source-only record. See the [R2 scoped result and exact test provenance](r2/R2_RESULT.md), [actual 27-file raw-evidence SHA-256 manifest](r2/SHA256SUMS.txt), [permanent executed job log](r2/github_actions_run_43440549340_job_131936727684.log), and [original runtime results](r2/runtime_results.json). The R2 run reproduced the reported failure on the separately pinned contrib release image with three readiness-only controls. No code fix, GREEN-on-patch, restart migration test or independent assurance has been performed. R1 remains a source-only historical observation.
