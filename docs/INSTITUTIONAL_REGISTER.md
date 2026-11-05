# Unified institutional contribution register

**AETHER X GLOBAL** · Baseline: 3 November 2026 · Dated additions: 4 and 5 November 2026.

The canonical machine-readable index is [`data/institutional_register.json`](../data/institutional_register.json), reconciled without rewriting original sources by [`scripts/validate_institutional_register.py`](../scripts/validate_institutional_register.py).

## What is indexed

- **262 unique participation permalinks** after deduplicating the 242 verified comment/review links, 10 verified authored discussions, 43 curated historical catalog links and three dated status records. The source groups overlap; their counts must **not** be added together.
- **233 discovered public discussion threads**, each linked to known participation permalinks and marked with its historical state observed on 3 November.
- **43 originally curated records** retain their historical classification and ID; **4 dated status observations** link to their source records without changing the old snapshot.
- **215 source-identity-only links** remain unqualified for editorial/engineering achievement claims; their existence does not imply implementation, acceptance, independent testing, endorsement or merging.

The register contains `records[]` keyed by canonical `source_url` and `threads[]` keyed by `thread_url`. Every record links to its original discussion thread, records applicable identity evidence, optionally references a historical catalog ID and a latest dated status ID, and has an explicit `qualification_tier`. State observed during discovery is historical, **not a live GitHub state**.

## Controlled maintenance

1. Capture original public source permalink, actual author and exact dated evidence from upstream.
2. Keep the 2026-11-03 historical JSON, CSV, author-discovery files and original test evidence immutable.
3. Add a new dated file in `data/status-updates/` when source state changes. Never rewrite an earlier observation to make a project appear accepted.
4. Rebuild the index from source files and run `python3 scripts/validate_catalog.py` plus `python3 -m unittest discover -s scripts -p 'test_*.py' -v` before PR review. The validator checks **all indexed sources**, links, tiers, threads and no duplicate URL.
5. A proposed advancement from an identity-only link to a qualified outcome needs fresh source checks, an evidence receipt, attribution and review. `scripts/verify_status_evidence.py` pins current dated observations; `scripts/verify_upstream_live.py --live` offers **on-demand read-only** re-verification. Upstream changes after the date are reported as drift, not retroactive falsification.
6. Only independently reviewed and Founder-approved internal PRs may update the public portfolio. This code does **not** post comments to any external project or merge code.

**Scope statement:** This is a public-safe, source-linked participation index for the company, not a cryptographically signed institutional approval ledger, warranty of external claims or a complete catalogue of unpublished internal engineering work.

## Targeted F01 frozen source inputs

Original 2026-11-03 source observations and the dated 2026-11-04 status/receipt have fixed Git blob SHAs in `scripts/verify_frozen_snapshots.py`. Both deterministic index generation `build()` and verification `check_register()` reject altered frozen source bytes **before** computing or accepting the derived register.

A real negative test copies source files into a temporary directory, replaces the original `Adyen/adyen-flutter#issuecomment-5952974431` permalink with a fabricated comment ID while preserving record counts, then attempts to regenerate the register. This is now rejected by the frozen-source SHA guard.

A future correction must create a new dated evidence item and pass genuine independent review rather than silently replacing historic input URLs or refreshing their pinned hashes. These offline code-defined pins cannot independently withstand an actor that can edit the verifier, pinned digests, and CI itself; enforcement remains part of the separately approved F02 control.

## New dated source links — append-only update lane

The original seven frozen source/receipt files and 262-link/233-thread baseline remain **byte-identical**. For future observations, create `data/updates/YYYY-MM-DD.json` with schema `AX-UNQUALIFIED-PARTICIPATION-v1`, `snapshot_date`, `source_account` and a nonempty `participations` array. Each row must supply exact source permalink, repository, declared author `aetherxeg-source`, `kind` (`comment`, `authored_issue`, `authored_pull_request`), matching `thread_url` and observed state (`open` / `closed` / `unknown`).

Append the dated path and exact file SHA-256 to `data/updates/manifest.json`, sorted by ascending dates. Source/manifest hashes guarantee internal byte consistency **only**, not genuine public authorship or upstream acceptance. The validator rejects duplicate JSON keys, path traversal, duplicate source links, unmanifested snapshots, incorrect digests, wrong repository/thread identities and false qualification fields. Always verify the original GitHub permalink independently before asking the Founder to approve the PR.

Run `python3 scripts/validate_institutional_register.py --write` on the review branch, inspect the derived-index diff, then run normal and optimized-mode CI. The resulting new links **always remain `SOURCE_IDENTITY_ONLY_UNQUALIFIED`** and cannot silently become merged, accepted or security-certified. A later qualified status requires a dedicated, separately reviewed, source-pinned dated status record and validator update. The original 2026-11-03/04 observations must never be rewritten.

For current **zero additional snapshots**, rebuilding reconciles to the same complete source/record identities, although list iteration order can differ; counts are lower bounds (262 sources, 233 threads, three historical dated statuses), not permanent ceilings. No new public source URLs have been claimed or published as part of this engineering upgrade.

## 5 November source-backed status

[NVIDIA OpenShell issue #4111](https://github.com/NVIDIA/OpenShell/issues/4111) closed after [PR #4714](https://github.com/NVIDIA/OpenShell/pull/4714) was merged by upstream author `lunarwhite`. The existing [AETHER X technical comment](https://github.com/NVIDIA/OpenShell/issues/4111#issuecomment-5955273345) is now classified as `UPSTREAM_RELATED_FIX_MERGED_THIRD_PARTY_AUTHORED`. This is **one qualified dated status**, not a new participation permalink or AETHER-authored upstream merge. The resulting institutional register remains **262 sources**, **233 threads**, **four dated status records**, and **215 unqualified sources**. No evidence establishes causal use of AETHER's advice or endorsement by NVIDIA.

The [dated report](STATUS_UPDATE_2026-11-05.md), [primary-source receipt](../data/evidence/2026-11-05-primary-receipts.json), [strict verifier](../scripts/verify_nvidia_2026_11_05.py), and independent negative tests supply the bounded release evidence. The source/receipt pair is not a cryptographic external attestation; simultaneous alteration of validator and records requires code review and Founder authorization.
