# OpenTelemetry Collector #16236 — AETHER R2 Engineering Qualification

**Mission:** `AXG-OTEL-PERSISTENT-RECOVERY-R2-20261114`  
**Decision:** **`R2_CANDIDATE_GREEN_SCOPED`** — internal engineering test only, **not** an accepted upstream fix.

## Exact source and scope

- Upstream repository: `open-telemetry/opentelemetry-collector`, original issue [#16236](https://github.com/open-telemetry/opentelemetry-collector/issues/16236).
- Original Go baseline HEAD: `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.
- Original upstream `persistent_queue.go` SHA-256: `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- **Exact internal candidate HEAD at successful R2 execution:** `7ef6689935c199e120ad1823d6ad652ce9f5b044`.
- Experimental implementation: [`persistent_queue_candidate.go`](persistent_queue_candidate.go); tested source SHA-256 `c9705f155cd3c143da236741947689120670d17817c0244e386a4d138f86afce`.
- Independent AETHER regression tests: [R1 committed-crash test](../axg_recovery_contract_test.go) and [R2 repeated/legacy/error tests](axg_recovery_r2_test.go); the R2 test SHA-256 is `c71090aed785912e0788b299f52ffca873ed1586444e968dec31079bccf78b3b`.
- Runtime: GitHub Actions `ubuntu-24.04`, Go `1.26.0 linux/amd64`, ephemeral pinned-source checkout, **no production/customer data**.

## What the experimental algorithm changes

On startup, each unacknowledged in-flight payload is copied to the queue tail, its index removed from the durable dispatched list, and its original key retired **within the same `storage.Client.Batch`**. The code uses a new metadata snapshot; it only advances in-memory metadata after the Batch succeeds. An ambiguous Batch failure causes initialization to fail rather than pretending recovery succeeded. The legacy metadata path is also tracked and migrated through the same bounded transactions. Invalid payloads already covered by existing compatibility tests are deliberately treated as corrupted and skipped with a warning using an atomic retirement; valid payloads must not disappear at a committed cut.

**Critical backend assumption:** these guarantees require `storage.Client.Batch` to be a genuinely atomic storage transaction. This was verified with a synthetic transactional in-memory client, **not** with real file_storage/bbolt or process-level power loss.

## Actual before/after evidence

| Test | Baseline HEAD | Candidate |
| --- | --- | --- |
| Existing R1 after-committed-retirement crash cut | **RED, exit 1; lost IDs 11,22**, retained only 33 | **GREEN, exit 0; retained all 11,22,33** |
| Normal restart control | PASS (R1 historical run) | PASS |
| Two independent committed recovery interruptions | Not added to baseline | **PASS** |
| Legacy metadata interrupted recovery | Not independently run baseline | **PASS** |
| Storage Batch rejection before commit, fail-closed | Not independently run baseline | **PASS** |
| Existing upstream queue package regression | Not re-run in baseline R2 | **PASS, exit 0**, package `go.opentelemetry.io/collector/exporter/exporterhelper/internal/queue` |
| Actual file_storage/bbolt and OS-kill | NOT RUN | **NOT RUN** |
| Code review, maintainers’ design agreement, Test Architect signoff | NOT OBTAINED | **NOT OBTAINED** |

The focused candidate command was `go -C /tmp/otel-16236-candidate/exporter/exporterhelper test -count=1 -v -timeout=6m -run '^TestAXGRecovery' ./internal/queue`; the existing package regression was `go -C /tmp/otel-16236-candidate/exporter/exporterhelper test -count=1 -timeout=6m ./internal/queue`. **All focused tests and the existing package suite passed** on successful run #43518638054.

The earlier two R2 failures are preserved, not concealed:
- [Run #43518092207](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43518092207) — Go harness compile error (incorrectly typed sizer), **REVISE**.
- [Run #43518345093](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43518345093) — focused candidate tests passed, but existing corrupted-payload compatibility tests failed, **REVISE**. The correction preserved historical corrupt-item handling without weakening valid-item atomicity.
- [Successful R2 run #43518638054](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43518638054) — baseline RED, candidate GREEN, full package PASS.

## Published raw evidence and integrity

- [Original exact 14-file R2 GitHub Actions artifact #14081821851](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43518638054/artifacts/14081821851), **ZIP SHA-256** `b4a130b30bd2c4900278466ae3c6646d9e005856f0570e32bba49d0b26f3595f`, expiry **2026-12-13**.
- ZIP downloaded and independently verified: **13/13 SHA-256 manifest entries match actual archive files**.
- [Permanent 34,040-character original job log](evidence/github_actions_run_43518638054_job_132206964545.log), including real RED/GREEN, original commands, exit status, artifact receipt and hash.
- [Byte-exact original machine result](evidence/result.json) and [byte-exact original SHA-256 manifest](evidence/SHA256SUMS.txt) committed to this GitHub branch.
- [Byte-exact original focused GREEN log](evidence/candidate_focused_green.log), [original package PASS output](evidence/upstream_queue_regression.log), [actual exit codes](evidence/baseline_red_exit.txt), [candidate exit](evidence/candidate_focused_exit.txt), [package exit](evidence/upstream_queue_regression_exit.txt).
- The remaining original raw entries, including full baseline RED module-download log and candidate unified diff, remain in the ZIP artifact while retained. They are reconstructible from the **pinned baseline** and the **committed candidate**; they are not falsely represented as already committed individually.

## Remaining gate / engineering risks

**R2 was not an independently conducted AETHER TEST ARCHITECT review.** No maintainer reply to the human comment at issue #16236 was visible when engineering began. The candidate is exploratory internal work; no upstream code was posted.

Before external publication:
1. Adversarial native file_storage/bbolt transaction/crash tests on current supported distribution and unmodified production interfaces.
2. Confirm failure semantics for non-atomic storage clients, ambiguous/partial batch errors, corrupted/absent payloads, legacy `ri/wi/di` and `qmv0`, full queues, duplicate delivery, and concurrent startup/shutdown.
3. Review risk of metadata aliasing, batch write amplification and temporary storage capacity; compare a copy-before-delete strategy vs resumable migration with upstream maintainers.
4. Independently executed **AETHER TEST ARCHITECT** requalification with archived raw artifacts, negative cases and SHA256, plus relevant security and assurance gates.
5. Do not merge internal PR #22, open an upstream PR, or post AI-authored comments. OpenTelemetry `AGENTS.md` requires human-authored GitHub discussion and PR description.

**Decision:** engineering `PASS_SCOPED` for simulated transaction cuts; **merge/external publication `BLOCKED`** pending the above evidence and authorization.
