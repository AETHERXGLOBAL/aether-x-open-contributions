# AETHER X GLOBAL — OpenTelemetry #16236 — independent R7 evidence index

**Actual independent verdict: REVISE.** The official original upstream queue package also **FAILS**; no merge/upstream submission authority is granted.

**Mutual report link:** [R7_INDEPENDENT_TEST_ARCHITECT_RESULT.md](../R7_INDEPENDENT_TEST_ARCHITECT_RESULT.md)  
**Internal change:** [Draft PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), retain Draft/unmerged.  
**Immutable tested internal source HEAD:** `2318e42dc29e46968609ea7f82bb108e8997fd90`.  
**Original upstream source HEAD:** `572057cde7e9bbe3aed6e5e3e8f16290d487f7d0`.

## Durable original evidence

- [**Complete permanent 17-file raw evidence archive**](AXG_OTEL_16236_R7_TA_INDEPENDENT_EVIDENCE.tar.xz). This contains raw independent CI execution logs, original exit receipts, unmodified run output, independent failures, machine `result.json`, checked source SHA-256, modules, `SHA256SUMS.txt` and exact source/runner HEAD.
- Archive **6,596 bytes**, SHA-256 **`538aa8aea696528dc86397ee3d7a7e74f7385d1bdf918c75b77d988e598413da`**. Original Git blob SHA **`71302e57f9348ee954a3416413e389e3680f78a4`**, verified locally against the exact uploaded Git object.
- The archive's original `SHA256SUMS.txt` validates **16/16 other files** with no mismatches. Validate: `sha256sum AXG_OTEL_16236_R7_TA_INDEPENDENT_EVIDENCE.tar.xz`; `tar -xJf AXG_OTEL_16236_R7_TA_INDEPENDENT_EVIDENCE.tar.xz -C <empty-directory>`; `cd <empty-directory> && sha256sum -c SHA256SUMS.txt`.
- [Completed GitHub Actions #43540293081](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43540293081) — actual source SHA `2318e42...`; raw original ZIP [#14091556616](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43540293081/artifacts/14091556616), **10,532 bytes**, SHA-256 **`30015ff776977e80668fbea37297a503f6e11c37a89c16c2f297632dbc403f43`**, may expire; the Git archive above does not.
- [Preserved first unsuccessful harness execution #43540154139](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43540154139), source `69ec4467c4370ea62f0f2f1d953f03707d7fdcb7`, aborted after expected original upstream failure before new tests. Do not count as independent qualification.
- Original immutable candidate SHA-256 `4b362e244ec5365ee6bfd5e5499bcba4be03078339fc3733943e2c8f71060d93`; original independent R6 fixture SHA-256 `e1ff29373e36588e283cda892a7ae8515e9d653775c4692905859a60d35891b7`; engineering R7 fixture SHA-256 `363c77238fc49c7148a4b575521a3ccaca4b13beaa979f5ae8e6f54023f87305`.

## Exact original machine outcomes

| Test stage | Exit code | Primary raw files |
| --- | --- | --- |
| Unmodified full upstream queue package | **1** (known qmv0 policy failure) | `full_original.exit`, `full_original.log` |
| Historical R5/R6 Contrib/bbolt suite | **0** | `historical_r5_r6.exit`, `historical_r5_r6.log` |
| Original untouched TA R6 regression and R7 engineering controls | **0** | `previous_r6_and_r7.exit`, `previous_r6_and_r7.log` |
| New independently authored TA R7 adversarial suite | **1** (three failing leaves) | `ta_r7_new.exit`, `ta_r7_new.log` |

The original upstream failing leaves are `TestPersistentQueue_CorruptedData/corrupted_metadata` and `.../corrupted_everything`. New independent R7 failing leaves: `TestAXGTAR7EmptyButPresentLegacyIndices/empty_both`, `TestAXGTAR7TrailingGarbageInDispatchArrayFailClosed`, `TestAXGTAR7OrphanNumericPayloadWithoutAnyMetadata`. The latter is the previously documented orphan-data limitation, now demonstrated by an independent real file_storage fixture.

**Conclusive gate:** `REVISE`; full upstream suite **FAIL**, original upstream contract unresolved, PR #22 remains Draft, no external publication. Not tested: hardware loss, real ENOSPC, full exporter journey, exactly-once delivery.

[Return to the independently executed R7 technical report](../R7_INDEPENDENT_TEST_ARCHITECT_RESULT.md).
