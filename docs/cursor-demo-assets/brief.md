# Demo brief — Cursor native surface (grove)

This session exercised plan → execute → verify → hand off against the Mangrove Biome multi-root workspace file at `/home/irfankabir/CascadeProjects/grove/mangrove-biome.code-workspace`, with concrete work anchored in the **grove** root (not the whole CascadeProjects tree).

**What ran:** IDE **Todo** list for phase tracking; **Read** on workspace JSON and `README.md`; **SemanticSearch** (empty hit on tokens query, noted); **terminal** `rg`, `find`, `python3 -m py_compile`; **StrReplace** for one comment line in `mangrove_palette_spectrum.py`; **WebFetch** MCP to `https://example.com` as a schema-driven fetch smoke test; **Task** tool with `subagent_type: explore` for a read-only directory map.

**Roots used:** Primary edits and assets under `Ⅴ TASTE ② grove` (`/home/irfankabir/CascadeProjects/grove`). Workspace orientation used the workspace file that names many folders (Cascade, Vision, design, `.cursor`, `roots`, `grove-dedicated`, etc.). User rule **home-meta** (concise, terminal for truth) was applied.

**Rules / skills:** Read `/home/irfankabir/.cursor/rules/home-meta.mdc`. No repo-local `CLAUDE.md` at grove root; sampled `archive/light_of_the_seven/CLAUDE.md` for culture context.

**Project Commands / hooks:** No `commands.json` or `hooks.json` under grove (verified with `find`); Browser MCP not in this agent’s tool schema.

**One-screen map (grove root):**

- Top-level: policy and exercise markdown, `README.md`, `TASK_TRACKER.md`, `Vision` symlink, `archive/`, `docs/`, `grove-dedicated/`, palette HTML/JSON, `mangrove_palette_spectrum.py`, `mangrove-biome.code-workspace`.
- `docs/`: demo prompts, `research/` notes (`canonical-bibliography.md`, etc.).
- `grove-dedicated/`: parallel “long games” tree (mirrors docs shape; not edited this run).

**With more time:** Add a Project Command string like “Run Mangrove demo: @docs/cursor-ambitious-agent-demo-prompt.md” (file verified at `/home/irfankabir/CascadeProjects/grove/docs/cursor-ambitious-agent-demo-prompt.md`); add `pre-commit` or `ruff` only where a real Python package root exists; run Playwright if a served app root is chosen.
