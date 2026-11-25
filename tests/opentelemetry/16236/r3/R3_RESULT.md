# AETHER X GLOBAL — R3 native bbolt SIGKILL qualification

**Mission:** `AXG-OTEL-16236-R3-NATIVE-BBOLT-SIGKILL-20261114`  
**Decision:** **`R3_NATIVE_BBOLT_PASS_SCOPED`** — *internal engineering qualification only*. No independent Test Architect decision, no maintainer acceptance, no merge or external PR.

**Issue:** [open-telemetry/opentelemetry-collector #16236](https://github.com/open-telemetry/opentelemetry-collector/issues/16236)  
**Internal Draft:** [AETHERXGLOBAL/aether-x-open-contributions #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22)

## Exact attested inputs

- **Upstream Go baseline exact commit:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`; baseline `exporter/exporterhelper/internal/queue/persistent_queue.go` SHA-256 `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- **Internal R3 tested HEAD:** `5520dcf0fe3367f29b722ccececb7094d346f77a` (later evidence-only commits do not change the R3 tested Go candidate or fixture).
- **Experimental Go source:** [R2 candidate](../r2/persistent_queue_candidate.go), SHA-256 `c9705f155cd3c143da236741947689120670d17817c0244e386a4d138f86afce`.
- **Original native R3 test file:** [`axg_bbolt_sigkill_linux_test.go`](axg_bbolt_sigkill_linux_test.go), SHA-256 `c461fc2ceceb4217bb8545562d3a6c43f10495566ee72e833591141c8667329a`; runner's formatted copy SHA-256 `e7eaacf26b84c59807bd917dbdbe0f22ba4458d96eee848f07bca530777a2899`.
- **Runtime:** GitHub Actions Ubuntu 24.04 / Go `1.26.0 linux/amd64`; `go.etcd.io/bbolt v1.5.0`; `NoSync=false` (fsync enabled), `NoFreelistSync=true`.
- The test's isolated `storage.Client` uses **actual bbolt DB files** and bbolt `DB.Update` to implement atomic `Batch`, following the relevant [Contrib file_storage v0.165.0 implementation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.165.0/extension/storage/filestorage/client.go). It **does not instantiate the Contrib extension**, build the production Collector distribution, replay a 267-ID fixture, prove power-loss durability, or exercise actual external exporter delivery.

## Actual native process kill at the committed boundary

The Go test runs an actual child OS process. After a `DB.Update` transaction **successfully commits** a Batch retiring an in-flight payload key, the storage wrapper sends the **actual operating-system `SIGKILL`** signal to its own PID. The parent asserts the child was signaled, reopens the on-disk bbolt file, runs original queue initialization against the reopened storage and independently inventories the reachable request IDs.

| Verified scenario | Original unpatched Go HEAD | R2 experimental source |
| --- | --- | --- |
| `qmv0`: SIGKILL after first committed retirement Batch | **Expected RED**, signal confirmed; only ID `33` recovered, `11` and `22` missing | **PASS**: SIGKILL confirmed; IDs `11,22,33` all recoverable |
| `qmv0`: SIGKILL after second committed retirement Batch | Not run as original baseline in R3 | **PASS**: SIGKILL confirmed; all three IDs recoverable |
| Legacy `ri/wi/di`: SIGKILL after first committed retirement Batch | Not run as original baseline in R3 | **PASS**: SIGKILL confirmed; all three IDs recoverable |
| Entire existing exporterhelper/internal/queue Go test package (including new native tests) | Not run at R3 baseline | **PASS**, exit `0`, Go package finished in 7.975s |

**Exact final outcomes:** `baseline_native_exit=1`, `candidate_native_exit=0`, `full_package_exit=0`. Machine-classified verdict `R3_NATIVE_BBOLT_PASS_SCOPED`. This is **a stronger check than synthetic in-memory panic**, but is still limited to a direct bbolt-backed adapter rather than the full Contrib extension.

## Evidence archive, integrity, and bidirectional source links

- [**Actual successful GitHub Actions run #43522401439**](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522401439), job `132219684042` with original tested internal commit `5520dcf0fe3367f29b722ccececb7094d346f77a`.
- [Complete original 17-file GitHub artifact #14083676099](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522401439/artifacts/14083676099), expiry 2026-12-13. **ZIP SHA-256:** `960226a92f56e90a2cb99ec9c10bc932c9f6061a2a14448b798270512c5f1bee`.
- The complete ZIP was downloaded and extracted independently. **All 16/16 raw-file SHA-256 entries passed `sha256sum -c`**.
- In addition, **all 17 source text evidence files from the ZIP are permanently committed under this `evidence/` directory**; their original Git blob SHA values were compared byte-for-byte against the GitHub versions. This includes [the original SHA-256 manifest](evidence/SHA256SUMS.txt), [the original machine result](evidence/result.json), [baseline native RED log](evidence/baseline_native_red.log), [candidate native GREEN log](evidence/candidate_native_green.log), [package test log](evidence/complete_package.log), original exits, SHA files, Go version, bbolt dependency provenance and exact HEAD. The complete ZIP is still separately linked while retained.
- [Original full GitHub Actions runner log (38,537 characters)](evidence/github_actions_run_43522401439_job_132219684042.log) is also permanently committed with actual source, commands, failures, test outcome and ZIP receipt.
- A direct source cross-reference lives in the [R1/R2 documentation](../README.md) and the internal Draft #22 body. Report and SHA-256 manifest are linked in both directions.

**The R3 failed attempts remain visible:**
1. [Run #43522084837](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522084837) **REVISE**: fixture gofmt preflight blocked execution; no native proof obtained. Fixed by formatting *only the isolated test copy* and attesting both hashes.
2. [Run #43522179999](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522179999) **REVISE**: candidate-only R2 test expected a changed `initClient` return type and could not compile against the old baseline. Fixed by moving that test into the candidate-only phase; in the same failed run, candidate's three actual native SIGKILL cases and full package had nevertheless passed.
3. [Run #43522401439](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43522401439) **R3_NATIVE_BBOLT_PASS_SCOPED** with independently reproduced baseline RED and candidate GREEN on the exact intended paths.

## Coverage limitations and next independent gate

**Do not call this production-ready or claim correctness for every storage backend.** Still NOT RUN / not verified:
- Full upstream Collector + Contrib `file_storage` extension integration, including its actual client lifecycle, directory naming and on-start/online compaction;
- true power loss or torn writes (SIGKILL after commit is not a power-loss test); intermittent ENOSPC, invalid payloads, rollback, extremely large backlogs, duplicate delivery accounting / committed external receipts;
- cross-backend support when a `storage.Client.Batch` implementation is not atomic;
- independent cold-start AETHER TEST ARCHITECT execution, independent security review where risk demands, and OpenTelemetry maintainer design approval.

The original upstream issue reporter owns the initial issue/historical proof; AETHER credits only its independent Go reproducer and experimental candidate. Upstream `AGENTS.md` prohibits publishing AI-generated issue/PR comments or PR descriptions. No external discussion, upstream PR or merge was published by this R3 run.

**Gate:** Candidate remains on **internal Draft PR #22**, unmerged. Independent specialist should reproduce at exact HEAD, challenge the transaction assumptions and confirm no loss/duplicate/downgrade in native and extension-backed storage before recommending any upstream publication.
