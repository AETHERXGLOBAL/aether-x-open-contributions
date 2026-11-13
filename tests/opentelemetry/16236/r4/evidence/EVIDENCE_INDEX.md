# AETHER X GLOBAL — Independent R4 evidence index

**Mission:** `AXG-OTEL-16236-R3-INDEPENDENT-NATIVE-REQUALIFICATION-20261114`  
**Technical report:** [TEST_ARCHITECT_R4_RESULT.md](../TEST_ARCHITECT_R4_RESULT.md)  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) — Draft / no upstream submission / no merge.

## Executed identities and raw evidence

- **Actual independently authored test run:** [GitHub Actions #43528322682](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528322682), job `132239471072`, outcome SUCCESS, **run HEAD `77fe44a90775a9b46a5237db684ac8fb20e98bb4`**.
- **Original upstream baseline commit:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`. Go `1.26.0 linux/amd64`; bbolt `v1.5.0`; native persisted DB, `NoSync=false`.
- **Original raw-run ZIP:** [GitHub artifact #14086630995](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528322682/artifacts/14086630995). ZIP SHA-256 `3ee44600e7f7e7a64c290edf005e84144b952e08c97dc5959d892e7855a5fd50`, size **5,183 bytes**, retention to **2026-12-13**. Independently downloaded and verified **13/13** original manifest file SHA-256 digests.
- [Original unmodified artifact SHA-256 manifest](ORIGINAL_ARTIFACT_SHA256SUMS.txt), [persisted classified result JSON](result.json), [complete actual GitHub Actions job log](github_actions_run_43528322682_job_132239471072.log). Original ZIP includes exact `baseline_red.log`, `independent_native.log`, `full_package.log`, exact exit files, Go and bbolt pin, source checksums and manifest; long-term independent read access to the ZIP itself ends at artifact expiration, whereas the report/index/job log/result/checksums in this Git branch remain durable.
- **Prior negative attempt:** [GitHub Actions #43528063602](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528063602), **run HEAD `212c018646af57db1cc6535bc36ec3b9e4833fbe`**, failed due to independent candidate-only fixture compiled against old baseline. [Permanent full failed job log](github_actions_run_43528063602_job_132238623112_INITIAL_REVISE.log); original [artifact #14085687895](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43528063602/artifacts/14085687895), ZIP SHA-256 `e84bc24cc6c8afb948710f8730d599c5dc6b715201976a71c5e116ac7b2536f9`, **13/13** original manifest files independently checked.
- **Original engineering R3** (not independent reviewer): [R3 report](../../r3/R3_RESULT.md), [R3 permanent source evidence](../../r3/evidence/SHA256SUMS.txt), and [native crash job](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522401439). Original 16/16 SHA entries validated against GitHub-hosted file contents.

## Exact source checks

Source hashes recorded by the new independent runner:

| Component | SHA-256 |
| --- | --- |
| upstream persistent_queue.go | `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4` |
| R2 experimental persistent_queue_candidate.go | `c9705f155cd3c143da236741947689120670d17817c0244e386a4d138f86afce` |
| R3 native SIGKILL fixture | `c461fc2ceceb4217bb8545562d3a6c43f10495566ee72e833591141c8667329a` |
| R4 independent Go fixture | `dfead9a31cc205ebdce9484f1e98442994b19fe0608348649d6d7a0629a4ec0d` |

**Scope/exclusions:** the original old-code baseline reproduced a native SIGKILL-loss control. Candidate crash recovery, eight restarts and pre-commit injected write rejection passed. A separate test **confirmed silent loss of logical reachability after corrupted `qmv0`**, while physical payloads remain on disk. This is an inherited error-handling behavior and is **NOT** a safe-corruption PASS. Full Contrib extension, all-backend atomicity, real ENOSPC, power-loss guarantees and collector delivery receipts were **NOT RUN**.

This manifest/index points to the report, and the report points back here and to exact raw evidence.
