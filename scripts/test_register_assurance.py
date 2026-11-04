"""Executable negative controls for AX-DEVREL-PR7-F1 and F01/F03.

Mutations operate on temporary in-memory copies: original data files stay unchanged.
"""
import copy
import json
import pathlib
import unittest
import tempfile
import shutil
from unittest import mock

import validate_institutional_register as register_module
from verify_frozen_snapshots import FROZEN_GIT_BLOBS, assert_frozen, check_all as check_all_frozen

from validate_institutional_register import build, check_register
from verify_status_evidence import check_status, read as read_evidence
from verify_upstream_live import audit_live

ROOT = pathlib.Path(__file__).resolve().parents[1]

class EvidenceIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = read_evidence("data/status-updates/2026-11-04.json")["records"]
        cls.receipt = read_evidence("data/evidence/2026-11-04-primary-receipts.json")
        cls.reg = json.loads(
            (ROOT / "data/institutional_register.json").read_text(encoding="utf-8")
        )

    def mutate_status(self, identifier, field, value):
        items = copy.deepcopy(self.rows)
        next(x for x in items if x["id"] == identifier)[field] = value
        with self.assertRaises(AssertionError):
            check_status(items, self.receipt)

    def mutate_registry(self, action):
        obj = copy.deepcopy(self.reg)
        action(obj)
        with self.assertRaises(AssertionError):
            check_register(obj)

    def test_source_receipts_green(self):
        self.assertTrue(check_status(self.rows, self.receipt))

    def test_unified_register_green(self):
        self.assertTrue(check_register(self.reg))

    def test_f1_apache_wrong_number_rejected(self):
        self.mutate_status(
            "APACHE-BALLISTA-2775", "source_url",
            "https://github.com/apache/datafusion-ballista/pull/9999999"
        )

    def test_f1_apache_wrong_head_rejected(self):
        self.mutate_status("APACHE-BALLISTA-2775", "head_commit", "0" * 40)

    def test_f1_apache_wrong_origin_rejected(self):
        self.mutate_status("APACHE-BALLISTA-2775", "head_repository", "apache/datafusion-ballista")

    def test_f1_apache_false_merge_rejected(self):
        self.mutate_status("APACHE-BALLISTA-2775", "merged", True)

    def test_f1_apache_false_ci_rejected(self):
        self.mutate_status("APACHE-BALLISTA-2775", "ci_boundary", "all upstream CI passed")

    def test_f1_apache_fake_approval_description_rejected(self):
        self.mutate_status("APACHE-BALLISTA-2775", "description", "Apache approved and merged the patch.")

    def test_f1_apache_wrong_evidence_link_rejected(self):
        self.mutate_status("APACHE-BALLISTA-2775", "evidence_urls", ["https://github.com/apache/datafusion-ballista/pull/1"])

    def test_f1_watchlist_wrong_number_rejected(self):
        self.mutate_status(
            "EXECSURFACE-WATCHLIST-133", "source_url",
            "https://github.com/scadastrangelove/awesome-ai-security-tools/issues/1"
        )

    def test_f1_watchlist_wrong_commit_rejected(self):
        self.mutate_status(
            "EXECSURFACE-WATCHLIST-133", "evidence_urls",
            ["https://github.com/scadastrangelove/awesome-ai-security-tools/commit/" + "f" * 40]
        )

    def test_watchlist_inflation_description_rejected(self):
        self.mutate_status("EXECSURFACE-WATCHLIST-133", "description", "Certified for all production systems.")

    def test_redis_wrong_issue_rejected(self):
        self.mutate_status("NODE-REDIS-3579", "source_url", "https://github.com/redis/node-redis/issues/999")

    def test_redis_wrong_disposition_rejected(self):
        self.mutate_status("NODE-REDIS-3579", "upstream_state_reason", "completed")

    def test_redis_false_author_rejected(self):
        self.mutate_status("NODE-REDIS-3579", "submitter_account", "unrelated-user")

    def test_duplicate_status_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows.append(copy.deepcopy(rows[0]))
        with self.assertRaises(AssertionError):
            check_status(rows, self.receipt)

    def test_receipt_joint_tamper_pinned_primary_facts_rejected(self):
        rows, receipt = copy.deepcopy(self.rows), copy.deepcopy(self.receipt)
        for x in rows + receipt["expected_records"]:
            if x["id"] == "APACHE-BALLISTA-2775":
                x["head_commit"] = "f" * 40
        with self.assertRaises(AssertionError):
            check_status(rows, receipt)

    def test_registry_duplicate_source_rejected(self):
        self.mutate_registry(lambda x: x["records"].append(copy.deepcopy(x["records"][0])))

    def test_registry_missing_known_link_rejected(self):
        self.mutate_registry(lambda x: x["records"].pop())

    def test_registry_promote_unqualified_rejected(self):
        def change(x):
            e = next(row for row in x["records"] if row["qualification_tier"] == "SOURCE_IDENTITY_ONLY_UNQUALIFIED")
            e["qualification_tier"] = "DATED_STATUS_WITH_PUBLIC_EVIDENCE"
            e["latest_dated_status"] = "MERGED_AUTHORED_PR"
        self.mutate_registry(change)

    def test_registry_history_rewrite_rejected(self):
        def change(x):
            e = next(row for row in x["records"] if row["historical_catalog_id"])
            e["historical_catalog_status"] = "MERGED_AUTHORED_PR"
        self.mutate_registry(change)

    def test_registry_thread_orphan_rejected(self):
        def change(x):
            e = next(row for row in x["threads"] if row["linked_participation_urls"])
            e["linked_participation_urls"] = []
        self.mutate_registry(change)

    def test_registry_forged_authorship_rejected(self):
        def change(x):
            e = next(row for row in x["records"] if row["identity_evidence"])
            e["identity_evidence"] = ["INDEPENDENT_MERGED_SOURCE"]
        self.mutate_registry(change)

    def mutate_status_and_receipt(self, identifier, field, addition):
        """Keep historical denial wording yet append the same false claim to both copies."""
        rows, receipt = copy.deepcopy(self.rows), copy.deepcopy(self.receipt)
        for item in rows + receipt["expected_records"]:
            if item["id"] == identifier:
                item[field] += addition
        with self.assertRaises(AssertionError):
            check_status(rows, receipt)

    def test_joint_watchlist_false_certification_rejected(self):
        self.mutate_status_and_receipt(
            "EXECSURFACE-WATCHLIST-133", "description",
            " Independent certification has now been granted for production."
        )

    def test_joint_apache_false_upstream_ci_rejected(self):
        self.mutate_status_and_receipt(
            "APACHE-BALLISTA-2775", "ci_boundary",
            " All upstream Apache CI jobs passed independently."
        )

    def test_joint_redis_false_company_authorship_rejected(self):
        self.mutate_status_and_receipt(
            "NODE-REDIS-3579", "description",
            " AETHER X GLOBAL authored the merged upstream Redis fix #3567."
        )

    def test_frozen_historical_sources_pass(self):
        self.assertTrue(check_all_frozen(ROOT))

    def test_f01_mutated_source_and_rebuilt_index_rejected(self):
        """Alter a genuine verified comment permalink without altering source record counts."""
        source_name = "data/discovery/2026-11-03-author-verified-links.json"
        original = b"https://github.com/Adyen/adyen-flutter/issues/756#issuecomment-5952974431"
        forged = b"https://github.com/Adyen/adyen-flutter/issues/756#issuecomment-99999999999999"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for filename in FROZEN_GIT_BLOBS:
                destination = root / filename
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / filename, destination)
            target = root / source_name
            content = target.read_bytes()
            self.assertIn(original, content)
            target.write_bytes(content.replace(original, forged, 1))
            with self.assertRaises(AssertionError):
                assert_frozen(source_name, root=root)
            # The full deterministic rebuild now refuses the substituted source.
            with mock.patch.object(register_module, "ROOT", root):
                with self.assertRaises(AssertionError):
                    register_module.build()

    def test_f01_historical_bytes_mutation_rejected(self):
        filename = "data/contributions.json"
        original = (ROOT / filename).read_bytes()
        self.assertTrue(assert_frozen(filename, original))
        with self.assertRaises(AssertionError):
            assert_frozen(filename, original + b" ")

    def test_joint_status_receipt_unapproved_field_rejected(self):
        rows, receipt = copy.deepcopy(self.rows), copy.deepcopy(self.receipt)
        for item in rows + receipt["expected_records"]:
            if item["id"] == "EXECSURFACE-WATCHLIST-133":
                item["independent_certification"] = True
        with self.assertRaises(AssertionError):
            check_status(rows, receipt)

    def test_plan_not_enforced_or_self_approved(self):
        plan = json.loads((ROOT / "data/review-gate-proposal.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["activation_state"], "PREPARED_NOT_ENFORCED")
        self.assertFalse(plan["independent_reviewer_verified"])
        self.assertNotEqual(plan["proposed_ruleset"]["required_approving_review_count"], 0)
        self.assertEqual(plan["current_code_owner"], "aetherxeg-source")
        self.assertEqual(plan["proposed_ruleset"]["required_status_checks"], ["catalog-integrity"])
        self.assertTrue(plan["founder_approval_required"])

    def test_live_audit_accepts_only_expected_evidence(self):
        from verify_upstream_live import fake_snapshot
        result = audit_live(fake_snapshot())
        self.assertEqual(result["verdict"], "SOURCE_FACTS_MATCH_DATED_SNAPSHOT")

    def test_live_audit_rejects_false_merge(self):
        from verify_upstream_live import fake_snapshot
        responses = fake_snapshot()
        responses["apache"]["merged_at"] = "2026-11-04T20:00:00Z"
        with self.assertRaises(AssertionError):
            audit_live(responses)

    def test_live_audit_rejects_other_author(self):
        from verify_upstream_live import fake_snapshot
        responses = fake_snapshot()
        responses["redis"]["user"]["login"] = "unrelated-user"
        with self.assertRaises(AssertionError):
            audit_live(responses)

if __name__ == "__main__":
    unittest.main()
