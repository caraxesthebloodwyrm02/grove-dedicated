# 🚀 Quick Start Guide

**Get hello-app running in 5 minutes or less.**

---

## Step 1: Install Dependencies (1 minute)

```powershell
# Navigate to project directory
cd e:\Projects\Python\hello

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed pytest-7.4.3 pytest-cov-4.1.0 flake8-6.1.0 black-23.12.1 ...
```

---

## Step 2: Run Your First Dice Roll (30 seconds)

```powershell
# Single roll
python -m src.main

# Multiple rolls with statistics
python -m src.main --rolls 5 --stats
```

**Expected output:**
```
[2025-11-14 12:03:06] [INFO] src.main - Rolls: [2, 6, 1, 5, 5]
[2025-11-14 12:03:06] [INFO] src.main - Statistics - Count: 5.0, Min: 1.0, Max: 6.0, Sum: 19.0, Mean: 3.80
```

---

## Step 3: Run All Tests (1 minute)

```powershell
# Run tests with coverage
pytest --cov=src --cov-report=term-missing -v

# Or just run tests
pytest
```

**Expected output:**
```
===================== 26 passed in 0.11s =====================
```

---

## Step 4: Check Code Quality (1 minute)

```powershell
# All quality checks in one go
flake8 src/ tests/
isort --check-only src/ tests/
black --check src/ tests/
mypy --strict src/
```

**Expected output:**
```
Success: no issues found in 4 source files
```

---

## Step 5: View Help & Options (30 seconds)

```powershell
python -m src.main --help
```

**Output:**
```
usage: main.py [-h] [--rolls ROLLS] [--seed SEED] [--verbose] [--stats]

Enterprise-grade dice rolling application.

optional arguments:
  -h, --help            show this help message and exit
  --rolls ROLLS         Number of rolls to perform (default: 1)
  --seed SEED           Random seed for reproducible results (optional)
  --verbose             Enable debug-level logging
  --stats               Display statistics (min, max, mean) for rolls
```

---

## Common Commands Reference

### Running the Application

```powershell
# Basic (1 roll)
python -m src.main

# 10 rolls with statistics
python -m src.main --rolls 10 --stats

# Reproducible rolls (same sequence every time)
python -m src.main --rolls 5 --seed 42

# Debug output
python -m src.main --rolls 3 --verbose

# View help
python -m src.main --help
```

### Testing

```powershell
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_dice.py

# Run specific test class
pytest tests/test_dice.py::TestSingleRoll

# Stop on first failure
pytest --maxfail=1
```

### Code Quality

```powershell
# Format code with Black
black src/ tests/

# Check formatting (no changes)
black --check src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy --strict src/
```

---

## Project Structure Overview

```
src/                 → Application code
├── main.py         → CLI entry point (argparse)
├── dice.py         → Core DiceRoller class
└── logger.py       → Logging setup

tests/              → Unit tests
├── test_dice.py    → 26 comprehensive tests
└── conftest.py     → pytest fixtures

.vscode/            → VS Code configuration
├── settings.json   → Workspace settings
├── launch.json     → Debug configs
└── extensions.json → Recommended extensions

Documentation
├── README.md                    → Full documentation
├── project_plan.md              → Roadmap & architecture
└── TRANSFORMATION_SUMMARY.md    → Transformation details
```

---

## VS Code Integration (Optional but Recommended)

### 1. Open Project in VS Code
```powershell
code .
```

### 2. Install Recommended Extensions
- Click "Install" on the notification for recommended extensions
- Or manually install: Python, Pylance, Ruff

### 3. Debug Your App
- Go to **Run and Debug** (Ctrl+Shift+D)
- Select **Python: Run hello-app**
- Click the green play button

### 4. Auto-format on Save
- Already configured in `.vscode/settings.json`
- Black will auto-format your code when you save

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution:** Run from the project root with `python -m src.main`

### Issue: "pytest: command not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: Black/isort/flake8 not found
**Solution:** Make sure virtual environment is activated: `.venv\Scripts\activate`

### Issue: Type checking errors in mypy
**Solution:** Ensure all functions have type hints; run `mypy --strict src/`

---

## What's Next?

### Phase 1 (Now ✅)
- ✅ Single die rolling
- ✅ Multiple rolls with stats
- ✅ Seeded reproducibility

### Phase 2 (Soon 📋)
- 📋 Weighted dice support
- 📋 Statistics (median, mode, std dev)
- 📋 Output formatters (JSON, CSV, table)

### Phase 3 (Roadmap 🗺️)
- 🗺️ FastAPI microservice
- 🗺️ Database persistence
- 🗺️ Analytics dashboard
- 🗺️ CI/CD pipeline (GitHub Actions)

---

## Files You Should Know About

| File | Purpose |
|------|---------|
| `README.md` | Complete documentation with examples |
| `project_plan.md` | Roadmap, architecture, risk matrix |
| `requirements.txt` | Python dependencies (pinned versions) |
| `pytest.ini` | Test configuration |
| `mypy.ini` | Type checking configuration |
| `.flake8` | Linting rules |
| `.gitignore` | Git exclusions |
| `Dockerfile` | Docker container image |

---

## Production Checklist

- ✅ Code passes all tests (26/26)
- ✅ 100% type coverage with mypy strict
- ✅ Zero linting violations
- ✅ Black formatting compliant
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ CLI interface complete
- ✅ Docker ready
- ✅ Documentation complete
- ✅ VS Code configured

---

## 🎯 You're Ready!

Your application is:
- **Well-tested** (26 unit tests, 100% coverage on core logic)
- **Type-safe** (100% type hints, mypy strict)
- **Production-grade** (error handling, logging, CLI)
- **Cloud-ready** (Dockerfile for deployment)
- **Team-friendly** (documentation, IDE config, standards)

**Happy rolling!** 🎲

