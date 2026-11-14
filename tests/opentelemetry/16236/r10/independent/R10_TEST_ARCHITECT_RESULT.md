# AETHER X GLOBAL — AETHER TEST ARCHITECT — R10 independent requalification

**Mission:** `AXG-OTEL-16236-R10-INDEPENDENT-QMV0-OWNER-REQUALIFICATION-20261114`  
**Technical verdict:** **REVISE — qmv0 pending-inventory PASS_SCOPED; ownership/TOCTOU, non-Walker ambiguity and upstream-contract gates remain BLOCKED**.  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) remains **Draft / unmerged**. No external upstream publication, production deployment or release.  
**Independent evidence index (mutual link):** [R10 TA EVIDENCE_INDEX.md](evidence/EVIDENCE_INDEX.md).

## Exact actual separately executed source and environment

- **Final independent run:** [Actions #43586199905](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43586199905), job `132421094358` (completed success as **evidence-adjudication workflow**, not blanket test PASS).
- **Final independently executed HEAD:** `5320db04fb89bc1f883fd8ec7bd1d8d224c2c38f`.
- **Final tested Git tree:** `3df759fdeca38c3144cdc34541f5a90589737058`.
- Earlier separate independent run (original separate tests, before evidence-publication workflow addition): [#43585849216](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43585849216), tested HEAD `18a148341bf5058e44b89be02689e41bd0215070`, tree `64eb52fed51da5a248444fdd3dd3160fbd67b1f5`.
- Engineering original executed HEAD `8c82c3a6ff9be73b2698eaf011d676414accae68`; only documentation and independent harness/evidence changes separate later HEADs from candidate source. The candidate code was not changed.
- Candidate SHA-256 **`5b1df085d3db0e91a2c0e8f5aef529087985b3cd102d725a206697cbdc3df176`**.
- Original unchanged R9 TA test Git blob `da58cdec582045b1506a5b992bca7132105ba84c`.
- R10 engineering test SHA-256 `ea7a616757b2ccc9db28c7513566d404feb15640ee0237700e2beacbcf00671c`.
- Original Collector HEAD `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`; original `persistent_queue.go` SHA-256 `c43eb30c537d6f11a04d23e2502ddf43f6aacb10a0c4b39a2da2069363339bc4`.
- Environment: GitHub-hosted `ubuntu-24.04`, Go 1.26.0, actual Contrib `file_storage v0.165.0`, actual bbolt v1.5.0. Real storage and restart, not an in-memory substitute.

## Executed results (from immutable machine result and raw logs)

| Suite | Go exit | Actual event counts | Decision |
| --- | ---: | --- | --- |
| New R10 engineering qmv0 tests | 0 | 7 PASS, 0 FAIL | `PASS_SCOPED` |
| Earlier R9 engineering tests | 0 | 6 PASS, 0 FAIL | `PASS_SCOPED` |
| Historical R5–R8 and earlier TA controls | 0 | 44 PASS, 0 FAIL, 1 SKIP helper | `PASS_SCOPED` |
| Unchanged TA R8 adversarial suite | 0 | 8 PASS, 0 FAIL | `PASS_SCOPED` |
| **Unchanged independent TA R9 suite** | **1** | **5 PASS, 3 FAIL** | **REVISE** |
| **New independently authored TA R10 suite** | **1** | **6 PASS, 1 FAIL** | **REVISE** |
| **Original upstream Go queue package test run** (original upstream expectations unchanged; R1–R5 extra fixtures injected) | **1** | **141 PASS events, 3 FAIL events, 2 SKIP helper events** | **REVISE** |

The upstream three FAIL events represent parent `TestPersistentQueue_CorruptedData` and its two specifically failing subtests; they are **two corrupt-metadata behaviors**, not three independent defects. Go `-json` events count parent/subtest cases and must not be misrepresented as unique top-level tests.

### Reproduced defects and independent adversarial oracle

1. **Walker post-scan TOCTOU — newly executed FAIL.** `TestAXGTAR10PostScanMutationCannotAuthorizeStaleQueue` injected a real physical deletion of pending key `1` through the actual storage client *after* Walker returned its inventory and *before* startup continued. Runner log: `did_delete=true startup_error=<nil> remaining_key_1=[]`. Queue startup incorrectly returned success on stale inventory. This is a deterministic, isolated concurrent-mutation model; it does **not** claim a live external writer exploit. Without cross-client ownership, fencing or transactional inventory/use, Walker's enumeration is not an atomic authorization contract.
2. **Unmodified TA R9 non-Walker present-empty numeric key.** `TestAXGTAR9NonWalkerEmptyPresentNumericSlotMustNotOverwrite` still FAILS; `Get` cannot prove physically absent versus present-empty.
3. **Unmodified TA R9 legacy present-empty markers.** `TestAXGTAR9NonWalkerPresentEmptyLegacyMarkersMustReject` still FAILS; same physical presence ambiguity for `ri/wi`.
4. **Unmodified TA R9 multi-client namespace loss.** `TestAXGTAR9ConcurrentWriterSharedNamespaceMustNotLoseRequest` still FAILS. Deterministic two-writer interleaving left physical inventory `[41]` when both original requests were expected; Get-then-Batch is not atomic CAS.
5. **Unmodified upstream expectations.** `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` FAIL because original tests expect reset-to-empty while candidate fails closed. A genuine upstream maintainer compatibility decision is still needed; no waiver or assertion edits applied.

### Confirmed positive and scope limits

- Separate TA R10 tests confirm rejected missing-middle, missing-last, noncanonical `01` alias, and extreme pending write range without durable mutation on the actual real storage. The valid 256-pending-index subrange restarted with 257 physical entries including qmv0 metadata. Observed single-run initialization duration was `137.859µs` on one hosted runner: **not a benchmark or large-database performance guarantee**.
- Original TA R9 and TA R8 source retained bit-for-bit; original upstream queue test expectations not edited.
- `storage.Client` explicitly permits overwrite on `Set`, returns nil for missing `Get`, and has no generic CAS/ownership/lease. Walker alone does not solve startup-to-use races.
- No independently justified safe all-backend startup guarantee exists; no proof of crash/power-loss recovery with owner fencing, transactional multiple-writer support or large-scale startup latency.
- No independent human maintainer accepted reset-vs-fail-closed semantics. No independent institutional sign-off or production permission is implied.

## Actual evidence integrity and publication

The independent run wrote the **25 raw machine/log/source/environment/exit files plus `SHA256SUMS.txt`** to the same internal PR branch:

[Durable run_43586199905 evidence directory](evidence/run_43586199905) — [machine result](evidence/run_43586199905/result.json) — [SHA-256 manifest](evidence/run_43586199905/SHA256SUMS.txt) — [new adversarial raw JSONL](evidence/run_43586199905/ta_r10.jsonl) — [unchanged TA R9 raw JSONL](evidence/run_43586199905/ta_r9.jsonl) — [original upstream raw JSONL](evidence/run_43586199905/upstream_queue.jsonl).

- GitHub Actions artifact: [#14110047910](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43586199905/artifacts/14110047910) (time-limited; *not* the durable sole evidence).
- Downloaded ZIP SHA-256: **`60cde20545325929f955597677287ac7d59319320a9196ab21fb5aba13745fb0`**; 26 ZIP members, including 25 covered files.
- Independently extracted ZIP and verified **25/25** SHA-256 entries, zero mismatch.
- Original artifact `result.json` SHA-256: `81b32ffa7bbca8ee08532175ece3ec76bc739b354a9cf7ace4938fb6c503a11d`; Git blob `7b4ce2f0d4cf07d48788b6525496fe3fef4cfff2` **matches committed result.json**.
- Original artifact `SHA256SUMS.txt` SHA-256: `55fe9fa953cbd6a7e91518df7ea5876bf360c01279b0e4ee27f93318e9b5d80c`; Git blob `a998c94819bb12049d0eb5decbe67b4973c92ba0` **matches committed manifest**.
- Run's evidence commit (not the tested source HEAD): `966a87b9b53446e382ca761756ff15d871a78236`. The evidence commit changes only evidence files; it is not a new code-test claim.

## Required disposition / minimal handoff

**AETHER ENGINEERING:** implement and prove an actual backend-specific transactional ownership/fencing path or atomic conditional-write guarantee. Explicitly fail closed unsupported non-Walker backends and obtain compatibility acceptance before changing supported-client behavior. Cover deterministic acquisition/reopen/lease fencing/ownership revocation, concurrent writers, empty-but-present physical keys, post-scan mutation, crash/power-loss, and bounded scan behavior. Do not change the independent failing assertions to obtain green.

**Upstream maintainer:** explicitly decide reset-to-empty vs fail-closed on corrupted qmv0 metadata. No unauthorized external upstream contact in this mission.

**Gate:** PR #22 remains Draft/unmerged; final merge/release/production **BLOCKED**. Independent TA scoped tests are genuinely executed and their evidence is durable; the software acceptance outcome is **REVISE**. The [evidence index](evidence/EVIDENCE_INDEX.md) is the reciprocal access point.
