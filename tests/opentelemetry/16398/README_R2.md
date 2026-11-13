# OpenTelemetry #16398 — R2 characterization

Mission: AXG-OTEL-QUEUE-BATCH-PERSISTENCE-R2

Internal Draft PR: https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/20

Pinned upstream source HEAD: 6d43df6a97f2806bbda92c6bce0e1b63440985dc.

The upstream queuebatch processor module declares Go 1.26.0 in its go.mod. The default otelcorecol test distribution does not include the file_storage extension; the Docker runtime reproducer uses release image otel/opentelemetry-collector-contrib:0.165.0 and records the image digest. These are separate evidence scopes and should not be conflated.

This branch does not contain a qualified fix. Native reproduction, RED and negative controls, recovery/migration testing, GREEN-on-patch and independent review remain NOT PROVEN until actual logs are published and checked. No upstream comments or PR are authorized. OpenTelemetry AGENTS.md requires human-authored discussions/PR descriptions and a human-checked authorship attestation.
