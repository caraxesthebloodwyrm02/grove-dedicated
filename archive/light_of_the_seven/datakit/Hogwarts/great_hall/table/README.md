# Great Hall — Table Builder CLI

This directory contains the **streaming-friendly** Great Hall table builder.

It turns a discussion stream into **spreadsheet-like outputs** plus a **take-home receipt**:

- `discussion_table.csv` (one row per discussion row; denormalized with links)
- `receipt.json` (portable summary: decisions, bridges, homework, snapshots)
- `warnings.log` (non-fatal parse/link warnings)

The intent is: **talk → capture → generate a slip you can revisit later** (even in a different vibe).

---

## What it does (v1)

- Reads **JSONL** (one JSON object per line) representing Great Hall events.
- Folds events into an in-memory model using **stable IDs** (upsert semantics).
- Writes outputs to an `--outdir`.

This version uses a **minimal JSON extractor** (not a full JSON parser):
- best for bootstrapping workflows
- expect limitations with escaped quotes and complex nested JSON

---

## Files

- `great_hall_table.c` — the CLI implementation
- `example_stream.jsonl` — sample input stream you can run immediately
- `TABLE_BUILDER.md` — design doc and mental model

---

## Input format (JSONL)

Each line is an object:

- `type`: `"session" | "criteria" | "setting" | "option" | "row" | "decision" | "action"`
- `at`: RFC3339 timestamp (optional)
- `payload`: object; shape depends on `type`

The minimal supported payloads are documented at the top of `great_hall_table.c`.

---

## Build

### Option A: clang (Windows) / gcc (Linux/macOS)
From this directory:

```/dev/null/shell#L1-3
cc -O2 -std=c99 great_hall_table.c -o great_hall_table
```

On Windows with MinGW you may get `great_hall_table.exe`.

### Option B: MSVC (Windows)
From a “Developer Command Prompt”:

```/dev/null/shell#L1-3
cl /O2 /std:c11 great_hall_table.c
```

This should produce `great_hall_table.exe`.

---

## Run (example)

### 1) Run against the included sample stream
```/dev/null/shell#L1-3
./great_hall_table --input example_stream.jsonl --outdir ../outputs
```

### 2) Inspect outputs
You should get:

- `../outputs/discussion_table.csv`
- `../outputs/receipt.json`
- `../outputs/warnings.log`

The CLI also prints a summary like:
- rows, criteria, options, decisions, actions, warnings

---

## Output: `discussion_table.csv`

Columns (v1):

- `row_id`
- `at`
- `speaker_id`
- `kind`
- `content`
- `tone_tag`
- `criteria_ids` (joined with `|`)
- `criteria_names` (joined with `|`)
- `option_ids` (joined with `|`)
- `option_labels` (joined with `|`)
- `decision_id`
- `decision_title`
- `decision_status`
- `bridge_used`
- `action_id`
- `action_title`
- `action_owner_id`
- `action_due_at`
- `action_status`

Notes:
- Missing references don’t crash the tool; they show up as empty details (and may log warnings).
- Row ordering is stable-sorted by RFC3339 timestamp when present.

---

## Output: `receipt.json`

A minimal take-home artifact containing:

- `receipt_meta`
- `session_snapshot`
- `inputs_snapshot` (criteria/settings/options)
- `discussion_summary` (counts-based one-liner)
- `decisions`
- `homework.action_items`

This is aligned with the intent in `../OUTPUT_ARTIFACT.md`.

---

## Known limitations (v1)

- Not a full JSON parser:
  - complex escaping (like `\"`) may misparse
  - deep nesting beyond the expected shapes may be ignored
- `settings.value` is captured as a best-effort JSON snippet, not strongly typed.
- No `calculator_results` folding yet (planned).

---

## Next upgrades (v2 ideas)

- Swap the minimal extractor for a real JSON library (robust parsing).
- Support `"calculator_results"` events and include ranked outputs in `receipt.json`.
- Support `"milestone"` events (from `calende`) and include in receipt homework.
- Emit `discussion_table.json` alongside CSV for richer downstream rendering.
- Optional: incremental mode (re-run as stream grows; deterministic output).

---