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
2. Source-pinned qualification has now run; see the dated section below. If permission is obtained, refresh and review the exact candidate against the then-current upstream source.
3. Submit outward content only following applicable upstream policy, meaningful human review, and explicit target-specific authorization.
4. Preserve this failed `--require-fix` result honestly; never promote this artifact to merged-test or accepted-fix status.

**Attribution:** Pydantic issue problem statement belongs to its original reporter. This bounded regression oracle and local experiment were prepared by AETHER X GLOBAL for independent review. No secrets, private logs, or company-specific machine identifiers are included.

## Source-pinned engineering qualification — 2026-11-06

**Source:** Official `pydantic/pydantic` at exact `main` commit
`dabcc6461dafa4337c52faf3e9941431ea41ce4a` (observed 6 November 2026).
This is a **fixed source snapshot**, not a claim that a moving `main` will remain unchanged.
GitHub Actions fetched the original repository and independently checked the Git HEAD **and actual imported `pydantic.__file__` path** from that isolated checkout.
The run used Python **3.14.4** and upstream development version **2.15.0a0+dev**. No modification or PR was sent to Pydantic.

**Evidence:** [Source-pinned qualification workflow and logs](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/42301621727).

| Gate | Official unmodified source | Internally patched source |
|---|---|---|
| Defined two-order bug signature | reproduced; `--expect-bug` exit 0 | not reproduced; `--expect-bug` exit 1 |
| Correct inherited-config behavior | `--require-fix` exit 1 (RED) | `--require-fix` exit 0 (GREEN) |
| Additional alternation/explicit-child/recursive cases | expected negative-control failures, explicit-child positive control PASS | all three checks PASS |
| Native Pydantic `tests/test_types_typeddict.py` (89 cases) | 86 PASS, **3 FAIL** | 86 PASS, **3 FAIL** |
| Differential native test identities | 89 source cases | same 89 case identities |
| Newly failing or newly skipped cases | — | **0 new failures; 0 new skips** |
| GitHub job result | source qualification executed | **PASS_NO_NEW_FAILURES** |

The native-suite result is **NOT** a clean full-suite pass. Its three baseline failures existed on the unmodified exact source under the tested runner and remain after the candidate patch. No claim is made about other upstream test modules, architectures or Python versions.

**Falsification retained:** A first minimal candidate that appended live `ConfigWrapper` object IDs directly to every unconfigured `TypedDict` reference was **rejected**: in the native suite it changed failure count from **3 baseline** to **19 patched**, and earlier did not solve the keying collision until lifetime retention was added. The improved candidate keeps original reference names for the first/equivalent inherited config, and assigns variant references only for genuinely different inherited config dictionaries. The existing [`candidate.patch`](candidate.patch) is the current bounded proposal, *not* an upstream-approved fix.

The complete comparison is performed by [`compare_native.py`](compare_native.py); [`extended_cases.py`](extended_cases.py) supplies additional adversarial cases. Neither script counts upstream author code or Pydantic release acceptance as an AETHER-authored merge.

## Remaining engineering and publication gates

1. Obtain **maintainer issue assignment** under [Pydantic CONTRIBUTING](https://github.com/pydantic/pydantic/blob/main/CONTRIBUTING.md). Until then **do not open an upstream PR**; the issue is still open and unassigned at the last verified check.
2. Conduct source review of the candidate's configuration-identity semantics and type/format checks on the exact patched source. Extend native tests to other relevant modules when warranted.
3. If assigned, rebase against a freshly pinned official head, follow the upstream contribution and GenAI rules, and seek separate explicit authority for an outward submission.
4. Keep the internal [Draft PR #14](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/14) under review; do not merge or claim external acceptance without the applicable exact-HEAD approval.


## Expanded pre-submission technical qualification — 7 November 2026

**Exact upstream source:** `pydantic/pydantic@dabcc6461dafa4337c52faf3e9941431ea41ce4a`. This was the current verified `main` at qualification time; a new upstream HEAD must be checked before any outward PR. No original upstream commit was modified. The comparison uses a temporary checkout on AETHER GitHub Actions runners.

**Public source of execution evidence:** [Five-version matrix run #42305831466](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/42305831466), on GitHub-hosted Linux with Python **3.10, 3.11, 3.12, 3.13, and 3.14**. The workflow pins setup-python and the source revision, verifies import provenance, applies the candidate only to the isolated checkout, runs candidate tests and Ruff, and compares native pytest/JUnit identities.

| Python | Native cases, each side | Before candidate | After candidate | New fails/skips | Check |
|---|---:|---:|---:|---:|---|
| 3.10 | 1,381 | 9 FAIL | 6 FAIL | 0 / 0 | PASS |
| 3.11 | 1,381 | 9 FAIL | 6 FAIL | 0 / 0 | PASS |
| 3.12 | 1,381 | 9 FAIL | 6 FAIL | 0 / 0 | PASS |
| 3.13 | 1,381 | 9 FAIL | 6 FAIL | 0 / 0 | PASS |
| 3.14 | 1,381 | 9 FAIL | 6 FAIL | 0 / 0 | PASS |

**Meaning:** Three deliberately added, previously failing *native* Pydantic regression cases now pass: both parent declaration orders and nested list inheritance. The other six failures were already present with unmodified production code in the tested source/environment and remain unchanged. Original six-suite coverage consists of `test_types_typeddict.py`, `test_type_adapter.py`, `test_config.py`, `test_json_schema.py`, `test_schema_gather.py`, and `test_dataclasses.py`. The exact native testcase identities match before/after. All five runs passed candidate-focused, additional nested list/map/forbid/equivalent-context tests, recursive and explicit-child controls, Ruff lint and format checks. **These are 5 executions of the same 1,381-case suite, not 6,905 distinct cases.**

**Submission package:** [`candidate.patch`](candidate.patch) is the production-code change; [`upstream_regression.patch`](upstream_regression.patch) adds three original Pydantic-native regression cases. Evidence oracles [`reproducer.py`](reproducer.py), [`extended_cases.py`](extended_cases.py), [`stress_cases.py`](stress_cases.py), and [`compare_native.py`](compare_native.py) are AETHER test harnesses and are **not** proposed wholesale for upstream inclusion.

### Explicit limitations and remaining gates

- **Bounded technical green, not a complete Pydantic release green.** Six existing native test failures on each runner remain. The full Pydantic test suite, Python 3.15, alternative OS and exceptional configuration value semantics were not fully qualified.
- **Critical code-review question:** `_Definitions._inherited_td_contexts` stores per-type reference variants based on equality of inherited `ConfigWrapper.config_dict`. A cold-start reviewer should challenge nonstandard equality / cyclic configuration objects, recursion, reference naming, schema growth, and behavior under unusual generic/forward-ref contexts. Existing tests do not mathematically prove these properties.
- **Review separation:** This is a source-linked executable engineering qualification, **not** an AETHER TEST ARCHITECT plugin execution, an independent AETHER ASSURANCE sign-off, or a human-maintainer approval. Require an actual separate reviewer to inspect the exact patch and trace; no self-certification.
- **Contributor policy:** Pydantic [requires assignment before an issue-fix PR](https://github.com/pydantic/pydantic/blob/main/CONTRIBUTING.md). As of this review, [issue #14230](https://github.com/pydantic/pydantic/issues/14230) remains open and unassigned; no external PR or new issue comment was sent in this mission.
- **Outward communication:** Human comprehension and upstream AI-policy compliance are mandatory. A request for assignment / issue discussion and eventual upstream PR each require distinct content-specific approval; this internal Draft PR does **not** grant either.
- **Decisions:** Internal, narrow engineering tests = `PASS_SCOPED`. External submission = `BLOCKED_PENDING_ASSIGNMENT_AND_INDEPENDENT_REVIEW`. PR #14 remains Draft, unmerged.
