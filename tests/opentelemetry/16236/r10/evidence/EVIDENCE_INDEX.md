# OpenTelemetry #16236 — R10 original evidence index

**Mission:** AXG-OTEL-16236-R10-QMV0-PENDING-REQUALIFICATION-20261114  
**Engineering result:** **R10_QMV0_PARTIAL_PASS_THREE_INDEPENDENT_BLOCKERS**. Not an independent Test Architect judgment, not merge-ready.  
**Mutual link:** [R10 engineering report](../R10_ENGINEERING_RESULT.md).  
**Internal PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), Draft/unmerged.

## Source identity and original execution

- Original [GitHub Actions run #43583939265](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43583939265), exact **tested HEAD** \`8c82c3a6ff9be73b2698eaf011d676414accae68\`, job \`132414326496\`, scoped workflow conclusion SUCCESS.
- Fixed upstream Collector \`572057cde7e9bbe3aed6e5e3e8f16290d487f7d0\`. Go 1.26.0, actual Contrib \`file_storage v0.165.0\` and bbolt v1.5.0.
- Candidate source SHA-256 \`5b1df085d3db0e91a2c0e8f5aef529087985b3cd102d725a206697cbdc3df176\`, R10 test source SHA-256 \`ea7a616757b2ccc9db28c7513566d404feb15640ee0237700e2beacbcf00671c\`.
- Complete original [GitHub Actions runner console](github_actions_run_43583939265_job_132414326496.log) (60,013 characters) committed.
- Original machine [result.json](result.json), byte-identical to original Actions ZIP, committed.
- Original 24-entry [SHA256SUMS.txt](SHA256SUMS.txt), byte-identical to original Actions ZIP, committed.
- Git blob SHA checks of archived JSON **\`3def7ac94c8ca743f2d723f6dc58b8659e653a12\`** and original SHA manifest **\`bd7782d52cd81f03305faa31f17600af59c00caf\`**, independently compared and verified exact.

## Original complete ZIP source

Original [GitHub Actions artifact #14109457993](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43583939265/artifacts/14109457993), ZIP size **13,966 bytes**, SHA-256 **\`0d41e593b1044e10f5b57355883716a021d23a0ad3879c564f867ed370b335a4\`**.

The actual ZIP was downloaded and opened. It contains **25 members**: one original manifest and 24 data/evidence files. Independently calculated SHA-256 for **every one of the 24 members** covered by the original manifest and verified **24/24 match, zero mismatches**. This is not inferred from the Actions success badge.

The ZIP includes original full command logs (\`full_original.log\`, \`historical.log\`, \`r9_focused.log\`, \`ta_r9.log\`, \`r10_focused.log\`), exits, source/dependency versions, SHA256 receipts and the original \`result.json\`. **The ZIP will expire** on its GitHub Actions retention schedule; all individual complete command log files are *not* separately committed in Git. The original full runner console, original decision file and original checksum manifest are durable here. Do not conflate ZIP retention with permanent preservation of every member.

## Verified actual positive and negative exits

| Original command | Exit | What it means |
| --- | ---: | --- |
| Full original upstream Go queue package with unchanged upstream test assertions | **1** | FAIL: \`TestPersistentQueue_CorruptedData/corrupted_metadata\` and \`.../corrupted_everything\` plus parent |
| Historical R5–R8 plus previous independent controls | **0** | scoped pass |
| R9 engineering regression tests | **0** | scoped pass |
| **Unchanged independent TA R9 test suite** | **1** | Exactly **three original independent cases remain failing**: Non-Walker empty numeric key, empty legacy markers, and concurrent writers sharing a namespace |
| New R10 full qmv0 pending inventory test suite | **0** | five negative and one valid-control case pass, including previously missing middle record |

Neither the three original independent TA failures nor the two original upstream corrupt-metadata failures were modified, skipped, waived or reclassified PASS. The machine verdict explicitly asserts both failure sets with their exact names.

## Decision

R10 fixes a **specific** qmv0 pending-inventory defect on the tested real bbolt/file_storage configuration; it does not solve non-Walker presence ambiguity or shared-namespace multi-writer TOCTOU, and it does not establish performance/atomic snapshot guarantees on every storage backend. Those are still **REVISE / BLOCKED**.

For the next gate, require an enforceable durable ownership/fencing or atomic conditional-write capability, and maintainer approval for the corrupt-qmv0 policy. The independent R10 Test Architect cold-start requalification has not run. Keep PR #22 Draft/unmerged, without upstream public PR/comment or production deployment.

[Back to R10 engineering report](../R10_ENGINEERING_RESULT.md).
