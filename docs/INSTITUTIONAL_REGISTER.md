# Unified institutional contribution register

**AETHER X GLOBAL** · Baseline: 3 November 2026 · Dated additions: 4 November 2026.

The canonical machine-readable index is [`data/institutional_register.json`](../data/institutional_register.json), reconciled without rewriting original sources by [`scripts/validate_institutional_register.py`](../scripts/validate_institutional_register.py).

## What is indexed

- **262 unique participation permalinks** after deduplicating the 242 verified comment/review links, 10 verified authored discussions, 43 curated historical catalog links and three dated status records. The source groups overlap; their counts must **not** be added together.
- **233 discovered public discussion threads**, each linked to known participation permalinks and marked with its historical state observed on 3 November.
- **43 originally curated records** retain their historical classification and ID; **3 dated status observations** link to their source records without changing the old snapshot.
- **216 source-identity-only links** remain unqualified for editorial/engineering achievement claims; their existence does not imply implementation, acceptance, independent testing, endorsement or merging.

The register contains `records[]` keyed by canonical `source_url` and `threads[]` keyed by `thread_url`. Every record links to its original discussion thread, records applicable identity evidence, optionally references a historical catalog ID and a latest dated status ID, and has an explicit `qualification_tier`. State observed during discovery is historical, **not a live GitHub state**.

## Controlled maintenance

1. Capture original public source permalink, actual author and exact dated evidence from upstream.
2. Keep the 2026-11-03 historical JSON, CSV, author-discovery files and original test evidence immutable.
3. Add a new dated file in `data/status-updates/` when source state changes. Never rewrite an earlier observation to make a project appear accepted.
4. Rebuild the index from source files and run `python3 scripts/validate_catalog.py` plus `python3 -m unittest discover -s scripts -p 'test_*.py' -v` before PR review. The validator checks **all indexed sources**, links, tiers, threads and no duplicate URL.
5. A proposed advancement from an identity-only link to a qualified outcome needs fresh source checks, an evidence receipt, attribution and review. `scripts/verify_status_evidence.py` pins current dated observations; `scripts/verify_upstream_live.py --live` offers **on-demand read-only** re-verification. Upstream changes after the date are reported as drift, not retroactive falsification.
6. Only independently reviewed and Founder-approved internal PRs may update the public portfolio. This code does **not** post comments to any external project or merge code.

**Scope statement:** This is a public-safe, source-linked participation index for the company, not a cryptographically signed institutional approval ledger, warranty of external claims or a complete catalogue of unpublished internal engineering work.
