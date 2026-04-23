# Great Hall — Discussion Table Builder (Streaming-Friendly Design)

This document explains how the Great Hall “room” becomes a **spreadsheet-like discussion table** and a **take-home receipt**, even when discussion is **streamed** and the modules feel mind-boggling at first.

The goal is to make the system feel like **one simple thing**:

> You talk → we capture rows → we link them to criteria/options/decisions/actions → we emit a table + receipt.

---

## 1) Problem this solves

Open discussions create manual overhead:
- reasoning gets lost,
- decisions get re-litigated,
- action items drift,
- different “vibes” distort memory.

So we need:
- a stable **event stream** representation of what happened,
- a way to render it into a **table** (comprehension),
- and a **quantifiable artifact** (receipt/homework).

---

## 2) “How the room works” in one mental model

Think of the Great Hall as a pipeline with one shared contract:

1) **Stream** of events happens (people talk, propose, bridge, decide).
2) **Scribe** writes those events into `discussion_rows`, `decisions`, `action_items`.
3) **Calculator** optionally attaches quantification (`calculator_results`).
4) **Calende** optionally attaches schedule structure (agenda/milestones).
5) **Table Builder** is the last mile:
   - reads the live document (or event stream),
   - produces:
     - `discussion_table.csv` (spreadsheet)
     - `discussion_table.json` (structured table)
     - `receipt.json` (take-home artifact)

**Key point:** the modules are internal; the user experience is “I get a clean slip at the end.”

---

## 3) Inputs and outputs

### Input (streamed)
The discussion is streamed as:
- either incremental JSON patches to a single document, or
- a line-delimited JSON event stream (`.jsonl`) that can be folded into a document.

This design supports both.

### Output artifacts
- `outputs/discussion_table.csv`
- `outputs/discussion_table.json`
- `outputs/receipt.json`

These correspond to:
- comprehension (table),
- portability (receipt).

---

## 4) Shared contract alignment (source of truth)

Source contract is documented in:
- `OPEN_POLICY.md` (shared schema principles + keys)
- `OUTPUT_ARTIFACT.md` (receipt format)

Table builder assumes a “canonical” document containing:
- `session`
- `criteria_set`
- `settings`
- `options`
- `discussion_rows`
- `decisions`
- `action_items`
- `calculator_results` (optional)
- `extensions.*` (optional)

---

## 5) Table Builder responsibilities (what it does)

### 5.1 Normalize for comprehension
A streamed discussion can be messy. The table builder makes it readable by:
- ordering rows by timestamp (`discussion_rows[].at`), then by insertion order
- filling missing optional fields with empty values (never crash)
- resolving references:
  - `criteria_touched[]` -> criteria names
  - `option_refs[]` -> option labels
  - `decision_ref` -> decision title/status
  - `action_ref` -> action title/status/owner/due

### 5.2 Produce a spreadsheet-friendly table
Each discussion row becomes one table record with denormalized columns.

Recommended columns:

- `row_id`
- `at`
- `speaker_id`
- `kind`
- `content`
- `tone_tag`
- `criteria_ids`
- `criteria_names`
- `option_ids`
- `option_labels`
- `decision_id`
- `decision_title`
- `decision_status`
- `bridge_used`
- `action_id`
- `action_title`
- `action_owner_id`
- `action_due_at`
- `action_status`

This makes “why + what + next” visible in one sheet.

### 5.3 Emit a take-home receipt
Receipt summarizes:
- session snapshot
- inputs snapshot (criteria/settings/options)
- quantified outputs (if any)
- decisions (with bridges)
- homework (actions + milestones if present)
- open questions (if they exist as row kinds or explicit field)

---

## 6) Streaming model: events and folding

### Option A: Single JSON document updated over time
- Producers append to arrays:
  - `discussion_rows[]`
  - `decisions[]`
  - `action_items[]`
- Table builder can re-run at any time to regenerate outputs.

### Option B: JSONL event stream (recommended for streaming)
Each line is an event object:

- `type`: `"row" | "decision" | "action" | "milestone" | "setting" | "criteria" | "option" | "calculator_results" | "session"`
- `at`: RFC3339 timestamp
- `payload`: object matching the corresponding element shape

The table builder “folds” events into a canonical in-memory document:
- insert/update by stable IDs (upsert),
- preserve insertion order for tie breaks.

**Why JSONL?**
- safe to append
- easy to replay
- supports partial availability and late-arriving context (criteria defined after a row, etc.)

---

## 7) “Mind-boggling modules” → simple UX

To reduce cognitive load, expose only 3 user-facing concepts:

1) **Rows**: what was said (plus tags)
2) **Outcomes**: decisions + actions + due dates
3) **Quantification**: scores/ranks when needed

Everything else is implementation detail.

If someone feels lost, the system should answer:
- “What are we deciding?”
- “What criteria matter?”
- “What’s the bridge to meet halfway?”
- “What’s my homework?”

---

## 8) Implementation plan (C-first, minimal dependencies)

### 8.1 Phase 1: Build without full JSON parsing (pragmatic)
If strict JSON parsing is too heavy initially:
- accept a constrained input format (JSONL events with simple string fields), OR
- require that upstream produces already-flattened row objects.

But the intended endpoint is proper JSON parsing.

### 8.2 Phase 2: Proper JSON parsing + export
Add a JSON library in the C implementation to:
- parse canonical Great Hall JSON or JSONL stream,
- build lookup maps for criteria/options/decisions/actions,
- export CSV with correct escaping,
- export JSON table + receipt.

### 8.3 Determinism
Outputs should be deterministic:
- stable sorting rules
- stable column order
- stable ID-based linking
- do not depend on runtime locale

---

## 9) Edge cases (must handle)

- Missing `criteria_set` or `options`: table still generates with IDs only.
- Missing timestamps: order by insertion, leave `at` blank.
- Dangling refs (`decision_ref` points to missing decision): keep ID, leave details blank.
- Duplicate IDs: last write wins (upsert), but log a warning.
- Mixed vibes: `vibe` is session-level, `tone_tag` is per-row.

---

## 10) Definition of done

A “good” v1 table builder:
- accepts a canonical Great Hall JSON (or JSONL events)
- emits `discussion_table.csv` with one row per discussion row
- emits `receipt.json` with decisions + bridges + homework
- never fails hard on missing optional fields

---

## 11) Suggested file outputs

- `outputs/discussion_table.csv`
- `outputs/discussion_table.json`
- `outputs/receipt.json`

Optionally:
- `outputs/warnings.log` (dangling refs, duplicate IDs, invalid timestamps)

---

## 12) Next concrete step

Implement a small CLI:

- Input:
  - `--input session.json` OR `--input stream.jsonl`
- Output:
  - `--outdir outputs/`

Command example:
- `great_hall_table --input session.json --outdir outputs`

This CLI becomes the “room’s final action”: it produces the slip you take home.