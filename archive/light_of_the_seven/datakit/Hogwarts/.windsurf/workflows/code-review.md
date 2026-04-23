# Code Review Workflow

## Description
Reviews Python code in a session after custom code has been written, focusing on dynamic code evaluation safety, code quality, and automated tooling standards.

## Trigger
- Manual trigger after custom Python code has been written in the session

## Steps

### 1. Security Audit - Dynamic Code Evaluation
- [ ] Scan for `eval()` usage - flag as critical if found with user input
- [ ] Scan for `exec()` usage - flag as critical if found with user input
- [ ] Recommend `ast.literal_eval()` for any literal parsing needs
- [ ] Check for `__import__` patterns that could indicate injection risks

### 2. Code Quality Evaluation
#### Style & Readability (PEP 8)
- [ ] Function names use `snake_case`
- [ ] Class names use `PascalCase`
- [ ] Constants use `UPPER_SNAKE_CASE`
- [ ] Line length ≤ 88 characters (Black standard)
- [ ] Proper spacing around operators and after commas

#### Complexity
- [ ] Functions follow Single Responsibility Principle
- [ ] No function exceeds ~20 lines without justification
- [ ] Cyclomatic complexity is reasonable (no deeply nested logic)

#### Robustness
- [ ] Inputs are validated/sanitized before use
- [ ] `try...except` blocks catch specific exceptions, not bare `except:`
- [ ] Resources are properly closed (use context managers)

#### Performance
- [ ] No obvious O(n²) patterns where O(n) is possible
- [ ] Suggest `cProfile` or `timeit` for hotspots if applicable

### 3. Automated Tool Recommendations (2025 Standards)
```bash
# Linting & Formatting
ruff check .                    # Fast linter (preferred 2025)
ruff format .                   # Formatter
black --check .                 # Alternative formatter

# Security Scanning
bandit -r . -ll                 # Find eval/exec and other vulnerabilities

# Type Checking
mypy --strict .                 # Validate type hints
```

### 4. Review Summary Template
```
## Code Review Summary

**Files Reviewed:** [list files]
**Critical Issues:** [count]
**Warnings:** [count]
**Suggestions:** [count]

### Critical (Must Fix)
- [ ] Issue description + file:line

### Warnings (Should Fix)
- [ ] Issue description + file:line

### Suggestions (Consider)
- [ ] Improvement description
```
