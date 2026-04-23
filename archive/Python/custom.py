#!/usr/bin/env python3
"""
project_lint.py - Lightweight project health checker.

Focuses on catching:
- pyproject.toml parse errors (unescaped backslashes, invalid TOML)
- plain-text file checks
- Python syntax errors (using ast)
- Simple lint heuristics (snake_case for defs, == None checks, spacing around operators)

Usage examples:
    python project_lint.py --check-project --path /path/to/project
    python project_lint.py --check-toml --file pyproject.toml
    python project_lint.py --check-py --path src/
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import sys
from typing import List, Optional, Tuple

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore

ENCODING = "utf-8"


def read_text_file(path: str) -> Tuple[bool, List[str]]:
    """Return (ok, lines). ok=False if file can't be decoded as UTF-8 or contains NUL bytes."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        if b"\x00" in data:
            return False, []
        text = data.decode(ENCODING)
        lines = text.splitlines()
        return True, lines
    except (IOError, UnicodeDecodeError):
        return False, []


def check_plain_text(path: str) -> List[str]:
    """Check if file is valid UTF-8 plain text."""
    ok, _ = read_text_file(path)
    if ok:
        return []
    return [f"Not plain text or not UTF-8: {path}"]


def try_parse_toml(path: str) -> List[str]:
    """Try to parse TOML using tomllib if available. On failure, return diagnostics."""
    errors: List[str] = []
    if tomllib:
        try:
            with open(path, "rb") as f:
                tomllib.load(f)
            return []
        except IOError as e:
            errors.append(f"TOML file read error: {e}")
        except Exception as e:
            errors.append(f"TOML parse error: {e}")

    # Fallback: simple line-based heuristics for common issues
    ok, lines = read_text_file(path)
    if not ok:
        return [f"Cannot read {path} as UTF-8 plain text"]

    diagnostics: List[str] = []
    trailing_backslash_re = re.compile(r"\\\s*(#.*)?$")
    quoted_span_re = re.compile(r'(["\'])(.*?)(\1)')

    for i, line in enumerate(lines, start=1):
        # skip comment-only lines
        if re.match(r"^\s*#", line):
            continue

        # trailing backslash (likely problematic in TOML)
        if trailing_backslash_re.search(line):
            diagnostics.append(f"Trailing backslash on line {i}: {line.strip()}")
            continue

        # Find quoted spans and look for backslashes inside them
        for m in quoted_span_re.finditer(line):
            span = m.group(2)
            if "\\" in span:
                diagnostics.append(
                    f"Possible unescaped backslash on line {i}: {line.strip()}"
                )
                break

    if diagnostics:
        errors.extend(diagnostics)

    return errors


def check_py_syntax(path: str) -> List[str]:
    """Check Python files for syntax errors."""
    issues: List[str] = []
    if os.path.isfile(path) and path.endswith(".py"):
        files_to_walk: List[str] = [os.path.abspath(path)]
    else:
        files_to_walk = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    files_to_walk.append(os.path.join(root, f))

    for fp in files_to_walk:
        ok, lines = read_text_file(fp)
        if not ok:
            issues.append(f"Cannot read {fp} as UTF-8 text")
            continue
        src = "\n".join(lines) + "\n"
        try:
            ast.parse(src, filename=fp)
        except SyntaxError as e:
            lineno = getattr(e, "lineno", "?")
            issues.append(f"SyntaxError in {fp}:{lineno}: {e.msg}")
    return issues


def is_snake_case(name: str) -> bool:
    """Check if name follows snake_case convention."""
    return bool(re.match(r"^[a-z_][a-z0-9_]*$", name))


def lint_python_heuristics(path: str) -> List[str]:
    """Apply heuristic linting rules to Python files."""
    issues: List[str] = []

    # Walk files
    python_files: List[str] = []
    if os.path.isfile(path) and path.endswith(".py"):
        python_files = [os.path.abspath(path)]
    else:
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    python_files.append(os.path.join(root, f))

    for fp in python_files:
        ok, lines = read_text_file(fp)
        if not ok:
            continue
        src = "\n".join(lines) + "\n"
        # Use ast to find function and class definitions (more reliable than regex)
        try:
            module = ast.parse(src, filename=fp)
        except Exception:
            # syntax issues handled elsewhere
            module = None

        if module is not None:
            for node in ast.walk(module):
                if isinstance(node, ast.FunctionDef):
                    if not is_snake_case(node.name):
                        issues.append(
                            f"Function name not snake_case {fp}:{node.lineno}: {node.name}"
                        )
                elif isinstance(node, ast.AsyncFunctionDef):
                    if not is_snake_case(node.name):
                        issues.append(
                            f"Async function name not snake_case {fp}:{node.lineno}: {node.name}"
                        )
                elif isinstance(node, ast.ClassDef):
                    # class names should start with uppercase letter (PascalCase)
                    if node.name and node.name[0].islower():
                        issues.append(
                            f"Class name may not be PascalCase {fp}:{node.lineno}: {node.name}"
                        )

        # Line-based heuristics
        assign_no_space_re = re.compile(r"\b\w+=(?!=)")
        compare_none_re = re.compile(r"(==\s*None|!=\s*None)")

        for i, line in enumerate(lines, start=1):
            if assign_no_space_re.search(line):
                issues.append(
                    f"Assignment missing spaces around '=' {fp}:{i}: {line.strip()}"
                )
            if compare_none_re.search(line):
                issues.append(
                    f"Use 'is None' / 'is not None' instead of ==/!= None {fp}:{i}: {line.strip()}"
                )

    return issues


def apply_safe_fixes_file(path: str) -> List[str]:
    """Apply safe, automated fixes to a Python file. Return list of applied fixes."""
    ok, lines = read_text_file(path)
    if not ok:
        return []

    new_lines: List[str] = []
    fixes: List[str] = []
    compare_none_re = re.compile(r"(==\s*None|is\s+not\s+None)")

    for i, line in enumerate(lines, start=1):
        new_line = line
        # Replace "== None" with "is None"
        if "== None" in line:
            new_line = line.replace("== None", "is None")
            fixes.append(f"Line {i}: Changed '== None' to 'is None'")
        # Replace "!= None" with "is not None"
        if "!= None" in line:
            new_line = new_line.replace("!= None", "is not None")
            fixes.append(f"Line {i}: Changed '!= None' to 'is not None'")

        new_lines.append(new_line)

    # Write back only if changes were made
    if fixes:
        try:
            with open(path, "w", encoding=ENCODING) as f:
                f.write("\n".join(new_lines) + "\n")
        except IOError as e:
            return [f"Failed to write {path}: {e}"]

    return fixes


def check_project(path: str) -> List[str]:
    """Run all checks on a project directory."""
    reports: List[str] = []

    # Check for pyproject.toml
    pt = os.path.join(path, "pyproject.toml")
    if os.path.exists(pt):
        reports.extend(try_parse_toml(pt))
    else:
        reports.append(f"pyproject.toml not found at: {path}")

    # Check Python path
    py_path = os.path.join(path, "src")
    if os.path.exists(py_path):
        reports.extend(check_py_syntax(py_path))
        reports.extend(lint_python_heuristics(py_path))
    else:
        reports.append(f"Python path not found: {py_path}")

    return reports


def apply_safe_fixes(path: str) -> List[str]:
    """Apply safe fixes to all Python files in a path."""
    fixes: List[str] = []

    if os.path.isfile(path) and path.endswith(".py"):
        files = [path]
    else:
        files = []
        for root, _, file_list in os.walk(path):
            for f in file_list:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))

    for target in files:
        if os.path.exists(target):
            fixes.extend(apply_safe_fixes_file(target))
        else:
            fixes.append(f"File not found: {target}")

    return fixes


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Lightweight project linter and fixer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--check-project",
        action="store_true",
        help="Check entire project (requires --path)",
    )
    parser.add_argument(
        "--check-toml", action="store_true", help="Check TOML file (requires --file)"
    )
    parser.add_argument(
        "--check-py", action="store_true", help="Check Python syntax (requires --path)"
    )
    parser.add_argument(
        "--lint", action="store_true", help="Run linting heuristics (requires --path)"
    )
    parser.add_argument(
        "--apply-fixes", action="store_true", help="Apply safe fixes (requires --path)"
    )
    parser.add_argument("--path", type=str, help="Path to file or directory")
    parser.add_argument("--file", type=str, help="Path to specific file")

    args = parser.parse_args()

    reports: List[str] = []

    if args.check_project:
        if not args.path:
            parser.error("--check-project requires --path")
        reports.extend(check_project(args.path))
    elif args.check_toml:
        if not args.file:
            parser.error("--check-toml requires --file")
        reports.extend(try_parse_toml(args.file))
    elif args.check_py:
        if not args.path:
            parser.error("--check-py requires --path")
        reports.extend(check_py_syntax(args.path))
    elif args.lint:
        if not args.path:
            parser.error("--lint requires --path")
        reports.extend(lint_python_heuristics(args.path))
    elif args.apply_fixes:
        if not args.path:
            parser.error("--apply-fixes requires --path")
        reports.extend(apply_safe_fixes(args.path))
    else:
        parser.print_help()
        sys.exit(1)

    if reports:
        print("\n".join(reports))
    sys.exit(0)


if __name__ == "__main__":
    main()
