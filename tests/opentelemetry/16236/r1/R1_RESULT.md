# AETHER X GLOBAL — Independent R1 fault-injection qualification

**Mission:** `AXG-OTEL-PERSISTENT-RECOVERY-R1-20261113`  
**Date:** 2026-11-13  
**Internal Draft PR:** [aether-x-open-contributions #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22)  
**Upstream issue:** [open-telemetry/opentelemetry-collector #16236](https://github.com/open-telemetry/opentelemetry-collector/issues/16236)  
**Issue reporter:** `Parikshit-Sahrawat`; AETHER does not claim the original report/historical experiments as its own.  
**Exact upstream baseline HEAD tested:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`  
**Exact internal commit executed in the original workflow:** `c5c0e3d9f28e6d0f2d7378fe97d7b9a677d2346b`  
**Upstream queue source SHA-256:** `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`  
**AETHER test fixture SHA-256:** `3ef0e0ba4ef1eae1c6509b29be0ac6b0054b043a1433b6ce56eca39751eda349`

## Verified result: RED_REPRODUCED_SCOPED (NOT GREEN)

The actual upstream Go queue package was checked out at exact HEAD and our independent original test file inserted in the ephemeral runner checkout, with Go 1.26.0 linux/amd64.

| Actual executed test | Exit | Actual result |
| --- | ---: | --- |
| `TestAXGRecoveryUninterruptedControl` | 0 | PASS: after an uninterrupted restart, durable inventory had **[11, 22, 33]** |
| `TestAXGRecoveryCutAfterCommittedRetirement` | 1 | **Expected RED**: after a simulated process death immediately after committed deletion of in-flight keys, durable inventory had only **[33]**; missing **[11, 22]** |

The `AXG_LOSS_CONFIRMED` line is a real Go test failure on the unpatched upstream code; this test is supposed to fail until the reported durability invariant is addressed. The **GitHub Actions workflow itself concluded SUCCESS** because it explicitly classifies a precise, controlled RED as successful *diagnostic execution*, not successful application behavior. Do not cite GitHub green checks as code fix evidence.

### Reproduction commands (run by CI)

The test fixture is maintained in [`axg_recovery_contract_test.go`](../axg_recovery_contract_test.go). The workflow downloaded and verified upstream exact commit, then copied this file to `exporter/exporterhelper/internal/queue/axg_recovery_contract_test.go` within the isolated checkout.

```sh
go -C /tmp/otel-16236-baseline/exporter/exporterhelper test -count=1 -v -timeout=6m -run '^TestAXGRecoveryUninterruptedControl$' ./internal/queue
go -C /tmp/otel-16236-baseline/exporter/exporterhelper test -count=1 -v -timeout=6m -run '^TestAXGRecoveryCutAfterCommittedRetirement$' ./internal/queue
```

This is a transactionally consistent **in-memory test storage client**, not actual bbolt, fsync, real OS process death, or an end-to-end collector distribution. It simulates a crash by panic at the **exact instant after a storage Batch that deletes existing in-flight entries is committed**. The latter is deliberately not a timer-based kill. It is not independent proof of cross-storage-backend guarantees, all recovery paths, or exactly-once delivery. A future implementation should be tested on legacy state, qmv0 state, repeated cuts, full capacity and true bbolt commit-level failures.

### Evidence: actual source output preserved on GitHub

- [Original GitHub Actions run #43512198962](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43512198962), job `132184976597`.
- [Original 11-file raw evidence ZIP artifact #14078817156](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43512198962/artifacts/14078817156) (retention 30 days, expiry 2026-12-13).
- **Original ZIP SHA-256:** `efda3a8385eb86485441d21be7f7fb10a7ed6068ab877efcb0744dff73f8c372`.
- Independently extracted the ZIP and checked its **10/10 SHA-256 manifest entries: all OK**.
- All **11 original text evidence files** were subsequently committed **byte-for-byte** to this PR branch and checked against each original file's Git blob SHA (including control and RED logs, exit codes, source/fixture hashes, machine verdict, toolchain and original [SHA256SUMS](SHA256SUMS.txt)).
- [Actual successful control raw Go log](control.log) and [actual failed adversarial raw Go log](recovery_cut.log).
- [Original machine-readable result](result.json), [actual control exit](control_exit.txt), [actual RED test exit](recovery_cut_exit.txt).
- [Permanent full original GitHub Actions job log](github_actions_run_43512198962_job_132184976597.log); this log contains run commands, exit/result and artifact receipt.
- [Original baseline source SHA](persistent_queue_source_sha256.txt), [actual toolchain](go_version.txt), [exact upstream HEAD](source_head.txt), [test fixture SHA](axg_fixture_sha256.txt).

## Interpretation and engineering decision

At baseline, `enqueueNotDispatchedReqs` retrieves previously dispatched data in one Batch, **deletes old durable payload keys in a second Batch**, then processes replacement requests by individual `putInternal` calls. Under the tested atomic in-memory storage, a stop immediately after the deletion commit loses those old payloads. A normal uninterrupted recovery preserves them. This independently confirms a deterministic source-level crash-consistency risk analogous to the issue reporter's earlier legacy-state experiments; the synthetic test additionally exercises the consolidated metadata (`qmv0`) path.

**Implementation agreement not yet granted:** OpenTelemetry [AGENTS.md](https://github.com/open-telemetry/opentelemetry-collector/blob/main/AGENTS.md) requires maintainer alignment when implementation direction is uncertain. Known open decisions include copy-before-delete vs single Batch vs durable migration journal, cross-backend atomicity, legacy/qmv0 migration and possible duplicate deliveries after restart. No code fix has been attempted, no GREEN test is claimed.

### Independent gate

- **Evidence & baseline falsification:** `RED_REPRODUCED_SCOPED`, actual raw test data preserved.
- **Proposed code patch:** `NOT_IMPLEMENTED`.
- **Native bbolt/process crash:** `NOT_RUN`.
- **Recovery correctness across all committed cuts:** `NOT_PROVEN`.
- **AETHER TEST ARCHITECT independent requalification:** `NOT_RUN`.
- **Upstream maintainer design agreement:** `NOT_OBTAINED`.
- **External discussion or PR:** `NOT_POSTED`.
- **Internal merge:** `BLOCKED` pending Founder exact-PR/HEAD and independent qualification.

**Next required human-controlled step:** the contributor must personally discuss the design questions on upstream #16236; no AI-written issue/PR comment or description may be submitted, and a human-authorship declaration must not be completed by AI. Until agreement, keep engineering focused on internal non-invasive verification and clear test criteria, not public patch publication.

This report and the [evidence index](SHA256SUMS.txt) link each other and are part of the same internal Draft PR.
