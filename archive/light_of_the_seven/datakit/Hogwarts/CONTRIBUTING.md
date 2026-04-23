# Contributing to the Hogwarts Visualization & Parseltongue CLI

This directory is a small, self-contained Hogwarts micro-project:

- `parseltongue_cli.py` – TemporalPatronus implementation + CLI
- `test_parseltongue_cli.py` – tests
- `HOGWARTS.md` + lore chapters – narrative and documentation

The goal of this guide is to keep **code, tests, and lore coherent** and
minimize confusion for anyone extending the project.

---

## General Principles

- **Stay self-contained.**  
  Use only the Python standard library. Avoid adding external
  dependencies unless absolutely necessary.

- **Keep code and prose in sync.**  
  When you change behavior in `parseltongue_cli.py`, update:
  - `test_parseltongue_cli.py` (tests)
  - `HOGWARTS.md` (technical doc)
  - Any relevant lore files (e.g. Snape chapters) that describe that
    behavior.

- **Prefer clarity over cleverness.**  
  This project is half educational, half narrative. Write code and prose
  that a future reader can understand without re-watching the original
  videos.

- **Respect source attribution.**  
  Keep the acknowledgement and chapter disclaimers intact. If you draw
  from new sources, add them to `ACKNOWLEDGEMENT.md`.

---

## Code Changes (`parseltongue_cli.py`)

- **Style & structure**
  - Keep using type hints (`-> int`, `-> str`, etc.).
  - Maintain the fluent interface pattern in `TemporalPatronus`.
  - If you add new presets, follow the pattern of
    `snapes_doe()` / `harry_later_years()`.

- **CLI behavior**
  - Extend `build_parser()` carefully if you add more presets or
    commands.  
  - Ensure the module docstring **Usage examples** section reflects the
    actual CLI arguments.

- **New features**
  - For new TemporalPatronus presets:
    - Give them clear, lore-aligned names (e.g.
      `hermione_ministry_years`).
    - Choose a caster, memory, form, and temporal anchors that tell a
      coherent story.
  - For new CLI commands or modes, document them in `HOGWARTS.md` and, if
    they relate to a specific character, in the appropriate lore file.

---

## Tests (`test_parseltongue_cli.py`)

- **Always add or update tests** when you change behavior.

- For new presets:
  - Add a test that:
    - Instantiates the preset (e.g.
      `TemporalPatronus.hermione_ministry_years()`),
    - Calls `manifest()`,
    - Asserts that key lines (caster, form, memory, anchors) appear in
      the output.

- For CLI changes:
  - Extend `CLITests` with a new method that:
    - Calls `main([...])` with your new argument,
    - Asserts `exit_code == 0`,
    - Asserts that the expected caster/form appear in the captured
      output.

- Run tests from this directory:

  ```bash
  python -m unittest test_parseltongue_cli
  ```

---

## Documentation & Lore

- **HOGWARTS.md**
  - Use this as the primary technical doc for `TemporalPatronus` and the
    CLI.
  - When adding new presets or CLI options, add a short, clear section
    explaining what they represent and how to call them.

- **Snape chapters** (`SSSEVERUS SNAPE/`)
  - Chapter 1 is biographical; Chapter 2 already integrates
    `TemporalPatronus` concepts.  
  - If you change how `snapes_doe()` works, or add new Snape-related
    presets, consider whether Chapter 2 needs an update to stay
    consistent.

- **Other lore docs** (`salazar_slytherin.md`, future chapters)
  - Keep the tone consistent: analytical, in-universe, and clearly
    labelled as fan-made, educational summaries.
  - If you introduce new code concepts (e.g. a Salazar-related class or
    CLI mode), you may add short "How this connects to the code" boxes to
    keep the mapping explicit.

---

## Housekeeping

- **File locations**
  - Keep all Python files (`*.py`) at the top level of this Hogwarts
    directory.
  - Keep character-specific lore grouped in subfolders (e.g.
    `SSSEVERUS SNAPE/`).

- **Version control hygiene**
  - Do not commit `__pycache__/` contents; add them to `.gitignore` at a
    higher level if needed.
  - Use descriptive commit messages that mention the area you touched
    (e.g. `cli: add hermione ministry preset`, `docs: link salazar essay
    to parseltongue cli`).

By following these guidelines, you help keep this Hogwarts micro-project
coherent: code, tests, and stories all telling the same tale from
slightly different angles.
