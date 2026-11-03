#!/usr/bin/env bash
# Repository admin-only identity and main ruleset. Dry-run by default.
set -euo pipefail
REPO="AETHERXGLOBAL/aether-x-open-contributions"
if [[ "${1:-}" != "--apply" ]]; then
  cat <<'PREVIEW'
DRY_RUN_ONLY: no GitHub settings changed
Target: AETHERXGLOBAL/aether-x-open-contributions
Description: Evidence-backed open-source engineering contributions, reproducible tests, and verified collaboration by AETHER X GLOBAL.
Homepage: https://aetherxglobal.com
Topics: open-source engineering regression-testing reproducibility software-assurance developer-relations aether-x
Policy: active PR-only default-branch ruleset; require catalog-integrity; no force-push/delete.
Approvals: initially 0 until a qualified second reviewer is enrolled.
Run: bash scripts/apply_repository_admin_settings.sh --apply
PREVIEW
  exit 0
fi
command -v gh >/dev/null || { echo "STOP: GitHub CLI missing"; exit 1; }
command -v python3 >/dev/null || { echo "STOP: Python 3 missing"; exit 1; }
gh auth status >/dev/null || { echo "STOP: gh not authenticated"; exit 1; }
DEFAULT="$(gh api "repos/$REPO" --jq '.default_branch')"
[[ "$DEFAULT" == "main" ]] || { echo "STOP: Unexpected default branch"; exit 1; }
GREEN="$(gh api "repos/$REPO/commits/main/check-runs?per_page=100" --jq '[.check_runs[] | select(.name=="catalog-integrity" and .conclusion=="success")] | length')"
[[ "$GREEN" -ge 1 ]] || { echo "STOP: Hosted catalog-integrity PASS required first"; exit 1; }
EXISTING="$(gh api "repos/$REPO/rulesets" --jq '[.[] | select(.name=="AETHER X Public Evidence Main Guard")] | length')"
[[ "$EXISTING" == "0" ]] || { echo "STOP: Named ruleset already exists; no duplicate creation"; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cat >"$TMP/settings.json" <<'JSON'
{
  "description": "Evidence-backed open-source engineering contributions, reproducible tests, and verified collaboration by AETHER X GLOBAL.",
  "homepage": "https://aetherxglobal.com",
  "has_issues": true,
  "has_wiki": false,
  "delete_branch_on_merge": true,
  "allow_squash_merge": true,
  "allow_merge_commit": false,
  "allow_rebase_merge": false,
  "allow_auto_merge": false
}
JSON
cat >"$TMP/topics.json" <<'JSON'
{"names":["open-source","engineering","regression-testing","reproducibility","software-assurance","developer-relations","aether-x"]}
JSON
cat >"$TMP/ruleset.json" <<'JSON'
{
  "name": "AETHER X Public Evidence Main Guard",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "bypass_actors": [],
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "linear_history"},
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 0,
      "dismiss_stale_reviews_on_push": true,
      "require_code_owner_review": false,
      "require_last_push_approval": false,
      "required_review_thread_resolution": true
    }},
    {"type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": true,
      "required_status_checks": [{"context": "catalog-integrity"}]
    }}
  ]
}
JSON
gh api --method PATCH "repos/$REPO" --input "$TMP/settings.json" >/dev/null
gh api --method PUT "repos/$REPO/topics" --input "$TMP/topics.json" >/dev/null
gh api --method POST "repos/$REPO/rulesets" --input "$TMP/ruleset.json" >/dev/null
echo "=== RULESET ==="
gh api "repos/$REPO/rulesets" --jq '.[] | select(.name=="AETHER X Public Evidence Main Guard") | [.name,.enforcement] | @tsv'
echo "=== METADATA ==="
gh api "repos/$REPO" --jq '{description,homepage,topics,allow_squash_merge,allow_merge_commit,allow_rebase_merge,delete_branch_on_merge}'
echo "ADMIN_SETTINGS_APPLIED_READBACK_COMPLETE"
