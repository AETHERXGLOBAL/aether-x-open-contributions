# AETHER X GLOBAL — gVisor #16723: CUDA checkpoint discovery test follow-up

**Observation date:** 13 November 2026 (UTC)  
**Original catalog record:** `C01-13` — historical `PUBLIC_COMMENT_ONLY` remains unchanged.  
**Dated evidence classification:** `UPSTREAM_RELATED_TEST_REPORTED` — participant-reported tests, not AETHER-run tests or an accepted fix.

## Original source and attribution

- **Original AETHER X contribution:** [aetherxeg-source, 30 October 2026](https://github.com/google/gvisor/issues/16723#issuecomment-6519314174). Identified a possible discovery miss where `cudaProcs()` scans only a thread-group leader's FD table while a non-leader owns a private table with CUDA device FDs. Proposed a private-FD negative control and a shared-FD positive control. The original comment explicitly said the test had **not** been run by AETHER.
- **Upstream participant experiment:** [AlanFokCo, 13 November 2026](https://github.com/google/gvisor/issues/16723#issuecomment-6844027148). The upstream participant **designed, executed and reported** the C probe, invocation census harness, controls and per-task-discovery patch. Source reported: [gVisor `ae0f8d5908b6a94de21eb9bc8ec0cb47f2cc3d9d`](https://github.com/google/gvisor/commit/ae0f8d5908b6a94de21eb9bc8ec0cb47f2cc3d9d), one GPU and driver `580.126.09`.
- **AETHER acknowledgment:** [authorized reply, 13 November 2026](https://github.com/google/gvisor/issues/16723#issuecomment-6853086416).

## Upstream-reported results

| Case | Discovery / driver behavior | Reported save / restore outcome |
|---|---|---|
| **Shared FD table — positive control** | `--get-state` and `--toggle` observed | Checkpoint and restore succeeded; device-memory checksum resumed |
| **Separate non-leader FD table — negative control, stock runsc** | CUDA-active thread group **not discovered** (empty invocation census) | Save **failed closed** (exit code **128**) due to non-saveable `*nvproxy.frontendFDMemmapFile` mapping. **Silent corruption was not observed.** |
| **Separate FD table plus participant's experimental per-task discovery patch** | Process discovered, but `cuCheckpointProcessGetState` returned **304** (`CUDA_ERROR_OPERATING_SYSTEM`); `--toggle` not run | Save still failed closed on the mapping. Patch **was not proposed for merge** because the end-to-end outcome did not improve. |
| **NVIDIA reference checkpoint tool on the private-FD workload** | Participant reports matching driver/API failures for `--get-state` and `--toggle` | Indicates an independent driver/API constraint for this specific workload, not universal impossibility. |

## Interpretation and strict limits

1. **Supported finding:** In the tested configuration, leader-only FD-table scanning missed a CUDA-active thread group whose GPU FD was only held by a non-leader with a private table.
2. **Important correction to risk framing:** The specific tested workload did **not** create a silently corrupted saved image; it failed closed. No broader absence of silent corruption is proven.
3. **Untested boundary:** A CUDA-initialized process **without device-memory mappings** might not encounter the observed non-saveable-PMA safety stop; that case was **not** executed. No claim about its outcome is justified.
4. **Separate design problem:** Two-phase CUDA orchestration addresses the per-process toggle window for supported interconnected GPU processes; the experiment does **not** prove the discovery gap is fixed or that the proposal is merged.
5. **Ownership:** The original technical observation and proposed control were AETHER's GitHub comment. The experimental harness, C workload, source patch, runtime execution and outcome description belong to **AlanFokCo**, not AETHER. AETHER did not rerun the native experiment.
6. **No institutional claim:** This is not proof of Google approval, endorsement, sponsorship, partnership, product adoption, security certification, a merged gVisor patch, or a new vulnerability classification.

## Company register and release control

This is a **dated source-linked annotation**, not a rewrite of the frozen 2026-11-03 `C01-13` record, its `PUBLIC_COMMENT_ONLY` classification, or the canonical derived institutional register. No duplicative historical contribution is created. Any later machine-readable qualification change needs its own reviewed evidence and validator controls.

The proposed documentation PR is **draft / review-only**: no integration into `main` without the repository's required integrity checks and explicit Founder authorization for that **exact PR, HEAD and base**.
