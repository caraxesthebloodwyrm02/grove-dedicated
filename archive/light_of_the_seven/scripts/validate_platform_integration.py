#!/usr/bin/env python3
"""
GRID Platform Integration Validator

Validates integrations/*/integration.json files against schemas/platform_integration_schema.json.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

try:
    import jsonschema
except ImportError:
    print("Error: 'jsonschema' package not found. Install it with 'pip install jsonschema'.")
    sys.exit(1)

def load_json(path: Path) -> Any:
    """Load JSON from file."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def validate_integration(integration_path: Path, schema: Dict[str, Any]) -> bool:
    """Validate a single integration file against the schema."""
    data = load_json(integration_path)
    if data is None:
        return False

    try:
        jsonschema.validate(instance=data, schema=schema)
        print(f"[PASS] {integration_path.relative_to(Path.cwd())}")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"[FAIL] {integration_path.relative_to(Path.cwd())}")
        print(f"  Reason: {e.message}")
        if e.path:
            print(f"  Location: {' -> '.join(str(p) for p in e.path)}")
        return False
    except Exception as e:
        print(f"[ERROR] {integration_path.relative_to(Path.cwd())}: {e}")
        return False

def main() -> int:
    """Main execution loop."""
    root = Path.cwd()
    schema_path = root / "schemas" / "platform_integration_schema.json"
    
    if not schema_path.exists():
        print(f"Error: Schema not found at {schema_path}")
        return 1
        
    schema = load_json(schema_path)
    if schema is None:
        return 1

    integrations_dir = root / "integrations"
    if not integrations_dir.exists():
        print(f"No integrations found in {integrations_dir}")
        return 0

    integration_files = list(integrations_dir.glob("**/integration.json"))
    
    if not integration_files:
        print("No 'integration.json' files found.")
        return 0

    print(f"Validating {len(integration_files)} platform integration(s)...")
    
    success_count = 0
    for file in integration_files:
        if validate_integration(file, schema):
            success_count += 1
            
    print(f"\nSummary: {success_count}/{len(integration_files)} passed.")
    
    return 0 if success_count == len(integration_files) else 1

if __name__ == "__main__":
    sys.exit(main())
