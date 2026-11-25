# AETHER X GLOBAL — verified positive external engineering outcomes

**Evidence date:** 17 November 2026 (GitHub source-of-truth inspection).  
**Publication state:** Review-only Draft PR; not yet on `main`.  
**Principle:** AETHER-authored merged code, upstream-authored implementation, upstream-reported verification and technical review are different outcomes. All claims below are bounded to the linked records.

## 1. Accepted AETHER-authored external pull requests

| Source | Verified upstream disposition | Exact credit and limit |
|---|---|---|
| [GuillaumeFalourd/useful-actions #1534](https://github.com/GuillaumeFalourd/useful-actions/pull/1534) | **MERGED — 28 Sep 2026**; author `aetherxeg-source`; head `f4dbf17b8064df54d584ed836ed04a243904cfbe` | AETHER contributed an ExecSurface directory entry and runnable GitHub Actions example; this is a directory contribution, **not** independent product certification or evidence of customer adoption. |
| [GuillaumeFalourd/useful-actions #1536](https://github.com/GuillaumeFalourd/useful-actions/pull/1536) | **MERGED — 29 Sep 2026**; author `aetherxeg-source`; head `fd1668ad369f469ec1c68afd88a29b082e8fc961` | AETHER contributed a follow-up Action version update; **not** a second unrelated product adoption. |

**Verified authored-merge count remains two.** Neither outcome implies that the upstream repository's maintainers endorse ExecSurface or AETHER X GLOBAL.

## 2. Material technical contributions with independently visible upstream outcomes

| Project / independent source | AETHER contribution | Confirmed third-party result and attribution boundary |
|---|---|---|
| [Redis #15930](https://github.com/redis/redis/pull/15930) | [Native RED→GREEN Tcl AOF replay controls](https://github.com/redis/redis/pull/15930#issuecomment-6605978538); [test source and original exact revisions](https://github.com/redis/redis/pull/16140#issuecomment-6578890208). | **MERGED — 10 Nov 2026**; PR author `namespaceMarcello`. The [author explicitly credited the AOF test path reported by `@aetherxeg-source` and another contributor](https://github.com/redis/redis/pull/15930#issuecomment-6663086469) and wrote an AOF regression in `stream-cgroups.tcl`. **The actual merged code and test are authored upstream**, not a byte-identical copy or an AETHER-authored PR. |
| [Cloudflare workers-sdk #16612](https://github.com/cloudflare/workers-sdk/pull/16612) | [Source-level review](https://github.com/cloudflare/workers-sdk/pull/16612#issuecomment-6543096080) identified excess environment-variable propagation to a browser child process and proposed credential-exclusion tests. | **MERGED — 9 Nov 2026**; PR author `petebacondarwin`. The merged change uses purpose-limited browser environment forwarding with related tests. **Direct causal influence is not established**, and AETHER authored neither the merged fix nor tests. [Prior dated audit](STATUS_UPDATE_2026-11-09.md). |
| [NVIDIA/aicr #3539](https://github.com/NVIDIA/aicr/pull/3539) | [Proposed an additional bundler-level verified-bytes/write-bytes regression](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6543586434). | **MERGED — 1 Nov 2026**, authored by `mohityadav8`. [Upstream reviewer acknowledged the additional test gap as nonblocking](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6547084760). **The proposed AETHER test was not included** in the verified merged patch; no authorship or fix credit is claimed. |
| [gVisor #16723](https://github.com/google/gvisor/issues/16723) | [Identified leader-only CUDA FD discovery completeness risk and proposed positive/negative controls](https://github.com/google/gvisor/issues/16723#issuecomment-6519314174). | [Upstream participant `AlanFokCo` executed the suggested tests](https://github.com/google/gvisor/issues/16723#issuecomment-6844027148), confirming the missed private-FD thread group in the tested case. **Checkpoint failed closed**; no silent corruption was demonstrated. Experiment, harness and patch belong to the upstream participant; not a merged fix. [Detailed bounded evidence](STATUS_UPDATE_2026-11-13_GVISOR_16723.md). |

These rows represent **four distinct externally observable outcome records**, **not four AETHER-authored merges**, endorsements, accepted security findings or commercial partnerships. The Cloudflare/NVIDIA merge dates are the original author's PR disposition, not AETHER code delivery. Historical `2026-11-03` catalog snapshots and original IDs are unchanged.

## 3. Promising AETHER-authored PRs — explicitly not accepted outcomes

| PR | Latest observed status | Remaining gate |
|---|---|---|
| [Apache DataFusion Ballista #2775](https://github.com/apache/datafusion-ballista/pull/2775) | **OPEN / UNMERGED**; head `09ecf8caa322c29ec57c2e9e1f7bebbffd987e93`; one changed file; locally reported **101/101** executor tests. | Earlier `CHANGES_REQUESTED` preceded the narrowed patch; upstream Rust CI remains approval-dependent. [Follow-up asking for re-review and CI approval](https://github.com/apache/datafusion-ballista/pull/2775#issuecomment-6933474036). |
| [AWS CDK #39680](https://github.com/aws/aws-cdk/pull/39680) | **OPEN / DRAFT / UNMERGED**; head `2b4d5714deb197029758663b686b443d7293b934`; seven changed files; merge conflict reconciled. | Official integration snapshot and upstream CI/maintainer review pending. The `77/77` PR-linter unit checks do **not** satisfy the snapshot requirement. [Exact maintainer assistance request](https://github.com/aws/aws-cdk/pull/39680#issuecomment-6933129595). |

## 4. Verification and publication boundaries

- **Evidence hierarchy:** GitHub-authenticated PR author, `merged=true`, merge date and original issue/comment permalink establish the specific upstream outcome. Local test reports remain author-reported unless separately executed and attested.
- **No duplication:** Do not add these as new participations to the frozen 3 Nov curated set or silently upgrade `data/outcomes.json` historical labels. This page is a dated annotation of existing source records.
- **No implied affiliation:** An open-source interaction with Redis, Cloudflare, NVIDIA, gVisor, AWS or Apache is **not** an endorsement, a partnership, a security certification or product adoption.
- **Release gate:** This documentation is intended for review in a Draft PR. Do not merge without the repository's `catalog-integrity` check and the Founder's explicit authorization for that PR, exact HEAD and base.

**Original source-of-truth links are authoritative** if a current upstream state changes after this observation.
