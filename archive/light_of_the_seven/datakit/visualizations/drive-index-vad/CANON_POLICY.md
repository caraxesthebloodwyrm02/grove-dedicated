# Canon Policy: Drive Index (V×A×D) Exhibit

## Overview

This exhibit maintains **moderate** canon discipline, balancing rigorous research citations with practical implementation validation.

---

## Rules

### 1. Research Claims Must Be Cited

All claims about real-world applications, academic models, or industry adoption must reference:
- Academic papers (IEEE, ACM, Frontiers, arXiv)
- Regulatory documents (EU regulations, standards bodies)
- Industry reports (validated sources only)

**Citation Format**:
```markdown
[Source, Year "Title"]
```

**Example**:
> The EU General Safety Regulation mandates driver drowsiness and attention warning systems in all new vehicles as of July 2024. [European Commission, 2024 "Mandatory drivers assistance systems"]

### 2. Implementation Must Be Tested

All code implementations must have:
- Automated test coverage
- Boundary condition validation
- Integration test verification

**Current Status**: 16/16 tests passing (100% coverage of drive coefficient, policy, gating, and observability)

### 3. Tooling Is Clearly Labeled

Non-canonical utilities and demos must include:
- **NON-CANONICAL** headers in code files
- Clear separation in directory structure (`tools/` vs `docs/`)
- Explicit disclaimers in documentation

### 4. Speculation Must Be Marked

Any speculative content (future applications, hypothetical scenarios) must be explicitly labeled:
```markdown
> **Speculative**: [Content]
```

---

## Layers

### Canon Layer (Docs)

**Location**: `docs/`

**Content**:
- Research citations and sources
- Implementation specifications
- Validated real-world applications
- Test results and benchmarks

**Verification**: All claims must be traceable to authoritative sources.

### Tooling Layer (Code)

**Location**: `tools/`, `workspace/`

**Content**:
- Snapshot systems (`dials_and_knobs.py`)
- Interactive demos (`drive_interface_demo.html`)
- Logging utilities (`drive_logger.py`)

**Verification**: Must include **NON-CANONICAL** disclaimers where appropriate.

### Testing Layer

**Location**: `tests/`

**Content**:
- Unit tests for drive coefficient
- Integration tests for pipeline gating
- Policy classification tests
- Observability tests

**Verification**: All tests must pass before exhibit status changes to "production".

---

## Compliance Checklist

- [x] All research claims cited with sources
- [x] Implementation validated through automated testing
- [x] Tooling clearly separated from canon documentation
- [x] No speculation without explicit labeling
- [x] Schema validation for exhibit manifest
- [x] Real-world applications grounded in published research

---

## Updates Log

| Date | Change | Contributor |
|------|--------|-------------|
| 2025-12-18 | Initial exhibit creation with drive index implementation | GRID Research Team |
| 2025-12-18 | Added 16 integration tests (all passing) | GRID Research Team |
| 2025-12-18 | Documented 5 real-world applications with citations | GRID Research Team |

---

**Canon Level**: Moderate  
**Last Reviewed**: 2025-12-18
