---
name: grid-exhibit-governance
description: Rules for managing museum-style research exhibits within the Grid workspace
version: 1.0.0
author: Grid Research Team
scope:
  - light_of_the_seven/**/visualizations/**
  - schemas/exhibit_manifest_schema.json
tags:
  - governance
  - exhibits
  - canon-policy
  - organization
---

# Grid Exhibit Governance Rules

> **"Words are our most inexhaustible source of magic. Therefore, cite them carefully."**

These rules govern the creation, maintenance, and integration of research exhibits within the Grid workspace.

---

## Rule 1: Exhibit Structure Requirements

Every exhibit MUST have:

```
<exhibit_root>/
├── exhibit.json          # Manifest (required)
├── README.md             # Entry point documentation
├── CANON_POLICY.md       # If strict canon enforcement
├── SOURCES.md            # Citation tracking (if canon)
└── <content>/            # Organized by type
```

### Manifest Validation

- All exhibits MUST have a valid `exhibit.json` conforming to `schemas/exhibit_manifest_schema.json`
- Run validation: `python -m jsonschema -i exhibit.json schemas/exhibit_manifest_schema.json`

---

## Rule 2: Canon vs Tooling Separation

### Canon Layer (Docs) — 🏛️

Files in the canon layer:
- MUST cite sources using the established format
- MUST NOT contain speculation without explicit labeling
- MUST NOT be modified by automated tooling
- SHOULD use the `📜` prefix in workspace folder names

### Tooling Layer (Code) — 🪄

Files in the tooling layer:
- MUST include non-canonical disclaimer in headers:
  ```python
  """NON-CANONICAL: This module is a creative/educational tool.
  It does not represent official [domain] lore."""
  ```
- MUST NOT write to canon layer files
- MAY extrapolate, simulate, and visualize freely
- SHOULD use the `🪄` or `🧪` prefix in workspace folder names

---

## Rule 3: Workspace Integration

When adding an exhibit to `grid.code-workspace`:

### Folder Naming Convention

```json
{
  "path": "path/to/exhibit",
  "name": "   ├─ 🏛️ ExhibitName · Category (Type)"
}
```

Categories:
- `Exhibit (Root)` — Main entry point
- `Canon` — Documentation/lore
- `Tools` — Non-canon code
- `Tests` — Verification
- `Prototypes` — Experimental

### Position in Workspace

Exhibits belong in "THE OPEN DRAWER" section, after `.claude` context:

```
╰──┤ 𝗧𝗛𝗘 𝗢𝗣𝗘𝗡 𝗗𝗥𝗔𝗪𝗘𝗥 ├── (all is given)
   ├─ 🪞 .claude · AI Context
   ├─ 🏛️ [Exhibit] · Exhibit (Root)
   ├─ 📜 [Exhibit] · [Section] (Canon)
   ├─ 🪄 [Exhibit] · [Section] (Tools)
   ...
```

---

## Rule 4: Sensory Layer Integration

Exhibits connecting to Grid's Sound/Vision layers MUST:

1. **Define mappings** in `exhibit.json` under `grid_integration.mappings`
2. **Use bridge modules** (e.g., `grid_bridge.py`) for translation
3. **Document entity→sensory mappings** explicitly:
   - Emotion/state → pitch, loudness, timbre
   - Relationships → edge style, weight, color
   - Confidence → glow, saturation, uncertainty noise

### Integration Contract

```json
{
  "grid_integration": {
    "enabled": true,
    "mappings": {
      "<domain>_to_polarity": { ... },
      "<domain>_to_sensory": { ... }
    },
    "sandbox_dataset": {
      "enabled": true,
      "entities": "...",
      "relationships": "...",
      "use_cases": [...]
    }
  }
}
```

---

## Rule 5: Launch Configuration

Exhibits with executable components SHOULD have:

### VS Code Launch Entries

```json
{
  "name": "🏛️ [Exhibit] Demo",
  "type": "debugpy",
  "request": "launch",
  "module": "light_of_the_seven.full_datakit.visualizations.[exhibit].[module]",
  "console": "integratedTerminal"
}
```

### Tasks

```json
{
  "label": "█ [EXHIBIT]",
  "type": "shell",
  "command": "python -m light_of_the_seven.full_datakit.visualizations.[exhibit].[module]"
}
```

---

## Rule 6: Testing Requirements

### Canon Validation Tests

- Citation format compliance
- Source reference validity
- No orphaned claims

### Tooling Tests

- Unit tests for all public functions
- Integration tests for Grid bridge mappings
- Output schema validation

### Test Location

```
tests/
└── exhibits/
    └── test_[exhibit_id].py
```

Or within the exhibit:
```
<exhibit_root>/
└── test_*.py
```

---

## Rule 7: Documentation Standards

### README.md Requirements

1. Purpose statement
2. Directory structure overview
3. Quick start commands
4. Canon policy summary (if applicable)
5. Integration points with Grid

### Code Documentation

- All public functions: docstrings with Args/Returns
- All classes: class-level docstring with purpose
- All modules: module-level docstring with NON-CANONICAL notice if tooling

---

## Rule 8: Version Control

### Commits Touching Exhibits

- Prefix: `[exhibit:id]` (e.g., `[exhibit:hogwarts] Add Patronus presets`)
- Separate canon changes from tooling changes
- Never mix exhibit changes with core Grid changes

### Protected Paths

Canon files should be reviewed carefully:
- `**/SOURCES.md`
- `**/CANON_POLICY.md`
- Files listed under `canon_docs` in `exhibit.json`

---

## Rule 9: Exhibit Lifecycle

### Creation Checklist

- [ ] Create exhibit directory structure
- [ ] Add `exhibit.json` manifest
- [ ] Add `README.md` with quick start
- [ ] Add workspace folder entries
- [ ] Add launch/task configurations
- [ ] Add basic tests
- [ ] Document in `.claude` context if AI-relevant

### Archival Checklist

- [ ] Set `metadata.status: "archived"` in manifest
- [ ] Add deprecation notice to README
- [ ] Remove from active workspace sections
- [ ] Preserve in `light_of_the_seven/archived/`

---

## Rule 10: Cross-Exhibit References

When one exhibit references another:

1. Use relative paths where possible
2. Document dependency in manifest:
   ```json
   {
     "metadata": {
       "related_exhibits": ["sound_layer", "vision_layer"]
     }
   }
   ```
3. Avoid circular dependencies
4. Test integration points explicitly

---

## Enforcement

These rules are enforced through:

1. **Manual Review** — PR reviews check exhibit structure
2. **Schema Validation** — `exhibit.json` validated against schema
3. **CI Checks** — Test suite includes exhibit validation
4. **Windsurf Workflows** — `/grid-organize` respects exhibit boundaries

---

## Examples

### Good: Properly Structured Exhibit

```
Hogwarts/
├── exhibit.json           ✓ Valid manifest
├── README.md              ✓ Entry documentation
├── CANON_POLICY.md        ✓ Governance defined
├── SOURCES.md             ✓ Citations tracked
├── HOGWARTS.md            ✓ Canon content
├── ancient_magic_lib.py   ✓ NON-CANONICAL header
├── grid_bridge.py         ✓ Integration bridge
└── test_*.py              ✓ Tests present
```

### Bad: Violations

```
MyExhibit/
├── data.json              ✗ No exhibit.json
├── cool_stuff.py          ✗ No NON-CANONICAL header
├── lore.md                ✗ No citations
└── (no tests)             ✗ No verification
```

---

*These rules ensure exhibits remain maintainable, trustworthy, and properly integrated with the Grid ecosystem.*