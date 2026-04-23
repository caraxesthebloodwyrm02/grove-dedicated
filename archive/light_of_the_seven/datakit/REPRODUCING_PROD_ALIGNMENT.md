# Reproducing Production Alignment (Reusable Guide)

This guide shows you how to take a cluttered Python repo and align it with production best practices, especially for projects that will call the OpenAI API (or any external API) safely and reliably.

It is designed to be **copy/pasteable** across repos, with **offline-first verification** and an **opt-in live smoke test** that uses minimal credits.

---

## What “production alignment” means (checklist)

### Security & compliance basics
- [ ] No secrets in git (no API keys in code, docs, notebooks, or CI logs)
- [ ] `.env` files are not committed (only `.env.example` templates)
- [ ] Keys are injected via environment or a secret manager
- [ ] Separate staging vs production keys/projects
- [ ] Spend and rate limits are configured in the platform dashboard

### Reliability
- [ ] Timeouts everywhere for outbound API calls
- [ ] Retries with backoff for transient failures (429/5xx/timeouts)
- [ ] Bounded generation/token budgets (cost control)
- [ ] Caching strategy (at least for repeated prompts or repeated retrieval steps)

### Operations
- [ ] Offline “doctor” checks for repo hygiene and config readiness
- [ ] Opt-in “smoke test” for live API connectivity
- [ ] Minimal, safe logging (no secrets; no sensitive prompts by default)
- [ ] Documented runbook (how to run, deploy, debug)

---

## Recommended standardized layout

Add these files/dirs to every repo:

- `config/.env.example`  
  Template for environment variables (no secrets committed).
- `PRODUCTION.md`  
  Your production checklist and policies (key safety, rate limits, latency/cost).
- `scripts/doctor.py`  
  Offline-first repo/config validator; optional `--live` minimal API call.
- `scripts/openai_smoketest.py`  
  Explicit opt-in live call; bounded and safe.
- `requirements-core.txt` (or `pyproject.toml`)  
  Includes the OpenAI SDK and other core deps.

---

## Step-by-step playbook (do this in any cluttered project)

### Step 1: Create a config template (no secrets)
Create `config/.env.example` with the minimum variables:

- `OPENAI_API_KEY=` (required for live calls)
- `OPENAI_DEFAULT_MODEL=gpt-4o-mini`
- `OPENAI_TIMEOUT_SECONDS=30`
- `OPENAI_MAX_OUTPUT_TOKENS=512`
- Optional scoping:
  - `OPENAI_ORG_ID=`
  - `OPENAI_PROJECT_ID=`

Rules:
- Never commit `.env`
- Commit only `.env.example`

---

### Step 2: Fix `.gitignore` (non-negotiable)
Ensure the repo root `.gitignore` includes at least:

- Virtual environments: `venv/`, `.venv/`, `env/`
- Secrets: `.env`, `.env.*` and allow template: `!.env.example`
- Python junk: `__pycache__/`, `*.pyc`
- Test/build: `.pytest_cache/`, `.tox/`, `dist/`, `build/`
- Generated outputs: `artifacts/`, `.cache/`

**Tip:** You can safely include duplicates; correctness matters more than elegance.

---

### Step 3: Add an offline “doctor” (fast feedback)
Create `scripts/doctor.py` that checks:
- Python version (>= 3.9 recommended; 3.11+ preferred)
- required paths exist (`README`, entrypoint, requirements, config template)
- `.env` is not present in repo root
- `.gitignore` includes required patterns
- heuristic scan for obvious key leaks (optional but helpful)
- OpenAI SDK import works
- `--live` runs a minimal, bounded API call

Design rules:
- Default mode is offline: no network, no credits.
- `--live` must be explicit.

Expected usage:
- `python scripts/doctor.py`
- `python scripts/doctor.py --live`

---

### Step 4: Add an explicit OpenAI smoke test (opt-in)
Create `scripts/openai_smoketest.py` that:
- does nothing unless `--live`
- reads `OPENAI_API_KEY` from environment only
- uses a tiny prompt like: `Say 'ok' only.`
- uses small `max_output_tokens` default (e.g., 16)
- enforces guardrails:
  - refuse huge tokens
  - refuse unreasonable timeouts
- prints:
  - model used
  - latency
  - output text
  - response id (safe)

Recommended default model: `gpt-4o-mini` (reliable text output in smoke tests).

---

### Step 5: Add/standardize dependencies
If you use requirements files, ensure your **core** deps include:

- `openai>=1.0.0`

Keep core minimal. If you have ML/viz extras, separate them:
- `requirements-core.txt`
- `requirements-ml.txt`
- `requirements-viz.txt`

This avoids “install everything” pain.

---

### Step 6: Validate in a clean environment
In a fresh venv:
1) Install core deps
2) Run doctor offline
3) Optionally run smoke test live

Example:
- `pip install -r requirements-core.txt`
- `python scripts/doctor.py`
- `python scripts/openai_smoketest.py --live`

If live fails:
- try a different model (`--model gpt-4.1-mini` or `--model gpt-4o-mini`)
- check dashboard spend/rate limits
- check network egress / proxies

---

## Tier / entitlement mapping (what you can and can’t assume)

You cannot infer “tier privileges” from code. They come from:
- your account’s billing and usage tier
- your organization role (reader/owner)
- your project settings (limits, keys, allowed models)
- model availability for your account

What you *should* do in every repo:
- treat the model as configurable (env var)
- treat rate limits as variable (client-side throttling/retry)
- document how to set spend/rate limits in the dashboard
- keep staging and production separate

---

## Operating practices to replicate everywhere

### Secrets
- Put secrets only in:
  - environment variables
  - a secret manager
- Never log:
  - API keys
  - raw sensitive prompts
  - full response payloads containing user data

### Reliability defaults
- Always set timeouts (e.g., 30s)
- Use retries with backoff for 429/5xx
- Budget tokens; cap outputs
- Cache when it makes sense (repeat prompts, retrieval results)

### Cost control
- Default to smaller/cheaper models where acceptable
- Use short prompts for tests
- Keep smoke tests bounded (16 tokens is plenty)

### Observability
- Log:
  - latency
  - model name
  - retry count
  - request ids (when available)
- Avoid logging:
  - sensitive content
  - secrets

---

## Minimal “copy into any repo” templates

### Minimal commands to include in README
- Install:
  - `pip install -r requirements-core.txt`
- Offline doctor:
  - `python scripts/doctor.py`
- Live smoke test:
  - `python scripts/openai_smoketest.py --live`

---

## Common pitfalls (and fixes)

### Pitfall: `.env` accidentally committed
Fix:
- add `.env` and `.env.*` to `.gitignore`
- remove from git history if needed
- rotate keys

### Pitfall: using one API key for everything
Fix:
- create separate staging and production projects/keys
- set strict spend limits on staging
- restrict production access

### Pitfall: smoke test works for one model but not another
Fix:
- make model configurable
- pick a “known text” model for smoke tests (e.g., `gpt-4o-mini`)
- keep smoke tests simple (text-only prompt)

### Pitfall: no timeouts/retries
Fix:
- add a small wrapper around API calls that enforces:
  - timeout
  - retry/backoff
  - bounded tokens

---

## Done criteria (when you can say “this repo is aligned”)
- `python scripts/doctor.py` passes offline
- `python scripts/doctor.py --live` passes (optional but recommended)
- no secrets in git
- `.env.example` exists and documents needed config
- README shows install + doctor + smoke test commands
- production checklist exists (`PRODUCTION.md`)

---