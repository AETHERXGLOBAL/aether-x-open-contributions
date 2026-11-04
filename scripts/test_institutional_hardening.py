"""Institutional hardening: optimized Python, secure uploads, and dated growth.

Uses synthetic URLs only inside temporary test files. No upstream publication.
"""
import copy
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import validate_institutional_register as register_module
from append_only_updates import read_updates
from integrity_runtime import require, scan_public_secrets
from verify_frozen_snapshots import FROZEN_GIT_BLOBS

ROOT = pathlib.Path(__file__).resolve().parents[1]
DAY = "2026-11-05"
NEW_LINK = "https://github.com/example-org/example-repo/issues/999999991#issuecomment-123450000"
EXISTING_THREAD_NEW_LINK = "https://github.com/Adyen/adyen-flutter/issues/756#issuecomment-123450001"

def sample(link=NEW_LINK, project="example-org/example-repo"):
    thread = link.split("#")[0]
    return {
        "source_url": link,
        "project": project,
        "author": "aetherxeg-source",
        "kind": "comment",
        "thread_url": thread,
        "observed_state": "unknown",
    }

def write_snapshot(root, participations, *, date=DAY, corrupt_digest=False):
    root = pathlib.Path(root)
    directory = root / "data/updates"
    directory.mkdir(parents=True, exist_ok=True)
    obj = {
        "schema_version": "AX-UNQUALIFIED-PARTICIPATION-v1",
        "snapshot_date": date,
        "source_account": "aetherxeg-source",
        "participations": participations,
    }
    raw = (json.dumps(obj, indent=2) + "\n").encode("utf-8")
    target = directory / (date + ".json")
    target.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    manifest = {
        "schema_version": "AX-APPEND-ONLY-PARTICIPATION-MANIFEST-v1",
        "baseline_as_of": "2026-11-04",
        "snapshots": [{
            "date": date,
            "path": "data/updates/" + date + ".json",
            "sha256": ("0" * 64 if corrupt_digest else digest),
        }],
        "notice": "Review-required data. Digest is not independent approval.",
    }
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return target

class InstitutionalHardeningTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = pathlib.Path(self.directory.name)
        for path in FROZEN_GIT_BLOBS:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        target = self.root / "data/updates/manifest.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "data/updates/manifest.json", target)

    def test_runtime_require_rejects_optimized_python(self):
        script = "from integrity_runtime import require; require(False, 'optimized rejected')"
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT / "scripts")
        proc = subprocess.run([sys.executable, "-O", "-c", script],
                              env=env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("optimized rejected", proc.stderr)

    def test_secret_scanner_covers_python_and_workflow_yaml(self):
        (self.root / "safe.py").write_text("print('safe')", encoding="utf-8")
        self.assertTrue(scan_public_secrets(self.root))
        (self.root / "fake.py").write_text("token = '" + "ghp_" + ("A" * 30) + "'")
        with self.assertRaises(AssertionError):
            scan_public_secrets(self.root)
        (self.root / "fake.py").unlink()
        (self.root / "workflow.yaml").write_text("key: " + "AKIA" + ("Z" * 16))
        with self.assertRaises(AssertionError):
            scan_public_secrets(self.root)

    def test_no_new_updates_preserves_baseline(self):
        self.assertEqual(read_updates(self.root)[0], [])
        with mock.patch.object(register_module, "ROOT", self.root):
            candidate = register_module.build()
        current = json.loads((ROOT / "data/institutional_register.json").read_text())
        # Source order is not evidence identity: check the full stable URL/key mapping.
        # The original generated index remains byte-identical on disk.
        self.assertTrue(register_module.check_register(current, candidate))
        self.assertEqual(candidate["counts"], current["counts"])

    def test_append_only_two_links_new_and_existing_threads(self):
        write_snapshot(self.root, [sample(), sample(EXISTING_THREAD_NEW_LINK, "Adyen/adyen-flutter")])
        with mock.patch.object(register_module, "ROOT", self.root):
            candidate = register_module.build()
        self.assertEqual(candidate["counts"]["unique_participation_sources"], 264)
        self.assertEqual(candidate["counts"]["discovered_threads"], 234)
        self.assertEqual(candidate["counts"]["append_only_unqualified_participations"], 2)
        self.assertEqual(candidate["counts"]["dated_status_updates"], 3)
        for url in (NEW_LINK, EXISTING_THREAD_NEW_LINK):
            record = next(x for x in candidate["records"] if x["source_url"] == url)
            self.assertEqual(record["qualification_tier"], "SOURCE_IDENTITY_ONLY_UNQUALIFIED")
            self.assertIsNone(record["latest_dated_status"])
        old_thread = next(x for x in candidate["threads"] if x["thread_url"] ==
                          "https://github.com/Adyen/adyen-flutter/issues/756")
        self.assertEqual(old_thread["linked_participation_urls"].count(EXISTING_THREAD_NEW_LINK), 1)

    def test_bad_digest_rejected(self):
        write_snapshot(self.root, [sample()], corrupt_digest=True)
        with self.assertRaises(AssertionError):
            read_updates(self.root)

    def test_duplicate_historical_participation_rejected(self):
        old = "https://github.com/Adyen/adyen-flutter/issues/756#issuecomment-5952974431"
        write_snapshot(self.root, [sample(old, "Adyen/adyen-flutter")])
        with mock.patch.object(register_module, "ROOT", self.root):
            with self.assertRaises(AssertionError):
                register_module.build()

    def test_wrong_repository_rejected(self):
        write_snapshot(self.root, [sample(project="other-user/another-repo")])
        with self.assertRaises(AssertionError):
            read_updates(self.root)

    def test_unmanifested_update_rejected(self):
        (self.root / "data/updates/2026-11-06.json").write_text("{}")
        with self.assertRaises(AssertionError):
            read_updates(self.root)

    def test_path_traversal_manifest_rejected(self):
        write_snapshot(self.root, [sample()])
        path = self.root / "data/updates/manifest.json"
        m = json.loads(path.read_text())
        m["snapshots"][0]["path"] = "../outside.json"
        path.write_text(json.dumps(m))
        with self.assertRaises(AssertionError):
            read_updates(self.root)

    def test_duplicate_json_keys_rejected(self):
        path = self.root / "data/updates/manifest.json"
        path.write_bytes(b'{"schema_version": "one", "schema_version": "two"}')
        with self.assertRaises(AssertionError):
            read_updates(self.root)

    def test_qualified_status_fields_not_allowed_in_unqualified_snapshot(self):
        forged = sample()
        forged["status"] = "MERGED_AUTHORED_PR"
        write_snapshot(self.root, [forged])
        with self.assertRaises(AssertionError):
            read_updates(self.root)

if __name__ == "__main__":
    unittest.main()
