# Production best practices (DataKit)

This document aligns `full_datakit/` with production-oriented security and operations guidance for projects that integrate the OpenAI API (or other external AI APIs).

## Goals

- Prevent secret leakage (API keys, tokens, credentials).
- Enable safe staging vs production separation.
- Improve reliability under load (rate limits, retries, caching, batching).
- Improve latency and cost efficiency (model choice, token budgeting, streaming).
- Add operational readiness (logging, monitoring, error handling, runbooks).

---

## 1) Account / organization hygiene (OpenAI)

### Organization and project separation
- Use separate **projects** for:
  - `staging` (dev/test traffic, limited spend)
  - `production` (restricted access, stricter spend/rate limits)
- Restrict production access to minimal required users/services.
- Prefer service-specific keys per environment; never reuse dev keys in prod.

### Billing and spend limits
- Set notification thresholds (email alerts) for usage.
- Use project-level limits to cap blast radius of misconfigurations.

### Rate limits
- Know your account/project rate limits and design accordingly:
  - Implement client-side throttling.
  - Use exponential backoff and retries on transient failures.
  - Consider batching where appropriate.

---

## 2) Secret management (must-do)

### Rules
- Never hardcode secrets in:
  - `.py` files
  - notebooks
  - docs
  - CI config logs
- Never commit secrets to git.
- Rotate keys if leakage is suspected.

### Recommended approach
- Local development:
  - Keep secrets in a local `.env` file (untracked).
  - Use `full_datakit/config/.env.example` as a template.
- Production:
  - Use a secret manager (cloud provider secret store, vault, CI secrets).
  - Inject secrets via environment variables.

### Minimum environment variables
- `OPENAI_API_KEY` (required if using OpenAI)
- Optional scoping:
  - `OPENAI_ORG_ID`
  - `OPENAI_PROJECT_ID`

---

## 3) Repository hygiene (what should be committed)

### Virtual environments
- Do not commit `venv/` or `.venv/` directories to source control.
- Ensure `.gitignore` excludes:
  - `venv/`, `.venv/`, `env/`, `.env/`
  - `__pycache__/`, `*.pyc`, build artifacts

### Configuration
- Commit templates (safe):
  - `config/.env.example`
- Do not commit environment-specific files:
  - `.env`, `.env.*` (unless they contain no secrets and are meant to be public)

---

## 4) Runtime configuration

Use environment variables for:
- Model selection (`OPENAI_DEFAULT_MODEL`)
- Output budget (`OPENAI_MAX_OUTPUT_TOKENS`)
- Sampling (`OPENAI_TEMPERATURE`)
- Timeouts (`OPENAI_TIMEOUT_SECONDS`)
- Streaming toggle (`OPENAI_STREAM`)
- Cache directory (`DATAKIT_CACHE_DIR`)
- Log level/format (`APP_LOG_LEVEL`, `LOG_FORMAT`)

Keep defaults conservative:
- low temperature (0–0.3)
- bounded max output tokens
- reasonable timeouts (e.g., 30s)
- safe retry strategy

---

## 5) Reliability patterns (API calls)

### Timeouts
Always set request timeouts to avoid stuck processes.

### Retries with backoff
Retry transient errors:
- network timeouts
- rate limits (HTTP 429)
- 5xx errors

Use exponential backoff with jitter, and cap max retries.

### Idempotency and safe replays
If you have “create” operations, consider idempotency keys and/or de-duplication.

### Circuit breakers
For high-traffic services, add circuit breaker behavior to prevent cascading failures.

---

## 6) Scaling architecture

### Horizontal scaling
If you turn DataKit into a service:
- Run multiple stateless instances behind a load balancer.
- Store state (sessions, caches) in shared storage (DB/Redis) if needed.

### Vertical scaling
If you run batch jobs:
- Increase CPU/RAM for tokenization, embeddings, or large IO loads.

### Caching (high impact)
Cache results for:
- repeated prompts (careful with personalization)
- computed metadata
- expensive retrieval steps

Cache invalidation:
- TTL-based for “best effort”
- versioned keys for deterministic outputs

### Load balancing
Use a standard load balancer for service deployments; keep instances stateless where possible.

---

## 7) Latency optimization

Major drivers:
- model choice
- number of output tokens

Recommendations:
- Use the smallest model that meets quality requirements.
- Reduce `max_output_tokens` and add stop conditions when possible.
- Stream responses when UX benefits from early tokens.
- Batch requests where it truly reduces overhead (test to confirm).

---

## 8) Cost management

Cost is driven by:
- total tokens (input + output)
- model pricing tier

Actions:
- Set token budgets per request.
- Use caching to eliminate repeated calls.
- Prefer smaller models for non-critical tasks.
- Monitor usage and set alerts.
- Log per-request token usage (if available) and correlate with user actions.

---

## 9) Logging and observability

### Logging
- Prefer structured logs (JSON) in production.
- Include:
  - request correlation IDs
  - error type/class
  - latency
  - retry count
  - model name
  - token usage (if available)
- Never log secrets or full user prompts if they contain sensitive data.

### Metrics
Track:
- request count / error rate
- latency percentiles (p50/p95/p99)
- rate-limit events
- cost estimates (tokens)

### Tracing (optional but recommended)
Adopt OpenTelemetry if you deploy as a service.

---

## 10) Data security and privacy

- Classify data: public, internal, confidential, regulated.
- Minimize data sent to external APIs:
  - redact PII where possible
  - avoid sending raw secrets, tokens, credentials
- Encrypt data at rest (if persisted) and in transit (TLS).
- Define retention policies for:
  - logs
  - cached responses
  - user-generated content

---

## 11) Safety and misuse prevention

- Add input validation and guardrails if exposing user input to automated actions.
- Monitor for abuse patterns (prompt injection, spam).
- Consider policy enforcement if generating public content.

---

## 12) Deployment checklist (practical)

### Before deploying
- [ ] Secrets injected via environment/secret manager (no hardcoded keys).
- [ ] Staging and production use different keys/projects.
- [ ] Rate limiting and retries are implemented and tested.
- [ ] Timeouts configured.
- [ ] Logs are structured and sanitized.
- [ ] Caching strategy defined (what/where/TTL).
- [ ] Token budgets enforced.
- [ ] Monitoring and alerting configured (errors, latency, spend).
- [ ] CI checks include lint/test.

### After deploying
- [ ] Verify real traffic under expected load.
- [ ] Monitor error spikes and rate limits.
- [ ] Tune model, max tokens, caching based on observed usage.
- [ ] Review costs daily initially, then weekly.

---

## 13) Local development (recommended workflow)

- Use a local virtual environment.
- Create a local `.env` from `config/.env.example`.
- Keep `.env` untracked by git.
- Run tests before pushing changes.

---

## References

- OpenAI API key safety: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
- Rate limits guide: https://platform.openai.com/docs/guides/rate-limits
- Latency optimization: https://platform.openai.com/docs/guides/latency-optimization
- Python venv docs: https://docs.python.org/3/library/venv.html