# Hogwarts Exhibit: Canon Policy

> **"The truth is a beautiful and terrible thing, and should therefore be treated with great caution."**
> — Albus Dumbledore

---

## Purpose

This document establishes the **strict governance policy** for all lore, content, and references within the Hogwarts Exhibit. The goal is to maintain **scholarly integrity** while enabling creative tooling that does not contaminate canonical sources.

---

## The Two Layers

### Layer 1: Canon (Docs) — 🏛️ Sacred Ground

These materials contain **only verified, source-cited Harry Potter lore**.

| Folder/File | Status | Source Requirement |
|-------------|--------|-------------------|
| `HOGWARTS.md` | Canon | Must cite book/film/Pottermore |
| `founders_archive.md` | Canon | Founder lore only from original 7 books |
| `Founders/*/README.md` | Canon | Per-founder canonical facts |
| `Salazar Slytherin/salazar_slytherin.md` | Canon | Chamber of Secrets, Deathly Hallows refs |
| `SSSEVERUS SNAPE/*.md` | Canon | Books 1-7, explicit citations required |
| `hogwarts_lore.json` | Canon | Structured data, all fields sourced |

**Rules for Canon Layer:**
1. **NO speculation** — Only facts established in source material
2. **NO fan theories** — Even popular ones are non-canonical
3. **NO cross-universe mixing** — No Fantastic Beasts unless explicitly HP-referenced
4. **Citation required** — Every claim must reference: `[Book X, Chapter Y]` or `[Film X, Scene]`
5. **Disputed facts** — If sources conflict, note the discrepancy; do not resolve it

### Layer 2: Tooling (Code) — 🪄 The Workshop

These materials are **explicitly non-canonical** creative/technical utilities.

| Folder/File | Status | Purpose |
|-------------|--------|---------|
| `ancient_magic_lib.py` | Non-Canon | Emotion→Patronus transformation demo |
| `hogwarts_toolkit.py` | Non-Canon | CLI utilities for exhibit navigation |
| `hogwarts_cli.py` | Non-Canon | Command-line interface wrapper |
| `parseltongue_cli.py` | Non-Canon | Temporal Patronus simulation |
| `spellbook_api.py` | Non-Canon | API abstraction for lore queries |
| `great_hall/` | Non-Canon | Multi-agent discussion simulation |
| `prototypes/` | Non-Canon | Experimental visualization tools |
| `output-0.3.0-/` | Non-Canon | Generated visualization artifacts |

**Rules for Tooling Layer:**
1. **Clearly labeled** — All non-canon code must have header comments stating `NON-CANONICAL`
2. **No lore modification** — Tools read from canon, never write to it
3. **Creative freedom** — Tools may extrapolate, simulate, visualize
4. **Educational purpose** — Tools exist to explore, not to establish facts
5. **Isolation** — No tool output should be cited as canonical evidence

---

## Canon Source Hierarchy

When evaluating the canonicity of information, use this precedence:

```
┌─────────────────────────────────────────────────┐
│  1. J.K. Rowling's 7 Harry Potter novels        │  ← HIGHEST AUTHORITY
├─────────────────────────────────────────────────┤
│  2. Pottermore / Wizarding World (original)     │
├─────────────────────────────────────────────────┤
│  3. Harry Potter films (where books are silent) │
├─────────────────────────────────────────────────┤
│  4. Supplementary texts (Beedle the Bard, etc.) │
├─────────────────────────────────────────────────┤
│  5. Interviews / Tweets (with caution)          │  ← LOWEST, often disputed
└─────────────────────────────────────────────────┘
```

**Fantastic Beasts**, **Cursed Child**, and **video games** are considered **extended universe** and should be explicitly marked if referenced.

---

## Citation Format

All canonical claims must include a source citation:

```markdown
Severus Snape's Patronus was a silver doe, identical to Lily Potter's,
because his love for her never wavered.
[Deathly Hallows, Chapter 33: "The Prince's Tale"]
```

For JSON/structured data:
```json
{
  "fact": "Snape's Patronus is a doe",
  "source": "Deathly Hallows Ch.33",
  "confidence": "canonical"
}
```

---

## Contribution Guidelines

### Adding Canon Content

1. **Verify** the fact exists in a canonical source
2. **Cite** the source using the format above
3. **Cross-check** against existing exhibit docs for consistency
4. **Flag** any conflicts with existing entries
5. **Submit** with clear changelog note

### Adding Tooling

1. **Add header** marking the file as non-canonical:
   ```python
   """NON-CANONICAL: This module is a creative/educational tool.
   It does not represent official Harry Potter lore."""
   ```
2. **Document** what canonical sources the tool references
3. **Test** that the tool does not modify canon files
4. **Submit** with demonstration of functionality

---

## Violations & Corrections

If a canonical violation is discovered:

1. **Document** the violation in an issue/PR
2. **Cite** the correct canonical source
3. **Propose** a correction or removal
4. **Review** related files for similar issues

Common violations:
- Fan theory presented as fact
- Film-only detail contradicting book
- Unattributed speculation
- Mixing Fantastic Beasts lore without labeling

---

## Why This Matters

The Hogwarts Exhibit serves as a **demonstration of disciplined knowledge management**:

- **Canon Layer** = Ground truth, evidence-grounded, immutable
- **Tooling Layer** = Exploration, simulation, mutable

This mirrors the Grid's core philosophy:
> **Information has structure. Structure requires governance. Governance enables trust.**

The exhibit proves that creative exploration and scholarly rigor can coexist—
when their boundaries are clearly defined and enforced.

---

## Exhibit Manifest Reference

This policy is enforced by the exhibit manifest:
- `exhibit.json` → Declares canon/tooling boundaries
- Workspace folders → Visual separation in IDE
- File headers → Self-documenting compliance

---

*"It does not do to dwell on dreams and forget to live."*
*But it also does not do to dwell on dreams and call them facts.*

— Hogwarts Exhibit Governance, v1.0