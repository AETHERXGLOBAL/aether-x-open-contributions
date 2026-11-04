"""Pinned byte identity for frozen historical GitHub source observations.

Git object SHA references are independently checked against the dated PR #7
and original baseline. This is not an immutable trust root against changes to
both source and verifier, which require independent human review.
"""
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FROZEN_GIT_BLOBS = {
    "data/contributions.json": "37a8cae0a985af602ceea5dc352a235628fe769a",
    "data/contributions.csv": "3313c0f13e7b24a0705772e7467aaedf87dc3a9a",
    "data/discovery/2026-11-03-author-verified-links.json": "504994f4f41e4f78b71e71c99eb49866caba76a3",
    "data/discovery/2026-11-03-public-threads.json": "27ede6d229897a7a3c53190143738ab7f5a991c2",
    "data/outcomes.json": "cfe3c410779c0b08854946c7a82a357702ebd95e",
    "data/status-updates/2026-11-04.json": "c3545bd50e4e679a2533eb3de8c7da44ef7e21fe",
    "data/evidence/2026-11-04-primary-receipts.json": "ca47090aa8b06ac28a6c19efdd70c5d954fb52b8",
}

def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def assert_frozen(path, raw=None, *, root=None):
    assert path in FROZEN_GIT_BLOBS, ("untracked historical snapshot", path)
    if raw is None:
        raw = ((root or ROOT) / path).read_bytes()
    actual = git_blob_sha(raw)
    assert actual == FROZEN_GIT_BLOBS[path], ("historical source identity changed", path, actual)
    return True

def check_all(root=None):
    for path in FROZEN_GIT_BLOBS:
        assert_frozen(path, root=root)
    return True
