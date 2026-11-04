#!/usr/bin/env python3
"""Offline checks for the 2026-11-03 public catalog; no external access."""
import csv, hashlib, json, pathlib, re
from urllib.parse import urlparse
root=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((root/"data/contributions.json").read_text(encoding="utf8"))
rows=data["records"]
assert data["snapshot_date"]=="2026-11-03"
assert len(rows)==43
assert len({x["id"] for x in rows})==43
assert len({x["source_url"] for x in rows})==43
assert sum(x["kind"]=="technical_comment" for x in rows)==40
assert sum(x["kind"]=="authored_pull_request" for x in rows)==3
assert sum(x["status"]=="MERGED_AUTHORED_PR" for x in rows)==2
for x in rows:
    p=urlparse(x["source_url"])
    assert p.scheme=="https" and p.netloc=="github.com"
    assert "/"+x["project"]+"/" in p.path
    if x["kind"]=="technical_comment": assert "#issuecomment-" in x["source_url"]
with (root/"data/contributions.csv").open(newline="",encoding="utf8") as f:
    assert len(list(csv.DictReader(f)))==43
for file, sha in {"tests/opentelemetry/otel15966_graph_build_test.go":"45221c859ecc9da6b190fcef009d66cde64fc1020020d6ddf5813d85bc81685b","tests/redis/15930/w07-aof-replay.tcl":"bbe6b2ef4970a954f9fb095e818fafdb0f6ffdeb8a6cf482eadafc56c6687f62"}.items():
    assert hashlib.sha256((root/file).read_bytes()).hexdigest()==sha,file
for f in root.rglob("*"):
    if f.is_file() and f.suffix.lower() in {".md",".json",".csv",".go",".tcl",".sh"}:
        t=f.read_text(encoding="utf8")
        assert not re.search(r"(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)",t),f

# The historical search census is a discovery tier, not an achievement count.
threads=json.loads((root/"data/discovery/2026-11-03-public-threads.json").read_text(encoding="utf8"))
assert len(threads["threads"])==233
assert len({(x["repo"],x["number"]) for x in threads["threads"]})==233
assert sum(x["kind"]=="issue" for x in threads["threads"])==217
assert sum(x["kind"]=="pull_request" for x in threads["threads"])==16
assert threads["totals"]["discovered_not_in_2026_11_03_verified_thread_set"]==200
assert all(x["comment_permalink_verification"]=="PENDING" for x in threads["threads"])

# Original public permalink identity proof from the successful GitHub-native discovery job.
evidence=json.loads((root/"data/discovery/2026-11-03-author-verified-links.json").read_text(encoding="utf8"))
assert evidence["account"]=="aetherxeg-source"
assert evidence["source_artifact_sha256"]=="8a163906a86ec7eafad3d4c2776a388c421dc11e004e57a7a40418f157c3c9f4"
comments=evidence["comments"]
authored=evidence["authored_discussions"]
assert len(comments)==242 and len(authored)==10
assert len({x["source_url"] for x in comments})==242
assert len({x["source_url"] for x in authored})==10
assert sum(not x["previously_cataloged"] for x in comments)==210
assert sum(not x["previously_cataloged"] for x in authored)==7
catalog_sources={x["source_url"] for x in rows}
for item in comments+authored:
    p=urlparse(item["source_url"])
    assert p.scheme=="https" and p.netloc=="github.com" and p.path.startswith("/"+item["project"]+"/")
    assert item["author"]=="aetherxeg-source"
    if item["previously_cataloged"]:
        assert item["source_url"] in catalog_sources
    else:
        assert item["source_url"] not in catalog_sources

print("PUBLIC_CATALOG=PASS entries=43 technical_comments=40 authored_prs=3 merged_prs=2 test_sources=2")

# The 2026-11-04 supplement is additive. Historical counts and original
# source byte digests above must continue to pass without relaxation.
delta=json.loads((root/"data/status-updates/2026-11-04.json").read_text(encoding="utf8"))
assert delta["schema_version"]=="AX-PUBLIC-STATUS-UPDATE-v1"
assert delta["snapshot_date"]=="2026-11-04"
assert delta["historical_catalog_snapshot"]==data["snapshot_date"]
items=delta["records"]
expected={
    "APACHE-BALLISTA-2775":("apache/datafusion-ballista","authored_pull_request","OPEN_UNMERGED_AUTHORED_PR"),
    "EXECSURFACE-WATCHLIST-133":("scadastrangelove/awesome-ai-security-tools","third_party_watchlist_inclusion","THIRD_PARTY_WATCHLIST_LISTED"),
    "NODE-REDIS-3579":("redis/node-redis","authored_issue_proposal","CLOSED_NOT_PLANNED_NO_FOLLOWUP"),
}
assert len(items)==len(expected)==3
assert len({x["id"] for x in items})==3
assert len({x["source_url"] for x in items})==3
for item in items:
    assert item["id"] in expected
    assert (item["project"],item["kind"],item["status"])==expected[item["id"]]
    assert item["as_of"]==delta["snapshot_date"]
    for link in [item["source_url"],*item["evidence_urls"]]:
        p=urlparse(link)
        assert p.scheme=="https" and p.netloc=="github.com"
        assert not p.username and not p.password
    assert item["source_url"].startswith("https://github.com/"+item["project"]+"/")
    assert item["source_url"] not in catalog_sources
assert next(x for x in items if x["id"]=="APACHE-BALLISTA-2775")["merged"] is False
assert next(x for x in items if x["id"]=="APACHE-BALLISTA-2775")["changed_files"]==12
assert next(x for x in items if x["id"]=="EXECSURFACE-WATCHLIST-133")["upstream_issue_closed_as"]=="completed"
assert next(x for x in items if x["id"]=="NODE-REDIS-3579")["upstream_state_reason"]=="not_planned"
assert next(x for x in items if x["id"]=="NODE-REDIS-3579")["follow_up_disposition"]=="ARCHIVED_NO_REPOST_UNLESS_NEW_EXECUTABLE_REPRO"
print("PUBLIC_STATUS_UPDATE=PASS date=2026-11-04 records=3 merged_new=0 historical_catalog=unchanged")
