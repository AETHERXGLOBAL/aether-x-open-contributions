# GitHub repository identity and branch-protection requirements

Repository: \`AETHERXGLOBAL/aether-x-open-contributions\` — public, default \`main\`.

## Proposed public identity

- Description: **Evidence-backed open-source engineering contributions, reproducible tests, and verified collaboration by AETHER X GLOBAL.**
- Homepage: https://aetherxglobal.com
- Topics: \`open-source\`, \`engineering\`, \`regression-testing\`, \`reproducibility\`, \`software-assurance\`, \`developer-relations\`, \`aether-x\`
- Preferred merge: squash only; delete feature branches after merge; maintain Issues; disable Wiki.

## Enforced protection target

Apply one repository-level ruleset named **AETHER X Public Evidence Main Guard** to the default branch:

- Require pull requests for changes to \`main\`.
- Require a successful \`catalog-integrity\` check, with up-to-date branch policy.
- Block force-pushes and deletion; require linear history.
- Require resolution of PR review conversations.
- Do not grant administrator or automation bypass.
- Set approval count **0 initially** to avoid deadlocking the sole authenticated contributor. Once a genuine second reviewer is authorized and onboarded, require **at least one independent review** and enforce CODEOWNERS. CODEOWNERS alone does *not* activate branch protection.

**Administrative permission gap:** The linked ChatGPT GitHub connector could read repository metadata and list current repository rulesets (\`[]\`), but the classic branch-protection endpoint returned **403**. The connector does not expose repository Administration writes, even though the connected identity may be an administrator in the GitHub UI.

## Application gate

Run [the reviewed admin script](../scripts/apply_repository_admin_settings.sh) from a \`gh\` CLI installation authenticated as a repository administrator. Default behavior is dry-run; \`--apply\` only proceeds after a real hosted \`catalog-integrity\` PASS on \`main\`. It updates description, homepage and topics, then creates the ruleset and prints actual read-back. If the GitHub account/token lacks repository Administration:write, it exits without claiming success.

Or use [Repository Settings](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/settings) and [Rulesets](https://github.com/AETHERXGLOBAL/aether-x-open-contributions/settings/rules).

**Do not state metadata or protection settings are applied until verified from GitHub after the admin mutation.**
