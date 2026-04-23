# Hogwarts Logbook (Canon-Only Reference)

This repository contains code utilities and study notes. This file is the **canon-only** logbook for Hogwarts-related facts.

## Canon Policy (Strict)

**Allowed sources**
- **Primary canon:** the seven *Harry Potter* novels.
- **Secondary canon (optional):** officially published Wizarding World / J.K. Rowling background writings **only when explicitly presented as canonical background**.

**Not allowed in this document**
- Fan theories, roleplay, “expanded universe” inventions, or third‑party storytelling/interpretation.
- Any invented spell mechanics, “temporal magic systems,” or new magical effects not stated in canon.
- Any framing that implies code artifacts are canon.

If a claim cannot be pointed to a canon source above, it must not appear here.

---

## What This Repo Contains (Separation of Concerns)

### Canon-only documents (lore reference)
- Documents intended to summarize canon facts must:
  - state only what canon supports,
  - avoid speculation,
  - include citations (see below).

### Code utilities (non-canon)
This repo includes Python tooling (e.g., CLI helpers) that **simulate** or **format** lore-like outputs. These are **non-canon utilities** for visualization and study workflows.  
They may reference canon names (e.g., “Snape”, “Patronus”) but they do **not** represent official magical theory.

> In short: **code = tooling**, not lore.

---

## Hogwarts (Canon Anchors)

The following are high-level canon anchors you can safely build on (details should live in focused documents with citations):

- Hogwarts School of Witchcraft and Wizardry is a magical school in Scotland.
- Hogwarts was founded by:
  - Godric Gryffindor
  - Helga Hufflepuff
  - Rowena Ravenclaw
  - Salazar Slytherin
- Hogwarts is divided into four houses:
  - Gryffindor, Hufflepuff, Ravenclaw, Slytherin
- Hogwarts has a Headmaster/Headmistress, professors, and a student body sorted into houses.
- The Sorting Hat is used to sort students.
- The Chamber of Secrets is a hidden chamber associated with Salazar Slytherin and a Basilisk (*Harry Potter and the Chamber of Secrets*).
- The Battle of Hogwarts occurs during the Second Wizarding War (*Harry Potter and the Deathly Hallows*).

This section is intentionally minimal. Add specifics only with citations.

---

## Canon Citation Standard (Required)

When you add or change any canon claim in this repo’s lore docs, include a short citation block near the claim:

- **Book:** *(title)*
- **Context:** where it appears (chapter name/number if you track it)
- **Claim:** the canon fact being recorded (keep it narrow)

Example (format only):
- **Book:** *Harry Potter and the Chamber of Secrets*
- **Context:** Chamber legend and confrontation
- **Claim:** “Harry kills the Basilisk with the Sword of Gryffindor.”

---

## Non-Canon Utility Note: `parseltongue_cli.py`

This repo contains a small CLI script intended as a **formatting/visualization tool**. Any constructs like “Temporal Patronus” are **non-canon** and must not be treated as official magical theory. If the CLI outputs narrative text, it should be interpreted as a generated artifact for testing/visualization only.

If you want canon-accurate Patronus documentation, it belongs in a separate canon-only file that cites the novels’ Patronus scenes and explains only what canon states.

---

## TODO (Canon-Only Next Steps)

1. Create `SOURCES.md` listing:
   - the seven novels (primary canon),
   - any secondary canon sources you choose to treat as canonical background.
2. Ensure each lore document includes citations for every non-trivial claim.
3. Keep all tool-generated narrative output out of canon-only docs.
4. If you want to preserve non-canon explorations, place them under a clearly labeled non-canon area (e.g., `NonCanon/`) so canon-only materials remain clean.