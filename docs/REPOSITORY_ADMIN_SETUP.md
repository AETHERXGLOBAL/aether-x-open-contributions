# Verified GitHub repository configuration

**AETHER X GLOBAL — Open Contributions**  
**Verification date:** 3 November 2026  
**Result:** `REPOSITORY_CONFIGURATION_PASS` (GitHub REST read-back)

## Public repository identity

- Repository: [AETHERXGLOBAL/aether-x-open-contributions](https://github.com/AETHERXGLOBAL/aether-x-open-contributions)
- Visibility: **Public**
- Default branch: `main`
- Description: *Evidence-backed open-source engineering contributions, reproducible tests, and verified collaboration by AETHER X GLOBAL.*
- Homepage: https://aetherxglobal.com
- Topics (as applied): `aether`, `developer-relations`, `engineering`, `open-source`, `regression-testing`, `reproducibility`, `software-assurance`

## Repository-wide merge policy

| Setting | Read-back |
|---|---|
| Squash merges | Enabled |
| Merge commits | Disabled |
| Rebase merges | Disabled |
| Delete head branch after merge | Enabled |

## Enforced ruleset for `main`

[**AETHER X Public Evidence Main Guard — Ruleset #26478002**](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/rules/26478002)

- **Enforcement:** Active
- **Target:** Default branch (`~DEFAULT_BRANCH`)
- **Bypass actors:** None; current authenticated user cannot bypass
- **Prohibit deletion and non-fast-forward / force pushes**
- **Require linear history**
- **Require a Pull Request before merging**
- **Resolve review conversations before merging**
- **Allowed PR merge method:** Squash only
- **Required status check:** `catalog-integrity` via GitHub Actions; strict up-to-date policy enabled
- **Required approving reviews:** `0` — intentional single-operator transitional state; not an independent approval gate
- **Extra approval for unattributed Copilot changes:** Enabled
- **Code-owner reviews:** Not yet mandatory

The `catalog-integrity` workflow [completed successfully on the baseline `main` merge commit](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/actions/runs/41692976046).

### Future hardening

When a qualified second reviewer is authorized, raise required approvals from zero to one and evaluate mandatory CODEOWNERS reviews. Do not add a review requirement before ensuring the independent reviewer can actually approve, to avoid a repository workflow deadlock.

### Scope of verification

These settings were read back from the live GitHub repository and ruleset endpoints. This is evidence of current configuration, **not** a penetration test, independent security certification, or guarantee against misconfigured future changes.

The historical [admin configuration script](../scripts/apply_repository_admin_settings.sh) is **not needed now** and should not be run: it deliberately refuses an already existing ruleset rather than modifying or duplicating it.

For future changes, use [Repository Settings](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/settings) and open a reviewed PR for any documentation/policy updates.

**Source-backed state:** `REPOSITORY_CONFIGURATION_PASS / INDEPENDENT_REVIEW_APPROVAL_PENDING`.
