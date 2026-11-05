"""Strict 2026-11-05 source-fact qualification; NOT a live upstream status feed.

Pinned facts are independently reviewable public GitHub URLs. Modifying both a
record and receipt cannot override the independent constants below.
"""
import json
import pathlib
from append_only_updates import read_bounded_json
from integrity_runtime import require
from verify_frozen_snapshots import check_all as check_frozen

ROOT = pathlib.Path(__file__).resolve().parents[1]
PINNED_RECORD = json.loads("{\"id\":\"NVIDIA-OPENSHELL-4111\",\"kind\":\"technical_comment\",\"project\":\"NVIDIA/OpenShell\",\"source_url\":\"https://github.com/NVIDIA/OpenShell/issues/4111#issuecomment-5955273345\",\"status\":\"UPSTREAM_RELATED_FIX_MERGED_THIRD_PARTY_AUTHORED\",\"as_of\":\"2026-11-05\",\"evidence_urls\":[\"https://github.com/NVIDIA/OpenShell/issues/4111\",\"https://github.com/NVIDIA/OpenShell/issues/4111#issuecomment-5955273345\",\"https://github.com/NVIDIA/OpenShell/issues/4111#issuecomment-6631499484\",\"https://github.com/NVIDIA/OpenShell/pull/4714\"],\"submitter_account\":\"aetherxeg-source\",\"issue_closed_at\":\"2026-11-05T08:21:03Z\",\"issue_state_reason\":\"completed\",\"related_pr_url\":\"https://github.com/NVIDIA/OpenShell/pull/4714\",\"related_pr_author\":\"lunarwhite\",\"related_pr_merged_at\":\"2026-11-05T08:21:01Z\",\"related_pr_head\":\"4422f21196316d720f4d4a64e079ada49c3ee44f\",\"aether_authored_upstream_fix\":false,\"aether_test_merged\":false,\"causal_adoption_proven\":false,\"description\":\"AETHER X GLOBAL supplied a security-focused comment about managed-volume ownership evidence. NVIDIA OpenShell issue #4111 was later closed as completed after upstream contributor lunarwhite authored and merged PR #4714. This observation does not establish use of AETHER code/tests, causal adoption of AETHER advice, review approval, certification, partnership, or vendor endorsement.\"}")

def read(path, *, root=None):
    return read_bounded_json(root or ROOT, path)

def check_new(status=None, receipt=None, *, root=None):
    root = root or ROOT
    check_frozen(root)
    status = status if status is not None else read("data/status-updates/2026-11-05.json", root=root)
    receipt = receipt if receipt is not None else read("data/evidence/2026-11-05-primary-receipts.json", root=root)
    require(isinstance(status, dict) and set(status) ==
            {"schema_version", "snapshot_date", "publisher", "historical_catalog_snapshot", "scope", "records"},
            "unexpected 2026-11-05 status schema")
    require(status["schema_version"] == "AX-PUBLIC-STATUS-UPDATE-v1")
    require(status["snapshot_date"] == "2026-11-05")
    require(status["publisher"] == "AETHER X GLOBAL")
    require(status["historical_catalog_snapshot"] == "2026-11-03")
    require(isinstance(status["scope"], str) and "byte-identical" in status["scope"],
            "historical source preservation disclaimer missing")
    require(status["records"] == [PINNED_RECORD], "unapproved source/identity/attribution/status change")
    require(isinstance(receipt, dict) and set(receipt) ==
            {"schema_version", "observed_as_of", "source_account", "original_status_file", "receipt_notice", "expected_records"},
            "unexpected 2026-11-05 receipt schema")
    require(receipt["schema_version"] == "AX-PRIMARY-SOURCE-RECEIPTS-v1")
    require(receipt["observed_as_of"] == "2026-11-05")
    require(receipt["source_account"] == "aetherxeg-source")
    require(receipt["original_status_file"] == "data/status-updates/2026-11-05.json")
    require(isinstance(receipt["receipt_notice"], str) and "not a cryptographic" in receipt["receipt_notice"])
    require(receipt["expected_records"] == [PINNED_RECORD], "receipt is not pinned to verified facts")
    return True

if __name__ == "__main__":
    check_new()
    print("NVIDIA_2026_11_05=PASS records=1 merged_by_third_party=true aether_authored_merge=false")
