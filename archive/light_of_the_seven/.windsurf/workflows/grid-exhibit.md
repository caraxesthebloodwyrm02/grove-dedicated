---
name: grid-exhibit
description: Manage museum-style research exhibits within the Grid workspace
version: 1.0.0
author: Grid Research Team
triggers:
  - manual
  - /grid-exhibit
tags:
  - exhibits
  - governance
  - canon-policy
  - organization
---

# Grid Exhibit Management Workflow

> **Purpose**: Create, validate, and maintain research exhibits with proper canon/tooling separation, manifest compliance, and sensory layer integration.

## Usage

Type `/grid-exhibit` in Cascade to start this workflow with one of the following commands:

| Command | Description |
|---------|-------------|
| `/grid-exhibit create <name>` | Create a new exhibit structure |
| `/grid-exhibit validate <path>` | Validate exhibit manifest and structure |
| `/grid-exhibit status` | Show all exhibits and their health status |
| `/grid-exhibit integrate <exhibit>` | Generate Grid sensory layer bridge |
| `/grid-exhibit workspace` | Update workspace folder entries |

---

## Phase 1: Discovery — Find Existing Exhibits

```bash
# Find all exhibit manifests
find . -name "exhibit.json" -type f 2>/dev/null

# Check for exhibits without manifests (potential issues)
find . -type d -name "visualizations" -exec sh -c 'for d in "$1"/*/; do [ -f "$d/exhibit.json" ] || echo "Missing manifest: $d"; done' _ {} \;

# List exhibit IDs and versions
find . -name "exhibit.json" -exec sh -c 'echo "=== $1 ===" && jq -r ".exhibit_id + \" v\" + .version" "$1"' _ {} \;
```

---

## Phase 2: Create New Exhibit

### Step 1: Generate Directory Structure

```bash
# Set exhibit name (lowercase, hyphenated)
EXHIBIT_NAME="my-exhibit"
EXHIBIT_ROOT="light_of_the_seven/full_datakit/visualizations/${EXHIBIT_NAME}"

# Create structure
mkdir -p "${EXHIBIT_ROOT}"
mkdir -p "${EXHIBIT_ROOT}/docs"
mkdir -p "${EXHIBIT_ROOT}/tools"
mkdir -p "${EXHIBIT_ROOT}/tests"
```

### Step 2: Generate exhibit.json Manifest

```python
import json
from datetime import date

def create_exhibit_manifest(exhibit_id: str, title: str, description: str = "") -> dict:
    """Generate a compliant exhibit manifest."""
    return {
        "$schema": "https://grid.local/schemas/exhibit_manifest_schema.json",
        "exhibit_id": exhibit_id,
        "version": "1.0.0",
        "title": title,
        "description": description,
        "icon": "🏛️",
        "canon_policy": {
            "level": "moderate",
            "description": "Curated content with annotations",
            "sources_required": True,
            "allow_speculation": False,
            "citation_format": "markdown_footnotes"
        },
        "paths": {
            "root": f"light_of_the_seven/full_datakit/visualizations/{exhibit_id}",
            "canon_docs": [
                {"path": "docs/", "label": "Documentation", "description": "Canon content"}
            ],
            "tools": [
                {"path": "tools/", "label": "Tooling", "description": "Non-canon utilities"}
            ],
            "tests": [
                {"path": "tests/", "framework": "pytest"}
            ]
        },
        "entrypoints": {
            "cli": [],
            "api": [],
            "launcher": {
                "script": None,
                "demo_mode": True,
                "requires": []
            }
        },
        "sensory_integration": {
            "sound_layer": {"enabled": False, "mappings": []},
            "vision_layer": {"enabled": False, "graph_type": "directed", "node_mappings": [], "edge_mappings": []}
        },
        "metadata": {
            "created": str(date.today()),
            "updated": str(date.today()),
            "maintainers": [],
            "tags": [],
            "status": "draft",
            "related_exhibits": []
        }
    }

# Example usage
manifest = create_exhibit_manifest(
    exhibit_id="my-exhibit",
    title="My Research Exhibit",
    description="A new research wing exploring..."
)
print(json.dumps(manifest, indent=2))
```

### Step 3: Generate Core Files

```bash
# README.md template
cat > "${EXHIBIT_ROOT}/README.md" << 'EOF'
# [Exhibit Title]

> [Brief description of the exhibit's purpose]

## Quick Start

```bash
# View exhibit structure
ls -la

# Run demo (if available)
python -m [module_path]
```

## Structure

- `docs/` — Canon documentation (cited sources)
- `tools/` — Non-canon utilities and demos
- `tests/` — Verification and validation

## Canon Policy

This exhibit follows a **[strict/moderate/loose]** canon policy.
See `CANON_POLICY.md` for details.

## Integration

[Describe how this exhibit integrates with Grid's sensory layers]
EOF

# CANON_POLICY.md template (if needed)
cat > "${EXHIBIT_ROOT}/CANON_POLICY.md" << 'EOF'
# Canon Policy

## Overview

This exhibit maintains [strict/moderate/loose] canon discipline.

## Rules

1. All claims must be cited
2. Tooling is clearly labeled non-canonical
3. Speculation must be explicitly marked

## Citation Format

```markdown
[Source, Chapter/Section "Title"]
```

## Layers

- **Canon (Docs)**: `docs/` — Verified content only
- **Tooling (Code)**: `tools/` — Non-canonical utilities
EOF

# SOURCES.md template
cat > "${EXHIBIT_ROOT}/SOURCES.md" << 'EOF'
# Sources

## Primary Sources

| Abbreviation | Title | Notes |
|--------------|-------|-------|
| | | |

## Citations Used

| Claim | Source | Citation |
|-------|--------|----------|
| | | |

## Updates Log

| Date | Change | Contributor |
|------|--------|-------------|
| | Initial creation | |
EOF
```

---

## Phase 3: Validate Exhibit

### Step 1: Schema Validation

```bash
# Validate exhibit.json against schema
python -c "
import json
import sys
from pathlib import Path

# Load exhibit manifest
exhibit_path = Path('$EXHIBIT_ROOT/exhibit.json')
if not exhibit_path.exists():
    print('ERROR: exhibit.json not found')
    sys.exit(1)

with open(exhibit_path) as f:
    manifest = json.load(f)

# Required fields check
required = ['exhibit_id', 'version', 'canon_policy', 'paths']
missing = [f for f in required if f not in manifest]
if missing:
    print(f'ERROR: Missing required fields: {missing}')
    sys.exit(1)

# Canon policy check
canon = manifest.get('canon_policy', {})
if 'level' not in canon:
    print('WARNING: canon_policy.level not specified')

print('✓ Manifest structure valid')
"
```

### Step 2: Structure Validation

```bash
# Check required files exist
REQUIRED_FILES="README.md"
for file in $REQUIRED_FILES; do
    if [ -f "${EXHIBIT_ROOT}/${file}" ]; then
        echo "✓ ${file} exists"
    else
        echo "✗ ${file} MISSING"
    fi
done

# Check for non-canonical headers in Python files
find "${EXHIBIT_ROOT}" -name "*.py" -exec grep -L "NON-CANONICAL" {} \; | while read f; do
    echo "WARNING: $f may need NON-CANONICAL header"
done
```

### Step 3: Citation Validation (for strict canon)

```python
import re
from pathlib import Path

def validate_citations(docs_path: str) -> list[str]:
    """Check that all claims have citations."""
    issues = []
    citation_pattern = r'\[.+?,\s*(Ch\.|Chapter|Section).+?\]'
    
    for md_file in Path(docs_path).glob("**/*.md"):
        content = md_file.read_text()
        # Look for factual statements without citations
        # (This is a simplified heuristic)
        paragraphs = content.split('\n\n')
        for i, para in enumerate(paragraphs):
            if len(para) > 100 and not re.search(citation_pattern, para):
                if not para.startswith('#') and not para.startswith('```'):
                    issues.append(f"{md_file}:para{i+1} - May need citation")
    
    return issues

# Run validation
issues = validate_citations("docs/")
for issue in issues:
    print(f"WARNING: {issue}")
```

---

## Phase 4: Integrate with Grid Sensory Layers

### Step 1: Generate Bridge Module

```python
# grid_bridge.py template
BRIDGE_TEMPLATE = '''"""Grid Bridge: {exhibit_title} → Sound/Vision Layer Mappings.

NON-CANONICAL: This module is a creative/educational tool.
It does not represent official [domain] lore.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# Sound Layer output
@dataclass
class SoundOutput:
    pitch_hz: float
    loudness_db: float
    timbre_brightness: float
    source: str

# Vision Layer output  
@dataclass
class VisionNode:
    id: str
    label: str
    type: str
    color: str = "#666666"
    size: float = 50.0

@dataclass
class VisionEdge:
    source: str
    target: str
    relationship: str
    weight: float = 0.5

class {exhibit_class}Bridge:
    """Bridge connecting {exhibit_title} to Grid sensory layers."""
    
    def entity_to_sound(self, entity: str, intensity: float = 1.0) -> SoundOutput:
        """Map entity to Sound Layer parameters."""
        # TODO: Implement domain-specific mapping
        return SoundOutput(
            pitch_hz=220.0 * (1 + intensity),
            loudness_db=-12.0 + (intensity * 6),
            timbre_brightness=intensity,
            source=entity
        )
    
    def entity_to_node(self, entity: str, entity_type: str) -> VisionNode:
        """Map entity to Vision Layer node."""
        return VisionNode(
            id=f"node_{{entity.lower().replace(' ', '_')}}",
            label=entity,
            type=entity_type
        )
    
    def create_full_sensory_state(
        self,
        entity: str,
        intensity: float = 1.0
    ) -> dict[str, Any]:
        """Create combined Sound + Vision output."""
        sound = self.entity_to_sound(entity, intensity)
        node = self.entity_to_node(entity, "default")
        
        return {{
            "sound_layer": {{
                "pitch_hz": sound.pitch_hz,
                "loudness_db": sound.loudness_db,
                "timbre_brightness": sound.timbre_brightness
            }},
            "vision_layer": {{
                "nodes": [node.__dict__],
                "edges": []
            }},
            "metadata": {{
                "source": "{exhibit_id}",
                "entity": entity,
                "intensity": intensity
            }}
        }}

def create_bridge() -> {exhibit_class}Bridge:
    """Factory function for bridge creation."""
    return {exhibit_class}Bridge()

if __name__ == "__main__":
    bridge = create_bridge()
    result = bridge.create_full_sensory_state("test_entity", 0.8)
    import json
    print(json.dumps(result, indent=2))
'''
```

### Step 2: Update Manifest Integration Section

```python
def add_sensory_integration(manifest: dict, mappings: list[dict]) -> dict:
    """Add sensory layer integration to exhibit manifest."""
    manifest["sensory_integration"] = {
        "sound_layer": {
            "enabled": True,
            "mappings": mappings
        },
        "vision_layer": {
            "enabled": True,
            "graph_type": "directed",
            "node_mappings": [],
            "edge_mappings": []
        }
    }
    manifest["grid_integration"] = {
        "enabled": True,
        "sandbox_dataset": {
            "enabled": True,
            "description": "Closed-world demo for Grid testing",
            "entities": "...",
            "relationships": "...",
            "use_cases": []
        }
    }
    return manifest
```

---

## Phase 5: Update Workspace

### Step 1: Generate Workspace Folder Entries

```python
def generate_workspace_entries(exhibit_id: str, exhibit_path: str, sections: dict) -> list[dict]:
    """Generate workspace folder entries for an exhibit."""
    entries = []
    
    # Root entry
    entries.append({
        "path": exhibit_path,
        "name": f"   ├─ 🏛️ {exhibit_id.title()} · Exhibit (Root)"
    })
    
    # Section entries
    for section_type, section_info in sections.items():
        icon = {
            "canon": "📜",
            "tools": "🪄", 
            "tests": "🧪",
            "visualizations": "🎭"
        }.get(section_type, "📁")
        
        entries.append({
            "path": f"{exhibit_path}/{section_info['path']}",
            "name": f"   ├─ {icon} {exhibit_id.title()} · {section_info['label']}"
        })
    
    return entries

# Example
entries = generate_workspace_entries(
    "hogwarts",
    "light_of_the_seven/full_datakit/visualizations/Hogwarts",
    {
        "canon": {"path": "Founders", "label": "Founders (Canon)"},
        "tools": {"path": "great_hall", "label": "Great Hall (Tools)"},
        "tests": {"path": "prototypes", "label": "Prototypes"}
    }
)
```

### Step 2: Insert into grid.code-workspace

Manually add entries to the "Open Drawer" section:

```json
{
  "folders": [
    // ... main body folders ...
    {
      "path": ".",
      "name": "╰──┤ 𝗧𝗛𝗘 𝗢𝗣𝗘𝗡 𝗗𝗥𝗔𝗪𝗘𝗥 ├── (all is given)"
    },
    {
      "path": ".claude",
      "name": "   ├─ 🪞 .claude · AI Context"
    },
    // INSERT EXHIBIT ENTRIES HERE
    {
      "path": "light_of_the_seven/full_datakit/visualizations/[exhibit]",
      "name": "   ├─ 🏛️ [Exhibit] · Exhibit (Root)"
    }
    // ... remaining drawer folders ...
  ]
}
```

---

## Phase 6: Launch Configuration

### Add Debug Configuration

```json
{
  "name": "🏛️ [Exhibit] Demo",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/light_of_the_seven/full_datakit/visualizations/[exhibit]/grid_bridge.py",
  "console": "integratedTerminal",
  "cwd": "${workspaceFolder}"
}
```

### Add Task

```json
{
  "label": "█ [EXHIBIT]",
  "type": "shell",
  "command": "python light_of_the_seven/full_datakit/visualizations/[exhibit]/grid_bridge.py"
}
```

---

## Done Criteria

An exhibit is complete when:

- [ ] `exhibit.json` manifest exists and validates
- [ ] `README.md` documents purpose and quick start
- [ ] Canon/tooling separation is enforced
- [ ] Non-canon code has NON-CANONICAL headers
- [ ] Sources are cited in `SOURCES.md` (if strict canon)
- [ ] `grid_bridge.py` exists (if Grid integration)
- [ ] Workspace folders are added
- [ ] Launch/task configurations are present
- [ ] Basic tests exist and pass

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Manifest validation fails | Check against `schemas/exhibit_manifest_schema.json` |
| Missing citations | Review `SOURCES.md` and add references |
| Bridge not found | Ensure `grid_bridge.py` is in exhibit root |
| Workspace not updating | Reload VS Code window after editing workspace file |

---

## Related

- `.windsurf/rules/grid-canon-policy.md`
- `.windsurf/rules/grid-exhibit-governance.md`
- `.windsurf/rules/grid-sensory-layers.md`
- `schemas/exhibit_manifest_schema.json`
- `AGENTS.md`
