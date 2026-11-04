"""Explicit on-demand read-only upstream verification.

Default CI remains offline and reproducible for historical snapshots.
Usage: python3 scripts/verify_upstream_live.py --live
A mismatch is an observation-drift gate, not retroactive falsification.
"""
import argparse
import base64
import json
import os
import urllib.request
from integrity_runtime import require

API_ROOT = "https://api.github.com/"
PATHS = {
    "apache": "repos/apache/datafusion-ballista/pulls/2775",
    "redis": "repos/redis/node-redis/issues/3579",
    "redis_pr": "repos/redis/node-redis/pulls/3567",
    "watch_issue": "repos/scadastrangelove/awesome-ai-security-tools/issues/133",
    "watch_comment": "repos/scadastrangelove/awesome-ai-security-tools/issues/comments/5857686313",
    "watch_file": "repos/scadastrangelove/awesome-ai-security-tools/contents/WATCHLIST.md?ref=e0ec97f6f0b696d6a5ab0cb2158b8b4c1458c831",
}

def fake_snapshot():
    return {
        "apache": {
            "user": {"login": "aetherxeg-source"},
            "state": "open", "merged_at": None, "changed_files": 12,
            "head": {
                "sha": "62543d90754a0e77e3d8a765ed82d8ccde9306ce",
                "repo": {"full_name": "AETHERXGLOBAL/datafusion-ballista"},
            },
        },
        "redis": {
            "user": {"login": "aetherxeg-source"},
            "state": "closed", "state_reason": "not_planned",
            "closed_at": "2026-11-04T10:10:31Z",
        },
        "redis_pr": {
            "user": {"login": "maxymlyskov"}, "merged_at": "2026-11-02T09:41:05Z",
        },
        "watch_issue": {
            "user": {"login": "aetherxeg-source"},
            "state": "closed", "state_reason": "completed",
        },
        "watch_comment": {
            "user": {"login": "scadastrangelove"},
            "body": "ExecSurface has been added to WATCHLIST.md after static review only.",
        },
        "watch_file": {
            "decoded_text": "- [ExecSurface](https://github.com/AETHERXGLOBAL/execsurface) - watchlist",
        },
    }

def audit_live(snapshot):
    a, r, rp = snapshot["apache"], snapshot["redis"], snapshot["redis_pr"]
    w, c, f = snapshot["watch_issue"], snapshot["watch_comment"], snapshot["watch_file"]
    require(a["user"]["login"] == "aetherxeg-source", "Apache PR author changed")
    require(a["state"] == "open" and a["merged_at"] is None, "Apache dated state drifted")
    require(a["head"]["sha"] == "62543d90754a0e77e3d8a765ed82d8ccde9306ce", "Apache HEAD drifted")
    require(a["head"]["repo"]["full_name"] == "AETHERXGLOBAL/datafusion-ballista", "integrity assertion 4")
    require(a["changed_files"] == 12, "integrity assertion 5")
    require(r["user"]["login"] == "aetherxeg-source", "Redis original author mismatch")
    require(r["state"] == "closed" and r["state_reason"] == "not_planned", "integrity assertion 7")
    require(r["closed_at"] == "2026-11-04T10:10:31Z", "integrity assertion 8")
    require(rp["user"]["login"] != "aetherxeg-source", "Upstream authorship inflated")
    require(rp["merged_at"] is not None, "integrity assertion 10")
    require(w["user"]["login"] == "aetherxeg-source", "integrity assertion 11")
    require(w["state"] == "closed" and w["state_reason"] == "completed", "integrity assertion 12")
    require(c["user"]["login"] == "scadastrangelove", "integrity assertion 13")
    require("ExecSurface has been added" in c["body"], "integrity assertion 14")
    require("ExecSurface" in f["decoded_text"] and "AETHERXGLOBAL/execsurface" in f["decoded_text"], "integrity assertion 15")
    return {"verdict": "SOURCE_FACTS_MATCH_DATED_SNAPSHOT", "remote_public_resources": len(PATHS)}

def fetch_live():
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "AETHERXGLOBAL-Public-Evidence-ReadOnly"}
    if token:
        headers["Authorization"] = "Bearer " + token
    values = {}
    for key, path in PATHS.items():
        req = urllib.request.Request(API_ROOT + path, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=12) as response:
            values[key] = json.load(response)
    content = values["watch_file"]["content"]
    values["watch_file"]["decoded_text"] = base64.b64decode(content).decode("utf-8")
    return values

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Query exact public GitHub API sources; no writes")
    args = parser.parse_args()
    if not args.live:
        parser.error("Use --live explicitly. Offline snapshot tests run in unittest.")
    result = audit_live(fetch_live())
    print(json.dumps(result, sort_keys=True))
