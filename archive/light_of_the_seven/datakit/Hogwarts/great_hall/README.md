# Great Hall

The **Great Hall** is where discussions happen and get turned into **comprehensible records**: clear criteria, explicit settings, transparent scoring (when needed), and durable notes that show *how* agreement was reached.

This directory contains:
- an **open conversation policy** (how we talk)
- a **shared JSON contract** (how we record)
- three C modules that serve the discussion table:
  - `calende` (agenda + milestones)
  - `calculator` (criteria + weights + scoring)
  - `scribe` (rows + decisions + action items)

---

## Core idea: “discussion table comprehension”

A discussion becomes easy to understand when you can answer, for every important line:
- What was said?
- Why was it said (evidence/assumptions)?
- Which criteria does it affect?
- Which options does it refer to?
- What decision/action did it cause?
- What “bridge” helped people meet halfway?

The Great Hall standardizes that into a JSON document and modules that produce/consume it.

---

## Open policy (tone + process)

See `OPEN_POLICY.md`.

Key points:
- Different vibes are allowed (nervous/high-stakes, exploratory/playful, analytical/methodical, restorative/repair).
- Default vibe: calm, direct, evidence-friendly.
- **Meet-halfway rule:** if you advocate strongly, you also propose a bridge:
  - minimum viable compromise, time-boxed trial, fallback plan, or testable condition.

This policy is not about policing—it's about keeping records legible and decisions durable.

---

## Shared JSON contract

`OPEN_POLICY.md` defines a stable JSON shape that renderers can display as a table:

Top-level keys (canonical):
- `meta`
- `session`
- `criteria_set`
- `settings`
- `options`
- `discussion_rows`
- `decisions`
- `action_items`
- `calculator_results` (optional)

Modules may also write under:
- `extensions.calende`
- `extensions.scribe`
…to avoid breaking the canonical contract while still storing extra data.

---

## Modules

### 1) `modules/calende/` — agenda + milestones
**Purpose:** structure the conversation in time.
- Session info (title, vibe, time bounds)
- Agenda items (ordered, timeboxed, linked to criteria/options)
- Milestones (due dates, owners, status)

Files:
- `modules/calende/calende.h` (API skeleton)

### 2) `modules/calculator/` — criteria scoring + ranking
**Purpose:** make decision math transparent when you need it.
- Criteria definitions (type, weight, polarity, optional range)
- Options
- Ratings matrix (option × criterion)
- Normalization + scoring + ranked results
- JSON import/export for `criteria_set`, `options`, and `calculator_results`

Files:
- `modules/calculator/calculator.h` (API skeleton)

### 3) `modules/scribe/` — structured record of the discussion
**Purpose:** capture what happened into table rows + outcomes.
- Discussion rows (`question`, `claim`, `evidence`, `proposal`, `bridge`, `decision`, `note`)
- Decision log (includes `bridge_used` to show how agreement happened)
- Action items (owner, due date, status)
- JSON import/export for `discussion_rows`, `decisions`, `action_items`

Files:
- `modules/scribe/scribe.h` (API skeleton)

---

## How they fit together (the “halfway” meeting point)

**One shared JSON document** is the handshake point:

1) `calende` shapes *when/what we discuss*
2) `scribe` records *what was said and decided*
3) `calculator` supports *why we chose something* with explicit scoring
4) A renderer reads `discussion_rows` and links criteria/options/decisions/actions into a readable table

The “meet halfway” bridge is represented explicitly in:
- `discussion_rows.kind == "bridge"`
- `decisions[].bridge_used`

---

## Suggested workflow

1) Start a session:
- set `session.vibe` and `session.title`
- define initial `criteria_set` and key `settings`

2) Run the discussion:
- `calende` provides agenda items and timeboxes
- `scribe` captures rows continuously, linking rows to criteria/options

3) Decide:
- optionally run `calculator` to rank options
- capture decision in `decisions[]`, including a bridge

4) Follow through:
- create `action_items[]` with owners and due dates
- add milestones in `calende` if you want schedule-level tracking

---

## Implementation notes (C + JSON)

- Modules currently provide C header skeletons; implementations (`*.c`) should:
  - explicitly document memory ownership
  - treat JSON as UTF-8 text
  - integrate a JSON parser/serializer library (recommended)
- Keep stable IDs (don’t rely on array indices).
- Use RFC3339 timestamps for `*_at` fields.

---

## Next step

If you want a “copy of toon” (a parallel vibe/policy or a themed variant), define it as either:
- a new `settings[]` bundle (recommended), or
- a second policy doc (e.g. `TOON_POLICY.md`) that maps onto the same JSON contract so the table renderer stays consistent.