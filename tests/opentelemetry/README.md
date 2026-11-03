# OpenTelemetry #15966 — double-batching warning regression

- Upstream: https://github.com/open-telemetry/opentelemetry-collector/pull/15966
- Original test: [otel15966_graph_build_test.go](otel15966_graph_build_test.go), SHA-256 `45221c859ecc9da6b190fcef009d66cde64fc1020020d6ddf5813d85bc81685b`.
- Exact upstream PR HEAD: `27ec6cca479037cc1654bf4f5e65649111fdcb87`.
- User-run WSL Go 1.26.10 **PASS**; removing `pipelines.warnIfDoubleBatching(set.PipelineConfigs)` made test **FAIL** (0 warning instead of 1); restoring original source **PASS**.
- Original logs and file hashes were independently inspected; **no independent second runtime** executed.
- [Results shared with upstream](https://github.com/open-telemetry/opentelemetry-collector/pull/15966#issuecomment-6607382404).

**Scope limitation:** synthetic pass-through processor registered under type `batch`, real exporterhelper queue-batching exporter, three pipelines via Graph.Build. Not a full Collector process startup test or actual legacy batchprocessor implementation; not upstream accepted. Historical test source preserves a now-stale pre-run comment to maintain exact byte identity.

In an isolated checkout of the pinned PR HEAD, copy this file to `service/internal/graph/aether_otel15966_graph_build_test.go`. From the `service` directory run:

```bash
GOTOOLCHAIN=local GOMAXPROCS=2 go test -p 2 ./internal/graph -run '^TestAetherGraphBuildDoubleBatchingWarningIsPipelineScoped$' -count=1 -v
```

Requalify the source and update the comment/hash before submitting a new upstream patch.
