## Purpose
This repository is a tiny, single-file Python project. These instructions tell AI coding agents how to be immediately productive here and where to make sensible changes.

## Quick facts
- Main entry: `hello.py` — currently a two-line script:
  - msg = "Roll a dice!"
  - print(msg)
- No dependencies, no tests, no packaging files.

## How to run (developer flow)
- On Windows PowerShell run:

  python hello.py

  (The workspace default shell is PowerShell; use the active Python interpreter.)

## What an agent should do first
- Read `hello.py` to understand current behavior (it's intentionally minimal).
- If making changes, keep edits minimal and focused (this project is a learning/toy repo).

## Editing and contribution patterns
- Make small, reversible commits. Use clear commit messages like: `feat: add greeting option to hello.py`.
- If you add features, also add a short README.md at repo root describing how to run and any new dependencies.
- If adding any third-party packages, add a `requirements.txt` listing exact pins.

## Project-specific conventions
- Top-level single script. Prefer adding small modules inside a new package directory if project grows (e.g., `src/` or `hello/`) rather than expanding `hello.py` indefinitely.
- Keep CLI entrypoints in `hello.py` or a new `__main__.py` for packages.

## Patterns to follow in code edits
- Use explicit, readable code (avoid clever one-liners). Example style to match: plain variable assignment then `print(...)`.
- No test harness exists — if you add logic, include at least one simple script or `tests/test_basic.py` using `unittest`.

## Integration points and responsibilities
- There are currently no external integrations (APIs, databases, CI). If you introduce them, update the README and add any environment variable docs.

## When merging existing AI guidance
- No `.github/copilot-instructions.md` or AGENT.md files were found in this repo. If you add AI guidance in multiple files, keep the single source here and reference others from the README.

## Minimal examples agents can use
- To add a CLI flag for a custom message, edit `hello.py` and demonstrate usage in README. Keep changes isolated to `hello.py` unless you create a new package.

## When to ask the human
- Ask if you plan to add external dependencies, CI, or restructure into a package. Also ask before making UI/UX changes to the output messaging.

---
If anything here is unclear or you'd like more detailed guidance (tests, CI, packaging), tell me which direction to expand and I'll update this file.
