# OpenTelemetry #16236 — R8 evidence index

**Internal draft:** [PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22)  
**Two-way source report:** [R8_ENGINEERING_RESULT.md](../R8_ENGINEERING_RESULT.md)  
**Overall decision:** `R8_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`; full original Go package **still FAIL**. No independent R8 signoff, no merge or external publication.

| Result | Source HEAD | Raw Actions run | Original full runner log, committed | Byte-exact machine result | Byte-exact original checksum manifest |
| --- | --- | --- | --- | --- | --- |
| Expected RED | `25a5b10e2973a524b19013553d8237d26aa478a9` | [#43541773685](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541773685) | [55,507-character original job log](red/original_job_132283729818.log) | [result.json](red/result.json) | [18-entry SHA256SUMS](red/SHA256SUMS.txt) |
| Original-suite compatibility REVISE | `d8d6777cf5ba12e68cc8cdd6303477f98cc02512` | [#43541879283](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541879283) | [52,727-character original job log](revise/original_job_132284061380.log) | [result.json](revise/result.json) | [18-entry SHA256SUMS](revise/SHA256SUMS.txt) |
| Final scoped GREEN | `1065e0870fbc8acf9db963cd38ed90f07f13b94e` | [#43542074773](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43542074773) | [52,742-character original job log](green/original_job_132284671211.log) | [result.json](green/result.json) | [18-entry SHA256SUMS](green/SHA256SUMS.txt) |

## Original full artifact integrity

All three original GitHub Actions artifacts were actually downloaded and opened and all **18/18** SHA-256 checks inside *each* archive independently matched actual members (54/54 total). The committed original machine result + original manifest for each run are byte-exact, independently compared against Git blob hashes, not transcribed summaries.

- **RED:** [original ZIP artifact #14092262161](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541773685/artifacts/14092262161), 19 files, ZIP SHA-256 `ba65cecedb478f104dde66a5f33b351764b806d8bf9867b6268188447f8d5bf4`. Original result Git SHA `e33c738baaf28b22d3075cba3a061057fa081324`; manifest Git SHA `31f234176115fc9bd18724c9051c94e108b45161`.
- **REVISE:** [original ZIP artifact #14092113575](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43541879283/artifacts/14092113575), 19 files, ZIP SHA-256 `fb9720c8c7d4e5e09f92c61f5441db7c68d45b3de49b34a47e32173cb272e892`. Original result Git SHA `34eb683dbd5e21bd829e1576f02c2a9e15415067`; manifest Git SHA `82e82a82159f0d3dda4c2b2decda9353a252ac30`.
- **GREEN:** [original ZIP artifact #14092233626](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43542074773/artifacts/14092233626), 19 files, ZIP SHA-256 `daf15464e2c65711f1a083d4385162aa4c054eab5bd0c3514c703c7321ac91c4`. Original result Git SHA `f1b8309428f43ae6ca23927e1b4baf7b66f072de`; manifest Git SHA `68f8a06dac9833a64d1219697968978d590237f8`.

**Retention boundary:** all complete GitHub Actions runner console logs, original machine decisions and SHA-256 manifests are permanently committed as text under this index. The full per-command individual Go logs and dependency receipts remain inside the original artifact ZIPs for the GitHub Actions retention period; **not every ZIP member is individually stored forever in Git**. Do not claim otherwise.

## Persistent blockers

The original upstream Go queue package reports **exit 1** even in the final green focused run, with exactly the old `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` leaves plus their parent. R8's output says `PASS_SCOPED`, not original-package PASS. A real upstream maintainer contract decision and a distinct independently executed AETHER TEST ARCHITECT R8 verdict remain outstanding. Non-Walker client orphan detection, actual ENOSPC and power loss also remain unqualified.

[Return to R8 engineering report](../R8_ENGINEERING_RESULT.md).
