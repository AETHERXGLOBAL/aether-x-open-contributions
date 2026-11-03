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
print("PUBLIC_CATALOG=PASS entries=43 technical_comments=40 authored_prs=3 merged_prs=2 test_sources=2")
