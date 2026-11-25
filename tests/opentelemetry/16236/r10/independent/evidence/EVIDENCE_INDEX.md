# R10 AETHER TEST ARCHITECT — independent evidence index

**Mission:** `AXG-OTEL-16236-R10-INDEPENDENT-QMV0-OWNER-REQUALIFICATION-20261114`  
**Decision:** **REVISE**; qmv0 pending inventory PASS_SCOPED; ownership/TOCTOU, non-Walker and unchanged original upstream failures unresolved.  
**Full independent report:** [R10_TEST_ARCHITECT_RESULT.md](../R10_TEST_ARCHITECT_RESULT.md) (mutual reference).  
**Internal source of truth:** [Draft PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22). No merge, external PR or production.

## Immutable executed source and CI

- [Final separately executed GitHub Actions #43586199905](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43586199905), job `132421094358`.
- Actual tested repository HEAD: `5320db04fb89bc1f883fd8ec7bd1d8d224c2c38f`; tree `3df759fdeca38c3144cdc34541f5a90589737058`.
- Experimental queue candidate SHA-256 `5b1df085d3db0e91a2c0e8f5aef529087985b3cd102d725a206697cbdc3df176`; exact upstream `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.
- Previous original TA R9 suite Git blob `da58cdec582045b1506a5b992bca7132105ba84c` unchanged; new separate [R10 TA test source](../axg_ta_r10_independent_test.go).
- Actual environment Go 1.26.0, Collector Contrib file_storage v0.165.0, bbolt v1.5.0, ubuntu-24.04.
- GitHub Actions evidence commit `966a87b9b53446e382ca761756ff15d871a78236`; this was **after** the tested source and is **not** itself a software test run.

## Permanent files committed on the PR branch

**[Full raw evidence directory: run_43586199905](run_43586199905)** contains **all 25 covered evidence files** plus checksum manifest (26 committed files total):

- [Machine-readable actual PASS / FAIL / SKIP / exit result.json](run_43586199905/result.json).
- [SHA256SUMS.txt, 25 independent exact-file SHA-256 digests](run_43586199905/SHA256SUMS.txt).
- [Full unchanged upstream queue Go test log](run_43586199905/upstream_queue.jsonl) and [exit](run_43586199905/upstream_queue.exit): **1**, original corrupt metadata expectation failures.
- [Full R9 unchanged TA log](run_43586199905/ta_r9.jsonl) and [exit](run_43586199905/ta_r9.exit): **1**, exactly 3 failures.
- [Full newly authored R10 TA log](run_43586199905/ta_r10.jsonl) and [exit](run_43586199905/ta_r10.exit): **1**, genuine post-Walker TOCTOU FAIL; other 6 PASS.
- [Full R10 engineering test log](run_43586199905/engineering_r10.jsonl), [R9 engineering log](run_43586199905/engineering_r9.jsonl), [historic log](run_43586199905/historical.jsonl) and [TA R8 log](run_43586199905/ta_r8.jsonl): each suite exit **0**.
- [Frozen code/test SHA-256](run_43586199905/frozen_code_test_sha256.txt), [tested HEAD](run_43586199905/tested_head.txt), [tested tree](run_43586199905/tested_tree.txt), [upstream source SHA](run_43586199905/upstream_original_sha256.txt), Go and exact backend versions, module-get log, all exit statuses.

## Independent integrity receipts

- Downloaded real [Actions artifact #14110047910](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43586199905/artifacts/14110047910), ZIP SHA-256 **`60cde20545325929f955597677287ac7d59319320a9196ab21fb5aba13745fb0`**, 26 members including original manifest.
- Verified actual extracted **25/25 entries** in original manifest; zero integrity mismatch.
- `result.json` bytes: SHA-256 **`81b32ffa7bbca8ee08532175ece3ec76bc739b354a9cf7ace4938fb6c503a11d`**, Git blob **`7b4ce2f0d4cf07d48788b6525496fe3fef4cfff2`**. The same Git blob is published in the evidence folder.
- `SHA256SUMS.txt` bytes: SHA-256 **`55fe9fa953cbd6a7e91518df7ea5876bf360c01279b0e4ee27f93318e9b5d80c`**, Git blob **`a998c94819bb12049d0eb5decbe67b4973c92ba0`**. The same Git blob is published in the evidence folder.
- The Actions artifact is retention-limited; the **26 individual files are permanent Git objects on this branch** as long as that Git history is retained. Do not conflate artifact retention with branch-history retention.
- Both first separate run [#43585849216](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43585849216) and this final evidence-preserving second run were real. The final verdict uses the **second run's HEAD and files**.

## Failure integrity and next owner

No original upstream tests, R9 independent assertions or negative findings were changed, deleted, masked, suppressed or waived. CI green only confirms the expected-failure evidence classifier and durable publication step; it does **not** convert failing Go tests into PASS.

**AETHER ENGINEERING:** enforce actual exclusive/fenced ownership or verified atomic backend conditional writes; resolve fail-closed non-Walker compatibility explicitly, then rerun unchanged TA/Go assertions. **Upstream human maintainer** must decide corrupted-metadata reset vs fail-closed expectations. Keep PR #22 Draft/unmerged.

[Return to full R10 independent report](../R10_TEST_ARCHITECT_RESULT.md).
