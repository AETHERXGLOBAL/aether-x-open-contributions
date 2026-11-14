# AETHER TEST ARCHITECT — R10 independent qmv0 and backend-capability requalification

**Mission:** AXG-OTEL-16236-R10-INDEPENDENT-QMV0-OWNER-REQUALIFICATION-20261114  
**Source of Truth:** [Internal PR #22](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/22), existing branch \`evidence/otel-queue-recovery-16236-r1-20261113\`.  
**Engineering execution HEAD:** \`8c82c3a6ff9be73b2698eaf011d676414accae68\` (later docs/evidence commits are not new code runs).  
**Candidate SHA-256:** \`5b1df085d3db0e91a2c0e8f5aef529087985b3cd102d725a206697cbdc3df176\`.  
**New R10 test SHA-256:** \`ea7a616757b2ccc9db28c7513566d404feb15640ee0237700e2beacbcf00671c\`.  
**Independent TA R9 unchanged original Git blob:** \`da58cdec582045b1506a5b992bca7132105ba84c\`.  
**Original pinned upstream:** \`572057cde7e9bbe3aed6e5e3e8f16290d487f7d0\`.

## Scope of separate independent review

1. Cold-start independent reproduction with **actual Contrib file_storage v0.165.0**, bbolt v1.5.0 and Go 1.26.0. Independently re-run unchanged R9 Test Architect suite, R10 new tests, all relevant historical R5–R9 and original upstream Go queue assertions. Do not accept Engineering’s original workflow success as independent approval.
2. Verify **missing middle and last pending keys** in qmv0 are rejected *before any durable mutation*, even when the first key exists. Check canonical numeric parsing (e.g. key \`01\` is not key \`1\`), extreme large write indices, valid subrange and interrupted recovery. Explicitly challenge the new Walker scan cost and its consistency under concurrent mutations, plus the non-Walker multiple-Get fallback.
3. Preserve three independent negative cases **as failing until independently fixed**: non-Walker physically present but empty numeric key, non-Walker empty-but-present \`ri/wi\` markers, and two clients sharing one storage namespace overwriting one request. Do not edit assertions merely to produce a green run.
4. Review storage ownership design with defensive adversarial reasoning. The published \`storage.Client\` contract permits overwriting \`Set\`, returns nil for absent \`Get\`, and has **no generic CAS or durable lease**. Require a demonstrable backend-specific transactional/conditional-write path or actual enforced exclusive ownership with fencing. If unsupported clients must fail closed, explicitly assess compatibility consequences; do not call that a broad PASS without acceptance.
5. **Unmodified upstream original test expectations still FAIL** in \`TestPersistentQueue_CorruptedData/corrupted_metadata\` and \`.../corrupted_everything\`. The reset-to-empty versus fail-closed contract needs an authentic human upstream maintainer decision. No test edits or waivers without that decision.

## Actual evidence to challenge

[Engineering report](R10_ENGINEERING_RESULT.md) ↔ [R10 original source/runner evidence index](evidence/EVIDENCE_INDEX.md). Frozen [Actions run #43583939265](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/43583939265), job \`132414326496\`; original ZIP SHA-256 \`0d41e593b1044e10f5b57355883716a021d23a0ad3879c564f867ed370b335a4\`, **24/24 file digests independently verified**. Original full job log, byte-exact machine \`result.json\`, byte-exact \`SHA256SUMS.txt\` committed. The complete individual original command logs inside the time-limited ZIP are not all separately committed.

## Independent deliverable

Publish a **genuinely separately executed** verdict, with actual new tested HEAD/Tree, unchanged source/fixture hashes, raw logs, PASS/FAIL/SKIP and full source/negative integrity evidence. Distinguish \`qmv0\` scoped result from ownership and original-suite overall **REVISE**. Report/ZIP/manifests must be mutually linked and durable to the extent claimed. Keep the existing PR Draft, unmerged; do not publish upstream, spend money, deploy or impersonate a separate human reviewer.

**Handoff state: PREPARED_ONLY; no independent R10 execution has been performed by Engineering.**
