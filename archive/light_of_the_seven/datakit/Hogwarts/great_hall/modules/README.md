# Great Hall Modules — Stream Mapping Guide

This file explains how the **modules** (`calende`, `calculator`, `scribe`) map onto the **stream format** and how that stream becomes final **outputs** (discussion table + receipt).

This is meant to reduce the “mind-boggling” feeling: you don’t have to understand all modules at once. You can think in one simple pipeline:

> stream events → folded into a canonical doc → table + take‑home receipt

---

## 1) The shared contract (source of truth)

- `../OPEN_POLICY.md` defines the conversation policy + the canonical document keys.
- `../OUTPUT_ARTIFACT.md` defines the “take‑home receipt” artifact.

The stream is simply a **time-ordered, append-only way** to build that document.

---

## 2) The recommended stream

The reference stream lives here:

- `recommended_stream.jsonl`

Each line is one JSON object shaped like:

- `type`: what kind of event this is
- `at`: timestamp (RFC3339)
- `payload`: the object for that event type

Example:

```json
{"type":"row","at":"...","payload":{"row_id":"r1","speaker_id":"p1","kind":"proposal","content":"..."}}
```

---

## 3) Module → stream event types

### 3.1 `scribe` → the narrative + outcomes
`scribe` owns the **comprehension layer**: what was said, what it touched, and what happened because of it.

It maps to these stream event types:

- `row`
  - `payload.row_id`
  - `payload.at` (optional; `event.at` can be used)
  - `payload.speaker_id`
  - `payload.kind`: `question|claim|evidence|proposal|bridge|decision|note`
  - `payload.content`
  - optional linking fields:
    - `payload.criteria_touched`: `["c_clarity", ...]`
    - `payload.option_refs`: `["o_a", ...]`
    - `payload.decision_ref`: `"d1"`
    - `payload.action_ref`: `"a1"`
    - `payload.tone_tag`: `"calm"|"tense"|...`
- `decision`
  - `payload.decision_id`
  - `payload.title`
  - `payload.status`: `made|deferred|reversed`
  - `payload.chosen_option_id` (optional)
  - `payload.rationale` (optional)
  - `payload.bridge_used` (optional but strongly recommended; it’s the “meet halfway” trace)
- `action`
  - `payload.action_id`
  - `payload.title`
  - `payload.owner_id`
  - `payload.due_at` (optional)
  - `payload.status`: `open|in_progress|done|dropped`
  - `payload.notes` (optional)

In the canonical document this feeds:
- `discussion_rows[]`
- `decisions[]`
- `action_items[]`

### 3.2 `calculator` → criteria + options (and later scoring)
`calculator` owns the **quantification layer**: criteria, weights, options, and (later) computed results.

It maps to these stream event types:

- `criteria`
  - `payload.id`
  - `payload.name`
  - `payload.type`: `number|bool|text`
  - `payload.weight`
  - `payload.polarity`: `higher_is_better|lower_is_better|neutral`
- `option`
  - `payload.id`
  - `payload.label`
  - `payload.notes` (optional)

Planned/next (not required for v1 outputs):
- `calculator_results`
  - ranked options + breakdown

In the canonical document this feeds:
- `criteria_set.criteria[]`
- `options[]`
- `calculator_results` (optional)

### 3.3 `calende` → schedule structure (optional in v1)
`calende` owns the **time/structure layer**: agenda, milestones, checkpoints.

In the recommended stream we haven’t emitted calende events yet, but the mapping is:

Planned/next:
- `milestone`
  - `payload.milestone_id`
  - `payload.title`
  - `payload.due_at`
  - `payload.owner_id` (optional)
  - `payload.status` (optional)
- `agenda_item`
  - `payload.item_id`
  - `payload.title`
  - `payload.timebox_minutes` (optional)
  - linkage:
    - criteria touched
    - option refs

In the canonical document this can live under:
- `extensions.calende` (recommended for non-breaking evolution)

---

## 4) Session context in the stream

Event type:

- `session`
  - `payload.session_id`
  - `payload.title`
  - `payload.vibe`
  - `payload.participants[]`

In the canonical document this feeds:
- `session`

---

## 5) Settings in the stream

Event type:

- `setting`
  - `payload.key`
  - `payload.value`
  - `payload.scope`: `session|topic|project`
  - `payload.rationale` (optional)

In the canonical document this feeds:
- `settings[]`

Settings are how you implement “different vibes” and “ecosystem/environment” themes without rewriting code:
- you encode the environment as explicit settings
- you later read/aggregate them into receipts and tables

---

## 6) How the outputs are produced

A table builder reads the stream and emits:

### 6.1 `outputs/discussion_table.csv`
One row per `row` event (scribe rows), denormalized into a spreadsheet-friendly table.

Typical columns:
- row metadata: `row_id`, `at`, `speaker_id`, `kind`, `content`, `tone_tag`
- linkage: `criteria_ids`, `criteria_names`, `option_ids`, `option_labels`
- outcomes: `decision_*`, `bridge_used`, `action_*`

### 6.2 `outputs/receipt.json`
A portable “take-home slip” summarizing:
- session snapshot
- inputs snapshot (criteria/settings/options)
- decisions (with bridges)
- homework (action items; milestones later)

This is the artifact you can revisit later in a different vibe without losing “why”.

---

## 7) Recommended stream: what it currently demonstrates

`recommended_stream.jsonl` (based on our conversation) demonstrates:

- uncertainty acknowledged (“scientists need time…”)
- ecosystem framing (root visibility / environment constraints)
- explicit criteria: clarity, risk, speed
- a meet-halfway bridge (trial now, upgrade later)
- a decision + a concrete action item (“run the table builder and inspect outputs”)

That is the intended Great Hall loop:
> discuss → bridge → decide → assign homework → generate slip

---

## 8) Practical usage

1) Keep appending events to `recommended_stream.jsonl` (or a new session stream).
2) Run the table builder to generate outputs.
3) Use the outputs as the “homework slip” and the spreadsheet view for later review.

If you ever feel lost in modules:
- focus on `row` (what was said),
- then `decision` (what we agreed),
- then `action` (what you do next),
- and only then `calculator`/`calende` if quantification or scheduling is needed.