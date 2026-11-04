"""Offline reconstruction and integrity validation of the unified public register.

No historical records are promoted, overwritten, or treated as proof of adoption.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = re.compile(
    r"https://github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)"
    r"(?:#(?:issuecomment-\d+|discussion_r\d+))?"
)

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def assert_valid_url(url, project):
    m = CANONICAL.fullmatch(url)
    assert m is not None, ("non-canonical GitHub contribution permalink", url)
    assert m.group(1) == project, ("wrong owner/repository", url, project)
    return "https://github.com/{}/{}/{}".format(m.group(1), m.group(2), m.group(3))

def build():
    history = read("data/contributions.json")
    discovery = read("data/discovery/2026-11-03-author-verified-links.json")
    threads_source = read("data/discovery/2026-11-03-public-threads.json")
    status = read("data/status-updates/2026-11-04.json")
    entries = {}

    def get(url, project):
        thread = assert_valid_url(url, project)
        if url not in entries:
            entries[url] = {
                "source_url": url,
                "project": project,
                "thread_url": thread,
                "identity_evidence": [],
                "historical_catalog_id": None,
                "historical_catalog_status": None,
                "latest_dated_status_id": None,
                "latest_dated_status": None,
            }
        return entries[url]

    for item in discovery["comments"]:
        assert item["author"] == "aetherxeg-source"
        get(item["source_url"], item["project"])["identity_evidence"].append(
            "GITHUB_PERMALINK_AUTHOR_VERIFIED_2026_11_03"
        )

    for item in discovery["authored_discussions"]:
        assert item["author"] == "aetherxeg-source"
        get(item["source_url"], item["project"])["identity_evidence"].append(
            "GITHUB_AUTHORED_DISCUSSION_VERIFIED_2026_11_03"
        )

    for item in history["records"]:
        entry = get(item["source_url"], item["project"])
        assert entry["historical_catalog_id"] is None, item["id"]
        entry["historical_catalog_id"] = item["id"]
        entry["historical_catalog_status"] = item["status"]

    for item in status["records"]:
        entry = get(item["source_url"], item["project"])
        assert entry["latest_dated_status_id"] is None, item["id"]
        entry["latest_dated_status_id"] = item["id"]
        entry["latest_dated_status"] = item["status"]

    for entry in entries.values():
        entry["identity_evidence"] = sorted(set(entry["identity_evidence"]))
        entry["qualification_tier"] = (
            "DATED_STATUS_WITH_PUBLIC_EVIDENCE" if entry["latest_dated_status_id"]
            else "CURATED_HISTORICAL_BASELINE" if entry["historical_catalog_id"]
            else "SOURCE_IDENTITY_ONLY_UNQUALIFIED" if entry["identity_evidence"]
            else "UNVERIFIED"
        )

    by_thread = {}
    for entry in entries.values():
        by_thread.setdefault(entry["thread_url"], []).append(entry["source_url"])

    threads = []
    for item in threads_source["threads"]:
        assert assert_valid_url(item["url"], item["repo"]) == item["url"]
        threads.append({
            "thread_url": item["url"],
            "project": item["repo"],
            "discussion_number": item["number"],
            "kind": item["kind"],
            "observed_state_2026_11_03": item["state"],
            "linked_participation_urls": sorted(by_thread.get(item["url"], [])),
        })

    return {
        "schema_version": "AX-INSTITUTIONAL-CONTRIBUTION-REGISTER-v1",
        "snapshot_generated_from": "2026-11-03 base plus 2026-11-04 dated update",
        "source_files": [
            "data/contributions.json",
            "data/discovery/2026-11-03-author-verified-links.json",
            "data/discovery/2026-11-03-public-threads.json",
            "data/status-updates/2026-11-04.json",
        ],
        "identity_rule": (
            "Source identity only is not engineering qualification or upstream acceptance. "
            "Dated statuses do not rewrite original observations."
        ),
        "counts": {
            "unique_participation_sources": len(entries),
            "identity_verified_comment_links": len(discovery["comments"]),
            "identity_verified_authored_discussions": len(discovery["authored_discussions"]),
            "curated_historical_links": len(history["records"]),
            "dated_status_updates": len(status["records"]),
            "discovered_threads": len(threads),
            "discovered_threads_without_matched_participation": sum(
                not x["linked_participation_urls"] for x in threads
            ),
        },
        "records": list(entries.values()),
        "threads": threads,
    }

def check_register(actual, expected=None):
    expected = expected or build()
    assert actual["schema_version"] == expected["schema_version"]
    assert actual["source_files"] == expected["source_files"]
    assert actual["identity_rule"] == expected["identity_rule"]
    assert actual["snapshot_generated_from"] == expected["snapshot_generated_from"]
    assert actual["counts"] == expected["counts"]
    assert len(actual["records"]) == len(expected["records"])
    assert len(actual["threads"]) == len(expected["threads"])
    actual_by_url = {x["source_url"]: x for x in actual["records"]}
    expected_by_url = {x["source_url"]: x for x in expected["records"]}
    assert len(actual_by_url) == len(actual["records"]), "duplicate contribution URLs"
    assert set(actual_by_url) == set(expected_by_url), "missing or unverified contribution URLs"
    for url, record in expected_by_url.items():
        assert actual_by_url[url] == record, ("contribution identity/status drift", url)
    actual_threads = {x["thread_url"]: x for x in actual["threads"]}
    expected_threads = {x["thread_url"]: x for x in expected["threads"]}
    assert len(actual_threads) == len(actual["threads"]), "duplicate thread"
    assert set(actual_threads) == set(expected_threads)
    for url, item in expected_threads.items():
        assert actual_threads[url] == item, ("thread evidence link drift", url)
    assert actual["counts"]["unique_participation_sources"] == 262
    assert actual["counts"]["discovered_threads"] == 233
    assert actual["counts"]["dated_status_updates"] == 3
    return True

if __name__ == "__main__":
    current = read("data/institutional_register.json")
    check_register(current)
    print("INSTITUTIONAL_REGISTER=PASS sources=262 threads=233 dated_updates=3")
