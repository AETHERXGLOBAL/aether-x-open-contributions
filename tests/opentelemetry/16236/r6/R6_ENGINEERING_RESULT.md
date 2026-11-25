# AETHER X GLOBAL — OpenTelemetry #16236 R6 Real file_storage reliability

**Mission:** AXG-OTEL-16236-R6-RELIABILITY-20261114  
**Engineering verdict:** **R6_RELIABILITY_PASS_SCOPED_WITH_UPSTREAM_COMPATIBILITY_BLOCK**  
**Broader release, original-package acceptance, merge and public upstream PR:** **REVISE / BLOCKED**.

## Exact inputs

- [Internal Draft PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22): OPEN, DRAFT, UNMERGED.
- **Exact executed R6 HEAD:** b42bb0aeefd4ac30a4d10a9b82f2308563c6a0f6. Later evidence/report commits are NOT new test runs.
- Upstream OpenTelemetry Collector core baseline HEAD: 572057cde7e9bbe3aed6e5e3e8f16290d487f7d0; baseline queue source SHA256 c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4.
- Experimental R5/R6 candidate unchanged: [persistent_queue_candidate.go](../r2/persistent_queue_candidate.go), SHA256 **52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446**.
- Newly executed [R6 reliability test](axg_real_filestorage_reliability_test.go), SHA256 **c09f2f0a72b5c49da3d4812b68ad2a1212f31c7522c29b04b5d12919158d4a1b**.
- Environment: GitHub Actions ubuntu-24.04, Go 1.26.0, actual published Contrib file_storage v0.165.0 extension factory and lifecycle, bbolt v1.5.0, FSync true.

## Actual executed results

**[Successful scoped R6 run #43534103589](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43534103589), job 132258765464.**

The focused R5/R6 Go invocation used -count=1 and returned **exit 0**. These tests passed on actual Contrib file_storage with physically persisted data:

- **Injected precommit storage.ErrStorageFull:** failed closed; all 11,22,33 requests preserved both logically and physically after reopening. This is NOT real ENOSPC.
- **Injected ambiguous postcommit error:** the actual Contrib Batch had committed but wrapper reported an error. A subsequent independent reopen recovered exactly 11,22,33.
- **Actual OS SIGKILL after a successful committed actual file_storage Batch:** confirmed real child process death in both qmv0 and legacy ri/wi/di cases; fresh reopen retained exactly 11,22,33.
- **Full capacity after crash/restart:** persistent capacity=3, preserved [11,22,33], correctly rejected a fourth offer.
- **Delivery acknowledgment semantics:** durably acknowledged 11 was not replayed; unacknowledged 11 was replayed. No exactly-once external delivery claim is justified.
- **Prior R5 focused Contrib qmv0, legacy and fail-closed corrupt-metadata safety tests:** repeated PASS.
- One top-level child-process-only helper is intentionally SKIPPED; it executed via explicit subprocess test invocations.

**Original upstream Go queue package is still FAIL, exit 1**. The unmodified original suite reported only the known failing cases:

1. TestPersistentQueue_CorruptedData (parent)
2. TestPersistentQueue_CorruptedData/corrupted_metadata
3. TestPersistentQueue_CorruptedData/corrupted_everything

The two leaf cases expect old behavior: silent reset/empty startup on corrupt qmv0. The new fail-closed policy intentionally blocks it to preserve payload access. **The original tests were neither rewritten, skipped nor counted as passing.** This contract conflict still needs upstream maintainer agreement, not a superficial test edit.

### Material exclusions

No real filesystem ENOSPC, true power loss or torn writes, non-atomic backends, online compaction, full Collector distribution, external exporter receipts or exactly-once delivery proof. The postcommit failure was simulated after actual successful storage commit. No separate AETHER TEST ARCHITECT R6 signoff. No maintainer direction has been received. Earlier independent R4 approval applied to an older candidate and does not authorize new R5/R6 code.

## Actual evidence and retention

This report is bidirectionally connected to the [R6 evidence index](evidence/EVIDENCE_INDEX.md).

- [Complete original 42,411-character GitHub Actions job log](evidence/github_actions_run_43534103589_job_132258765464.log), permanently stored, includes true PASS and original-suite failures.
- [Original machine-classified result.json](evidence/result.json), [original SHA256SUMS manifest](evidence/SHA256SUMS.txt), [original focused exit 0](evidence/r6_focused_exit.txt), [original upstream full package exit 1](evidence/full_package_exit.txt), [original exact tested HEAD](evidence/internal_head.txt) permanently committed; original JSON and manifest match original Git blob SHA byte-for-byte.
- [Original complete 15-file raw artifact #14089221251](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43534103589/artifacts/14089221251): ZIP size 7,168 bytes, SHA256 **5ab292c0f6a6042920d98d012099d9a78a06f70ad2a27da7df3a53ffa19266df**, expires 2026-12-14. Downloaded actual ZIP, extracted, independently verified **14/14 SHA-256 manifest entries, zero mismatches**.
- The ZIP contains all individual original Go stdout logs and dependency information. They are time-limited by artifact retention; **not all original ZIP members are separately committed in Git**, while the complete job log and key machine evidence are durable.

## Decision

**Continue engineering and maintain current Draft PR #22 unmerged.** Seek the human upstream maintainers' choice about corrupt qmv0 behavior, then qualify that agreed contract on a new frozen HEAD with independent Test Architect. The Founder retains any merge/public release authority. Do not publish AI-authored upstream GitHub comments/descriptions in violation of target project AGENTS.md.
