# Portfolio evidence and closure audit — 3 November 2026

**Publisher:** AETHER X GLOBAL · **Status:** PUBLIC-SOURCE AUDIT / CURATED SNAPSHOT

The public portfolio is a defensible record of *participation and results*, not a claim that every public interaction is original code or is endorsed by a company mentioned here.

## Coverage verified against this repository

| Layer | Grounded count | Meaning / limitation |
|---|---:|---|
| Curated source-linked references | **43** | 40 technical comment links and 3 AETHER-authored upstream PRs, including 2 merged and 1 closed without merge |
| Demonstrable original test candidates | **2** | [OpenTelemetry Graph.Build test](../tests/opentelemetry/README.md) and [Redis AOF-replay Tcl test](../tests/redis/15930/README.md); **not** merged into their upstream projects |
| Selected source-backed outcome cases | **8** | Evidence-tiered cases in [achievements](../achievements/README.md), not 8 AETHER-authored fixes |
| Historical source-linked participation | **233** public threads; **242** comment/review URLs | [Identity-confirmed historical discovery](../data/discovery/README.md); *not* 242 separate validated engineering achievements |
| Confirmed AETHER-authored merged upstream PRs | **2** | [useful-actions #1534](https://github.com/GuillaumeFalourd/useful-actions/pull/1534) and [#1536](https://github.com/GuillaumeFalourd/useful-actions/pull/1536) |

The categorized 43-item catalog is a **curated evidence tier**, not an exhaustive substantive review of all 242 source-linked comment URLs. The historical census preserves discovery coverage; only evidence-qualified engineering outcomes are featured. Further items from the census require validation before promotion.

## NVIDIA/aicr #3539 — completed / no dangling submission

- **Upstream record:** [PR #3539](https://github.com/NVIDIA/aicr/pull/3539) **MERGED / CLOSED** on **2026-11-01 23:12:43 UTC**; [merge commit `3013757e14742640032148fb84c42e745ea00399`](https://github.com/NVIDIA/aicr/commit/3013757e14742640032148fb84c42e745ea00399).
- **Actual upstream author:** `mohityadav8`. Three changed files: `pkg/bundler/bundler.go`, `pkg/bundler/verifier/verifier.go`, and `pkg/bundler/verifier/verifier_test.go`.
- **Actual merged behavior:** the bundler reads the binary attestation once, verifies the returned bytes, and uses the same bytes for the bundle copy. Upstream tests cover reader bytes, symlink refusal and cancellation, **not** a deterministic end-to-end bundler-level verified-bytes-equal-written-bytes oracle.
- **AETHER-authored review:** [source-linked proposal](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6543586434) requested the additional bundler-level check. [Reviewer `yuanchen8911`](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6547084760) independently called the gap nonblocking and suitable for a follow-up.
- **Attribution:** the source fix and included tests were authored by upstream. **AETHER did not submit or merge the extra bundler regression.** This is `UPSTREAM_REVIEWER_ACKNOWLEDGED_GAP`, *not* `MERGED_AUTHORED_PR` and *not* an independent runtime result.
- **Disposition:** AETHER's existing review is **DOCUMENTED_AND_CLOSED**; no new request or reply is owed on #3539. A later, truly distinct test proposal would be a **new separately approved contribution**, not an unresolved item in the completed PR.

## Reputational accuracy and primary-source corrections

- **[PyTorch issue #202806](https://github.com/pytorch/pytorch/issues/202806#issuecomment-6551875732):** keep the historical comment as an original public record. [Upstream maintainer correction](https://github.com/pytorch/pytorch/issues/202806#issuecomment-6581961573): the observed inconsistency is a **missing in-place modification version-error check**, not silently wrong gradients on a valid program. The project index and outcomes page explicitly preserve this nuance.
- **[OpenTelemetry PR #15966](https://github.com/open-telemetry/opentelemetry-collector/pull/15966):** native `Graph.Build` evidence remains explicitly bounded and is *not* a merged test or full Collector startup. Respect the [maintainer's GenAI communication warning](https://github.com/open-telemetry/opentelemetry-collector/pull/15966#issuecomment-6607683058); no AI-generated follow-up comments.
- **[Redis PR #15930](https://github.com/redis/redis/pull/15930):** original AETHER Tcl source has exact-base and exact-HEAD WSL evidence, but the code stored in the [company contributor fork](https://github.com/aetherxeg-source/redis/blob/test/xclaim-aof-replay/tests/unit/type/w07-aof-replay.tcl) remains **unsubmitted** to upstream pending author coordination and terms.
- **[AWS CDK PR #39581](https://github.com/aws/aws-cdk/pull/39581):** AETHER identified the failure mode; the *upstream author* implemented the correction. No AETHER-authored merge or AWS product release is established.
- **[Google gVisor PR #16774](https://github.com/google/gvisor/pull/16774):** upstream contributor reported running a differential case; independent author credit retained.
- **[node-redis PR #3567](https://github.com/redis/node-redis/pull/3567):** upstream PR merged. AETHER's additional strict ACL test was not part of that verified merge.

## Public integrity gates and ongoing eligibility

1. Preserve the original catalog record identifiers, authored PR counts, discovery artifacts and executable test hashes. A new PR is needed to upgrade an evidence tier; no automatic marketing or endorsement claims.
2. Store only public GitHub permalinks and non-sensitive, source-verified classifications. Do not mirror private project receipts or personal/credential information.
3. Before promoting a new contribution from the discovery census: confirm original author, current source and exact commit, novelty and negative control, contributor rules, engineering test evidence and explicit publication authority.
4. Resolve claims that have received maintainer corrections *in the public display*, not by silently changing the historical comment links.

**Closure scope:** This audit closes the **NVIDIA #3539 documentation item**, not unrelated unfinished engineering candidates or any other company's PR. The repository's standing [weekly source discovery](GOVERNED_UPDATES.md) remains read-only; no new monitor or repository is created.
