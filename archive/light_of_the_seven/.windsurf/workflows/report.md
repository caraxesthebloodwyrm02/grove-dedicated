# GRID Report

Date: 2025-12-15

## Summary

- `python -m grid analyze` was crashing due to an import-time `NameError` in the NER API module.
- The crash is fixed and verified end-to-end.
- The narrative explanation of the sample analysis output mostly matches intent, but there are several schema/behavior mismatches worth tracking.

## How to invoke the CLI

- The `grid` command is not available on PATH in this environment.
- Use:

```powershell
python -m grid --help
```

## Issue 1 — CLI crash in `python -m grid analyze`

### Symptom

Running:

```powershell
python -m grid analyze "..." --output yaml
```

failed with:

- `NameError: name 'ExtractRequest' is not defined`

### Root cause

File: `circuits/services/ner_api/api.py`

- The module created the default FastAPI app at import time (`app = create_app()`) **before** defining the Pydantic request/response models (`ExtractRequest`, `ExtractResponse`, etc.).
- During `create_app()`, FastAPI registered the `/extract` route using `ExtractRequest` as a type annotation, which triggered the import-time `NameError`.

### Fix applied

File: `circuits/services/ner_api/api.py`

- Moved `app = create_app()` to the end of the file, after all model class definitions.
- Restored `return app` at the end of `create_app()`.

### Verification

Command:

```powershell
python -m grid analyze "Alice met Bob at Acme Corp on 2025-12-15 for $5M" --output yaml
```

Result:

- Exit code: `0`
- Output contained entities + relationships as expected.

## Issue 2 — Review of the received narrative vs actual output schema

Input used:

```text
Alice met Bob at Acme Corp on 2025-12-15 for $5M
```

Actual output (abridged):

- Entities returned: 4
  - `Alice` (`type: ENTITY`)
  - `Bob` (`type: ENTITY`)
  - `Acme Corp` (`type: ORG`)
  - `2025-12-15` (`type: DATE`)
- Relationships returned: 6 (`4` entities → all unique pairs)

### Mismatches spotted

1. **Person typing**
   - Narrative: "two people (Alice, Bob)"
   - Actual schema: both are `type: ENTITY` (not `PERSON`).

2. **Missing MONEY entity**
   - Narrative context implies `$5M` is present.
   - Actual entities did not include `$5M`.
   - Likely cause on PowerShell: `$5M` inside **double quotes** can be interpreted as variable expansion and not passed to Python.

3. **Relationship fields vs explanation text**
   - Narrative refers to interaction count, tone, risk, etc.
   - In the current output, these are not structured fields; they only appear inside the `explanation` string.

4. **"No explicit relational signal"**
   - The verb "met" is an explicit interaction signal, but the relationship layer currently still reports "0 interactions".
   - The narrative is conceptually reasonable (weak evidence), but the specific justification doesn’t strictly match the input.

## Recommended follow-up tasks

### P0 (stability / release confidence)

- **Add an import regression test for the NER API module**
  - Why: aligns with `TODO.md` ("Validate Python/ module imports") and `PUSH_PLAN.md` pre-flight emphasis on tests.
  - Acceptance: `pytest` includes a test that imports `circuits.services.ner_api` (or `circuits.services.ner_api.api`) without raising, and validates `app` is created.

### P1 (developer workflow & docs correctness)

- **Fix `/grid-report` workflow commands**
  - Why: `DEVELOPMENT.md` stresses "verified entrypoints"; the current workflow uses non-existent CLI flags and assumes `grid` is on PATH.
  - Acceptance: workflow uses `python -m grid ...` (or another verified entrypoint) and produces a `report.md` via PowerShell redirection.

- **Clarify PowerShell quoting for `$` in examples**
  - Why: in PowerShell, `$...` expands inside double quotes, which can silently change the text sent to `grid analyze`.
  - Acceptance: docs/workflow show safe examples (single quotes, escaping, or `--file`) for text containing `$`.

### P2 (analysis output semantics / user trust)

- **Adjust relationship output when evidence is missing**
  - Use `polarity_label: unknown` (or similar) instead of defaulting to `competitive` at `confidence: 0.0`.
  - Optionally suppress relationships below a confidence threshold.

- **Add structured relationship fields (not only `explanation`)**
  - Candidates: `interaction_count`, `detected_tone`, `risk`.

### P3 (NER quality)

- **Improve or document fallback entity typing**
  - Option A: improve heuristic typing so single capitalized names can become `PERSON`.
  - Option B: document that fallback NER uses coarse `ENTITY` types.

