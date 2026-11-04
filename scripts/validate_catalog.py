#!/usr/bin/env python3
"""Offline checks for the 2026-11-03 public catalog; no external access."""
import csv, hashlib, json, pathlib, re
from urllib.parse import urlparse
from integrity_runtime import require, scan_public_secrets
from append_only_updates import read_updates
root=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((root/"data/contributions.json").read_text(encoding="utf8"))
rows=data["records"]
require(data["snapshot_date"]=="2026-11-03", "integrity assertion 1")
require(len(rows)==43, "integrity assertion 2")
require(len({x["id"] for x in rows})==43, "integrity assertion 3")
require(len({x["source_url"] for x in rows})==43, "integrity assertion 4")
require(sum(x["kind"]=="technical_comment" for x in rows)==40, "integrity assertion 5")
require(sum(x["kind"]=="authored_pull_request" for x in rows)==3, "integrity assertion 6")
require(sum(x["status"]=="MERGED_AUTHORED_PR" for x in rows)==2, "integrity assertion 7")
for x in rows:
    p=urlparse(x["source_url"])
    require(p.scheme=="https" and p.netloc=="github.com", "integrity assertion 8")
    require("/"+x["project"]+"/" in p.path, "integrity assertion 9")
    if x["kind"]=="technical_comment": require("#issuecomment-" in x["source_url"], "integrity assertion 10")
with (root/"data/contributions.csv").open(newline="",encoding="utf8") as f:
    require(len(list(csv.DictReader(f)))==43, "integrity assertion 11")
for file, sha in {"tests/opentelemetry/otel15966_graph_build_test.go":"45221c859ecc9da6b190fcef009d66cde64fc1020020d6ddf5813d85bc81685b","tests/redis/15930/w07-aof-replay.tcl":"bbe6b2ef4970a954f9fb095e818fafdb0f6ffdeb8a6cf482eadafc56c6687f62"}.items():
    require(hashlib.sha256((root/file).read_bytes()).hexdigest()==sha, file)
scan_public_secrets(root)

# The historical search census is a discovery tier, not an achievement count.
threads=json.loads((root/"data/discovery/2026-11-03-public-threads.json").read_text(encoding="utf8"))
require(len(threads["threads"])==233, "integrity assertion 14")
require(len({(x["repo"],x["number"]) for x in threads["threads"]})==233, "integrity assertion 15")
require(sum(x["kind"]=="issue" for x in threads["threads"])==217, "integrity assertion 16")
require(sum(x["kind"]=="pull_request" for x in threads["threads"])==16, "integrity assertion 17")
require(threads["totals"]["discovered_not_in_2026_11_03_verified_thread_set"]==200, "integrity assertion 18")
require(all(x["comment_permalink_verification"]=="PENDING" for x in threads["threads"]), "integrity assertion 19")

# Original public permalink identity proof from the successful GitHub-native discovery job.
evidence=json.loads((root/"data/discovery/2026-11-03-author-verified-links.json").read_text(encoding="utf8"))
require(evidence["account"]=="aetherxeg-source", "integrity assertion 20")
require(evidence["source_artifact_sha256"]=="8a163906a86ec7eafad3d4c2776a388c421dc11e004e57a7a40418f157c3c9f4", "integrity assertion 21")
comments=evidence["comments"]
authored=evidence["authored_discussions"]
require(len(comments)==242 and len(authored)==10, "integrity assertion 22")
require(len({x["source_url"] for x in comments})==242, "integrity assertion 23")
require(len({x["source_url"] for x in authored})==10, "integrity assertion 24")
require(sum(not x["previously_cataloged"] for x in comments)==210, "integrity assertion 25")
require(sum(not x["previously_cataloged"] for x in authored)==7, "integrity assertion 26")
catalog_sources={x["source_url"] for x in rows}
for item in comments+authored:
    p=urlparse(item["source_url"])
    require(p.scheme=="https" and p.netloc=="github.com" and p.path.startswith("/"+item["project"]+"/"), "integrity assertion 27")
    require(item["author"]=="aetherxeg-source", "integrity assertion 28")
    if item["previously_cataloged"]:
        require(item["source_url"] in catalog_sources, "integrity assertion 29")
    else:
        require(item["source_url"] not in catalog_sources, "integrity assertion 30")

print("PUBLIC_CATALOG=PASS entries=43 technical_comments=40 authored_prs=3 merged_prs=2 test_sources=2")

# The 2026-11-04 supplement is additive. Historical counts and original
# source byte digests above must continue to pass without relaxation.
delta=json.loads((root/"data/status-updates/2026-11-04.json").read_text(encoding="utf8"))
require(delta["schema_version"]=="AX-PUBLIC-STATUS-UPDATE-v1", "integrity assertion 31")
require(delta["snapshot_date"]=="2026-11-04", "integrity assertion 32")
require(delta["historical_catalog_snapshot"]==data["snapshot_date"], "integrity assertion 33")
items=delta["records"]
expected={
    "APACHE-BALLISTA-2775":("apache/datafusion-ballista","authored_pull_request","OPEN_UNMERGED_AUTHORED_PR"),
    "EXECSURFACE-WATCHLIST-133":("scadastrangelove/awesome-ai-security-tools","third_party_watchlist_inclusion","THIRD_PARTY_WATCHLIST_LISTED"),
    "NODE-REDIS-3579":("redis/node-redis","authored_issue_proposal","CLOSED_NOT_PLANNED_NO_FOLLOWUP"),
}
require(len(items)==len(expected)==3, "integrity assertion 34")
require(len({x["id"] for x in items})==3, "integrity assertion 35")
require(len({x["source_url"] for x in items})==3, "integrity assertion 36")
for item in items:
    require(item["id"] in expected, "integrity assertion 37")
    require((item["project"],item["kind"],item["status"])==expected[item["id"]], "integrity assertion 38")
    require(item["as_of"]==delta["snapshot_date"], "integrity assertion 39")
    for link in [item["source_url"],*item["evidence_urls"]]:
        p=urlparse(link)
        require(p.scheme=="https" and p.netloc=="github.com", "integrity assertion 40")
        require(not p.username and not p.password, "integrity assertion 41")
    require(item["source_url"].startswith("https://github.com/"+item["project"]+"/"), "integrity assertion 42")
    require(item["source_url"] not in catalog_sources, "integrity assertion 43")
require(next(x for x in items if x["id"]=="APACHE-BALLISTA-2775")["merged"] is False, "integrity assertion 44")
require(next(x for x in items if x["id"]=="APACHE-BALLISTA-2775")["changed_files"]==12, "integrity assertion 45")
require(next(x for x in items if x["id"]=="EXECSURFACE-WATCHLIST-133")["upstream_issue_closed_as"]=="completed", "integrity assertion 46")
require(next(x for x in items if x["id"]=="NODE-REDIS-3579")["upstream_state_reason"]=="not_planned", "integrity assertion 47")
require(next(x for x in items if x["id"]=="NODE-REDIS-3579")["follow_up_disposition"]=="ARCHIVED_NO_REPOST_UNLESS_NEW_EXECUTABLE_REPRO", "integrity assertion 48")
print("PUBLIC_STATUS_UPDATE=PASS date=2026-11-04 records=3 merged_new=0 historical_catalog=unchanged")


# Additive F01/F03 checks; all historical assertions above are preserved.
from validate_institutional_register import read as read_register, check_register
from verify_status_evidence import read as read_status_evidence, check_status

read_updates(root)
check_register(read_register("data/institutional_register.json"))
print("INSTITUTIONAL_REGISTER=PASS source-linked reconciled")
check_status(
    read_status_evidence("data/status-updates/2026-11-04.json")["records"],
    read_status_evidence("data/evidence/2026-11-04-primary-receipts.json"),
)
print("EVIDENCE_PINNING=PASS status_records=3 primary_source_anchors=strict")
