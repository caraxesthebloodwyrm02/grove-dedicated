# Grid Sensory Layers Rules

> Rules governing the Sound Layer, Vision Layer, and Exhibit integration system.

---

## Overview

Grid's sensory layers provide multi-modal representations of information dynamics:
- **Sound Layer**: Auditory sonification of data (pitch, loudness, timbre, rhythm)
- **Vision Layer**: Graph-based visualization (nodes, edges, flows)
- **Exhibits**: Curated research wings with canon/tooling separation

---

## Schema References

| Layer | Schema Path | Description |
|-------|-------------|-------------|
| Sound | `schemas/sound_layer_schema.json` | Audio parameter mappings |
| Vision | `schemas/vision_layer_schema.json` | Graph visualization primitives |
| Exhibit | `schemas/exhibit_manifest_schema.json` | Museum wing definitions |

---

## Sound Layer Rules

### SL-001: Perceptual Normalization
All sound parameters MUST use perceptually-normalized scales:
- Pitch: Logarithmic (semitones/octaves)
- Loudness: Decibels (dB) with -24 to -3 dB range
- Timbre: 0.0-1.0 normalized brightness/roughness/warmth

### SL-002: Uncertainty Signaling
Low-confidence data MUST be represented with:
- Increased noise/roughness
- Reduced pitch clarity
- Lower loudness

### SL-003: Rate Limiting
Sound updates MUST be rate-limited to prevent auditory fatigue:
- Minimum 50ms between state changes
- Smooth transitions for continuous parameters

---

## Vision Layer Rules

### VL-001: Graph Consistency
All vision outputs MUST conform to the graph schema:
- Nodes: id, label, type, visual properties
- Edges: source, target, relationship, visual properties
- Layout: force-directed, tree, dag, or custom

### VL-002: Color Semantics
Colors MUST follow semantic conventions:
- Supportive polarity: Green (#4CAF50)
- Neutral polarity: Gray (#9E9E9E)
- Adversarial polarity: Red (#F44336)
- Temporal events: Purple (#6A5ACD)
- Transformations: Gold (#FFD700)

### VL-003: Node Sizing
Node size MUST reflect importance/intensity:
- Range: 10-100 (normalized)
- Intensity scaling: linear
- Glow for high-confidence nodes (>0.5 intensity)

---

## Exhibit Rules

### EX-001: Canon Policy Enforcement
Every exhibit MUST declare a `canon_policy` with:
- `level`: strict | moderate | loose
- `sources_required`: boolean
- `allow_speculation`: boolean

### EX-002: Layer Separation
Exhibits MUST maintain strict separation:
- **Canon (Docs)**: Verified, source-cited documentation
- **Tools (Code)**: Non-canon, clearly labeled utilities
- **Tests**: Verification layer

### EX-003: Manifest Required
Every exhibit MUST have an `exhibit.json` manifest containing:
- `exhibit_id`: Unique identifier
- `version`: Semantic version
- `canon_policy`: Policy object
- `paths`: Root and section paths
- `entrypoints`: CLI/API/launcher definitions

### EX-004: Non-Canon Labeling
All non-canon code files MUST include a header comment:
```python
"""NON-CANONICAL: This module is a creative/educational tool.
It does not represent official [domain] lore."""
```

### EX-005: Source Citations
Canon documents MUST cite sources using the format:
```markdown
[Source, Chapter/Section "Title"]
```

---

## Integration Rules

### INT-001: Bridge Modules
Exhibit-to-Grid integration MUST use a dedicated bridge module:
- Located at: `<exhibit_root>/grid_bridge.py`
- Exports: `*_to_sound()`, `*_to_vision()`, `create_full_sensory_state()`

### INT-002: Sandbox Datasets
Exhibits MAY provide sandbox datasets for Grid testing:
- Closed-world, reproducible data
- Documented entity types and relationships
- Use cases for each sensory layer

### INT-003: Workspace Shelves
Exhibits MUST define workspace folder entries with semantic labels:
- Canon folders: 📜 prefix
- Tool folders: 🪄 prefix
- Test folders: 🧪 prefix
- Root folder: 🏛️ prefix

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Schema | `*_schema.json` | `sound_layer_schema.json` |
| Bridge | `*_bridge.py` | `grid_bridge.py` |
| Manifest | `exhibit.json` | `exhibit.json` |
| Canon Policy | `CANON_POLICY.md` | `CANON_POLICY.md` |
| Sources | `SOURCES.md` | `SOURCES.md` |

---

## Validation Checklist

When creating or modifying sensory layer integrations:

- [ ] Schema validation passes for all JSON outputs
- [ ] Sound parameters within defined ranges
- [ ] Vision nodes have required fields (id, label, type)
- [ ] Exhibit manifest conforms to schema
- [ ] Canon/tooling separation maintained
- [ ] Source citations present for canon claims
- [ ] Bridge module exports documented functions
- [ ] Workspace shelves use correct prefix icons

---

## Related Documentation

- `docs/VISION_LAYER.md` - Vision layer architecture
- `docs/SOUND_LAYER.md` - Sound layer architecture (if exists)
- `.claude/SYSTEM_CONTEXT.md` - AI context overview
- `AGENTS.md` - Agent operating protocol