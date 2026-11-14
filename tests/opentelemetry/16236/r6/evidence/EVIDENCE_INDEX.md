# AETHER X GLOBAL — R6 evidence index

**Mission:** AXG-OTEL-16236-R6-RELIABILITY-20261114  
**Report:** [R6_ENGINEERING_RESULT.md](../R6_ENGINEERING_RESULT.md) — linked in both directions.  
**Decision:** **R6 reliability focused PASS_SCOPED; overall upstream compatibility REVISE/BLOCKED.**  
**Internal Draft:** [PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22).

## Actual source and run

- Real [GitHub Actions run #43534103589](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43534103589), job 132258765464, **SUCCESS for scoped classifier**, run HEAD **b42bb0aeefd4ac30a4d10a9b82f2308563c6a0f6**.
- Upstream pinned source HEAD **572057cde7e9bbe3aed6e5e3e8f16290d487f7d0**; original source SHA-256 **c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4**.
- Current candidate SHA-256 **52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446**, new R6 test source SHA-256 **c09f2f0a72b5c49da3d4812b68ad2a1212f31c7522c29b04b5d12919158d4a1b**.
- Actual Contrib file_storage v0.165.0 and bbolt v1.5.0, Go 1.26.0 on ubuntu-24.04, actual child-process SIGKILL after committed file-storage Batch, freshly opened persisted database.

## Permanently committed actual primary evidence

- [Complete original GitHub Actions job log](github_actions_run_43534103589_job_132258765464.log) — 42,411 characters; contains actual R5/R6 PASS, original suite known FAIL, source checks and artifact receipt.
- [Exact original machine decision JSON](result.json) — focused_exit=0, full_package_exit=1; verdict R6_RELIABILITY_PASS_SCOPED_WITH_UPSTREAM_COMPATIBILITY_BLOCK.
- [Exact original SHA-256 manifest](SHA256SUMS.txt), 14 original source entries.
- [Original focused test exit code](r6_focused_exit.txt): 0.
- [Original upstream full package test exit code](full_package_exit.txt): 1.
- [Original exact run HEAD](internal_head.txt).
- Original result.json SHA Git blob **91c7898f652d1a20b60d91810dd778ee6281658c** and manifest SHA Git blob **ce6dffaa70ad38082d235bd4f040ff38559788b4**; both compared byte-for-byte against the actual ZIP members and match.

## Complete original time-limited ZIP evidence

- [GitHub Actions artifact #14089221251](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43534103589/artifacts/14089221251), ZIP SHA-256 **5ab292c0f6a6042920d98d012099d9a78a06f70ad2a27da7df3a53ffa19266df**, size 7,168 bytes, expires **2026-12-14**.
- Original archive was downloaded and extracted; all **14/14 original raw-file SHA256 digest entries independently matched**. Source archive contains all original 15 files, including r6_focused.log and full_package.log. Those individual original full file logs remain in the expiring archive; the complete job log permanently preserved above contains output of their relevant executed steps.
- Archive retention may end; do **not** claim every original ZIP member is separately stored forever. The full runner log, original result, manifest and exit codes are durable.

## Negative results and unresolved gates

The **same original upstream** TestPersistentQueue_CorruptedData/corrupted_metadata and /corrupted_everything cases still fail because they require silently clearing corrupt qmv0 rather than fail-closed startup. The workflow explicitly validated **that exact failure list** instead of hiding it.

The extra R6 tests use **injected** storage.ErrStorageFull and **injected** postcommit error; they do not prove actual ENOSPC or arbitrary postcommit storage faults. External exactly-once delivery is **not established**; unacknowledged requests intentionally replay. Hardware power loss, online compaction, full distribution, other storage backends and independent R6 Test Architect review **NOT RUN**.

No publication, no code merge, no policy alteration. The live PR head can include later evidence-only commits. Refer to the pinned tested HEAD for any source qualification.

[Return to engineering report](../R6_ENGINEERING_RESULT.md).
