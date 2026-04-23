# Great Hall — Open Policy (Conversations + Shared JSON Contract)

This Great Hall exists to turn discussion into **clear, useful outcomes** without forcing a single mood or style. You can bring urgency, calm, humor, rigor, or brainstorming energy—just keep it constructive and legible.

This document sets:
1) an **open conversation policy** (how we talk)
2) a **shared JSON schema contract** (how we record)

---

## 1) Open conversation policy

### 1.1 Purpose
- Make disagreements productive.
- Preserve context so newcomers can understand decisions.
- Create a “meet halfway” path: every strong position must present a bridge.

### 1.2 Allowed vibes (explicitly)
Different sessions can be different:
- **Nervous / high-stakes**: prioritize risk management, crisp decisions, minimal ambiguity.
- **Exploratory / playful**: prioritize idea generation, allow unfinished thoughts.
- **Analytical / methodical**: prioritize evidence, modeling, explicit assumptions.
- **Restorative / repair**: prioritize tone, clarity of intent, de-escalation.

State the vibe at session start. If not stated, default to: **calm, direct, evidence-friendly**.

### 1.3 “Meet halfway” rule (bridge requirement)
When you argue for an option, you must offer at least one bridge:
- a **minimum viable compromise** (MVC),
- a **time-boxed trial**,
- a **fallback plan**,
- or a **testable condition** under which you’d change your mind.

This keeps the table comprehensible and prevents stalemates.

### 1.4 What belongs in the record (scribe rules)
A record entry should answer:
- **What was claimed?**
- **Why (evidence or reasoning)?**
- **Which criteria does it touch?**
- **What changed?** (decision, action, settings, or next question)
- **Who owns the next step?** (if any)

### 1.5 Disagreement protocol
1) Clarify the **decision type**: reversible vs irreversible.
2) Surface assumptions.
3) Map conflict to criteria (see schema): speed, cost, risk, quality, alignment, etc.
4) Propose a bridge.
5) Decide, defer with a deadline, or split into parallel experiments.

### 1.6 Safety + respect
- Attack problems, not people.
- No threats, harassment, doxxing, or coercion.
- If temperature rises: pause, restate intentions, return to criteria, propose bridge.

### 1.7 Defaults (when uncertain)
- Prefer reversible actions.
- Prefer written criteria over gut feelings.
- Prefer small experiments over large commitments.
- Prefer explicit settings over implicit expectations.

---

## 2) Shared JSON contract for “discussion table comprehension”

This contract is what the `calende`, `calculator`, and `scribe` modules will exchange and what a Great Hall “discussion table” will render.

### 2.1 Design principles
- **Human-readable** first, machine-friendly second.
- Stable IDs and timestamps.
- Record *both* outcomes and reasoning.

### 2.2 Canonical top-level document
A Great Hall document is a single JSON object with these top-level keys:

- `meta`: document metadata
- `session`: the meeting/session context (time/vibe/participants)
- `criteria_set`: criteria + weights + types
- `settings`: explicit settings/policies used in this session/topic
- `options`: things being compared or discussed
- `discussion_rows`: table rows (the core narrative)
- `decisions`: decision log
- `action_items`: follow-ups with owners and due dates
- `calculator_results`: scoring/ranking outputs (optional)

### 2.3 JSON Schema (Draft 2020-12)

```/dev/null/great_hall_open_policy_schema.json#L1-206
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "great_hall://schema/discussion_document.json",
  "title": "Great Hall Discussion Document",
  "type": "object",
  "required": ["meta", "session", "criteria_set", "settings", "options", "discussion_rows", "decisions", "action_items"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["doc_id", "created_at", "version"],
      "properties": {
        "doc_id": { "type": "string", "description": "Stable identifier for this document." },
        "created_at": { "type": "string", "description": "RFC3339 timestamp." },
        "version": { "type": "string", "description": "Schema/format version, e.g. '1.0.0'." },
        "source": { "type": "string", "description": "Where it came from (tool, user, import)." }
      },
      "additionalProperties": false
    },

    "session": {
      "type": "object",
      "required": ["session_id", "title", "vibe", "participants"],
      "properties": {
        "session_id": { "type": "string" },
        "title": { "type": "string" },
        "vibe": {
          "type": "string",
          "enum": ["calm_direct", "nervous_high_stakes", "exploratory_playful", "analytical_methodical", "restorative_repair", "custom"]
        },
        "vibe_notes": { "type": "string" },
        "started_at": { "type": "string", "description": "RFC3339 timestamp." },
        "ended_at": { "type": "string", "description": "RFC3339 timestamp." },
        "participants": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "display_name"],
            "properties": {
              "id": { "type": "string" },
              "display_name": { "type": "string" },
              "role": { "type": "string", "description": "Optional role (facilitator, scribe, stakeholder, etc.)." }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    },

    "criteria_set": {
      "type": "object",
      "required": ["criteria"],
      "properties": {
        "criteria": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "name", "type", "weight"],
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "description": { "type": "string" },
              "type": { "type": "string", "enum": ["bool", "number", "text"] },
              "weight": { "type": "number", "minimum": 0 },
              "range": {
                "type": "object",
                "properties": {
                  "min": { "type": "number" },
                  "max": { "type": "number" }
                },
                "additionalProperties": false
              },
              "polarity": { "type": "string", "enum": ["higher_is_better", "lower_is_better", "neutral"] }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    },

    "settings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["key", "value", "scope"],
        "properties": {
          "key": { "type": "string" },
          "value": {},
          "scope": { "type": "string", "enum": ["session", "topic", "project"] },
          "rationale": { "type": "string" }
        },
        "additionalProperties": false
      }
    },

    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "label"],
        "properties": {
          "id": { "type": "string" },
          "label": { "type": "string" },
          "notes": { "type": "string" }
        },
        "additionalProperties": false
      }
    },

    "discussion_rows": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["row_id", "at", "speaker_id", "kind", "content"],
        "properties": {
          "row_id": { "type": "string" },
          "at": { "type": "string", "description": "RFC3339 timestamp." },
          "speaker_id": { "type": "string" },
          "kind": { "type": "string", "enum": ["question", "claim", "evidence", "proposal", "bridge", "decision", "note"] },
          "content": { "type": "string" },

          "criteria_touched": { "type": "array", "items": { "type": "string" }, "description": "Array of criteria IDs." },
          "option_refs": { "type": "array", "items": { "type": "string" }, "description": "Array of option IDs referenced." },

          "decision_ref": { "type": "string" },
          "action_ref": { "type": "string" },

          "tone_tag": { "type": "string", "description": "Optional: calm, tense, playful, etc. Not for policing, just context." }
        },
        "additionalProperties": false
      }
    },

    "decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["decision_id", "at", "title", "status"],
        "properties": {
          "decision_id": { "type": "string" },
          "at": { "type": "string", "description": "RFC3339 timestamp." },
          "title": { "type": "string" },
          "status": { "type": "string", "enum": ["made", "deferred", "reversed"] },
          "summary": { "type": "string" },
          "chosen_option_id": { "type": "string" },
          "rationale": { "type": "string" },
          "bridge_used": { "type": "string", "description": "What compromise/trial/fallback enabled agreement." }
        },
        "additionalProperties": false
      }
    },

    "action_items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["action_id", "title", "owner_id", "status"],
        "properties": {
          "action_id": { "type": "string" },
          "title": { "type": "string" },
          "owner_id": { "type": "string" },
          "due_at": { "type": "string", "description": "RFC3339 timestamp." },
          "status": { "type": "string", "enum": ["open", "in_progress", "done", "dropped"] },
          "notes": { "type": "string" }
        },
        "additionalProperties": false
      }
    },

    "calculator_results": {
      "type": "object",
      "properties": {
        "model": { "type": "string", "description": "Name/version of the scoring model." },
        "ranked_options": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["option_id", "score"],
            "properties": {
              "option_id": { "type": "string" },
              "score": { "type": "number" },
              "breakdown": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": ["criteria_id", "contribution"],
                  "properties": {
                    "criteria_id": { "type": "string" },
                    "contribution": { "type": "number" },
                    "raw": {},
                    "normalized": { "type": "number" }
                  },
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

---

## 3) Table comprehension rules (how renderers should behave)

A discussion table renderer should:
- Show `discussion_rows` in time order.
- Make `criteria_touched` and `option_refs` clickable/traceable.
- Display decision rows (`kind="decision"`) and link to `decisions[]`.
- Highlight bridges (`kind="bridge"`) to show how agreement was reached.

---

## 4) Minimal example (starter JSON document)

```/dev/null/great_hall_minimal_example.json#L1-63
{
  "meta": { "doc_id": "gh-001", "created_at": "2025-01-01T00:00:00Z", "version": "1.0.0", "source": "manual" },
  "session": {
    "session_id": "s-001",
    "title": "Example: pick an approach",
    "vibe": "calm_direct",
    "participants": [{ "id": "p1", "display_name": "Facilitator", "role": "facilitator" }]
  },
  "criteria_set": {
    "criteria": [
      { "id": "c_speed", "name": "Speed", "type": "number", "weight": 1.0, "polarity": "higher_is_better", "range": { "min": 0, "max": 10 } }
    ]
  },
  "settings": [{ "key": "decision_reversibility", "value": "reversible", "scope": "session", "rationale": "Prefer experiments first." }],
  "options": [{ "id": "o_a", "label": "Option A" }, { "id": "o_b", "label": "Option B" }],
  "discussion_rows": [
    { "row_id": "r1", "at": "2025-01-01T00:00:01Z", "speaker_id": "p1", "kind": "proposal", "content": "Try A first.", "option_refs": ["o_a"], "criteria_touched": ["c_speed"] },
    { "row_id": "r2", "at": "2025-01-01T00:00:02Z", "speaker_id": "p1", "kind": "bridge", "content": "If A doesn’t work by Friday, switch to B.", "option_refs": ["o_a", "o_b"] }
  ],
  "decisions": [],
  "action_items": []
}
```

---

## 5) Notes for C implementation
- Keep the schema in JSON; validate with a library if needed.
- Use stable string IDs; avoid implicit array-index identity.
- Prefer RFC3339 timestamps for `*_at` fields.

End of policy.