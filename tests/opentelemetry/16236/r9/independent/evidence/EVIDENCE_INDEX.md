# AETHER X GLOBAL — OpenTelemetry #16236 — R9 Test Architect permanent independent evidence

**Mutual report link:** [R9_TEST_ARCHITECT_RESULT.md](../R9_TEST_ARCHITECT_RESULT.md)  
**Technical verdict:** `REVISE` (4/8 independent top-level tests FAIL; original Upstream exit `1`).  
**No code-source modification:** candidate SHA-256 `74a66d85a4e2000a3292aeed1ec2e3cfe59e1de9b9c873fb07c5620a6158469c` verified in actual run.

## Immutable real-run receipts

- Actual independent [Actions run #43582341324](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43582341324), original job `132409540943`; source HEAD `b18313bfa30ee098b0e6a2de074245589b7d90bf`, exact execution tree `417ff03881ba814318a6027a33c93e7c5da162bb`.
- Original [Actions artifact #14109425122](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43582341324/artifacts/14109425122) SHA-256 `051abfd0776d2bfcda01a485c78ca3d0e8c4ea5120bb3788bb71114da7fe8761`, 12,608 bytes. All **18/18** manifest members independently checked after original ZIP download.
- Actual preservation workflow [#43582825596](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43582825596) succeeded; original complete text artifacts from the separate run are preserved in this same PR branch rather than relying on the expiring Actions ZIP.
- Original machine [result.json](result.json), original [SHA256SUMS.txt](SHA256SUMS.txt), [sources.sha256](sources.sha256) and [ARCHIVE_PROVENANCE.txt](ARCHIVE_PROVENANCE.txt).
- Pinned actual Collector source `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`; Go 1.26.0, Contrib file_storage v0.165.0, bbolt v1.5.0.

## Permanent, real stdout/stderr and exit codes

| Real execution | Complete persisted stdout/stderr | Original exit file | Actual result |
|---|---|---|---|
| Entire upstream original Go queue package (no original test edits) | [original_upstream.log](original_upstream.log) | [original_upstream.exit](original_upstream.exit) | `1` — corrupt qmv0 leaves FAIL |
| Historical R5–R8 + TA R6–R8 | [historical.log](historical.log) | [historical.exit](historical.exit) | `0` |
| Earlier R9 Engineering fixture, only comparator | [r9_engineering_comparator.log](r9_engineering_comparator.log) | [r9_engineering_comparator.exit](r9_engineering_comparator.exit) | `0` |
| **Independent TA R9 adversarial tests** | [ta_r9_independent.log](ta_r9_independent.log) | [ta_r9_independent.exit](ta_r9_independent.exit) | `1`; 4 PASS / 4 FAIL / 0 SKIP |

Additional original environment receipts: [upstream_head.txt](upstream_head.txt), [execution_head.txt](execution_head.txt), [execution_tree.txt](execution_tree.txt), [go_version.txt](go_version.txt), [contrib_version.txt](contrib_version.txt), [bbolt_version.txt](bbolt_version.txt), [module_get.log](module_get.log), [pristine_checkout.log](pristine_checkout.log).

**Integrity:** the original `SHA256SUMS.txt` hashes all 18 output members, not the manifest itself. Verification via `sha256sum -c SHA256SUMS.txt` reported **18/18 OK** for both the independently downloaded ZIP and the separate verified archival workflow. Do not conflate Git blob SHA-1 identities with SHA-256 contents.

## Reproduction, provenance and limitations

- Test program: [independent R9 Go fixture](../axg_ta_r9_independent_test.go).
- Fully pinned execution: [`.github/workflows/otel-16236-r9-independent.yml`](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/b18313bfa30ee098b0e6a2de074245589b7d90bf/.github/workflows/otel-16236-r9-independent.yml). The workflow retains original Upstream tests, unchanged historical tests, real storage dependencies and unconditional negative evidence.
- R9 new independent tests are deterministic; concurrency interleaving is controlled by a two-reader barrier. There are no random seeds or retries concealing failures.
- The original workflow is deliberately red on observed failure. The artifact contains the exact command exits; a successful evidence archival workflow is **not** a product PASS.
- Scope excludes all-backend certification, real power loss/ENOSPC, full Collector E2E and upstream policy resolution. No external publication or production authority.

**Back-link:** [independent technical verdict and Engineering issues](../R9_TEST_ARCHITECT_RESULT.md). 
