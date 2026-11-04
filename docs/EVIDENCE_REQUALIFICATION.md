# Dated evidence receipt and requalification rules

The 4 November 2026 status file is pinned in [`data/evidence/2026-11-04-primary-receipts.json`](../data/evidence/2026-11-04-primary-receipts.json). The additive [validator](../scripts/verify_status_evidence.py) checks exact source URL, project, account where applicable, status, Apache fork/HEAD, original evidence permalinks, third-party Watchlist commit, Redis closure reason, and field-by-field consistency between the record and the stored receipt.

This prevents the specific [Assurance F1 finding](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/pull/7#issuecomment-6641466111): an Apache PR number replaced by another PR on the same host; a fabricated head SHA; an ExecSurface submission swapped for another issue; or a claim in the description altered independently of the receipt. Independent mutation tests are in [`test_register_assurance.py`](../scripts/test_register_assurance.py).

**Trust boundary:** The stored receipt is public GitHub source metadata and a repeatable evidence pointer, **not** an external signature, authenticated human reviewer approval or proof that GitHub's current status remains unchanged. For a proposed status promotion, rerun the read-only [live audit](../scripts/verify_upstream_live.py) using `python3 scripts/verify_upstream_live.py --live` in a networked environment, inspect any source drift, collect new upstream links with times, then add a **new dated snapshot** and separately review it. Offline CI remains deterministic and rejects edits to these 2026-11-04 observations that were not independently updated through a reviewable source/receipt pair.

**No legacy weakening:** the original `validate_catalog.py` assertions, historical curated 43-entry JSON/CSV, 242 original author-linked source URLs, 233 discovery threads, and source test bytes/hashes remain untouched. New tests extend, not replace, the original checks.

## Targeted F03 and PR7-F1 joint-edit resistance

The published 4 November status and receipt JSON are now pinned to their original Git **blob SHA** in `scripts/verify_frozen_snapshots.py`. Each original record's full fields, including `description` and `ci_boundary`, are compared to fixed reviewed literals in `scripts/verify_status_evidence.py` instead of relying on agreement between two editable records.

Real Python negative tests append a false certification, false Apache upstream CI pass, or false AETHER authorship of another maintainer's Redis patch to **both** the record and receipt, preserving the prior denial phrases. All such paired mutations must be rejected. Future status changes belong in a new separately reviewed dated snapshot.

**Security boundary:** these pins prevent edits to historical data **without editing verification code**. They are not immutable remote signatures or a substitute for independently authenticated GitHub review. An authorized actor able to change the validator and CI together can invalidate these controls unless the distinct F02 review gate is activated. Upstream current truth remains subject to read-only source verification.
