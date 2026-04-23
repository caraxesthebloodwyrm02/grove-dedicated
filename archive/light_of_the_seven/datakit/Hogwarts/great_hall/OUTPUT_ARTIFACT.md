# Great Hall — Output Artifact (“Take‑Home Receipt”)

This file defines the **output artifact** produced after an open discussion in the Great Hall.

It is meant to be a **quantifiable receipt** you can take home:
- to remember what happened,
- to see *why* it happened,
- to track homework (actions/milestones),
- and to revisit later in a different vibe without losing context.

This receipt assumes **manual overhead** is real: people talk, disagree, negotiate, and need a clean end-state.

---

## Q‑1: what does it do?

**A:** When you come to the `great_hall` for an open discussion, the topic carries some manual overhead: it needs reasoning, discussion, and clear quantifiable outputs. The modules work together and produce a final quantifiable receipt artifact for homework—any topic, tense ones, or late-night one‑on‑one sessions. The hall creates a slip you can take home so you don’t forget, and can revisit later in a different vibe.

---

## Output Artifact: “Receipt” JSON (format v1)

### Intent
A receipt should answer these questions quickly:
1) **What did we talk about?** (topic, vibe, participants, timeframe)
2) **What did we decide?** (decision log + rationale)
3) **What are we doing next?** (action items + milestones)
4) **How do we measure success?** (criteria, metrics, targets)
5) **What’s the bridge / halfway point?** (compromise/trial/fallback/condition)
6) **What is quantifiable?** (scores, ranks, deadlines, ownership)

### Recommended top-level shape

- `receipt_meta`: versioning + identifiers
- `session_snapshot`: vibe + participants + time window
- `inputs_snapshot`: criteria + settings + options (what we used)
- `discussion_summary`: short narrative + key points
- `quantified_outputs`: scoring/ranking/metrics (optional but preferred)
- `decisions`: decision log (must be explicit)
- `homework`: action items + milestones + due dates
- `bridges`: explicit halfway points that enabled progress
- `open_questions`: what remains unresolved (with next review date if possible)
- `links`: pointers to fuller logs or source docs

This is intentionally compatible with the shared contract in `OPEN_POLICY.md`:
- You can generate a receipt from a full Great Hall document by selecting and summarizing fields.
- You can also store receipt data back into the full document under `extensions.receipt`.

---

## Receipt JSON schema (practical, not strict)

### `receipt_meta`
- `receipt_id` (string, stable)
- `created_at` (RFC3339 string)
- `format_version` (string, e.g. `"1.0.0"`)
- `source_doc_id` (string; link to the full discussion document if present)

### `session_snapshot`
- `session_id` (string)
- `title` (string)
- `vibe` (string enum or freeform)
- `participants` (array: `{id, display_name, role?}`)
- `time_window` (optional: `{started_at?, ended_at?}`)

### `inputs_snapshot`
- `criteria` (array: `{id, name, weight, type, polarity?}` minimal)
- `settings` (array: `{key, value, scope, rationale?}`)
- `options` (array: `{id, label}` minimal)

### `discussion_summary`
- `one_liner` (string)
- `key_points` (array of strings)
- `assumptions` (array of strings)
- `risks` (array of strings)

### `quantified_outputs` (optional)
- `calculator`:
  - `model` (string)
  - `ranked_options` (array: `{option_id, score, breakdown?}`)
- `metrics` (array: `{name, baseline?, target?, unit?, due_at?, owner_id?}`)

### `decisions`
Array of:
- `decision_id`
- `title`
- `status` (`made|deferred|reversed`)
- `chosen_option_id?`
- `rationale?`
- `bridge_used?` (string; required for “made” decisions if enforcing meet-halfway)

### `homework`
- `action_items` (array: `{action_id, title, owner_id, due_at?, status, notes?}`)
- `milestones` (array: `{milestone_id, title, owner_id?, due_at?, status?, notes?}`)

### `bridges`
Array of:
- `bridge_id`
- `type` (`mvc|trial|fallback|condition`)
- `text` (string)
- `links` (optional: `{decision_id?, rows?}`)

### `open_questions`
Array of:
- `question`
- `owner_id?`
- `review_at?` (RFC3339)

---

## Minimal example receipt (take-home slip)

```/dev/null/great_hall_receipt_example.json#L1-120
{
  "receipt_meta": {
    "receipt_id": "receipt-gh-0001",
    "created_at": "2025-12-14T00:00:00Z",
    "format_version": "1.0.0",
    "source_doc_id": "gh-001"
  },
  "session_snapshot": {
    "session_id": "s-001",
    "title": "Tense topic: pick a path without burning out",
    "vibe": "nervous_high_stakes",
    "participants": [
      { "id": "p_fac", "display_name": "Facilitator", "role": "facilitator" },
      { "id": "p_scr", "display_name": "Scribe", "role": "scribe" }
    ],
    "time_window": { "started_at": "2025-12-14T00:10:00Z", "ended_at": "2025-12-14T01:00:00Z" }
  },
  "inputs_snapshot": {
    "criteria": [
      { "id": "c_risk", "name": "Risk", "type": "number", "weight": 2.0, "polarity": "lower_is_better" },
      { "id": "c_speed", "name": "Speed", "type": "number", "weight": 1.0, "polarity": "higher_is_better" }
    ],
    "settings": [
      { "key": "decision_reversibility", "value": "reversible", "scope": "session", "rationale": "Prefer trials first." }
    ],
    "options": [
      { "id": "o_a", "label": "Option A" },
      { "id": "o_b", "label": "Option B" }
    ]
  },
  "discussion_summary": {
    "one_liner": "We agreed to run a short trial of A with a clear fallback to B.",
    "key_points": [
      "We need measurable progress this week.",
      "Risk must be controlled; reversibility matters."
    ],
    "assumptions": [
      "We can evaluate the trial outcome by Friday."
    ],
    "risks": [
      "If we don’t define success metrics, we’ll re-argue the same thing next time."
    ]
  },
  "quantified_outputs": {
    "calculator": {
      "model": "weighted_sum/v1",
      "ranked_options": [
        { "option_id": "o_a", "score": 0.62 },
        { "option_id": "o_b", "score": 0.58 }
      ]
    },
    "metrics": [
      { "name": "Trial completed", "baseline": 0, "target": 1, "unit": "boolean", "due_at": "2025-12-19T18:00:00Z", "owner_id": "p_fac" }
    ]
  },
  "decisions": [
    {
      "decision_id": "d_001",
      "title": "Proceed with Option A as a trial",
      "status": "made",
      "chosen_option_id": "o_a",
      "rationale": "Fastest path with controlled risk via reversibility.",
      "bridge_used": "Time-boxed trial: if A fails by Friday, switch to B."
    }
  ],
  "homework": {
    "action_items": [
      { "action_id": "a_001", "title": "Define success criteria for the trial", "owner_id": "p_scr", "due_at": "2025-12-15T12:00:00Z", "status": "open" },
      { "action_id": "a_002", "title": "Run the trial for Option A", "owner_id": "p_fac", "due_at": "2025-12-19T18:00:00Z", "status": "open" }
    ],
    "milestones": [
      { "milestone_id": "m_001", "title": "Friday evaluation checkpoint", "owner_id": "p_fac", "due_at": "2025-12-19T18:00:00Z", "status": "open" }
    ]
  },
  "bridges": [
    { "bridge_id": "b_001", "type": "trial", "text": "Run A until Friday; if success metrics aren’t met, switch to B.", "links": { "decision_id": "d_001" } }
  ],
  "open_questions": [
    { "question": "What does 'success' mean numerically for this trial?", "owner_id": "p_scr", "review_at": "2025-12-15T12:00:00Z" }
  ],
  "links": {
    "policy": "OPEN_POLICY.md",
    "modules": "modules/",
    "full_discussion_document": "gh-001.json"
  }
}
```

---

## Notes (how modules produce this receipt)

- `scribe` supplies:
  - `discussion_summary` (from rows) + `decisions` + `homework.action_items` + `bridges`
- `calculator` supplies:
  - `quantified_outputs.calculator` (rank + score breakdown)
- `calende` supplies:
  - `homework.milestones` + (optionally) evaluation checkpoints

The receipt is the **portable artifact**: concise enough to reread, structured enough to compute, and explicit enough to reduce re-litigating the same discussion later.