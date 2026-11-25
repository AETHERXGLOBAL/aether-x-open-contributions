# R6 AETHER TEST ARCHITECT — Independent Evidence Index

**Mission:** `AXG-OTEL-16236-R6-INDEPENDENT-REQUALIFICATION-20261114`.  
**Independently executed source HEAD:** `ca1eaadfe041685754cd4acfd3d0c848c7ac5c20` / Git tree `9aa29c999961ba686af4ca803dce83b95acedcb7`.  
**Technical verdict:** `REVISE` — upstream original package red and additional independent corrupt-legacy failure. No merge authorization.  
**Mutual report link:** [R6_INDEPENDENT_RESULT.md](../R6_INDEPENDENT_RESULT.md).

## Durable, committed GitHub evidence

- [Complete original decoded GitHub Actions runner job log](github_actions_job_132268165104.log) (45,500 UTF-8 bytes), source [job #132268165104](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536954950/job/132268165104). SHA-256: `10af6647093cb3e92e5914f3011701f031351bdaeea04630e8a506b8023ada3c`. This is the original **job console transcript**, not a substitute for every individual full Go stdout member.
- [Machine `result.json`](result.json), **byte-for-byte reconstructed and SHA-256 checked against the original downloaded artifact**: `2ff1a64ed25f73440c153c819a5550327cf2317df3232fa97c75bbd1ed86d650`. Original result file size **1,056 bytes**.
- [Byte-exact original artifact SHA-256 manifest](original_artifact_SHA256SUMS.txt), SHA-256 `46fd95c8abe3ac22eeff4df5d54ddd6f024f02e4eff84bdcd791c91e9c8a74cf`, 17 constituent entries; the downloaded original ZIP was extracted and `sha256sum -c` returned **17/17 OK**.
- [Published evidence-file checksum manifest](DELIVERED_SHA256SUMS.txt) provides SHA-256 for the durable log, result, and source ZIP-manifest copies.
- [Test source and workflow](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/ca1eaadfe041685754cd4acfd3d0c848c7ac5c20/tests/opentelemetry/16236/r6/axg_ta_r6_independent_requalification_test.go) and [workflow definition](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/ca1eaadfe041685754cd4acfd3d0c848c7ac5c20/.github/workflows/otel-16236-r6-independent.yml).

## Original time-limited full stdout evidence

- Original [GitHub Actions run #43536954950](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536954950) and [18-file raw artifact #14090431222](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536954950/artifacts/14090431222).
- Original ZIP 8,244 bytes; SHA-256 `b3a21653fa0573a2e58dd867c321607938ed30b7a0e070aeabca555419c32cba`.
- Original archive contains full `r5_r6_focused.log`, `full_original.log`, `independent_controls.log`, `independent_legacy_adversarial.log`, four raw exit-code files, module metadata, source checksums, original result JSON and SHA256SUMS manifest. **This archive is subject to GitHub Actions retention**; although the job log, machine result and checksums are now durable, **the complete individual original Go logs have not all been separately committed here**. Do not assert indefinite retention of the complete original ZIP.

## Original machine outcomes

- R5/R6 focused `exit=0`; original upstream entire package `exit=1`; independent controls `exit=0`; novel corrupt legacy regression `exit=1` (deliberate defect detection).
- Original upstream leaf failures: `TestPersistentQueue_CorruptedData/corrupted_metadata`, `/corrupted_everything`; parent failure reported separately.
- Independent positive fresh-reopen cycles: 5 qmv0 + 5 legacy = 10 successful cycles; all three requests retained once physically each.
- Independent corrupt-legacy case: malformed `ri` silently accepted, original `ri` deleted, physical request `11` remains. The risk is logically orphaned durable data, not proof of physical deletion.
- Genuine filesystem ENOSPC/power loss/non-atomic backends/compaction/full Collector/exporter exactly-once remain NOT_RUN.

## Previous reviewer-harness negatives (not hidden)

- [Formatting preflight failure, run #43536555597](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536555597).
- [Missing fixture directory/classifier whitespace, run #43536743345](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43536743345).

The separate evidence commit follows the **frozen tested** source HEAD; it is not a claim that documentation commits have been re-executed.

[Return to independent report](../R6_INDEPENDENT_RESULT.md).
