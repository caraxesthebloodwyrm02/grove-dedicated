# Grove workspace

This directory holds repositories for the `irfankabir02` GitHub account. It is **not** a single installable Python tree: do not create one virtual environment for all of `grove/`.

## Where to put a virtual environment

| Area | Role | Venv rule |
| --- | --- | --- |
| [`Vision/`](Vision/) | Active **vision-ui** project (`pyproject.toml`, Python 3.13+). Resolves to the real git checkout under `CascadeProjects/Projects/Vision`. | Create and use **`.venv/` only inside `Vision/`** (same directory as `pyproject.toml` and `uv.lock`). |
| [`archive/`](archive/) | Historical or inactive trees (mixed `pyproject.toml` / `requirements.txt`). | **One `.venv` per subproject** you are actually editing, at **that** project’s root—never a shared env for all of `archive/`. |

Authoritative commands for Vision (sync, tests, lint, CLI) live in [`Vision/CONTRIBUTING.md`](Vision/CONTRIBUTING.md) (open via the symlink path above).
