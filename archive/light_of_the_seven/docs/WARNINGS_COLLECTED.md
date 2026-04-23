# Warnings Collected — Light of the Seven

**Date:** 2026-03-05  
**Context:** Post-debug run; test suite: 163 passed, 5 skipped.

## Summary

| Category | Count | Action |
|----------|--------|--------|
| PydanticDeprecatedSince20 (class-based `config`) | 10 | Migrate to ConfigDict |
| PydanticDeprecatedSince20 (`json_encoders`) | 1 | Use custom serializers |
| UserWarning (optional deps) | 2 | Document optional installs |
| PytestUnhandledThreadExceptionWarning | 1 | Subprocess encoding on Windows |

---

## 1. Pydantic V2 deprecation: class-based `config`

**Message:** `Support for class-based config is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0.`

**Locations:**

| File | Class |
|------|--------|
| `grid/organization/models.py` | `Organization` (line 71), `User` (line 123) |
| `grid/organization/discipline.py` | `Penalty` (23), `RuleViolation` (53), `Rule` (74), `DisciplineAction` (98) |
| `grid/tracing/action_trace.py` | `TraceContext` (26), `ActionTrace` (65) |
| `grid/prompts/models.py` | `Prompt` (41) |
| `grid/senses/sensory_input.py` | `SensoryInput` (31) |
| `grid/temporal_safety/context.py` | `AsyncTemporalContext` (18) |

**Remedy:** Replace `class Config:` with `model_config = ConfigDict(...)` and use Pydantic V2 migration guide.

---

## 2. Pydantic V2 deprecation: `json_encoders`

**Message:** `json_encoders is deprecated. See https://docs.pydantic.dev/2.12/concepts/serialization/#custom-serializers for alternatives.`

**Location:** `grid/organization/models.py` (triggered from `Organization` model, line 71; also from pydantic internal when `json_encoders` is used).

**Remedy:** Use custom serializers (e.g. `field_serializer` / `model_serializer`) instead of `json_encoders`.

---

## 3. Optional dependencies (UserWarning)

| Message | Location |
|---------|----------|
| IBM watsonx.ai not available. Install with: `pip install ibm-watsonx-ai` | `tests/test_integration.py:15` |
| CuPy not available. Install with: `pip install cupy-cuda11x` (match your CUDA version) | `tests/test_integration.py:15` |

**Remedy:** Document in README/INSTALL; tests already skip when unavailable.

---

## 4. PytestUnhandledThreadExceptionWarning (test_ollama_rag_demo)

**Message:** Exception in thread `_readerthread`: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 541: character maps to <undefined>`

**Cause:** Subprocess (Ollama) output read with default encoding (e.g. cp1252 on Windows); output contains non-ASCII bytes.

**Remedy:** Use `subprocess.run(..., encoding="utf-8", errors="replace")` or set `PYTHONIOENCODING=utf-8` when invoking the subprocess so the reader thread uses UTF-8.

---

## Verification

To regenerate this list:

```bash
uv run pytest tests/ -q -W default 2>&1 | tail -n 200
```
