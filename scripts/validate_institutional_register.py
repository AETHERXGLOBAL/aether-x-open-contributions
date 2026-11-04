"""Offline reconstruction and integrity validation of the unified public register.

No historical records are promoted, overwritten, or treated as proof of adoption.
"""
import json
import pathlib
import re
from integrity_runtime import require

from verify_frozen_snapshots import check_all as assert_frozen_sources
from append_only_updates import read_updates

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = re.compile(
    r"https://github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)"
    r"(?:#(?:issuecomment-\d+|discussion_r\d+))?"
)

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def assert_valid_url(url, project):
    m = CANONICAL.fullmatch(url)
    require(m is not None, ("non-canonical GitHub contribution permalink", url))
    require(m.group(1) == project, ("wrong owner/repository", url, project))
    return "https://github.com/{}/{}/{}".format(m.group(1), m.group(2), m.group(3))

def build():
    assert_frozen_sources(ROOT)
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
        require(item["author"] == "aetherxeg-source", "integrity assertion 3")
        get(item["source_url"], item["project"])["identity_evidence"].append(
            "GITHUB_PERMALINK_AUTHOR_VERIFIED_2026_11_03"
        )

    for item in discovery["authored_discussions"]:
        require(item["author"] == "aetherxeg-source", "integrity assertion 4")
        get(item["source_url"], item["project"])["identity_evidence"].append(
            "GITHUB_AUTHORED_DISCUSSION_VERIFIED_2026_11_03"
        )

    for item in history["records"]:
        entry = get(item["source_url"], item["project"])
        require(entry["historical_catalog_id"] is None, item["id"])
        entry["historical_catalog_id"] = item["id"]
        entry["historical_catalog_status"] = item["status"]

    for item in status["records"]:
        entry = get(item["source_url"], item["project"])
        require(entry["latest_dated_status_id"] is None, item["id"])
        entry["latest_dated_status_id"] = item["id"]
        entry["latest_dated_status"] = item["status"]

    # New dated source links are always unqualified; authorship requires separate
    # live source review and a Founder-authorized PR.
    additions, added_paths, added_dates = read_updates(ROOT)
    for item in additions:
        url = item["source_url"]
        require(url not in entries, ("duplicate historical/dynamic source URL", url))
        record = get(url, item["project"])
        record["identity_evidence"].append(
            "PUBLIC_SOURCE_LINK_DECLARED_UNQUALIFIED_" + item["snapshot_date"].replace("-", "_")
        )

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
        require(assert_valid_url(item["url"], item["repo"]) == item["url"], "integrity assertion 7")
        threads.append({
            "thread_url": item["url"],
            "project": item["repo"],
            "discussion_number": item["number"],
            "kind": item["kind"],
            "observed_state_2026_11_03": item["state"],
            "linked_participation_urls": sorted(by_thread.get(item["url"], [])),
        })

    result = {
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

    # Preserve exact original index bytes when no updates exist. New links and
    # threads are added only by dated, hash-reconciled, explicitly reviewed PRs.
    if added_dates:
        source_threads = {row["thread_url"]: row for row in result["threads"]}
        for item in additions:
            thread = item["thread_url"]
            if thread in source_threads:
                row = source_threads[thread]
                require(row["project"] == item["project"], "thread project drift")
                if item["source_url"] not in row["linked_participation_urls"]:
                    row["linked_participation_urls"].append(item["source_url"])
                    row["linked_participation_urls"].sort()
            else:
                number = int(thread.rsplit("/", 1)[-1])
                row = {
                    "thread_url": thread,
                    "project": item["project"],
                    "discussion_number": number,
                    "kind": "pull_request" if "/pull/" in thread else "issue",
                    "observed_state_date": item["snapshot_date"],
                    "observed_state": item["observed_state"],
                    "linked_participation_urls": [item["source_url"]],
                }
                source_threads[thread] = row
                result["threads"].append(row)
        result["source_files"].extend(["data/updates/manifest.json", *added_paths])
        result["snapshot_generated_from"] += " plus dated append-only updates through " + added_dates[-1]
        result["counts"]["unique_participation_sources"] = len(result["records"])
        result["counts"]["discovered_threads"] = len(result["threads"])
        result["counts"]["discovered_threads_without_matched_participation"] = sum(
            not row["linked_participation_urls"] for row in result["threads"]
        )
        result["counts"]["append_only_unqualified_participations"] = len(additions)
    return result


def check_register(actual, expected=None):
    assert_frozen_sources(ROOT)
    expected = expected or build()
    require(actual["schema_version"] == expected["schema_version"], "integrity assertion 8")
    require(actual["source_files"] == expected["source_files"], "integrity assertion 9")
    require(actual["identity_rule"] == expected["identity_rule"], "integrity assertion 10")
    require(actual["snapshot_generated_from"] == expected["snapshot_generated_from"], "integrity assertion 11")
    require(actual["counts"] == expected["counts"], "integrity assertion 12")
    require(len(actual["records"]) == len(expected["records"]), "integrity assertion 13")
    require(len(actual["threads"]) == len(expected["threads"]), "integrity assertion 14")
    actual_by_url = {x["source_url"]: x for x in actual["records"]}
    expected_by_url = {x["source_url"]: x for x in expected["records"]}
    require(len(actual_by_url) == len(actual["records"]), "duplicate contribution URLs")
    require(set(actual_by_url) == set(expected_by_url), "missing or unverified contribution URLs")
    for url, record in expected_by_url.items():
        require(actual_by_url[url] == record, ("contribution identity/status drift", url))
    actual_threads = {x["thread_url"]: x for x in actual["threads"]}
    expected_threads = {x["thread_url"]: x for x in expected["threads"]}
    require(len(actual_threads) == len(actual["threads"]), "duplicate thread")
    require(set(actual_threads) == set(expected_threads), "integrity assertion 19")
    for url, item in expected_threads.items():
        require(actual_threads[url] == item, ("thread evidence link drift", url))
    require(actual["counts"]["unique_participation_sources"] >= 262, "original source baseline lost")
    require(actual["counts"]["discovered_threads"] >= 233, "original thread baseline lost")
    require(actual["counts"]["dated_status_updates"] == 3, "integrity assertion 23")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reconcile the source-linked institutional register")
    parser.add_argument("--write", action="store_true", help="Regenerate the register for review; never changes source snapshots")
    args = parser.parse_args()
    if args.write:
        generated = build()
        path = ROOT / "data/institutional_register.json"
        path.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("INSTITUTIONAL_REGISTER=REGENERATED review_diff_before_commit=true")
    else:
        current = read("data/institutional_register.json")
        check_register(current)
        print("INSTITUTIONAL_REGISTER=PASS sources={} threads={} dated_updates={}".format(current["counts"]["unique_participation_sources"], current["counts"]["discovered_threads"], current["counts"]["dated_status_updates"]))
