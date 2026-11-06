# AXG Pydantic #14230 — R2 bounded engineering remediation

Mission: AXG-PYDANTIC-14230-F01F02-REMEDIATION-R2-20261107
Source: pydantic/pydantic@dabcc6461dafa4337c52faf3e9941431ea41ce4a
Previous exact company HEAD: b5c31f4e8202109596ca5e8a74d3ea6c07981976
Previous failed matrix: https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/42308605738

## Technical changes
- Preserve the previous rejected implementation verbatim as `candidate_r1_rejected.patch`. The Git ancestry and previous CI remain intact.
- Rebuild `candidate.patch` from the pinned official source. For inherited unconfigured TypedDict references, normalize effective default values (including extra=None vs explicit extra='ignore').
- Use a built-in-only fingerprint, never calling equality or hashing on arbitrary user-provided config values; unknown objects remain distinguished by identity and are retained through the schema build.
- Use O(1) expected indexed context lookup (per TypedDict reference) instead of sequential comparison over prior contexts. This does not guarantee O(N) whole-schema generation.
- Preserve the original reference for the first effective context; assign variant refs only when key differs.
- Keep explicit child config independent of parent inheritance.

## Tests and evidence protocol
The unchanged negative controls `independent_f01_f02.py` MUST still fail the prior candidate and pass the revised candidate. The pinned-source GitHub Actions matrix executes:
- Original issue reproduction, nested/recursive cases, upstream native three-test patch, 1,381-case native differential, and Ruff.
- R2 strict child inherited validation, Generic TypedDict, JSON Schema, default normalization, identity/cyclic config fingerprints.
- F03 measurements in CI for 16/32/64 parent contexts in equivalent vs distinct scenarios, with actual elapsed time and peak Python allocations (2 samples).

**CI verdict pending execution at the new commit.** A successful CI alone is not final acceptance. Any failure is a hard gate; do not rewrite or relabel previous evidence.

## Authority
Internal Draft PR #14 only, no merge, no upstream Pydantic PR/comments, no spending or Codex.
Review requires separately executed AETHER TEST ARCHITECT and AETHER ASSURANCE on an immutable new HEAD. External submission BLOCKED pending upstream assignment and explicit Founder approval.
