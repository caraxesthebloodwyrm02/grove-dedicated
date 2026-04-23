## Grid Project Task Runner Steps

### Prerequisites
1. Ensure Python 3.11+ is installed
   - **In WSL Ubuntu:** Install Python if not available:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-venv
     # Create symlink if needed
     sudo ln -s /usr/bin/python3 /usr/bin/python
     ```
2. Navigate to the project root directory
3. **Activate virtual environment first:**
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   # Or in WSL: source .venv/bin/activate
   ```

### Fundamental Steps to Run Tasks

#### 1. Setup Environment
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Run Unit Tests
```bash
# Run all tests with pytest (recommended)
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_specific.py -v

# Run with coverage
python -m pytest tests/ --cov=grid --cov-report=html
```

#### 3. Run Full DataKit Tests
```bash
cd light_of_the_seven/full_datakit
python -m pytest tests/ -v
```

#### 4. Linting and Code Quality
```bash
# Run ruff linter
python -m ruff check .

# Auto-fix ruff issues
python -m ruff check --fix .

# Format code with ruff
python -m ruff format .
```

#### 5. Build and Package
```bash
# Build the project (if build tools installed)
python -m build

# Install locally for development
pip install -e .
```

### Common Actions

| Action | Command |
|--------|---------|
| Run all tests | `python -m pytest tests/ -v` |
| Run single test | `python -m pytest tests/test_module.py::TestClass::test_method` |
| Check coverage | `python -m pytest tests/ --cov=grid --cov-report=html` |
| Format code | `python -m ruff format .` |
| Lint code | `python -m ruff check .` |
| Auto-fix lint | `python -m ruff check --fix .` |
| Clean build artifacts | `rm -rf build/ dist/ *.egg-info` |
