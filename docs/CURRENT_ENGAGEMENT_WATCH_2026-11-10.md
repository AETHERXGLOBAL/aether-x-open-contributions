# AETHER X GLOBAL — Engineering contribution priorities (10 November 2026)

**Owner:** AETHER DEVREL & INBOX (editorial accountability), with engineering support for reproducible targeted tests.  
**Evidence date:** 2026-11-10 UTC. **Mode:** source-linked public observation, not an authorization for external posting or merging.

## P0 — AWS CDK #39680: targeted qualification, not volume

- **Source:** [upstream Draft PR #39680](https://github.com/aws/aws-cdk/pull/39680); [bug #39674](https://github.com/aws/aws-cdk/issues/39674); [published commit](https://github.com/aetherxeg-source/aws-cdk/commit/86c250c6802d2d0035ea58ec12970229e59d9d3d).
- **Observed state:** authored by `aetherxeg-source`, **OPEN / DRAFT / UNMERGED**, seven files, exact PR HEAD `86c250c6802d2d0035ea58ec12970229e59d9d3d`.
- **Upstream blocker (separate from CI approval):** [AWS CDK automation review](https://github.com/aws/aws-cdk/pull/39680#pullrequestreview-5847544183) says fixes must include an integration test **and its generated snapshot**. Source test file alone does not satisfy the rule.
- **CI state:** workflows were `action_required` awaiting upstream maintainer approval. This is not a failing test and not a PASS.
- **Engineering disposition:** use an isolated exact-source candidate and official integration tooling to generate and verify the missing snapshot, capturing actual command/exit code and file list. The previous full JSII build exited with status 1 but did not capture diagnostic stderr; do **not** label it OOM without evidence. Run targeted dependency/build/lint/EC2/feature-flags checks on the publish candidate, including the **2×2 trust vs permissions flag matrix** where the related [permissions PR #39536](https://github.com/aws/aws-cdk/pull/39536) warrants it. Preserve backward compatibility and user-supplied IAM role behavior. No AWS deployment.
- **Stop / proceed gate:** do not mark PR ready for review, request an exemption or claim upstream qualification based solely on earlier-baseline local results. Change only what actual tooling/reviewer evidence requires; avoid duplicate external comments.

## P1 — Apache Ballista #2775: maintainers' narrower design

- **Source:** [upstream PR #2775](https://github.com/apache/datafusion-ballista/pull/2775), exact HEAD `09ecf8caa322c29ec57c2e9e1f7bebbffd987e93`.
- **Observed state:** **OPEN / UNMERGED**, authored by `aetherxeg-source`. Maintainer [requested a minimal TempDir guard and targeted test](https://github.com/apache/datafusion-ballista/pull/2775#pullrequestreview-5792764496); the submitter [reported the reduced one-file candidate and 101/101 local executor library tests](https://github.com/apache/datafusion-ballista/pull/2775#issuecomment-6688758962) on 6 Nov.
- **Remaining gate:** upstream Rust CI remains `action_required` on the existing HEAD; earlier local results are not upstream CI. Await a real maintainer/CI event, then inspect and fix the specific failure if any. **No repeated approval requests or unsolicited comments**.

## P2 — Preserve accurately attributed third-party outcomes

- **[Redis PR #15930](https://github.com/redis/redis/pull/15930):** **MERGED 10 Nov 2026**, authored by `namespaceMarcello`. The author [explicitly credited the AETHER-reported AOF regression path](https://github.com/redis/redis/pull/15930#issuecomment-6663086469), but the merged source and tests are upstream-author-owned; exact byte-for-byte adoption and causality are unproven. Existing AETHER [pinned RED/GREEN source evidence](../tests/redis/15930/README.md) must remain separately attributed. No new third-party outreach.
- **[Cloudflare workers-sdk #16612](https://github.com/cloudflare/workers-sdk/pull/16612):** **MERGED 9 Nov 2026**, authored by `petebacondarwin`. Earlier AETHER review identified environmental forwarding risk; merged authorship and causal influence remain distinct. See [dated source evidence](STATUS_UPDATE_2026-11-09.md).

## Operating gates and measurement

1. **Measure accepted code and test adoption separately from comments and opened PRs.** Highlight verified authored merges, then the best open code candidates with exact unresolved blockers. Do not optimize for total discussion count.
2. A real outcome update requires an original upstream permalink, source author, date, exact state/head, what tests actually ran and limits; preserve prior observations.
3. Keep the public machine-readable register and 3 November historical catalog immutable except via governed append-only snapshots and specifically reviewed qualification paths. Do not change achievement tiers merely because an upstream related PR merged.
4. Company internal merges require Founder authorization for the exact PR and HEAD plus repository integrity checks. This plan itself does not authorize external publication, new AWS spend, deployment, live trading, or merging any upstream PR.

**Immediate next decision:** focus engineering on AWS CDK official integration snapshot evidence, and keep Ballista monitoring passive until maintainers supply actionable results.
