"""Pinned dated source receipts and explicit anti-inflation checks.

This is an offline evidence-gate, not a substitute for querying upstream live state.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = {
    "APACHE-BALLISTA-2775": {
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
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def check_status(records, receipt):
    assert receipt["schema_version"] == "AX-PRIMARY-SOURCE-RECEIPTS-v1"
    assert receipt["observed_as_of"] == "2026-11-04"
    assert receipt["source_account"] == "aetherxeg-source"
    assert receipt["original_status_file"] == "data/status-updates/2026-11-04.json"
    assert len(records) == len(SOURCES) == 3
    by_id = {x["id"]: x for x in records}
    assert len(by_id) == len(records) and set(by_id) == set(SOURCES)
    pinned = {x["id"]: x for x in receipt["expected_records"]}
    assert len(pinned) == len(receipt["expected_records"]) and set(pinned) == set(SOURCES)

    for identifier, fixed in SOURCES.items():
        record = by_id[identifier]
        assert record == pinned[identifier], ("dated receipt no longer matches record", identifier)
        assert record["as_of"] == receipt["observed_as_of"]
        for field, exact_value in fixed.items():
            assert record.get(field) == exact_value, ("wrong source/identity/status/HEAD", identifier, field)
            assert pinned[identifier].get(field) == exact_value, ("receipt tampering", identifier, field)
        # A free-text assertion is not a substitute for editorial review.
        assert isinstance(record["description"], str) and len(record["description"]) >= 40
        if identifier == "APACHE-BALLISTA-2775":
            assert "not upstream CI" in record["ci_boundary"]
            assert "no apache approval" in record["description"].lower()
        if identifier == "EXECSURFACE-WATCHLIST-133":
            assert "not certification" in record["description"]
        if identifier == "NODE-REDIS-3579":
            assert "No reply or re-submission planned" in record["description"]
    return True

if __name__ == "__main__":
    records = read("data/status-updates/2026-11-04.json")["records"]
    receipt = read("data/evidence/2026-11-04-primary-receipts.json")
    check_status(records, receipt)
    print("EVIDENCE_PINNING=PASS status_records=3 identity_status_head_and_urls=pinned")
