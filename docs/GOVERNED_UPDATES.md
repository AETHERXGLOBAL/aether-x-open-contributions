# Governed external contribution operations

## One accountable owner; no duplicate registries

AETHER X GLOBAL uses one primary DevRel operating function for upstream technical participation. **AETHER DEVREL & INBOX is the accountable editorial lead**, working with Engineering for executable code, tests and independent technical checks when required. A named role does not establish an autonomous deployed agent: actions occur only through the actual tools and delegated human approvals available.

| System | Sole purpose | Allowed outputs |
|---|---|---|
| Private company institutional memory | Detailed source of truth for investigations, test receipts, decisions and internal review | Private evidence, hashes, approvals and engineering plans |
| [Public Open Contributions](../README.md) | Curated, public-safe portfolio of verified external participation and reproducible engineering artifacts | Public pages, source-linked snapshots, licensed code and reviewed PRs |
| **AETHER GitHub Interaction Watch** | Incoming human replies, questions, reviewer requests, actionable PR changes and reputational/security risks | Alerts and proposed actions, **not** automatic external replies or catalog changes |
| [Public activity discovery](../.github/workflows/public-activity-discovery.yml) | Weekly historic public account activity and exact commenter identity | Read-only, SHA-256-verifiable review artifact; **never** a new achievement claim |
| [Public catalog integrity](../.github/workflows/public-catalog-integrity.yml) | Validate curated catalog and source integrity on pull requests and `main` | GitHub Actions PASS/FAIL; no automatic approval or merge |

**Single-entry rule:** once a public comment or PR has an exact GitHub permalink, store it **once** under its canonical ID in the curated catalog. Preserve older dated observations rather than duplicating entries or rewriting the historical evidence. The private ledger can contain additional nonpublic technical details; the public repository is a sanitized projection, not a parallel private source of truth.

## Controlled updates and evidence promotion

1. **Discover:** the weekly read-only action finds source-linked activity. The interaction watch separately reports only human responses that require a decision, not the same weekly discovery feed.
2. **Verify:** open the original upstream thread, check exact comment author, relevant license/policy, issue/PR state, current HEAD, duplicate work and reviewer instructions. Separate actual change authorship from suggestions.
3. **Qualify:** if claiming an executable result, supply exact source revision, reproducible test, positive and negative controls, original byte hashes and precise limitations. Verification by a human or an independent run must be described truthfully.
4. **Editorial review:** the DevRel lead prepares a dated status update. Engineering assesses code correctness; security/privacy/rights risks are explicitly resolved. A human must review any AI-assisted material intended for upstream.
5. **Publish:** only a reviewed PR to this public repository may upgrade the curated portfolio; the branch ruleset requires `catalog-integrity`. External upstream comments or code PRs need **separate explicit authorization for the exact platform, target, identity and content**, plus compliance with that upstream project's contributor rules.
6. **Observe:** continue monitoring for actual maintainer decisions, upstream merge and release. Do not re-post unresolved comments or confuse acknowledgement with adoption.

## AI-assisted external contributions — mandatory human control

Open-source maintainers set project-specific contribution policies. Before any external publication, inspect the current upstream `CONTRIBUTING`, conduct guidelines, AI usage policy, and PR/issue templates. If maintainers object to AI-generated comments, **stop automated posting**, respect their instruction and route the situation to a human accountable contributor. A successful local test does not override a communication policy.

For example, OpenTelemetry's [Generative AI policy](https://github.com/open-telemetry/community/blob/main/policies/genai.md) permits assistance with test/code authoring under meaningful human review and appropriate disclosure, and expressly discourages copy/pasting LLM-generated issue or PR commentary. A human driving such a contribution must read, understand, independently check and take responsibility for it; add an appropriate `Assisted-by:` trailer when primarily AI-assisted code is proposed under that policy. **No automatic upstream resubmission is authorized.**

## Automation boundaries

The weekly GitHub Actions discovery runs Mondays at **05:31 UTC**, or manually through `workflow_dispatch`; it has read-only GitHub content permissions and emits a 30-day review artifact with a SHA-256 manifest. It cannot write the public catalog, third-party repositories or private memory. Scheduled GitHub runs are subject to GitHub availability and must be verified individually.

The [source-link register](../data/discovery/README.md) contains 233 discussion threads and 242 original public comment/review permalinks from the dated 2026-11-03 discovery run. These records are **participation signals**, not 242 accepted engineering contributions. The original 43 curated entries remain the separately qualified historical baseline.

## Operational exception handling

Safety, legal/license concerns, explicit maintainer warnings, disclosure problems, false impact claims, duplicate unwanted outreach, or material CI regression take priority over new contributions. Preserve the authoritative original URL/time and a proportionate internal receipt. Never attribute an upstream author's code to AETHER, imply institutional endorsement, or publish a private infrastructure report.

**Founder-controlled merge authority (current):** the Founder personally and directly authorizes each specific PR and exact HEAD before final integration. See [machine-readable authority and live limitations](../data/founder-merge-policy.json) and [F02 decision record](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/issues/9). Reviewers, including `ahmed363younis-dot` with prior `read` permission, are optional technical reviewers and have **no release approval authority**. The actual GitHub ruleset still enforces `catalog-integrity`, PR creation and squash-only, but does **not** authenticate Founder approvals expressed in a separate chat; check the recorded personal decision before any action. No agent may self-authorize a merge. Genuinely binding project-specific, legal or contractual review requirements remain applicable. The earlier extra human-reviewer activation proposal was superseded as a voluntary prerequisite; it must not be represented as a live GitHub control.

**Evidence integrity and future additions:** run `python3 scripts/validate_catalog.py`, `python3 -O scripts/validate_catalog.py` and the test suite. Frozen 2026-11-03/04 source bytes remain pinned. New participation is appended through date-ordered SHA-256 reconciled files in `data/updates/`, never rewriting historical observations and never automatically asserting authorship verification, code merge or adoption. New status classifications require their own specifically reviewed evidence and validation; a new link is `SOURCE_IDENTITY_ONLY_UNQUALIFIED` until then.
