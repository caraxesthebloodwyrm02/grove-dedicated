---
name: grid-canon-policy
description: Rules governing canonical content, exhibit management, and documentation integrity
version: 1.0.0
author: Grid Research Team
scope:
  - light_of_the_seven/**
  - docs/**
  - schemas/**
priority: high
---

# Grid Canon Policy Rules

> **"Information has structure. Structure requires governance. Governance enables trust."**

These rules govern how AI assistants interact with canonical documentation, exhibit content, and research materials within the Grid project.

---

## Rule 1: Two-Layer Separation

All content in research exhibits (e.g., Hogwarts, Sound Layer, Vision Layer) follows a strict two-layer model:

### Canon Layer (🏛️ Sacred Ground)
- **Files**: `*.md` docs, `*_lore.json`, `SOURCES.md`, `founders_archive.md`
- **Policy**: READ-ONLY unless explicitly instructed to update with citations
- **Modifications require**:
  - Source citation in approved format
  - Cross-reference with `SOURCES.md`
  - No speculation or fan theories

### Tooling Layer (🪄 Workshop)
- **Files**: `*.py`, `*_cli.py`, `*_api.py`, `*_toolkit.py`, `test_*.py`
- **Policy**: MUTABLE for improvements, demos, and experiments
- **Requirements**:
  - Header comment stating `NON-CANONICAL` for exhibit code
  - Clear separation from lore documents
  - No modifications to canon files from tooling logic

---

## Rule 2: Citation Discipline

When adding or modifying canonical claims:

### Required Format (Markdown)
```markdown
[Source Abbreviation, Chapter/Section "Title"]
```

### Required Format (JSON)
```json
{
  "claim": "...",
  "source": {"book": "...", "chapter": "...", "title": "..."},
  "confidence": "canonical"
}
```

### Prohibited Actions
- Adding claims without citations
- Citing extended universe without explicit labels
- Presenting speculation as fact
- Mixing canon and non-canon in same document section

---

## Rule 3: Exhibit Manifest Compliance

All exhibits must have an `exhibit.json` manifest defining:

| Field | Required | Purpose |
|-------|----------|---------|
| `exhibit_id` | ✓ | Unique identifier |
| `version` | ✓ | Semantic version |
| `canon_policy` | ✓ | Strictness level and rules |
| `paths` | ✓ | Root and section paths |
| `entrypoints` | | CLI, API, launcher configs |
| `grid_integration` | | Sound/Vision layer mappings |

### Validation
Before modifying exhibit structure:
1. Check `exhibit.json` exists
2. Verify change aligns with `canon_policy.strictness`
3. Update manifest if paths change

---

## Rule 4: Schema Alignment

Exhibit integrations must align with Grid schemas:

### Sound Layer (`schemas/sound_layer_schema.json`)
- Pitch mappings use Hz values in range [110, 880]
- Loudness in dB range [-24, -3]
- Timbre parameters normalized [0, 1]

### Vision Layer (`schemas/vision_layer_schema.json`)
- Nodes require: `id`, `label`, `type`
- Edges require: `source`, `target`, `relationship`
- Layouts: `force-directed`, `hierarchical`, `radial`

### Exhibit Manifest (`schemas/exhibit_manifest_schema.json`)
- All exhibits must validate against this schema
- Run validation before commits affecting exhibit structure

---

## Rule 5: Workspace Shelf Naming

When adding exhibit shelves to `grid.code-workspace`:

### Main Body (The Figure)
```
║ [emoji] [Component] · The [Metaphor]
```

### Open Drawer (All Is Given)
```
   ├─ [emoji] [Name] · [Category] ([Role])
```

### Exhibit Entries
| Icon | Meaning |
|------|---------|
| 🏛️ | Exhibit root or museum space |
| 📜 | Canon documentation |
| 🪄 | Non-canon tooling |
| 🧪 | Tests or experiments |
| 🎭 | Visualizations/demos |

---

## Rule 6: Documentation Updates

### When to Update SOURCES.md
- Adding new canonical claims
- Discovering citation errors
- Adding new source categories

### When to Update CANON_POLICY.md
- Changing exhibit strictness level
- Adding new contribution guidelines
- Clarifying edge cases

### When to Update exhibit.json
- Adding/removing paths
- Modifying integration mappings
- Changing entrypoints

---

## Rule 7: AI Interaction Guidelines

When working with exhibit content:

### DO
- Verify claims against `SOURCES.md` before stating facts
- Mark tooling code with non-canonical headers
- Suggest citations when adding lore content
- Respect the two-layer separation
- Update manifests when changing structure

### DO NOT
- Present non-canonical tooling behavior as lore fact
- Merge canon and tooling in same file
- Add uncited claims to canon documents
- Remove citations from existing claims
- Modify `SOURCES.md` without verification

---

## Rule 8: Integration Bridges

When creating bridges between exhibits and Grid core:

### Required Documentation
- Mapping rationale (why this emotion → this sound?)
- Source entity types and target parameters
- Confidence/uncertainty handling

### Required Testing
- Unit tests for mapping functions
- Integration tests for sensory output
- Validation against schema contracts

### Naming Convention
- Bridge modules: `{exhibit}_bridge.py`
- Bridge functions: `{source}_to_{target}()`

---

## Enforcement

These rules are enforced through:

1. **Pre-commit hooks** - Validate exhibit.json schema
2. **CI checks** - Verify SOURCES.md citations
3. **Code review** - Human verification of canon claims
4. **AI guardrails** - This rules file

---

## Related Files

- `light_of_the_seven/full_datakit/visualizations/Hogwarts/CANON_POLICY.md`
- `light_of_the_seven/full_datakit/visualizations/Hogwarts/SOURCES.md`
- `light_of_the_seven/full_datakit/visualizations/Hogwarts/exhibit.json`
- `schemas/exhibit_manifest_schema.json`
- `AGENTS.md`

---

*"Therefore, cite them carefully."*