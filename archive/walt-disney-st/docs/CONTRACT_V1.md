# Artifact Contract v1.0

## Overview

The Artifact Contract defines the structure and compatibility guarantees for `artifact.json` files produced by the Python→Rust contract pipeline. This document specifies versioning, compatibility policies, and migration paths.

## Version Format

Artifact versions follow [Semantic Versioning](https://semver.org/):
- **Major (x.0.0)**: Breaking changes
- **Minor (1.x.0)**: Backward-compatible additions
- **Patch (1.0.x)**: Backward-compatible fixes

## Current Version

**v1.0** - Initial stable release

## Compatibility Policy

### Patch Releases (1.0.x)

**Allowed Changes:**
- Add optional fields to existing artifact types
- Extend arrays with new optional elements
- Relax validation constraints (e.g., allow empty arrays where previously required)
- Improve error messages without changing structure

**Consumer Impact:**
- Existing consumers continue to work without changes
- New optional fields are ignored by old consumers
- No migration required

**Example:**
```json
// v1.0.0
{
  "artifact_version": "1.0",
  "modules": [...]
}

// v1.0.1 - Added optional "metadata" field
{
  "artifact_version": "1.0",
  "modules": [...],
  "metadata": { "generated_at": "2024-01-01" }  // New optional field
}
```

### Minor Releases (1.x.0)

**Allowed Changes:**
- Add new artifact types (e.g., `InterfaceArtifact`, `TypeAliasArtifact`)
- Add optional top-level fields
- Add optional fields to existing types
- Extend enums with new values

**Consumer Impact:**
- Existing consumers continue to work
- New artifact types are ignored by old consumers
- Consumers may need updates to handle new types (optional)

**Example:**
```json
// v1.0.0
{
  "artifact_version": "1.0",
  "modules": [...]
}

// v1.1.0 - Added new artifact type
{
  "artifact_version": "1.1",
  "modules": [...],
  "interfaces": [...]  // New artifact type
}
```

### Major Releases (x.0.0)

**Breaking Changes:**
- Rename fields
- Change field types
- Remove fields
- Make optional fields required
- Change structure significantly

**Consumer Impact:**
- Existing consumers will break
- Migration path must be provided
- Deprecation period recommended (e.g., support both formats for one release)

**Example:**
```json
// v1.0.0
{
  "artifact_version": "1.0",
  "modules": [...]
}

// v2.0.0 - Breaking change: renamed "modules" to "artifacts"
{
  "artifact_version": "2.0",
  "artifacts": [...]  // Breaking: old name "modules" removed
}
```

## Format Support

### Legacy Array Format

For backward compatibility, the schema supports the legacy array format:

```json
[
  {
    "path": "module.py",
    "has_doc": true,
    "imports": [],
    "total_lines": 10,
    "functions": [],
    "classes": []
  }
]
```

**Status:** Supported but deprecated. New generators should use the object format.

### Current Object Format (v1.0)

```json
{
  "artifact_version": "1.0",
  "modules": [
    {
      "path": "module.py",
      "has_doc": true,
      "imports": [],
      "total_lines": 10,
      "functions": [],
      "classes": []
    }
  ]
}
```

## Supported Versions

| Version | Status | Supported Until |
|---------|--------|----------------|
| 1.0     | Current | TBD |
| Legacy (array) | Deprecated | v2.0.0 |

## Migration Guide

### From Legacy Array Format to v1.0

**Automatic:** Rust consumers automatically handle both formats. No code changes needed.

**Manual (if needed):**
```python
# Legacy format
artifacts = json.loads(content)  # List

# v1.0 format
data = json.loads(content)
if isinstance(data, dict) and "modules" in data:
    artifacts = data["modules"]
else:
    artifacts = data  # Legacy array
```

### From v1.0 to Future Versions

Migration guides will be provided in release notes for major versions.

## Validation

All artifacts must:
1. Pass schema validation (handwritten or JSON Schema)
2. Pass type validation (Python vs Rust struct matching)
3. Include valid `artifact_version` (if using object format)

## Testing

Golden fixtures are maintained in `tests/fixtures/`:
- `small_artifact_v1.0.json` - Minimal valid artifact
- `medium_artifact_v1.0.json` - Typical artifact
- `legacy_array_format.json` - Legacy format for backward compat testing

All fixtures are validated in CI with both validation engines.

## Questions?

- Open an issue for compatibility questions
- Check `tests/fixtures/` for examples
- See `schemas/artifact.schema.json` for full schema definition

