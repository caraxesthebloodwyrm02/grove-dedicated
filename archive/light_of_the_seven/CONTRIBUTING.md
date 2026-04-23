# Contributing to Light of the Seven

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

- **Bug Fixes** - Fix issues and improve stability
- **Documentation** - Improve docs, add examples, fix typos
- **Tests** - Increase test coverage and add edge cases
- **Features** - Propose and implement new features
- **Research** - Contribute to the knowledge branches

## Development Setup

```bash
# Clone the repository
git clone https://github.com/irfankabir02/light_of_the_seven.git
cd light_of_the_seven

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# Install development dependencies
pip install -e ".[dev,test]"
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src/light_of_the_seven --cov-report=html

# Run specific test
pytest tests/test_geometry.py -v
```

## Code Quality

Before submitting, ensure your code passes all checks:

```bash
# Format with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Sort imports
isort src/ tests/
```

## Submitting Changes

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Make** your changes with clear, focused commits
4. **Test** your changes locally
5. **Push** to your fork: `git push origin feature/your-feature`
6. **Open** a Pull Request with a clear description

## Commit Messages

Use clear, descriptive commit messages:

- `fix: Resolve geometry calculation error`
- `feat: Add new sorting algorithm`
- `docs: Update installation guide`
- `test: Add edge case tests for integration`

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Open an issue or start a discussion on GitHub.
