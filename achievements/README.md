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
| NVIDIA/aicr | `UPSTREAM_REVIEWER_ACKNOWLEDGED_GAP` | [View original](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6547084760) |
| redis/node-redis | `UPSTREAM_AUTHOR_IMPLEMENTED_TEST_ON_CLOSED_PR` | [View original](https://github.com/redis/node-redis/pull/3564#issuecomment-6544676687) |

These represent eight source-backed **observations**, not eight AETHER-authored merged fixes. The tests in OpenTelemetry and Redis are AETHER candidate source with local native evidence; PyTorch and AWS CDK modifications belong to the upstream authors. NVIDIA/aicr merged a PR without proof of AETHER test inclusion, and node-redis #3564 was closed unmerged.

[Detailed outcome descriptions](../data/outcomes.json) · [Status meanings](../docs/STATUS_DEFINITIONS.md)
