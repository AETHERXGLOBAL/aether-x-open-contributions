"""Pinned dated source receipts and explicit anti-inflation checks.

This is an offline evidence-gate, not a substitute for querying upstream live state.
"""
import json
import pathlib
from integrity_runtime import require
from append_only_updates import read_unique_json

from verify_frozen_snapshots import check_all as assert_frozen_sources

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = {
    "APACHE-BALLISTA-2775": {
        "ci_boundary": "Only Process success observed; six upstream workflows required maintainer approval at the 2026-11-04 checkpoint; internal targeted 13/13 tests are not upstream CI.",
        "description": "AETHER-authored Rust workdir/shuffle lifetime fix published as Apache upstream PR #2775. Open and unmerged; no Apache approval, merge or production adoption established.",
        "project": "apache/datafusion-ballista",
        "kind": "authored_pull_request",
        "status": "OPEN_UNMERGED_AUTHORED_PR",
        "source_url": "https://github.com/apache/datafusion-ballista/pull/2775",
        "evidence_urls": [
            "https://github.com/apache/datafusion-ballista/issues/2767",
            "https://github.com/AETHERXGLOBAL/datafusion-ballista/commit/62543d90754a0e77e3d8a765ed82d8ccde9306ce",
        ],
        "submitter_account": "aetherxeg-source",
        "organization": "AETHER X GLOBAL",
        "head_repository": "AETHERXGLOBAL/datafusion-ballista",
        "head_commit": "62543d90754a0e77e3d8a765ed82d8ccde9306ce",
        "changed_files": 12,
        "merged": False,
        "review_state": "UPSTREAM_REVIEW_PENDING",
    },
    "EXECSURFACE-WATCHLIST-133": {
        "description": "ExecSurface was listed in the upstream WATCHLIST.md, with explicit limitations: early public alpha, Linux x86_64, ptrace observation after the inspected command runs, and possible sensitive evidence artifacts. This is watchlist visibility, not certification, verified runtime testing, security endorsement or broader adoption.",
        "project": "scadastrangelove/awesome-ai-security-tools",
        "kind": "third_party_watchlist_inclusion",
        "status": "THIRD_PARTY_WATCHLIST_LISTED",
        "source_url": "https://github.com/scadastrangelove/awesome-ai-security-tools/issues/133",
        "evidence_urls": [
            "https://github.com/scadastrangelove/awesome-ai-security-tools/issues/133#issuecomment-5857686313",
            "https://github.com/scadastrangelove/awesome-ai-security-tools/commit/e0ec97f6f0b696d6a5ab0cb2158b8b4c1458c831",
            "https://github.com/scadastrangelove/awesome-ai-security-tools/blob/e0ec97f6f0b696d6a5ab0cb2158b8b4c1458c831/WATCHLIST.md",
        ],
        "submitted_by": "aetherxeg-source",
        "upstream_issue_closed_as": "completed",
        "review_scope": "Static reviewer assessment only; no commands executed by upstream maintainer.",
    },
    "NODE-REDIS-3579": {
        "description": "Maintainer declined the proposed additional cached EVALSHA_RO/EVAL_RO ACL test as redundant with existing coverage and closed issue #3579 as not planned. The separately authored upstream fix #3567 was merged; the proposed additional test is not a merged AETHER contribution. No reply or re-submission planned absent new runnable evidence.",
        "project": "redis/node-redis",
        "kind": "authored_issue_proposal",
        "status": "CLOSED_NOT_PLANNED_NO_FOLLOWUP",
        "source_url": "https://github.com/redis/node-redis/issues/3579",
        "evidence_urls": [
            "https://github.com/redis/node-redis/issues/3579#issuecomment-6628131939",
            "https://github.com/redis/node-redis/pull/3567",
        ],
        "submitter_account": "aetherxeg-source",
        "issue_closed_at": "2026-11-04T10:10:31Z",
        "upstream_state_reason": "not_planned",
        "follow_up_disposition": "ARCHIVED_NO_REPOST_UNLESS_NEW_EXECUTABLE_REPRO",
    },
}

def read(path):
    return read_unique_json((ROOT / path).read_bytes())

def check_status(records, receipt):
    assert_frozen_sources(ROOT)
    require(receipt["schema_version"] == "AX-PRIMARY-SOURCE-RECEIPTS-v1", "integrity assertion 1")
    require(receipt["observed_as_of"] == "2026-11-04", "integrity assertion 2")
    require(receipt["source_account"] == "aetherxeg-source", "integrity assertion 3")
    require(receipt["original_status_file"] == "data/status-updates/2026-11-04.json", "integrity assertion 4")
    require(len(records) == len(SOURCES) == 3, "integrity assertion 5")
    by_id = {x["id"]: x for x in records}
    require(len(by_id) == len(records) and set(by_id) == set(SOURCES), "integrity assertion 6")
    pinned = {x["id"]: x for x in receipt["expected_records"]}
    require(len(pinned) == len(receipt["expected_records"]) and set(pinned) == set(SOURCES), "integrity assertion 7")

    for identifier, fixed in SOURCES.items():
        record = by_id[identifier]
        require(record == pinned[identifier], ("dated receipt no longer matches record", identifier))
        require(record["as_of"] == receipt["observed_as_of"], "integrity assertion 9")
        require(set(record) == set(fixed) | {"id", "as_of"}, ("unexpected or missing record fields", identifier))
        for field, exact_value in fixed.items():
            require(record.get(field) == exact_value, ("wrong source/identity/status/HEAD", identifier, field))
            require(pinned[identifier].get(field) == exact_value, ("receipt tampering", identifier, field))
        # A free-text assertion is not a substitute for editorial review.
        require(isinstance(record["description"], str) and len(record["description"]) >= 40, "integrity assertion 13")
        if identifier == "APACHE-BALLISTA-2775":
            require("not upstream CI" in record["ci_boundary"], "integrity assertion 14")
            require("no apache approval" in record["description"].lower(), "integrity assertion 15")
        if identifier == "EXECSURFACE-WATCHLIST-133":
            require("not certification" in record["description"], "integrity assertion 16")
        if identifier == "NODE-REDIS-3579":
            require("No reply or re-submission planned" in record["description"], "integrity assertion 17")
    return True

if __name__ == "__main__":
    records = read("data/status-updates/2026-11-04.json")["records"]
    receipt = read("data/evidence/2026-11-04-primary-receipts.json")
    check_status(records, receipt)
    print("EVIDENCE_PINNING=PASS status_records=3 identity_status_head_and_urls=pinned")
