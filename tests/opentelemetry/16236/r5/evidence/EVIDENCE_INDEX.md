# AETHER X GLOBAL — OTel #16236 R5 original GitHub evidence index

**Engineering verdict:** **`R5_REVISE`**; the three actual Contrib file_storage integration checks independently result in **`R5_ACTUAL_FILESTORAGE_PASS_SCOPED`** only. These are not equivalent to a clean full upstream test suite or an independent AETHER TEST ARCHITECT certification.

**Report (mutual link):** [R5_ENGINEERING_RESULT.md](../R5_ENGINEERING_RESULT.md)  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) — Draft/unmerged.

## Original evidence, source identities, true negative cases

### R5 before-fix contract RED

- [Original GitHub Actions run #43530352324](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530352324), exact HEAD `18b47660b1ee0c2e681eba89e0e2d765247ab262`.
- [Complete original original job log](github_actions_run_43530352324_original_expected_RED.log) · [Original result.json](R5_BEFORE_FIX_ORIGINAL_result.json) · [Original SHA-256 manifest](R5_BEFORE_FIX_ORIGINAL_SHA256SUMS.txt).
- [Original full artifact #14086832088](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530352324/artifacts/14086832088), ZIP SHA-256 `8dc00d7f6c7128f375f324d9191e9ed299c6f98311f3eed7e86f423eb56cb055`, 7,989 bytes. **15/15 original manifest file hashes verified.** Original old R4 code failed three newly added safety tests as expected; whole package exit 1.

### R5 revised metadata safety, contract conflict

- [Original run #43530527088](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530527088), exact source HEAD `a876e1686e8c653c4a5cf92b8511558c44b5136a`.
- [Complete original job log](github_actions_run_43530527088_original_compatibility_REVISE.log) · [Original result.json](R5_POLICY_REVISE_ORIGINAL_result.json) · [Original SHA-256 manifest](R5_POLICY_REVISE_ORIGINAL_SHA256SUMS.txt).
- [Original full artifact #14087082289](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530527088/artifacts/14087082289), ZIP SHA-256 `9e70f1989f28ed0ace61bd42af193e26c8bdaaaaa88b2fe41db69381a8dfef29`, 8,287 bytes. **15/15 original manifest hashes verified.** The four R5 targeted tests pass, but full original Go package still exits 1 due to `corrupted_metadata` and `corrupted_everything` historical expectations. No test was ignored.

### R5 actual Contrib file_storage scoped integration

- [Original run #43530894477](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530894477), exact source HEAD `178e00c5acba5fb254b96000b4a7f1be89bb6572`.
- [Complete original job log](github_actions_run_43530894477_original_extension_PASS_SCOPED.log) · [Original result.json](R5_EXTENSION_ORIGINAL_result.json) · [Original SHA-256 manifest](R5_EXTENSION_ORIGINAL_SHA256SUMS.txt).
- [Original full artifact #14087970028](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43530894477/artifacts/14087970028), ZIP SHA-256 `40053c31e9205b2d710f89e3f09375fe63179da53f9da51288ba2d365b9ba7a9`, 5,658 bytes. **12/12 original manifest hashes verified.** Full production Contrib extension factory with `FSync=true` and bbolt on disk: three focused tests PASS, not a full Collector or end-to-end delivery test.

## Integrity handling and limitations

The original ZIP files were actually downloaded and unpacked, not inferred from workflow status. SHA-256 checks of **every original artifact manifest entry** succeeded (15/15, 15/15, 12/12). The three original machine decision files and three original manifests were committed byte-for-byte; Git blob SHA matched the independently calculated original Git object SHA. Complete GitHub runner logs were fetched from the exact jobs and committed as raw text. All source and workflow files remain in [PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22).

Original full ZIPs are **time-limited GitHub Actions artifacts**, not permanently committed binaries. The complete individual original run-specific Go output files and dependency inventories inside ZIPs may expire; the committed **full runner logs, original machine results, manifests and source code** remain durable. Do not overstate perpetual accessibility or substitute a green workflow badge for compatibility acceptance.

**No original suite green, no metadata-policy signoff, no separate R5 Test Architect decision, no merge or external publication.**

[Return to technical report](../R5_ENGINEERING_RESULT.md).
