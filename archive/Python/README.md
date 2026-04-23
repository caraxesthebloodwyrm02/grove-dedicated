# Python Monorepo: hello-app & Sora Video System

This repository contains two main components:
- **hello-app**: Enterprise-grade dice rolling CLI (see below).
- **Sora video generation system**: Repository-driven Sora 2 video prompt and client integration (see `Docs/SORA_README.md`).

For a quick start with hello-app, see `QUICKSTART.md`. For the Sora system, start with `Docs/SORA_QUICKSTART.txt` and `Docs/SORA_README.md`.

---

## hello-app: Enterprise-Grade Dice Rolling Application

A production-ready Python CLI application demonstrating modern software engineering best practices, including modular architecture, comprehensive testing, type hints, logging, and containerization.

## 🎯 Features

- **Modular Architecture**: Clean separation of concerns with `src/` package structure
- **Comprehensive Testing**: 95%+ code coverage with pytest
- **Type Safety**: Full type hints with mypy strict mode validation
- **Code Quality**: Linting (flake8), formatting (Black), and import sorting (isort)
- **Structured Logging**: Production-grade logging with structured output
- **CLI Interface**: Command-line tool with argparse for parameterized control
- **Docker Ready**: Multi-stage Dockerfile for reproducible deployments
- **Cross-Platform**: Tested on Windows, Linux, and macOS

---

## 📋 Quick Start

### Prerequisites

- **Python 3.9+** (tested on 3.9, 3.10, 3.11, 3.12)
- **pip** or **conda** for dependency management
- **Docker** (optional, for containerized deployment)

### Installation

#### Option 1: Local Development Setup

```bash
# Clone or navigate to project directory
cd hello-app

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using conda

```bash
conda create -n hello-app python=3.11
conda activate hello-app
pip install -r requirements.txt
```

### Run the Application

```bash
# Basic usage: roll once
python -m src.main

# Roll 10 times
python -m src.main --rolls 10

# Roll 5 times with statistics
python -m src.main --rolls 5 --stats

# Reproducible rolls with seed
python -m src.main --rolls 3 --seed 42

# Enable debug logging
python -m src.main --rolls 2 --verbose

# View all options
python -m src.main --help
```

### Output Examples

```bash
$ python -m src.main --rolls 3 --stats
[2024-01-15 10:23:45] [INFO    ] src.main - Starting hello-app dice roller
[2024-01-15 10:23:45] [INFO    ] src.main - Rolls: [4, 2, 5]
[2024-01-15 10:23:45] [INFO    ] src.main - Statistics - Count: 3, Min: 2, Max: 5, Sum: 11, Mean: 3.67
[2024-01-15 10:23:45] [INFO    ] src.main - Completed successfully
```

---

## 🏗️ Project Structure

```
hello-app/
├── .github/
│   └── copilot-instructions.md          # AI agent guidelines
├── .vscode/
│   ├── settings.json                    # Workspace configuration
│   ├── launch.json                      # Debug configurations
│   └── extensions.json                  # Recommended extensions
├── src/
│   ├── __init__.py                      # Package marker
│   ├── main.py                          # CLI entry point with argparse
│   ├── dice.py                          # Core DiceRoller class
│   └── logger.py                        # Logging setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # pytest fixtures
│   └── test_dice.py                     # Comprehensive unit tests (70+ tests)
├── .flake8                              # Linting configuration
├── .gitignore                           # Git exclusions
├── .pre-commit-config.yaml              # (Future) Pre-commit hooks
├── Dockerfile                           # Container image definition
├── mypy.ini                             # Type checker configuration
├── project_plan.md                      # Roadmap & architecture
├── pyproject.toml                       # Build metadata & tool configs
├── pytest.ini                           # Test runner configuration
├── README.md                            # This file
└── requirements.txt                     # Python dependencies
```

---

## 🧪 Testing

### Run All Tests

```bash
# Standard test run
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_dice.py

# Run specific test class
pytest tests/test_dice.py::TestSingleRoll

# Run specific test
pytest tests/test_dice.py::TestSingleRoll::test_roll_within_range

# Stop on first failure
pytest --maxfail=1

# Run tests matching pattern
pytest -k "reproducib"
```

### Test Coverage

Target: **≥95% coverage** on all modules

```bash
# Generate coverage report
pytest --cov=src --cov-report=term-missing --cov-report=html

# View HTML report
# Open htmlcov/index.html in browser
```

---

## 🔍 Code Quality

### Linting with flake8

```bash
# Check all files
flake8 src/ tests/

# Show statistics
flake8 --statistics src/ tests/

# Format string check
flake8 --select=W504 src/
```

### Formatting with Black

```bash
# Check formatting (no changes)
black --check src/ tests/

# Format in place
black src/ tests/
```

### Import Sorting with isort

```bash
# Check import order
isort --check-only src/ tests/

# Sort imports in place
isort src/ tests/
```

### Type Checking with mypy

```bash
# Basic type check
mypy src/

# Strict mode (recommended)
mypy --strict src/

# Show configuration
mypy --config-file=mypy.ini --show-config
```

### All-in-One Quality Check

```bash
# Run all linters
flake8 src/ tests/ && \
  black --check src/ tests/ && \
  isort --check-only src/ tests/ && \
  mypy --strict src/ && \
  pytest --cov=src
```

---

## 🐳 Docker Deployment

### Build the Image

```bash
# Standard build
docker build -t hello-app .

# With build args
docker build -t hello-app:1.0 --build-arg PYTHON_VERSION=3.11 .

# Show build layers
docker build --progress=plain -t hello-app .
```

### Run the Container

```bash
# Basic run (3 rolls with stats)
docker run hello-app

# Custom parameters
docker run hello-app --rolls 10 --seed 42

# Interactive with debug logging
docker run -it hello-app --rolls 5 --verbose

# Mount local code (for development)
docker run -v $(pwd)/src:/app/src hello-app
```

### Docker Compose (Optional)

```bash
# Create docker-compose.yml for multi-service deployments
docker-compose up

# Clean up
docker-compose down
```

---

## 🚀 Development Workflow

### Environment Setup

```bash
# Create .env file for secrets (if needed)
cat > .env << EOF
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
EOF
```

### Pre-commit Hooks (Recommended)

```bash
# Install pre-commit framework
pip install pre-commit

# Set up hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### VS Code Setup

1. **Install Extensions** (from `.vscode/extensions.json`):
   - Python (ms-python.python)
   - Pylance (ms-python.vscode-pylance)
   - Ruff (charliermarsh.ruff)

2. **Enable Auto-format on Save**:
   - Workspace settings are pre-configured in `.vscode/settings.json`
   - Black will auto-format on save
   - isort organizes imports automatically

3. **Debug Configurations**:
   - Use **Run and Debug** view in VS Code
   - Select "Python: Run hello-app" to execute with sample parameters
   - Select "Python: pytest" to run test suite

---

## 📊 Architecture

### Module Overview

#### `src/dice.py`
Core business logic for dice rolling.

```python
roller = DiceRoller(seed=42)      # Optional seeding for reproducibility
rolls = roller.roll_multiple(10)  # Roll 10 times
stats = DiceRoller.calculate_stats(rolls)  # Get statistics
```

#### `src/main.py`
CLI interface powered by argparse.

```bash
python -m src.main --rolls 5 --stats --verbose
```

#### `src/logger.py`
Structured logging setup.

```python
from src.logger import setup_logger
logger = setup_logger(__name__)
logger.info("Event: %s", value)
```

### Data Flow

```
User Input (argparse)
    ↓
DiceRoller.roll_multiple(n)
    ↓
Individual roll() calls
    ↓
DiceRoller.calculate_stats()
    ↓
Structured Logger
    ↓
Console Output
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Python settings
export PYTHONUNBUFFERED=1           # Real-time output
export PYTHONDONTWRITEBYTECODE=1    # No .pyc files
export PYTHONPATH="$(pwd)"          # Module discovery
```

### Type Checking (`mypy.ini`)

- Strict mode enabled
- Python 3.9+ compatibility
- Per-file configuration override possible

### Linting (`.flake8`)

- Max line length: 88 (Black compatible)
- Ignored rules: E203 (whitespace), W503 (line breaks)

### Testing (`pytest.ini`)

- Test discovery: `test_*.py` in `tests/` directory
- Output: Verbose with short tracebacks
- Markers: `unit`, `integration`, `slow`

---

## 📈 Scaling & Future Enhancements

### Phase 2: Advanced Features
- Statistics module (median, mode, std dev, quartiles)
- Weighted die support (custom probabilities)
- Output formatters (JSON, CSV, ASCII table)
- YAML configuration files

### Phase 3: Production Features
- FastAPI microservice wrapper
- PostgreSQL result persistence
- Analytics dashboard (Plotly/Dash)
- GitHub Actions CI/CD pipeline
- Helm charts for Kubernetes

### Performance Optimization
- Benchmark with `timeit` module
- Profile with `cProfile`
- Cache frequently accessed data
- Batch processing for large roll sets

---

## 🛡️ Error Handling

The application gracefully handles:

- **Invalid input**: Negative or zero roll counts
- **Type errors**: Non-integer arguments
- **Edge cases**: Empty roll lists, single rolls
- **Logging failures**: Graceful degradation

Examples:

```bash
# Invalid roll count
$ python -m src.main --rolls -5
[ERROR] Invalid input: Roll count must be a positive integer

# Non-integer seed
$ python -m src.main --seed abc
[ERROR] Invalid input: seed must be integer

# Help text
$ python -m src.main --help
```

---

## 📝 Contributing

### Workflow

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test: `pytest --cov=src`
3. Format code: `black src/ tests/`
4. Check types: `mypy --strict src/`
5. Commit: `git commit -m "feat: descriptive message"`
6. Push and create PR

### Code Standards

- **Type Hints**: 100% of function signatures
- **Docstrings**: Google-style for all public functions
- **Tests**: Minimum 95% coverage
- **Linting**: Zero flake8 violations
- **Formatting**: Black compliance

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'src'`
**Solution**: Ensure you run from project root with `python -m src.main`

### Issue: `pytest: command not found`
**Solution**: Install dev dependencies: `pip install -r requirements.txt`

### Issue: Type checking errors in mypy
**Solution**: Enable strict mode to catch issues early: `mypy --strict src/`

### Issue: Docker build fails
**Solution**: Verify Python version compatibility; rebuild with `--no-cache`

---

## 📚 References

- [Python Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [pytest Documentation](https://docs.pytest.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

## 📄 License

MIT License — See LICENSE file for details

---

## ✨ Author

**Atmosphere**

For questions or contributions, please open an issue or pull request.

