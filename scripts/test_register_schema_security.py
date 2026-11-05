"""F03-SEC-01/02: raw register parser and institutional schema adversarial tests.

Synthetic tampering remains confined to temporary files and in-memory objects.
These cases are intentionally added before the production remediation (RED).
"""
import copy
import json
import pathlib
import tempfile
import unittest
from unittest import mock

import validate_institutional_register as register_module

ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstitutionalRegisterSchemaSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(
            (ROOT / "data/institutional_register.json").read_text(encoding="utf-8")
        )

    def read_synthetic(self, raw):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "data/institutional_register.json"
            path.parent.mkdir(parents=True)
            path.write_bytes(raw)
            with mock.patch.object(register_module, "ROOT", root):
                return register_module.read("data/institutional_register.json")

    def expect_duplicate_rejected(self, raw):
        with self.assertRaises(AssertionError):
            self.read_synthetic(raw)

    def expect_mutation_rejected(self, mutation):
        candidate = copy.deepcopy(self.baseline)
        mutation(candidate)
        with self.assertRaises(AssertionError):
            register_module.check_register(candidate, expected=self.baseline)

    def test_valid_nested_json_read_from_temporary_root(self):
        self.assertEqual(self.read_synthetic(b'{"records":[{"key":"value"}]}'),
                         {"records": [{"key": "value"}]})

    def test_duplicate_latest_dated_status_first_forged_rejected(self):
        self.expect_duplicate_rejected(
            b'{"records":[{"latest_dated_status":"MERGED_AUTHORED_PR",'
            b'"latest_dated_status":"UPSTREAM_RELATED_FIX_MERGED_THIRD_PARTY_AUTHORED"}]}'
        )

    def test_duplicate_counts_unique_sources_rejected(self):
        self.expect_duplicate_rejected(
            b'{"counts":{"unique_participation_sources":999,'
            b'"unique_participation_sources":262}}'
        )

    def test_nested_duplicate_record_key_rejected(self):
        self.expect_duplicate_rejected(
            b'{"records":[{"identity_evidence":[],"identity_evidence":["FORGED"]}]}'
        )

    def test_nested_duplicate_thread_key_rejected(self):
        self.expect_duplicate_rejected(
            b'{"threads":[{"thread_url":"https://github.com/a/b/issues/1",'
            b'"thread_url":"https://github.com/a/b/issues/2"}]}'
        )

    def test_unknown_root_vendor_endorsement_rejected(self):
        self.expect_mutation_rejected(
            lambda doc: doc.update({"upstream_vendor_endorsement_by_NVIDIA": True})
        )

    def test_unknown_root_aether_code_ownership_rejected(self):
        self.expect_mutation_rejected(
            lambda doc: doc.update({"aether_authored_NVIDIA_merged_code": True})
        )

    def test_unknown_root_founder_approval_rejected(self):
        self.expect_mutation_rejected(
            lambda doc: doc.update({"founder_release_approval": "GRANTED"})
        )

    def test_nested_record_claim_rejected(self):
        self.expect_mutation_rejected(
            lambda doc: doc["records"][0].update({"upstream_merged_aether_test": True})
        )

    def test_nested_thread_claim_rejected(self):
        self.expect_mutation_rejected(
            lambda doc: doc["threads"][0].update({"external_certification": True})
        )

    def test_path_traversal_out_of_root_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = pathlib.Path(directory)
            root = parent / "repo"
            root.mkdir()
            (parent / "outside.json").write_text('{"value":1}', encoding="utf-8")
            with mock.patch.object(register_module, "ROOT", root):
                with self.assertRaises(AssertionError):
                    register_module.read("../outside.json")

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = pathlib.Path(directory)
            root = parent / "repo"
            target = root / "data/institutional_register.json"
            target.parent.mkdir(parents=True)
            outside = parent / "outside.json"
            outside.write_text('{"value":1}', encoding="utf-8")
            try:
                target.symlink_to(outside)
            except (OSError, NotImplementedError) as error:
                self.skipTest("symlinks unavailable: " + str(error))
            with mock.patch.object(register_module, "ROOT", root):
                with self.assertRaises(AssertionError):
                    register_module.read("data/institutional_register.json")


if __name__ == "__main__":
    unittest.main()
