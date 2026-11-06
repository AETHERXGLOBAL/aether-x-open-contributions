# Pydantic #14230 — bounded local reproduction and fix oracle

**Scope:** AETHER X GLOBAL local, **not** a Pydantic upstream code contribution, upstream-maintainer approval, full source qualification, accepted fix, or third-party independent validation.

- Original source: [Pydantic issue #14230](https://github.com/pydantic/pydantic/issues/14230) (nested `TypedDict` reuses the first parent's `extra` configuration).
- Observation: **2026-11-06**, Python **3.13.5**, installed Pydantic **2.13.5**. Python package distribution tested, **not a pinned checkout of upstream `main`**.
- Upstream `main` HEAD observed separately on 2026-11-06: `c9b92900dc74802a04cc20519b753a7d8f3d2844` — **not executed**.
- Current upstream status at observation: issue open and **unassigned**. The [Pydantic contributing policy](https://github.com/pydantic/pydantic/blob/main/CONTRIBUTING.md) says nontrivial issue-fix PRs opened without assignment are automatically closed.
- Script: [`reproducer.py`](reproducer.py); SHA-256 of tested bytes: `e4cb62ecd0ad086600202845998568f8ccb92cdf68431ff51ddbd25d45745ade`.

## What the test proves

The same child `Item` is included under parents with `extra='allow'` and `extra='ignore'`. Each parent is first checked separately as a **positive control**, then tested together under both field declaration orders.

On the installed Pydantic v2.13.5, the combined schema applies the first branch's `extra` behavior to both branches. Reversing the parent order reverses the leaked behavior. A corrected implementation must return the appropriate branch-specific values **in both orders**.

## Commands and actual local results

```bash
python -m pip install "pydantic==2.13.5"
python tests/pydantic/14230/reproducer.py --expect-bug
# observed: exit 0, result PASS; both independent controls PASS; both combined orderings exhibit expected defect

python tests/pydantic/14230/reproducer.py --require-fix
# observed: exit 1, result FAIL; this is the expected RED baseline, NOT a fixed package

python -O tests/pydantic/14230/reproducer.py --expect-bug
# observed: exit 0; avoids reliance on Python assert stripping
```

The local environment already had Pydantic 2.13.5 installed; the `pip install` line above is a reproduction prerequisite, **not a claim an installation occurred during qualification**.

| Oracle | Actual outcome | Interpretation |
|---|---|---|
| Independent `Permissive` and `Restrictive` controls | PASS | Each parent configuration works when built alone |
| Combined root, permissive-first | Defect observed | Both children allow the extra key |
| Combined root, restrictive-first | Defect observed | Both children drop the extra key |
| `--expect-bug` | exit 0 / PASS | Defined pre-fix signature is present |
| `--require-fix` | exit 1 / FAIL | Correct branch-specific configuration is still missing |
| `python -O ... --expect-bug` | exit 0 | Oracle does not depend on runtime assertions |

## Next allowed steps

1. Await explicit assignment / owner approval from Pydantic maintainers; **do not submit an upstream PR before assignment**.
2. If permission is obtained, qualify a minimal correction against a **pinned Pydantic main checkout**, using this oracle, repo-native test tooling and negative cases.
3. Submit outward content only following applicable upstream policy, meaningful human review, and explicit target-specific authorization.
4. Preserve this failed `--require-fix` result honestly; never promote this artifact to merged-test or accepted-fix status.

**Attribution:** Pydantic issue problem statement belongs to its original reporter. This bounded regression oracle and local experiment were prepared by AETHER X GLOBAL for independent review. No secrets, private logs, or company-specific machine identifiers are included.

## Source-pinned qualification (separate CI run)

The [read-only workflow](../../../.github/workflows/pydantic-14230-source-qualification.yml) checks out Pydantic at exact official `main` commit `dabcc6461dafa4337c52faf3e9941431ea41ce4a`, installs the official source into an isolated venv, validates that the import comes from that checkout, and runs both oracle modes. **The outcome is pending the actual workflow run and cannot be inferred from the existing Pydantic 2.13.5 result.** The runner does not submit code to the upstream project.
