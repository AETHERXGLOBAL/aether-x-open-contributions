# AETHER X GLOBAL — Outcome-Gated Engineering Impact Program

**Decision:** Founder-endorsed strategic direction, 2026-11-06; **no fixed calendar deadline**.
**Document state:** Proposed operational record on a review branch. This document does not by itself constitute a merged policy, authenticate the Founder's exact-HEAD merge approval, or authorize external publication.
**Accountable owner:** AETHER DEVREL & INBOX; Engineering owns executable code and tests, with proportionate independent technical challenge for material claims.

## Mission and success rule

Build AETHER X GLOBAL's credibility through reproducible fixes accepted by external maintainers, externally confirmed technical outcomes, and independent use of our products. Optimize for **verified impact per unit of effort**, not issue/comment counts or association with famous organizations. The company builds governed/verifiable intelligence and execution infrastructure; this contribution program is not a claim that the company is a cybersecurity vendor.

Move between workstreams **when evidence-based criteria are met**, not when a week or month ends. Milestones below are directional targets, **not deadlines**, acceptance guarantees, or a mandate to publish low-quality contributions.

## Workstreams and advancement gates

| Workstream | Execute now | Evidence required to advance | STOP / exclusion |
|---|---|---|---|
| **A. Close accepted upstream work** | Prioritize the already-submitted Apache Ballista PR, then assess Pydantic readiness; monitor other existing technical responses. | External maintainer decision, source-verified PR state, upstream CI outcome, exact commit, and confirmation of who actually authored the change. | No repetitive status comments, branch churn just to look active, or declaration of success before merge. |
| **B. Code-first external engineering** | Maintain at most **two** active *new* technical candidate investigations. Select for relevance to reliability, execution behavior, data integrity, and AI infrastructure. | Reproducible failing baseline; targeted fix or test; passing positive and negative controls; relevant upstream contribution/GenAI policy; duplicate-work check; author-approved exact outward contribution. | No unsolicited AI-generated discussion, speculative mass outreach, untested patches, or publication of vulnerability details outside appropriate private channels. |
| **C. Independent product use** | Prepare reproducible, truthful workflows showing ExecSurface and ReproCert used in real CI / developer situations. Invite independent technical trials **only through separately approved and policy-compliant outreach**. | Independent operator, reproducible environment and outcome, explicit consent to publish attributed results, limitation/false-positive record, and genuine usage (not just stars or directory listings). | No fabricated users, endorsements, metrics or certified security claims. No paid infrastructure without approval. |
| **D. Evidence-to-reputation** | Curate only qualified external outcomes into this repository and produce concise technical case studies when supported. | Source permalinks, exact HEAD/base, author attribution, actual test results, negative controls, licensing/privacy clearance, and independent check where material. | Never promote public participation-only links to achievement status without a reviewed dated evidence update. |

## Current operational priority queue (source-checked 2026-11-06)

1. **Apache Ballista #2775 — active AETHER-authored PR:** [PR](https://github.com/apache/datafusion-ballista/pull/2775). Minimal workdir-lifetime fix at head `09ecf8caa322c29ec57c2e9e1f7bebbffd987e93`; local executor qualification reported as 101/101 and local scheduler/executor integration, while upstream CI runs report `action_required`. The maintainer's earlier `CHANGES_REQUESTED` review remains the latest review. AETHER's reply is [already posted](https://github.com/apache/datafusion-ballista/pull/2775#issuecomment-6688758962). **Next permitted action:** monitor a real maintainer response or CI authorization; react to new evidence, do not repeat the same request. An open PR is not an accepted fix.
2. **Pydantic #14230 — candidate, not a PR:** [issue](https://github.com/pydantic/pydantic/issues/14230). Issue open, maintainer assignment/acceptance not confirmed. **Next permitted action:** inspect upstream requirements and wait for maintainer disposition before an outward PR. Prepared local code does not equal accepted code.
3. **Redis #15930 — existing upstream-author change:** [PR](https://github.com/redis/redis/pull/15930). AETHER prepared a separately executed AOF replay test candidate; the upstream author added AOF regression coverage and credited the contribution. **Next permitted action:** watch final review and merge, verify any included exact code; do not claim AETHER-authored merged code or duplicate the owner's tests.
4. **Cloudflare #16755 — reproduced external issue:** [issue](https://github.com/cloudflare/workers-sdk/issues/16755). An upstream reproduction confirmed misleading Access redirect recognition; another contributor has volunteered. **Next permitted action:** monitor assignment and fix; avoid competing work and do not equate reproduced issue with accepted patch.
5. **PyTorch #202881 — upstream test author response:** [PR](https://github.com/pytorch/pytorch/pull/202881). Upstream author implemented a deterministic regression after the AETHER proposal. **Next permitted action:** follow review/merge and credit upstream authorship.
6. **OpenTelemetry #15966 — upstream PR merged, AETHER test not merged:** [PR](https://github.com/open-telemetry/opentelemetry-collector/pull/15966). Preserve the independently executed AETHER Graph.Build candidate evidence without presenting it as an upstream-merged test. **Hard communication rule:** respect its GenAI policy and prior maintainer warning; no automatically generated follow-up comments.

The existing [current participation watch](CURRENT_ENGAGEMENT_WATCH_2026-11-06.md) and canonical sources remain the operational source for dated factual changes. This priority queue is not a parallel issue register.

## Directional outcome measures — milestone-based, not time-based

- **Two additional AETHER-authored upstream code/test PRs merged** beyond the historical two accepted `useful-actions` directory PRs. Prefer substantial tested functionality over listing-only edits.
- **Three separate technical improvements or test cases demonstrably acted on by upstream authors**, each with accurately attributed source evidence. Reviewer acknowledgement alone is a lower tier.
- **Three independent users or teams running a documented ExecSurface or ReproCert workflow** and providing reproducible outcomes. A download, star, or reply does not count.
- **Two source-verified case studies** containing the failure, test, result, limits, and actual author/maintainer outcome.
- **Zero known policy or consent violations**, unsolicited repeated follow-ups, unsupported endorsements, or inflated acceptance claims.

These targets guide allocation only. Missing a numeric target never justifies weaker evidence or unapproved communications.

## Operating decision gates

- **Single source of truth:** existing GitHub discussion/PR is authoritative for upstream state; this repository provides a reviewed, public-safe evidence projection. Private institutional memory contains detailed private execution receipts; do not duplicate its ledger here.
- **Low-cost execution:** use connected GitHub tools, local tests, and existing ChatGPT access; no mandatory Codex, paid API, cloud spend or new parallel agent fleet.
- **Publication boundary:** inspect current target repository conduct, contributor, license, disclosure and GenAI rules before *each* new outward comment, issue or PR; obtain explicit target-and-content-specific approval. Strategy approval is **not** blanket permission to post.
- **Merger boundary:** company-owned changes are reviewed through Draft PR and the repository's real checks. Final merge remains Founder-only, tied to the **exact PR, head SHA and base**; do not infer this from general strategy approval.
- **Assurance:** independent critical review for meaningful security or reliability claims; preserve failed tests, falsifiers, correction notices and full third-party author credit. No independent endorsement claim without source proof.
- **Cadence:** progress only on new upstream evidence, passing a technical gate, verified pilot feedback or a meaningful risk. **No fixed calendar schedule, fabricated background work, or forced number of weekly posts.**

## First executable actions

1. Maintain Ballista #2775 as the primary code-acceptance gate, while awaiting Apache's next response or CI authorization.
2. Qualify Pydantic #14230 against contributor policy and a reproducible failing/passing baseline before proposing any code.
3. Prepare **one** local, reproducible ExecSurface CI demonstration and a matching ReproCert evidence example using existing projects; collect the exact execution transcript, limitations and secret-safety check before any external invitation.
4. Screen only one additional issue for high-value code-first work once active capacity allows; prefer a maintainer-receptive problem with a failing test. No launch based on brand name alone.
5. Update the public achievement tier only after new primary-source evidence is verified through the existing dated, append-only review lane.

**Not an upstream approval, product certification, affiliation claim, automatic publishing instruction, or corporate spending authority.**
