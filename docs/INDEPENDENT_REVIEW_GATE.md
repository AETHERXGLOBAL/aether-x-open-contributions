# Independent PR review — proposed enforcement, not activated

**Scope:** AETHER X GLOBAL / `aether-x-open-contributions` · **Status:** PREPARED_NOT_ENFORCED.

## Current verified condition (4 November 2026)

The active `AETHER X Public Evidence Main Guard` ruleset #26478002 requires a PR, squash-only merge, and a successful `catalog-integrity` check. Its required approving reviews count is **zero**. `.github/CODEOWNERS` lists only `@aetherxeg-source`, the same account that authored PR #7. This is **not** a verifiable independent reviewer. A PR author, a separate plugin writing through the same GitHub login, or a narrative review posted as a PR comment does not satisfy an independently authenticated GitHub review.

## Proposed gate for Founder consideration

[Machine-readable proposal](../data/review-gate-proposal.json) records the desired settings, without applying any of them:

- Register a genuinely independent **eligible human GitHub reviewer** with appropriate write/review permissions and distinct identity from the PR author / last pusher.
- Replace author-only CODEOWNERS with that explicitly authorized reviewer (or properly managed independent team). Do **not** invent usernames or create placeholder approvals.
- Set `required_approving_review_count: 1`; enable stale-review dismissal and last-push approval, require code-owner review **only once the independent CODEOWNER is effective**, retain unresolved-thread checks, `catalog-integrity`, linear history and squash-only merges.
- Ensure all paths (especially `data/`, `scripts/` and workflow files) are covered by a genuinely independent review owner. Keep safe administrative recovery.
- Obtain explicit Founder approval of the final identity/roles and exact ruleset/CODEOWNERS configuration before a privileged actor applies it.

## Accountable workflow and auditability

**Engineering** supplies source changes, hashes and rerunnable tests, and cannot approve its own implementation. **Assurance** performs cold-start evidence/falsification review, signs its dated verdict tied to the exact candidate HEAD, and remains separate from the author; an Assurance opinion issued through the author's GitHub identity is evidence of review activity, **not** a distinct authenticated reviewer approval. **Founder** alone authorizes institutional acceptance and merge after the applicable gates pass. A merge action also requires the real GitHub ruleset to be satisfied, not just written policy.

**Activation acceptance:** demonstrate on an expendable test PR that author-only approval does not meet the rule; a current independent eligible reviewer approval does; the last push invalidates stale approvals; unresolved threads and failing `catalog-integrity` block merge; authorized administrators retain recovery access. Record the actual GitHub Ruleset revision and validation links. No settings, memberships, reviewer permissions or CODEOWNERS changes are part of this PR.

**Known blocker:** an independent, eligible human GitHub reviewer account has **not yet been identified/verified**. Consequently F02 is **designed and testable at the policy level**, but **not technically enforced**.
