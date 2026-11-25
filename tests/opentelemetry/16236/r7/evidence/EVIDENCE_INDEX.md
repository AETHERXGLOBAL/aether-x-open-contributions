# R7 OpenTelemetry #16236 — primary evidence index

**Decision:** `R7_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK` for the specifically enumerated actual Contrib tests; **overall merge / upstream policy still `REVISE`**.

**Mutually linked engineering report:** [R7_ENGINEERING_RESULT.md](../R7_ENGINEERING_RESULT.md)  
**Internal PR:** [AETHERXGLOBAL/aether-x-open-contributions #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22) — Draft/unmerged.

## Pin exact immutable test sources and original results

| Stage | Actual tested HEAD | Native Go result | Original job log | Original data |
| --- | --- | --- | --- | --- |
| Baseline **RED** | `7c15dd3bdcfc9c6bd76efee9a65e1ffc830b78b8` | Legacy failure reproduced, original suite still FAIL; machine `R7_EXPECTED_LEGACY_RED` | [Complete 50,117-character job log](red/github_actions_job_132274052417.log) | [Byte-exact result](red/result.json), [byte-exact 19-line SHA manifest](red/SHA256SUMS.txt) |
| Intermediate **compile failure** | `afb6346de405233c4d5f934cd1350a58550310d0` | `persistent_queue.go:256:5: undefined: err`; harness/engineering compile mistake corrected by scoped declaration | [Complete 39,759-character failed job log](compile_failure/github_actions_job_132274225177.log) | [Failed Actions #43538804092](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538804092) |
| Amended **GREEN** | `1188a18cb42dc3938337e2bd7ee06a0680224360` | Six malformed Legacy cases and the **unchanged** independent Test Architect R6 negative regression PASS; original suite still FAIL; machine `R7_ENGINEERING_PASS_SCOPED_UPSTREAM_POLICY_BLOCK` | [Complete 47,186-character job log](green/github_actions_job_132274706426.log) | [Byte-exact result](green/result.json), [byte-exact 19-line SHA manifest](green/SHA256SUMS.txt) |

Pinned upstream core exact HEAD `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`. Experiment candidate Go SHA-256 old `52e5bc04cbc9cb46f1fe4e3e432a19bacb47c5ff0d44232ac337f557e33e6446`, new `4b362e244ec5365ee6bfd5e5499bcba4be03078339fc3733943e2c8f71060d93`. R7 engineering test SHA-256 `363c77238fc49c7148a4b575521a3ccaca4b13beaa979f5ae8e6f54023f87305`. Original untouched independent R6 test SHA-256 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`.

## Independently verified original machine-source integrity

The source archive **was downloaded and extracted**, not inferred from the GitHub Actions SUCCESS badge:

- [Original baseline RED run #43538751874](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538751874), [complete original 20-file artifact #14089969753](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538751874/artifacts/14089969753) — ZIP SHA-256 `38128930b45a79643985d251715618374b2c30b6b064720c57f424f2b245ffca`; **19/19 original file hashes verified**.
- [Amended GREEN run #43538951873](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538951873), [complete original 20-file artifact #14091120594](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43538951873/artifacts/14091120594) — ZIP SHA-256 `9ac0b34c0c4f3179bf89c05766e78d2d078f86beccdc0231b3ce175540a8686c`; **19/19 original file hashes verified**.
- The original RED JSON Git blob SHA **`967efb6731ab4e1bf6f8feaf27ba8b08c5c2305e`** and SHA manifest blob **`99326301a74cd73f30061e4a46918c2a5e28d854`**, and GREEN JSON blob **`7bad21265d0366ac875738a55c022520e346b0d6`** and manifest blob **`432262b1ccd62fb233937eaa08bcd56c3e46e7be`**, matched byte-for-byte against original archive members.
- The archived 20-file ZIPs retain full original command log files only through GitHub Actions artifact expiry. The committed full original job console logs contain the commands, test output excerpts, source identity and original-package failures; **individual ZIP member logs are not all durably committed**. Never represent the entire binary ZIP as a permanent Git file.

## Outstanding blockers

The **unchanged full upstream Go package** still fails `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything` (and their parent), the well-known **old reset-to-empty versus new fail-closed qmv0** contract. The original tests were not amended, skipped or categorized PASS. Real hardware power loss, filesystem ENOSPC, full Collector export roundtrip and exactly-once external delivery remain NOT TESTED.

R7 engineering execution is **not** an independently executed R7 Test Architect signoff. Only a separate reviewer replaying the new code SHA can close the independent gate; only human maintainers can determine the intended upstream `qmv0` contract. Internal PR #22 stays Draft, unmerged, and upstream publication is blocked.

[Return to R7 engineering result](../R7_ENGINEERING_RESULT.md).
