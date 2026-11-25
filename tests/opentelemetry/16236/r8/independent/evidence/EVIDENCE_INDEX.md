# R8 independent execution — permanent GitHub evidence index

**Mutual technical report:** [R8_TA_INDEPENDENT_RESULT.md](../R8_TA_INDEPENDENT_RESULT.md)  
**Internal existing Draft PR:** [#22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22)  
**Outcome:** `REVISE` — no upstream approval or merge.

| Test attempt | Executed exact HEAD | GitHub Actions original run | Permanent full console stdout/stderr + step log | Machine result reproduced from original console |
| --- | --- | --- | --- | --- |
| First: included three test-harness false positives and two genuine adversarial findings | `5df51a2a1bcd0804ebcac408da43888cbcca72b2` | [#43543717153](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43543717153) / job `132289933932` | [first_full_job_132289933932.log](first_full_job_132289933932.log) | [first_result_from_console.json](first_result_from_console.json) |
| Corrected, final R8 independent execution | `c79f031015244e0d5c7f6d653b36e71bcde4da42` | [#43543925006](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43543925006) / job `132290586326` | [final_full_job_132290586326.log](final_full_job_132290586326.log) | [final_result_from_console.json](final_result_from_console.json) |

## Original artifact receipts (separately downloaded and verified)

- [First original ZIP artifact #14092732821](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43543717153/artifacts/14092732821), **11,529 bytes**; SHA-256 `6e60c9f78242e77a9b1d15084ede99d67343c20da677d25f273491f81950470c`. 17 member files; **16/16** original `SHA256SUMS.txt` file checks PASS, zero mismatches.
- [Final original ZIP artifact #14092409763](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43543925006/artifacts/14092409763), **11,362 bytes**; SHA-256 `2998e09dcfac4e19fc4f78d26508ea903b87f6ab744c8552160e7734086c488a`. 17 member files; **16/16** original `SHA256SUMS.txt` file checks PASS, zero mismatches.

The original compressed archive and original `SHA256SUMS.txt` inside it are subject to GitHub Actions retention. Permanent full GitHub console logs above include the complete per-command Go stdout/stderr (the workflow uses `cat` for each Go test log). Linked machine JSON files reflect exact key/value results printed in the original runner and are **extracted representations, not independently certified byte-exact reproductions of the original ZIP member**.

## SHA-256 inventory of key original ZIP members

| Original member | First original SHA-256 | Corrected original SHA-256 |
| --- | --- | --- |
| `full_original.log` | `1dcff93b08c8b8c5b90438e49b6e4dc1fdb51573f4f946df38cb84b35356cffc` | `e3180295c41a20b93ed38233b33c0042d9e7ec9df411bd4d02dddcab55b3d738` |
| `independent_r8.log` | `d094822f5f1e5a188de2cf585161c9792ef821450be9a7fffe86243401eb9e70` | `fee1c0343646dca34157769d0605fbc21fe2850b03466e6f45d2220f9870494f` |
| `result.json` | `35e8ccf35040db7773ffbff75eb69c47c8e431c975632f01c22ee4a521b09c42` | `7adf8195c53c22e1ca1e80bfcef4efb96a6fca2b2724fbe2e47d0a25ea3110bc` |
| `source_hashes.sha256` | `8a854e2ed9f995d7adb44876f6937793c381247b55ae86c21853fa6df21bdb1` | `7952c54bed62a2e9ad7d0aada3d1c136e66656d91ab1e2c04883dfbc86d9fa05` |
| `unchanged_regressions.log` | `6c28283d6c849172cfeff312280ade2f68e6bbf88f7adc6000b1d43388ce8bc9` | `e991a546385b0b14a27c30e934762f4f1c63c02cc6e2130d58d51434c394de91` |

**Source integrity:** R8 candidate SHA-256 `200cb460efa44879827f9074edb911276a3ff1f7ca2f51a4d44c2f5ba844506c`; unchanged TA R6 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`; unchanged TA R7 `e994907ab702f68415e113b7dc948595f7a9a61437da85cec867439956a9dfd5`; unchanged R8 engineering test `8431c66f8d8745e7e13a134151f7542619c735762b91924eecbb98aed7ce28cf`; corrected independent R8 file `2a5ea725923b3a36a4a00af06bf05a21d45eb37cc2718d4a549bd9e2c8eaf3c8`. All were checked by the actual GitHub Actions source-preflight step.

**Actual final command exits:** unmodified original upstream queue suite `1`; historical R3–R6 `0`; unchanged R6/R7/R8 focused suite `0`; new independent R8 suite `1`. Two test roots fail, four named positive controls pass. Source SHA, environment/dependency versions, complete stdout/stderr and all original member hashes are available in the attached artifacts and permanent logs.

Reproduction is pinned by the exact [independent workflow at tested HEAD](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/c79f031015244e0d5c7f6d653b36e71bcde4da42/.github/workflows/otel-16236-r8-independent.yml) and [independent test at tested HEAD](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/blob/c79f031015244e0d5c7f6d653b36e71bcde4da42/tests/opentelemetry/16236/r8/independent/axg_ta_r8_independent_test.go). The workflow runs the unchanged upstream package with `go -C /tmp/otel-ta-r8/exporter/exporterhelper test -count=1 -v -timeout=7m ./internal/queue`, the unchanged historical scope, and `-run '^TestAXGTAR8'` after installing the standalone TA R8 file.

[Return to mutual technical report](../R8_TA_INDEPENDENT_RESULT.md).
