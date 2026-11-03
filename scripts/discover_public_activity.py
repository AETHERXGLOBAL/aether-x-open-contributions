#!/usr/bin/env python3
"""AETHER X: read-only external GitHub activity census (not an achievement publisher)."""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

ACCOUNT = "aetherxeg-source"
API = "https://api.github.com"
QUERIES = (
    ("commented_issue", "commenter:aetherxeg-source -org:AETHERXGLOBAL is:issue"),
    ("commented_pr", "commenter:aetherxeg-source -org:AETHERXGLOBAL is:pr"),
    ("authored_issue", "author:aetherxeg-source -org:AETHERXGLOBAL is:issue"),
    ("authored_pr", "author:aetherxeg-source -org:AETHERXGLOBAL is:pr"),
)

def valid_public_url(url, repo):
    p = urlparse(url)
    return p.scheme == "https" and p.netloc == "github.com" and p.path.startswith("/" + repo + "/")

class Reader:
    def __init__(self, token):
        if not token:
            raise RuntimeError("STOP: GITHUB_TOKEN required")
        self.token = token
        self.requests = 0

    def get(self, path, params=None):
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("Only GitHub API-relative paths accepted")
        url = API + path + (("?" + urlencode(params)) if params else "")
        headers = {"Accept": "application/vnd.github+json",
                   "Authorization": "Bearer " + self.token,
                   "User-Agent": "AETHER-X-Public-Contributions/1.0",
                   "X-GitHub-Api-Version": "2022-11-28"}
        for attempt in range(3):
            try:
                with urlopen(Request(url, headers=headers), timeout=45) as response:
                    raw = response.read(5_000_001)
                if len(raw) > 5_000_000:
                    raise RuntimeError("Oversized GitHub API response: " + path)
                self.requests += 1
                return json.loads(raw)
            except HTTPError as e:
                self.requests += 1
                if e.code in (429, 502, 503, 504) and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"GitHub API HTTP {e.code}: {path}") from e
        raise RuntimeError("API retries exhausted")

    def pages(self, path, params=None, limit=35):
        values = []
        for page in range(1, limit + 1):
            r = self.get(path, {**(params or {}), "per_page": 100, "page": page})
            if isinstance(r, dict):
                if r.get("incomplete_results") or r.get("total_count", 0) > 1000:
                    raise RuntimeError("Search incomplete or over 1000; partition query before counting")
                batch = r["items"]
                total = r.get("total_count", 0)
            else:
                batch, total = r, None
            values.extend(batch)
            if len(batch) < 100 or (total is not None and len(values) >= total):
                return values
        raise RuntimeError("Pagination limit exceeded; fail closed")

def normalize(raw, repo, num, discussion_url, kind):
    if (raw.get("user") or {}).get("login", "").lower() != ACCOUNT:
        return None
    url = raw.get("html_url", "")
    if not valid_public_url(url, repo):
        raise RuntimeError("Invalid original comment URL: " + repo)
    return {"project": repo, "discussion_number": num, "discussion_url": discussion_url,
            "source_url": url, "kind": kind, "author": ACCOUNT, "comment_id": raw.get("id"),
            "created_at": raw.get("created_at") or raw.get("submitted_at"),
            "evidence_state": "PUBLIC_AUTHOR_PERMALINK_VERIFIED__TECHNICAL_REVIEW_PENDING"}

def collect(reader, existing_urls):
    threads = {}
    receipts = {}
    for label, query in QUERIES:
        hits = reader.pages("/search/issues", {"q": query}, limit=11)
        receipts[label] = len(hits)
        for h in hits:
            repo = h["repository_url"].replace(API + "/repos/", "", 1)
            if repo.lower().startswith(("aetherxglobal/", "aetherxeg-source/")):
                continue
            if not valid_public_url(h["html_url"], repo):
                raise RuntimeError("Invalid search result URL")
            key = (repo, h["number"])
            entry = threads.setdefault(key, {"project": repo, "discussion_number": h["number"],
                "discussion_url": h["html_url"], "title": h.get("title"),
                "kind": "pull_request" if h.get("pull_request") else "issue",
                "author": (h.get("user") or {}).get("login"), "discoveries": []})
            if label not in entry["discoveries"]:
                entry["discoveries"].append(label)

    comments, authored, unresolved = {}, {}, []
    for (repo, number), thread in sorted(threads.items()):
        path = "/repos/" + repo
        source = thread["discussion_url"]
        items = [("issue_comment", x) for x in reader.pages(path + f"/issues/{number}/comments")]
        if thread["kind"] == "pull_request":
            items += [("review_comment", x) for x in reader.pages(path + f"/pulls/{number}/comments")]
            items += [("review", x) for x in reader.pages(path + f"/pulls/{number}/reviews")
                      if (x.get("body") or "").strip()]
        found = 0
        for kind, raw in items:
            entry = normalize(raw, repo, number, source, kind)
            if entry is not None:
                comments[entry["source_url"]] = entry
                found += 1
        if any(d.startswith("commented_") for d in thread["discoveries"]) and not found:
            unresolved.append(source)
        if any(d.startswith("authored_") for d in thread["discoveries"]):
            if (thread["author"] or "").lower() != ACCOUNT:
                raise RuntimeError("Authored thread identity mismatch")
            authored[source] = {"project": repo, "source_url": source, "author": ACCOUNT,
                "discussion_number": number, "kind": "authored_" + thread["kind"],
                "evidence_state": "PUBLIC_AUTHOR_THREAD_VERIFIED__TECHNICAL_REVIEW_PENDING"}
    result_comments = sorted(comments.values(), key=lambda x: (x["created_at"] or "", x["source_url"]))
    result_authored = sorted(authored.values(), key=lambda x: x["source_url"])
    for entry in result_comments + result_authored:
        entry["already_cataloged"] = entry["source_url"] in existing_urls
    summary = {
        "source_search_counts": receipts, "unique_public_threads": len(threads),
        "verified_original_comment_links": len(result_comments),
        "verified_authored_external_threads": len(result_authored),
        "new_comment_candidates": sum(not x["already_cataloged"] for x in result_comments),
        "new_authored_thread_candidates": sum(not x["already_cataloged"] for x in result_authored),
        "threads_without_retrievable_comment": unresolved,
        "api_requests": reader.requests}
    return result_comments, result_authored, summary

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--catalog", default="data/contributions.json")
    args = p.parse_args()
    reader = Reader(os.environ.get("GITHUB_TOKEN"))
    old = json.loads(Path(args.catalog).read_text(encoding="utf8"))
    comments, authored, summary = collect(reader, {x["source_url"] for x in old["records"]})
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    data = {"schema_version": "1.0", "checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "identity": ACCOUNT, "approval_state": "DISCOVERY_ONLY_NOT_CURATED_OR_APPROVED",
        "scope_note": "Identity-verified public URL does not establish engineering quality, adoption or vendor endorsement",
        "summary": summary, "comments": comments, "authored_threads": authored}
    blob = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()
    (out / "public-activity-candidates.json").write_bytes(blob)
    (out / "SHA256SUMS.txt").write_text(hashlib.sha256(blob).hexdigest() +
        "  public-activity-candidates.json\n", encoding="ascii")
    (out / "SUMMARY.md").write_text(
        "# Source-backed discovery — review only\n\n"
        f"Threads: {summary['unique_public_threads']}; "
        f"exact original comment/review URLs: {summary['verified_original_comment_links']}; "
        f"new comment candidates: {summary['new_comment_candidates']}.\n\n"
        "No contribution status is promoted automatically. A curator must review source context, "
        "authorship, technical relevance, licensing, privacy and impacts before a reviewed PR.\n",
        encoding="utf8")
    print(json.dumps({"result": "DISCOVERY_ONLY_PASS", **summary}, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("DISCOVERY_FAILED_CLOSED: " + str(exc), file=sys.stderr)
        sys.exit(2)
