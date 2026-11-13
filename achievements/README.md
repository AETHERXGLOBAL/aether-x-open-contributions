# Engineering outcomes with primary-source evidence

**Snapshot:** 2026-11-03. Original upstream authors retain full credit for their own code and tests.

## Our pull requests actually merged

- [useful-actions #1534](https://github.com/GuillaumeFalourd/useful-actions/pull/1534) — merged 2026-09-28, commit `1ab2b4ccac754b4d10b04c6e88829d6d628974bd`.
- [useful-actions #1536](https://github.com/GuillaumeFalourd/useful-actions/pull/1536) — merged 2026-09-29, commit `3e0b48c11c926d2dc7b271620cb61e0fd831a339`.
- [awesome-security #747](https://github.com/sbilly/awesome-security/pull/747) — **closed without merge** (retained for accuracy).

## Eight selected evidence-backed technical cases

| Project | Supported result | Primary source |
|---|---|---|
| open-telemetry/opentelemetry-collector | `NATIVE_TEST_EXECUTED` | [View original](https://github.com/open-telemetry/opentelemetry-collector/pull/15966#issuecomment-6607382404) |
| redis/redis | `NATIVE_TEST_EXECUTED` | [View original](https://github.com/redis/redis/pull/15930#issuecomment-6605978538) |
| pytorch/pytorch | `UPSTREAM_AUTHOR_IMPLEMENTED_TEST` | [View original](https://github.com/pytorch/pytorch/pull/202881#issuecomment-6552016471) |
| aws/aws-cdk | `UPSTREAM_AUTHOR_CHANGED_CODE` | [View original](https://github.com/aws/aws-cdk/pull/39581#issuecomment-6543447817) |
| redis/redis | `UPSTREAM_AUTHOR_ACKNOWLEDGED_PROPOSAL` | [View original](https://github.com/redis/redis/issues/16130#issuecomment-6568601668) |
| google/gvisor | `UPSTREAM_RELATED_TEST_REPORTED` | [View original](https://github.com/google/gvisor/pull/16774#issuecomment-6542899955) |
| NVIDIA/aicr | `UPSTREAM_REVIEWER_ACKNOWLEDGED_GAP` — upstream fix independently merged; our suggested extra test **not** merged | [Reviewer note](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6547084760) · [Merge commit](https://github.com/NVIDIA/aicr/commit/3013757e14742640032148fb84c42e745ea00399) |
| redis/node-redis | `UPSTREAM_AUTHOR_IMPLEMENTED_TEST_ON_CLOSED_PR` | [View original](https://github.com/redis/node-redis/pull/3564#issuecomment-6544676687) |

### Dated follow-up — google/gvisor #16723 (13 November 2026)

The original [AETHER technical proposal, catalog ID C01-13](https://github.com/google/gvisor/issues/16723#issuecomment-6519314174), identified leader-only FD discovery as a testable boundary. [Upstream participant AlanFokCo executed the proposed controls](https://github.com/google/gvisor/issues/16723#issuecomment-6844027148) and reported that a private-FD CUDA-active thread group was missed, but that checkpoint save **failed closed** in the tested mapped-memory case. Their experimental per-task patch still met CUDA driver error 304; an unmapped-memory variant remains **untested**. AETHER [acknowledged the result](https://github.com/google/gvisor/issues/16723#issuecomment-6853086416).

**Dated outcome:** `UPSTREAM_RELATED_TEST_REPORTED` (upstream participant-reported, not AETHER native test, adopted code, upstream merge, demonstrated silent corruption, Google endorsement or partnership). [Read exact evidence and scope](../docs/STATUS_UPDATE_2026-11-13_GVISOR_16723.md). This addition does not change the eight-case **3 November historical snapshot** or historical `C01-13` classification.

### NVIDIA #3539 — completed upstream outcome, no outstanding AETHER submission

- **Upstream status:** [PR #3539](https://github.com/NVIDIA/aicr/pull/3539) merged and closed on **2026-11-01**; merge commit [`3013757e14742640032148fb84c42e745ea00399`](https://github.com/NVIDIA/aicr/commit/3013757e14742640032148fb84c42e745ea00399), authored upstream by `mohityadav8`.
- **Merged scope (three files):** `pkg/bundler/bundler.go`, `pkg/bundler/verifier/verifier.go`, `pkg/bundler/verifier/verifier_test.go`. The upstream patch reads once, verifies that buffer and writes the same buffer; included tests exercise the reader, symlink refusal and cancellation.
- **AETHER contribution:** [AETHER's source-linked review](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6543586434) called for an additional deterministic **bundler-level** verified-bytes-versus-written-bytes regression. [Reviewer `yuanchen8911`](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6547084760) independently recognized the gap as a **nonblocking** future test opportunity.
- **Attribution and closure:** no evidence that AETHER authored the merged fix or that this additional AETHER-proposed test was included. The existing PR is **CLOSED / MERGED**, and the AETHER review-follow-up is **DOCUMENTED / CLOSED**, not a pending PR or an implemented test. A new test would require separate distinct-source qualification and approval.

### Public correction preserved — PyTorch #202806

The original [AETHER technical comment](https://github.com/pytorch/pytorch/issues/202806#issuecomment-6551875732) used a stronger "silently wrong gradient" characterization. [Upstream maintainer `ezyang` clarified](https://github.com/pytorch/pytorch/issues/202806#issuecomment-6581961573) that eager execution should raise an in-place-modification error and the compiler omits this version check; the verified characterization is a **missing error check**, **not** a wrong gradient from a valid program. We retain this correction alongside the original public historical link.

These represent eight source-backed **observations**, not eight AETHER-authored merged fixes. The tests in OpenTelemetry and Redis are AETHER candidate source with local native evidence; PyTorch and AWS CDK modifications belong to the upstream authors. NVIDIA/aicr merged a PR without proof of AETHER test inclusion, and node-redis #3564 was closed unmerged.

[Detailed outcome descriptions](../data/outcomes.json) · [Status meanings](../docs/STATUS_DEFINITIONS.md)
