# Governed public-contribution updates

The existing 2026-11-03 portfolio in \`data/contributions.json\` is a verified **historical snapshot**. Automatically discovered activity is **not** a new achievement and must not silently overwrite a dated report.

## Active automation after merge

- [Public catalog integrity](../.github/workflows/public-catalog-integrity.yml) checks repository PRs and commits to \`main\` against JSON/CSV consistency, published-source SHA-256 values and Python discovery unit tests.
- [Public activity discovery](../.github/workflows/public-activity-discovery.yml) is scheduled **Mondays at 05:31 UTC** and supports manual workflow dispatch.
- The discovery job is **read-only**, using only GitHub's repository-scoped token. It searches public issues and PRs involving \`aetherxeg-source\`, then checks original issue comments, PR review comments and public reviews against the exact author identity.
- It emits a GitHub Actions artifact with exact comment permalinks, dates, provenance, review-only status, summary and SHA-256; no public JSON catalog writes, external messages, automatic PRs or merges.
- GitHub can delay or disable scheduled runs. Successful future execution **must be verified from an actual workflow run**, not inferred from this file. The artifact is retained for 30 days.

## Controlled promotion

Only after human engineering and provenance review may candidates be promoted via a separate PR:

1. Verify public original GitHub permalink, login, context and technical relevance.
2. Distinguish an original issue, authored PR, discussion comment, native executable test, upstream author's code correction and actual merged/released material.
3. Preserve test hashes, exact revisions and limits for runtime claims.
4. Attribute upstream-authored tests/fixes to their original authors.
5. Check privacy, third-party rights, reproducibility and existing historical duplicates.
6. Update the structured catalog and display together; validate via passing GitHub-hosted CI.
7. Review and merge on \`main\` under repository ruleset. Do not auto-promote technical comments to merged achievements.

## Historical discovery baseline

[data/discovery/2026-11-03-public-threads.json](../data/discovery/2026-11-03-public-threads.json) is a GitHub-search **thread census**, not 233 independently verified comment IDs. It found 210 issue threads and 13 PR threads containing contributor comments; it also searched seven external authored issues and three external authored PRs, producing **233 distinct external discussion threads**, with **200 threads beyond the previously cataloged discussion set**.

The original 43 public permalink records are retained, without inflation of impact metrics. Discovery candidates remain \`TECHNICAL_REVIEW_PENDING\` until their exact original comments are inspected.
