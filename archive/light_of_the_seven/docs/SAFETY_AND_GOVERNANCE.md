# Safety rules and governance

**Purpose:** Single source of truth for enforced safety rules and governance. Agents and contributors must follow these; PRs that violate them must not merge without explicit exception and document update.

---

## 1. Safety rules (enforced)

### 1.1 Local-first and external APIs

- **No external AI APIs** unless explicitly requested: do not suggest or add OpenAI, Anthropic, or other cloud LLM/embedding APIs. Use local Ollama models (e.g. `nomic-embed-text-v2-moe:latest`, `ministral`, `gpt-oss-safeguard`) and local RAG (ChromaDB in `.rag_db/`).
- **Default to local-only** for all new features; document and justify any exception.

### 1.2 Execution and subprocess

- **No `shell=True`** with user-controlled or unvalidated command strings. Use argument lists and `shell=False`; prefer allowlisted commands.
- **No `eval`, `exec`, or `compile(..., "exec")`** on user or LLM input. Use only in controlled or admin/operator contexts and document the boundary.
- When adding new subprocess or script execution, document allowlist and failure behavior (see [OPERATIONAL_SAFETY_CHECKLIST.md](OPERATIONAL_SAFETY_CHECKLIST.md)).

### 1.3 Secrets and configuration

- **No secrets in repo.** Use environment variables; keep `.env` and secret patterns in `.gitignore`. Align with workspace ignore baseline (`E:\Seeds\ECOSYSTEM_BASELINE.md` § 2.1).
- **Single env reference per project:** document which subsystem reads which variable (e.g. in `.env.example` or project docs).

### 1.4 Code and architecture

- **No breaking changes** without explicit approval; do not remove functionality without documented exception.
- **Type hints required** on all public functions; no untyped code in production paths.
- **No hardcoded secrets or magic numbers**; use named constants and env/config.
- **Respect module boundaries** and layered architecture; use repository/ORM patterns for data access, not ad-hoc direct DB access.

### 1.5 Optional and heavy dependencies

- Follow the **torch/transformers guardrail pattern** (Ecosystem baseline § 1): lazy import (try/except `ImportError`) at use site; provide a deterministic fallback so the module works with and without the optional dependency. Do not add heavy deps to default install without justification.

---

## 2. Governance

### 2.1 Authority

- **Workspace baseline** is the authority for guardrails, config, versioning, and QA: `E:\Seeds\ECOSYSTEM_BASELINE.md`. New repos and changes must align.
- **Project rules** (`.cursorrules`, `CLAUDE.md`, this doc) define project-specific safety and behavior; they must not contradict the workspace baseline.

### 2.2 Change control

- **Breaking changes** (API removal, behavior change, major version): require explicit approval and must be documented (changelog, migration, or ADR). Do not merge without it.
- **New env vars, new optional heavy deps, new execution paths:** document per Ecosystem baseline § 4 (QA checklist) and § 2 (env reference, ignore baseline).
- **Safety or governance exceptions:** must be recorded in this doc or the operational checklist, with rationale and expiry/review if applicable.

### 2.3 Alignment points

| Area | Reference |
|------|-----------|
| Workspace guardrails and config | `E:\Seeds\ECOSYSTEM_BASELINE.md` |
| Build, test, lint, commit | `E:\AGENTS.md`, project `CLAUDE.md` |
| Operational safety (subprocess, exec, tools) | [OPERATIONAL_SAFETY_CHECKLIST.md](OPERATIONAL_SAFETY_CHECKLIST.md) |
| Local-first and prohibited practices | `.cursorrules` (Project Identity, Prohibited Practices) |
| Environment and test-lint routines | [ENVIRONMENT_AND_ROUTINES.md](ENVIRONMENT_AND_ROUTINES.md) |

---

## 3. Enforcement

- **PRs:** Before merge, confirm compliance with the operational checklist and that no safety rule above is violated. Use the checklist in [OPERATIONAL_SAFETY_CHECKLIST.md](OPERATIONAL_SAFETY_CHECKLIST.md).
- **Agents and automation:** Treat this doc and the operational checklist as mandatory. Do not suggest or implement changes that violate § 1; do not bypass governance in § 2.
- **Lint and tests:** Run `make lint` and `make test` (or equivalent) before commit; fix failures before pushing. Safety-related tests (e.g. no `shell=True` in hot paths) should be added when adding new execution paths.

---

## 4. Summary

- **Safety:** Local-first, no unsafe subprocess/eval, no secrets in repo, no breaking changes without approval, optional heavy deps behind lazy import and fallback.
- **Governance:** Workspace baseline is authority; document breaking changes and exceptions; align with ecosystem and project docs.
- **Enforcement:** PR checklist, agent adherence, and pre-commit lint/test.
