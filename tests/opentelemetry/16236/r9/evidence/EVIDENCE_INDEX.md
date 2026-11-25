# OpenTelemetry Collector #16236 — R9 original evidence index

**Engineering decision:** `R9_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK`. **Broad acceptance: REVISE/BLOCKED**.  
**Mutually linked report:** [R9_ENGINEERING_RESULT.md](../R9_ENGINEERING_RESULT.md).  
**Internal Draft PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22). Nothing merged or published upstream.

## Actual source-locked GitHub Actions runs

| Stage and exact tested HEAD | Original workflow | Full original GitHub Actions runner log, permanently committed | Original machine result | Original 19-file SHA-256 manifest |
| --- | --- | --- | --- | --- |
| RED `dee14219def8c64e7c9a8f6f547dac055ded01d8` | [Run #43545600682](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545600682) | [Original 55,494-character log](red/original_job_132296069706.log) | [Byte-exact result.json](red/result.json) | [Byte-exact SHA256SUMS.txt](red/SHA256SUMS.txt) |
| REVISE `3e9fa68bb270c8a1d75b08b13533ac56f3ef154d` | [Run #43545705820](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545705820) | [Original 51,322-character log](revise/original_job_132296400248.log) | [Byte-exact result.json](revise/result.json) | [Byte-exact SHA256SUMS.txt](revise/SHA256SUMS.txt) |
| GREEN `d290913250985480e9fab08222a82642ee55bf67` | [Run #43545871406](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545871406) | [Original 50,912-character log](green/original_job_132296922280.log) | [Byte-exact result.json](green/result.json) | [Byte-exact SHA256SUMS.txt](green/SHA256SUMS.txt) |

Go 1.26.0; original Collector upstream pinned HEAD `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`, actual Contrib `file_storage v0.165.0`, bbolt `v1.5.0`; source SHA256 **`74a66d85a4e2000a3292aeed1ec2e3cfe59e1de9b9c873fb07c5620a6158469c`** at GREEN; R9 added test source SHA256 `81eaf422d0063bb38d9e38f13ca34d066970b75fa3b1d35d4eb88717838631d4`. Historical independent fixtures frozen and unchanged as recorded by the job logs and machine manifest.

## Downloaded and independently hash-verified primary ZIP artifacts

| Stage | Actual original GitHub Actions ZIP | ZIP SHA-256 | ZIP bytes | Digest verification |
| --- | --- | --- | --- | --- |
| RED | [Artifact #14093717454](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545600682/artifacts/14093717454) | `243d925c8aa7eb1657feb8c0345305701f866f0aea90b35e5ab37a8987e890e8` | 12,297 | **19/19 PASS** |
| REVISE | [Artifact #14094410671](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545705820/artifacts/14094410671) | `36d41d7b7715e4aa012251dda760bf1a06165e352f0acc659c58d82488297b81` | 11,846 | **19/19 PASS** |
| GREEN | [Artifact #14093664654](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545871406/artifacts/14093664654) | `1dbeafbe414e6f19be83c02014a5a5b3b02ee0a59ebdb40dfbc02a1dff2ded1d` | 11,754 | **19/19 PASS** |

The original three ZIP files were **actually downloaded, opened and each of their SHA256SUMS 19 entries checked against the original member bytes**: **57/57 total PASS, zero mismatches**. Each has 20 archive members including the manifest. The runner logs, original JSON results and original SHA256 manifests are now **permanently committed to Git** with *exact Git blob SHA-1 matching the original files*:

- RED: result blob `a638691dfd0442d65a0646e07705d9615b7de4e7`, original manifest blob `57c2fe43a5691f27ff44effff2b15d2957cf9394`.
- REVISE: result `340fafb65464ea768b6ae653047d0a8f959d0c95`, manifest `2c58436559eebe2a4ca1fe24241ca0d827dd16ba`.
- GREEN: result `28c2882cf9257f89be7cfa30dae8da002fa22b0b`, manifest `b79816f96a51ba16cb1632cdf931352aad847dce`.

**Retention caveat:** Original individual `full_original.log`, `historical.log`, `independent_r8.log`, `r9_focused.log` and module inventory remain in the original ZIPs, which **expire** under GitHub Actions retention; the complete decoded original Actions runner console logs, machine decisions and manifests are durably committed. Not every ZIP member is separately committed as an independent file. Do not claim perpetual accessibility of expiring ZIPs. Initial failed workflow authoring attempts [#43545392585](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545392585) and [#43545565920](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43545565920) remain visible but are **not classified as true baseline Go package evidence**.

## Exact rejection gate

- Full **unchanged original** upstream Go queue package still **FAIL exit 1** with two leaf cases `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` and their parent only. The old original tests were not modified or skipped.
- R9 GREEN proves **only** actual R8 adversarial, R9 focused and historical targeted behaviors. **Not** all-storage backend safety, all qmv0 key consistency, real ENOSPC or power loss, safe concurrency across writers or upstream-maintainer acceptance.
- **Distinct AETHER TEST ARCHITECT R9 gate not yet executed; no upstream policy decision.** Keep PR Draft/unmerged.

[Return to source technical report](../R9_ENGINEERING_RESULT.md).
