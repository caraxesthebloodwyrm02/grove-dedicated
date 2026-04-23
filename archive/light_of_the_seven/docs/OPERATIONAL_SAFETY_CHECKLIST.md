# Operational safety checklist

Use this checklist in PRs that touch execution, subprocess, or scripts. **Governance:** [SAFETY_AND_GOVERNANCE.md](SAFETY_AND_GOVERNANCE.md).

## Before merge

- [ ] **Subprocess**: No `subprocess.run(..., shell=True)` or equivalent with user-controlled or unvalidated command strings. Use argument lists and `shell=False`; prefer allowlisted commands where applicable.
- [ ] **Execution scope**: Scripts or code that use `compile(..., "exec")`, `exec`, or `eval` run only in controlled or admin/operator contexts, not from user or LLM input.
- [ ] **Secrets**: No secrets in repo; env and secret patterns remain in `.gitignore`.
- [ ] **Local-first**: No new external AI APIs (OpenAI, Anthropic, etc.) unless explicitly approved and documented.

## Reference

- **Safety rules and governance:** [docs/SAFETY_AND_GOVERNANCE.md](SAFETY_AND_GOVERNANCE.md).
- Workspace: align with `E:\AGENTS.md`, `E:\CLAUDE.md`, and `E:\Seeds\ECOSYSTEM_BASELINE.md`.
- When adding new subprocess or script execution paths, document allowlist and failure behavior.
