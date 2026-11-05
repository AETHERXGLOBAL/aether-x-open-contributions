"""Independent, offline 2026-11-05 source-fact anti-inflation regressions."""
import copy
import unittest
from append_only_updates import read_unique_json
from verify_nvidia_2026_11_05 import check_new, read

class TestNvidiaStatusQualification(unittest.TestCase):
    def setUp(self):
        self.status = read("data/status-updates/2026-11-05.json")
        self.receipt = read("data/evidence/2026-11-05-primary-receipts.json")

    def test_good_record_and_receipt(self):
        self.assertTrue(check_new(self.status, self.receipt))

    def test_rejected_false_company_authorship_in_both(self):
        self._tamper_both("aether_authored_upstream_fix", True)

    def test_rejected_false_company_test_merge_in_both(self):
        self._tamper_both("aether_test_merged", True)

    def test_rejected_false_caused_upstream_fix_in_both(self):
        self._tamper_both("causal_adoption_proven", True)

    def test_rejected_wrong_third_party_author_in_both(self):
        self._tamper_both("related_pr_author", "aetherxeg-source")

    def test_rejected_wrong_head_in_both(self):
        self._tamper_both("related_pr_head", "0" * 40)

    def test_rejected_wrong_comment_perma_link_in_both(self):
        self._tamper_both("source_url", "https://github.com/NVIDIA/OpenShell/issues/4111#issuecomment-123456")

    def test_rejected_wrong_status_classification_in_both(self):
        self._tamper_both("status", "MERGED_AUTHORED_PR")

    def test_rejected_mutated_description_in_both(self):
        self._tamper_both("description", "AETHER X GLOBAL implemented NVIDIA's merged fix.")

    def test_rejected_additional_unqualified_record(self):
        self.status["records"].append(copy.deepcopy(self.status["records"][0]))
        with self.assertRaises(AssertionError):
            check_new(self.status, self.receipt)

    def test_rejected_receipt_without_matching_record(self):
        self.receipt["expected_records"] = []
        with self.assertRaises(AssertionError):
            check_new(self.status, self.receipt)

    def test_rejected_duplicate_json_keys(self):
        with self.assertRaises(AssertionError):
            read_unique_json(b'{"schema_version":1,"schema_version":2}')

    def _tamper_both(self, key, value):
        for item in [self.status["records"][0], self.receipt["expected_records"][0]]:
            item[key] = value
        with self.assertRaises(AssertionError):
            check_new(self.status, self.receipt)

if __name__ == "__main__":
    unittest.main()
