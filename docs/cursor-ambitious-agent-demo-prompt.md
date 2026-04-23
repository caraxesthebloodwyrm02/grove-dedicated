# Ambitious Cursor demo — one-shot agent prompt (copy into a new **Agent** chat)

Use the block below as the **entire user message** (or save as a Cursor **Project Command** / pinned snippet and invoke it when you want a capability showcase run).

---

## The prompt (paste everything under "START" to end of "END")

**START**

You are running a **Cursor capability demonstration** in the **Mangrove / grove** repo. Your goal is not “finish a random feature” but to **exercise native Cursor product surface area** in one coherent session: **plan → execute → verify → hand off**, with **visible progress**, **custom artifacts**, and **delegation** where the product allows it.

### Non-negotiables

1. **Runtime TODOs (live checklist)**
  - Create a structured task list at the start (use whatever todo affordance the IDE exposes in this environment; if none, use a markdown task list in `docs/cursor-demo-runtime-todo.md` and keep it updated every phase).  
  - Mark items **in progress** only while you are actually doing them, then **completed** when done.  
  - The todo list is part of the demo: it must reflect **real** work, not decor.
2. **Feature-rich “native” actions** (hit as many as are safe and available in *this* session)
  Aim to touch **several** of the following, with short evidence in your final report (file path, keybinding or UI surface, or command name):
  - **Repository intelligence**: search across the repo (semantic or ripgrep), read related files, trace how something works.  
  - **Multi-file + minimal-diff discipline**: only change what the demo requires; no drive-by refactors.  
  - **Terminal** where appropriate (install, format, one-shot script, or `ls` to confirm paths) — you have shell access; do not only describe commands.  
  - **MCP** (if configured): discover tools by schema, call one with correct arguments, cite what you used.  
  - **Browser / app surface** (if the Browser MCP is enabled): one deliberate navigation or snapshot to prove integration; if blocked, say what was missing.  
  - **Workspace or cross-root awareness**: this repo may be a multi-root workspace; if so, name which root you used for what.  
  - **Rules / skills alignment**: if `.cursor/rules`, `AGENTS.md`, or project skills exist, read what applies and follow them for this repo.
3. **Custom assets (deliverables you create)**
  Produce **at least three** distinct artifacts under `docs/cursor-demo-assets/` (create the directory):
  - **A1 — “Demo brief”** (`brief.md`): 12–20 lines, what you did, which Cursor actions you used, and what you would add with more time.  
  - **A2 — “Capability matrix”** (`matrix.md`): a small table mapping **capability** → **what you did** → **path or proof**.  
  - **A3 — Custom asset of your choice** (choose one that fits the repo culture), e.g.:  
    - a `tokens`-style JSON snippet (`mangrove-demo-tokens.json`) with 6–10 keys, **or**  
    - a single HTML or SVG “forest canopy” mini-preview (static, no build), **or**  
    - a Mermaid diagram file (`.mmd` or embedded in md) of your execution flow.
4. **Subagents / commands (delegation & boundaries)**
  - If the environment offers **subagents** or a **Task** tool, use **one** focused delegation (e.g. read-only explore pass or shell specialist) and **merge** the result into the mainline narrative—do not fork unrelated work.  
  - If **Cursor Project Commands** or **slash** hooks exist in this project, reference them by name; if they do not, state “not present” and **propose** one command string you would add (single sentence) without inventing file paths you did not verify.
5. **Verification**
  - End with a **3-part summary**: (a) what shipped to disk, (b) which native surfaces were touched, (c) one honest limitation of this run.

### Suggested story arc (you may adjust, but keep it one thread)

- **Phase 0 — Orient**: read `mangrove-biome.code-workspace` and `README` or `CLAUDE.md` if present; state the workspace’s intent in one paragraph.  
- **Phase 1 — Map**: produce a one-screen map of `grove/` (tree of important dirs, or a short bullet outline).  
- **Phase 2 — Touch**: one **small** code or config change that is *reversible* and **harmless** (e.g. a comment in a non-critical file, or a doc link fix)—or skip with justification if the repo is too sensitive.  
- **Phase 3 — Bundle**: write the three assets, sync todos, final report.

### Style

- **Measured, precise** language; no hype; **em-dash** for inline breaks; use `→` only in small flow notes if needed.  
- Cite real paths:  `/home/irfankabir/CascadeProjects/grove/...` when absolute helps reproducibility.

**END**

---

## How to use

1. Open **Agent** in Cursor (this repo as workspace).
2. Paste **only** the content between **START** and **END** (or the whole section if you prefer the framing).
3. Let the run complete; then inspect `docs/cursor-demo-assets/` and the runtime todo file.

## Optional: register as a Project Command (Cursor 0.4x+)

If your Cursor version supports **Project Commands**, add a short command in `.cursor` that **includes** a `@`-reference to this file so the agent loads the spec from disk—keeps a single source of truth.

---

*Mangrove Biome — demo harness; safe to delete after review.*