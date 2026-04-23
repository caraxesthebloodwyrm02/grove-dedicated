---
name: grid-report
description: Generate comprehensive Grid analysis reports including exhibit status, sensory layer health, and canon compliance
version: 2.0.0
author: Grid Research Team
triggers:
  - manual
  - /grid-report
tags:
  - reporting
  - analysis
  - diagnostics
  - exhibits
---

# Grid Report Workflow

> **Purpose**: Generate structured reports on Grid project health, exhibit compliance, sensory layer status, and development diagnostics.

## Usage

Type `/grid-report` in Cascade's prompt to start this workflow.

| Command | Description |
|---------|-------------|
| `/grid-report` | Full project report |
| `/grid-report --quick` | Summary only |
| `/grid-report --exhibits` | Exhibit compliance check |
| `/grid-report --sensory` | Sound/Vision layer status |
| `/grid-report --fix` | Auto-fix detected issues |

---

## Phase 1: Environment Check

```bash
# Verify Python environment
python --version
python -c "import sys; print(f'Python path: {sys.executable}')"

# Check Grid is importable
python -c "import grid; print(f'Grid package: {grid.__file__}')" 2>/dev/null || echo "Grid package not installed"

# Check core dependencies
python -c "
try:
    import fastapi; print(f'✓ FastAPI {fastapi.__version__}')
except ImportError: print('✗ FastAPI missing')
try:
    import pydantic; print(f'✓ Pydantic {pydantic.__version__}')
except ImportError: print('✗ Pydantic missing')
"
```

---

## Phase 2: CLI Diagnostics

```powershell
# The correct way to invoke Grid CLI (not `grid` directly)
python -m grid --help

# Run basic analysis
python -m grid analyze "Test entity recognition" --output yaml

# Check circuits API health
python -c "from circuits.main import app; print('✓ Circuits app importable')"
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: grid` | Not installed | `pip install -e .` |
| `NameError` on import | Import order issue | Check model definitions before `create_app()` |
| `$` expansion in PowerShell | Variable interpolation | Use single quotes or escape `\$` |

---

## Phase 3: Exhibit Compliance Check

```bash
# Find all exhibits
echo "=== EXHIBITS FOUND ==="
find . -name "exhibit.json" -type f 2>/dev/null | while read f; do
    echo "  $f"
done

# Validate exhibit manifests
python -c "
import json
from pathlib import Path

exhibits = list(Path('.').rglob('exhibit.json'))
print(f'\n=== EXHIBIT VALIDATION ({len(exhibits)} found) ===')

for exhibit_path in exhibits:
    try:
        with open(exhibit_path) as f:
            manifest = json.load(f)
        
        exhibit_id = manifest.get('exhibit_id', 'MISSING')
        version = manifest.get('version', 'MISSING')
        canon = manifest.get('canon_policy', {})
        level = canon.get('level', 'unspecified')
        
        # Required field check
        required = ['exhibit_id', 'version', 'canon_policy', 'paths']
        missing = [r for r in required if r not in manifest]
        
        status = '✓' if not missing else '✗'
        print(f'{status} {exhibit_id} v{version} [{level}]')
        if missing:
            print(f'    Missing: {missing}')
    except Exception as e:
        print(f'✗ {exhibit_path}: {e}')
"
```

### Canon Policy Compliance

```python
# Check for NON-CANONICAL headers in exhibit tooling
from pathlib import Path

def check_noncanon_headers(exhibit_root: str) -> list[str]:
    issues = []
    root = Path(exhibit_root)
    
    for py_file in root.rglob("*.py"):
        content = py_file.read_text(errors='ignore')
        # Skip test files
        if py_file.name.startswith("test_"):
            continue
        # Check for header
        if "NON-CANONICAL" not in content[:500]:
            issues.append(str(py_file))
    
    return issues

# Run for Hogwarts
hogwarts_root = "light_of_the_seven/full_datakit/visualizations/Hogwarts"
issues = check_noncanon_headers(hogwarts_root)
if issues:
    print("Files missing NON-CANONICAL header:")
    for f in issues:
        print(f"  - {f}")
else:
    print("✓ All tooling files have NON-CANONICAL headers")
```

---

## Phase 4: Sensory Layer Status

### Schema Validation

```bash
# Check schemas exist
echo "=== SENSORY LAYER SCHEMAS ==="
for schema in sound_layer_schema.json vision_layer_schema.json exhibit_manifest_schema.json; do
    if [ -f "schemas/$schema" ]; then
        echo "✓ $schema"
    else
        echo "✗ $schema MISSING"
    fi
done
```

### Integration Health

```python
# Test sensory layer imports
print("=== SENSORY LAYER HEALTH ===")

# Sound Layer
try:
    from pathlib import Path
    import json
    schema = json.loads(Path("schemas/sound_layer_schema.json").read_text())
    print(f"✓ Sound Layer schema loaded ({len(schema.get('properties', {}))} properties)")
except Exception as e:
    print(f"✗ Sound Layer: {e}")

# Vision Layer
try:
    schema = json.loads(Path("schemas/vision_layer_schema.json").read_text())
    print(f"✓ Vision Layer schema loaded ({len(schema.get('properties', {}))} properties)")
except Exception as e:
    print(f"✗ Vision Layer: {e}")

# Hogwarts Bridge
try:
    import sys
    sys.path.insert(0, "light_of_the_seven/full_datakit/visualizations/Hogwarts")
    from grid_bridge import HogwartsGridBridge
    bridge = HogwartsGridBridge()
    print("✓ Hogwarts Grid Bridge importable")
except Exception as e:
    print(f"✗ Hogwarts Bridge: {e}")
```

---

## Phase 5: Generate Report

```python
from datetime import datetime
from pathlib import Path
import json

def generate_report() -> str:
    """Generate comprehensive Grid status report."""
    
    lines = [
        "# GRID Report",
        f"",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## Summary",
        ""
    ]
    
    # Exhibits
    exhibits = list(Path('.').rglob('exhibit.json'))
    lines.append(f"- **Exhibits**: {len(exhibits)} found")
    
    # Schemas
    schemas = list(Path('schemas').glob('*.json')) if Path('schemas').exists() else []
    lines.append(f"- **Schemas**: {len(schemas)} defined")
    
    # Tests
    tests = list(Path('tests').rglob('test_*.py')) if Path('tests').exists() else []
    lines.append(f"- **Tests**: {len(tests)} test files")
    
    lines.extend([
        "",
        "---",
        "",
        "## Exhibits",
        ""
    ])
    
    for exhibit_path in exhibits:
        try:
            manifest = json.loads(exhibit_path.read_text())
            exhibit_id = manifest.get('exhibit_id', 'unknown')
            version = manifest.get('version', '?')
            level = manifest.get('canon_policy', {}).get('level', '?')
            lines.append(f"### {exhibit_id} (v{version})")
            lines.append(f"- Canon policy: {level}")
            lines.append(f"- Path: `{exhibit_path.parent}`")
            lines.append("")
        except Exception as e:
            lines.append(f"- ✗ Error reading {exhibit_path}: {e}")
    
    lines.extend([
        "---",
        "",
        "## Recommendations",
        "",
        "- [ ] Run `python -m pytest tests -v` to verify test health",
        "- [ ] Validate exhibit manifests against schema",
        "- [ ] Check NON-CANONICAL headers in exhibit tooling",
        "- [ ] Review SOURCES.md citations for strict-canon exhibits",
        ""
    ])
    
    return "\n".join(lines)

# Generate and save
report = generate_report()
Path("GRID_REPORT.md").write_text(report)
print(report)
print("\n--- Report saved to GRID_REPORT.md ---")
```

---

## Quick Reference

### Correct CLI Invocations

```powershell
# Help
python -m grid --help

# Analyze text (use single quotes for $ in PowerShell)
python -m grid analyze 'Alice met Bob at Acme Corp' --output yaml

# Run circuits server
python -m uvicorn circuits.main:app --reload --host 127.0.0.1 --port 8002
```

### Environment Variables

```powershell
$env:ALLOW_ENTRY = "1"
$env:PYTHONPATH = "$PWD;$PWD\grid;$PWD\circuits"
```

---

## Related Rules & Workflows

- `.windsurf/rules/grid-canon-policy.md` — Canon governance
- `.windsurf/rules/grid-sensory-layers.md` — Sound/Vision layer rules
- `.windsurf/rules/grid-exhibit-governance.md` — Exhibit management
- `.windsurf/workflows/grid-exhibit.md` — Exhibit creation workflow
- `.windsurf/workflows/grid-optimize-performance.md` — Performance tuning

---

## Done Criteria

This workflow is complete when:

- [ ] Environment is verified (Python, dependencies)
- [ ] CLI invocations work correctly
- [ ] All exhibits validate against schema
- [ ] Sensory layer schemas are present and valid
- [ ] Report is generated and saved