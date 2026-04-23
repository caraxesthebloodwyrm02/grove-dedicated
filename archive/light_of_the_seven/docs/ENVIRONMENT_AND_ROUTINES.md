# Sanitized environment, activation checks & test-lint routines

**Purpose:** Repeatable setup and verification for Light of the Seven (UV-based). Use before development, after cloning, or when the venv is broken.

---

## 1. Sanitized virtual environment installation

Run from the repository root (`E:\Seeds\light_of_the_seven` or equivalent).

### 1.1 Remove existing venv (if broken or stale)

**Windows (PowerShell):**
```powershell
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
```

**Unix / WSL / Git Bash:**
```bash
rm -rf .venv
```

### 1.2 Create a fresh venv with UV

Use a Python version that satisfies `requires-python` (e.g. `>=3.10`). Prefer 3.12 for consistency.

```bash
uv venv --python 3.12
```

Optional: pin the venv to the project directory so `uv` uses it automatically:
- UV will use `.venv` in the project root if present; no extra config needed.

### 1.3 Install dependencies (dev + test groups)

```bash
uv sync --group dev --group test
```

This installs:
- **Default:** core dependencies from `pyproject.toml`
- **Group test:** pytest, pytest-cov (and any other test deps in `[dependency-groups] test`)
- **Group dev:** black, ruff, isort, mypy (and any other dev deps in `[dependency-groups] dev`)

If `[dependency-groups]` is not yet in `pyproject.toml`, use optional extra instead:
```bash
uv sync --extra test --extra dev
```

---

## 2. Activation checks

Verify the environment before running tests or lint.

### 2.1 Check that the venv is active (optional but recommended)

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
# Then:
$env:VIRTUAL_ENV
# Should show path to .venv
```

**Unix / WSL / Git Bash:**
```bash
source .venv/bin/activate
echo $VIRTUAL_ENV
```

If you prefer not to activate, use `uv run` for all commands (see below); it will use the project’s `.venv` when present.

### 2.2 Verify Python and UV

```bash
uv run python -c "import sys; print(sys.executable)"
# Should print path inside .venv (e.g. .../light_of_the_seven/.venv/Scripts/python.exe on Windows)

uv run python -c "import pytest, ruff; print('OK')"
# Ensures test and lint tools are importable
```

### 2.3 Quick sanity run

```bash
uv run pytest tests/ -q --tb=line -x
# Stops at first failure; confirms tests can run
```

If any of these fail, re-run the sanitized installation (Section 1).

---

## 3. Test and lint routines

Run from the repository root. Use `uv run` so the project venv is used even when not activated.

### 3.1 Lint (must pass before pushing)

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```

Both commands must exit 0. To auto-fix and format:

```bash
uv run ruff format src/ tests/
uv run ruff check src/ tests/ --fix
```

### 3.2 Tests

**Default (fast):**
```bash
uv run pytest tests/ -v --tb=short
```

**With coverage:**
```bash
uv run pytest tests/ -v --tb=short --cov=src --cov-report=term-missing
```

**Quiet, stop at first failure:**
```bash
uv run pytest tests/ -q --tb=line -x
```

### 3.3 Recommended order before commit/push

1. **Lint**
   - `uv run ruff check src/ tests/`
   - `uv run ruff format --check src/ tests/`
2. **Tests**
   - `uv run pytest tests/ -v --tb=short`
3. Fix any failures, then re-run 1 and 2 until both pass.

### 3.4 Makefile equivalents (if `make` is available)

```bash
make install   # uv sync --group dev --group test
make test     # uv run pytest tests/ -v --tb=short
make lint     # ruff check + format --check on src/ tests/
make format   # ruff format + ruff check --fix
```

---

## 4. One-time setup summary

| Step | Command |
|------|--------|
| 1. Remove old venv | `Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue` (Windows) or `rm -rf .venv` (Unix) |
| 2. Create venv | `uv venv --python 3.12` |
| 3. Install deps | `uv sync --group dev --group test` |
| 4. Verify | `uv run python -c "import pytest, ruff; print('OK')"` |
| 5. Run tests | `uv run pytest tests/ -q --tb=line -x` |
| 6. Run lint | `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` |

---

## 5. References

- **CLAUDE.md** — Project overview and commands
- **pyproject.toml** — `[dependency-groups]` and `[tool.ruff]` configuration
- **Makefile** — `install`, `test`, `lint`, `format` targets
