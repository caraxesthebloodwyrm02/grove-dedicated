# Drive Index (V×A×D): Emotional Vector Intelligence

> **Research exhibit exploring the V×A×D drive coefficient for affective computing applications**

## Overview

The **Drive Index** is a scalar coefficient derived from the three-dimensional emotional model:

```
drive = Valence × Arousal × Dominance
```

Where:
- **Valence (V)**: Emotional polarity, range `[-1.0, +1.0]`
- **Arousal (A)**: Activation/energy level, range `[0.0, 1.0]`
- **Dominance (D)**: Sense of control/agency, range `[0.0, 1.0]`

**Result**: Drive coefficient in range `[-1.0, +1.0]`

---

## Quick Start

### Run Tests
```bash
cd "e:\grid\light_of_the_seven\full_datakit\At the rate\grep_eq_spectrum"
python -m pytest tests/test_drive_integration.py -v
```

### Demo Dials & Knobs System
```bash
python workspace/dials_and_knobs.py
```

### View Visualizations
- **Interactive Demo**: `workspace/drive_interface_demo.html`
- **Dashboard**: `tools/dashboard_visualization.html` (Focused Work state)
- **Snapshot**: `docs/focused_work_dashboard.webp` (High-fidelity SVG render)

---

## Structure

- **`docs/`** — Canon documentation (cited research, implementation details)
- **`tools/`** — Non-canon utilities and demos
- **`tests/`** — Verification and validation (16 integration tests)

---

## Implementation

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Drive Property | `core/models.py:107-116` | V×A×D calculation |
| Drive Policy | `core/models.py:708-742` | Band classification (HIGH_POSITIVE, NEUTRAL, HIGH_NEGATIVE) |
| Pipeline Integration | `core/pipeline.py:435-541` | Behavior gating based on drive |
| Logging | `core/drive_logger.py` | Observability and telemetry |
| Snapshot System | `workspace/dials_and_knobs.py` | State preservation with LPF smoothing |

### Policy Bands

| Band | Threshold | Pipeline Mode | EQ Multiplier | Behavior |
|------|-----------|---------------|---------------|----------|
| **HIGH_POSITIVE** | ≥ +0.20 | FULL | 1.3x | Accelerate / aggressive refactor |
| **NEUTRAL** | -0.20 to +0.20 | REFACTOR | 1.0x | Standard / balanced mode |
| **HIGH_NEGATIVE** | ≤ -0.20 | ANALYZE | 0.7x | Stabilize / de-escalate |

---

## Real-World Applications

Based on research from IEEE, Frontiers, ACM, and EU regulatory sources (2023-2025):

1. **Automotive Safety** (EU mandatory 2024): Driver drowsiness/attention monitoring
2. **Mental Health**: Emotionally adaptive digital health interventions
3. **Education**: Adaptive learning systems with emotion-aware tutoring
4. **Human-AI Interaction**: Emotion-aware chatbots and assistants
5. **Robotics**: Social robots with adaptive workplace interventions

See `docs/APPLICATIONS.md` for detailed citations.

---

## Canon Policy

This exhibit follows a **moderate** canon policy:
- All research claims are cited with academic sources
- Implementation is validated through automated testing
- Tooling is clearly labeled as non-canonical
- Real-world applications are grounded in published research

See `CANON_POLICY.md` for full details.

---

## Integration with GRID

The drive coefficient integrates with GRID's grep-eq-spectrum pipeline:
- **Effect in place**: Drive modulates pipeline behavior based on emotional state
- **Observability**: Drive values logged and visible in output metadata
- **Testing**: 16 integration tests verify all policy bands and edge cases

---

## Quick Reference

```python
from core.models import EmotionalValence
from core.pipeline import GrepEQSpectrumPipeline

# High positive drive
valence = EmotionalValence(polarity=0.8, arousal=0.8, dominance=0.8)
pipeline = GrepEQSpectrumPipeline()
output = pipeline.process([1.0, 2.0, 3.0], valence=valence)

# Check drive telemetry
print(output.stage_results[0].metadata["drive"])        # 0.512
print(output.stage_results[0].metadata["drive_band"])   # "HIGH_POSITIVE"
```

---

**Status**: Production-ready (v1.0.0)  
**Last Updated**: 2025-12-18
