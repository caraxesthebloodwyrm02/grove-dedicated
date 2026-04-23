## 1. File analyzed

I scanned the Story EQ package:

- [full_datakit/story_eq/__init__.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/__init__.py:0:0-0:0)
- [full_datakit/story_eq/config.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/config.py:0:0-0:0)
- [full_datakit/story_eq/errors.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/errors.py:0:0-0:0)
- [full_datakit/story_eq/models.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/models.py:0:0-0:0)
- [full_datakit/story_eq/parser.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/parser.py:0:0-0:0)
- [full_datakit/story_eq/validation.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/validation.py:0:0-0:0)
- [full_datakit/story_eq/ui/__init__.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/ui/__init__.py:0:0-0:0)

All of these are **syntactically valid** Python. No syntax errors or obvious runtime crashes in the core modules; the only hard failure risk is the missing UI modules referenced by [story_eq.ui.__init__](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/visualizations/Hogwarts/hogwarts_toolkit.py:35:4-41:51).

---

## 2. [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0) contents (red = bugs, yellow = info/lint)

The file is now a **valid JSON array**:

```json
[
  {
    "color": "red",
    "type": "bug",
    "file": "story_eq/ui/__init__.py",
    "line": 29,
    "message": "Lazy UI exports refer to modules (window.py, timeline_canvas.py, panels.py) that do not exist yet; accessing MainWindow, TimelineCanvas, TraitPanel, or ScenePanel will raise ImportError.",
    "notes": "Create the referenced UI modules or temporarily remove these exports to silence runtime import errors and editor diagnostics."
  },
  {
    "color": "yellow",
    "type": "lint",
    "file": "story_eq/config.py",
    "line": 14,
    "message": "Type alias RGBTuple is defined but never used.",
    "notes": "Either remove RGBTuple or start using it for color triplets to avoid unused-symbol warnings."
  },
  {
    "color": "yellow",
    "type": "lint",
    "file": "story_eq/config.py",
    "line": 247,
    "message": "DEFAULT_CONFIG is instantiated at import time with base_dir set to the current working directory.",
    "notes": "This can be surprising if the process changes working directories. Consider constructing StoryEQConfig explicitly at call sites instead of relying on a global instance."
  },
  {
    "color": "yellow",
    "type": "docs",
    "file": "story_eq/__init__.py",
    "line": 7,
    "message": "Docstring mentions 'TriageCase' as a core export, but no such class exists in story_eq.",
    "notes": "Either remove TriageCase from the documentation or add a matching data model if it is intended to exist."
  },
  {
    "color": "yellow",
    "type": "lint",
    "file": "story_eq/parser.py",
    "line": 227,
    "message": "Known sections set includes 'scene' even though scenes are only stored in scenes_raw, so 'scene' will never appear in sections.",
    "notes": "Harmless, but may confuse future readers; consider removing 'scene' from known_sections or adjusting section handling."
  }
]
```

### Interpretation

- **Red (bug)**  
  - [story_eq/ui/__init__.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/ui/__init__.py:0:0-0:0):
    - [__getattr__](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/ui/__init__.py:26:0-43:74) tries to import .window, .timeline_canvas, .panels, but those files don’t exist yet.
    - Any code doing from story_eq.ui import MainWindow (or similar) will raise ImportError.

- **Yellow (info / lint / docs)**  
  - [config.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/config.py:0:0-0:0):
    - RGBTuple currently unused.
    - DEFAULT_CONFIG uses Path.cwd() at import time; could be surprising if cwd shifts.
  - [__init__.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/__init__.py:0:0-0:0):
    - Docstring still mentions [TriageCase](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/visualizations/static/smartdecisor.py:73:0-107:9), which doesn’t exist in [story_eq](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0).
  - [parser.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/parser.py:0:0-0:0):
    - known_sections includes "scene", but scene sections are never stored in sections (they go into scenes_raw), so that branch never fires.

---


## 1. Goals of the debugging plan

- **Make failures explain themselves**  
  When something breaks (or feels “off”), you should be able to see *where* and *why* without guesswork.

- **Respect the project’s layered design**  
  Debug at the right layer: datakit CLI, [core](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/core:0:0-0:0) loader/explorer, [visualizations](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/visualizations:0:0-0:0), [story_eq](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0), not all at once.

- **Plant reusable “debug seeds”**  
  Small, repeatable scenarios: sample context files, debug entrypoints, and [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0) tasks that you can re-run.

---

## 2. Layered map of [full_datakit](cci:7://file:///e:/grid/light_of_the_seven/full_datakit:0:0-0:0) (for debugging)

- **Top level**
  - [datakit.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/datakit.py:0:0-0:0) – main CLI / interactive app.
  - [core/](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/core:0:0-0:0) – configuration, context loader, interactive explorer.
  - [data/](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/data:0:0-0:0) – JSON/YAML contexts.
  - [visualizations/](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/visualizations:0:0-0:0) – static/interactive plots (circle_graph, smartdecisor, Hogwarts tools).
  - [story_eq/](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0) – Hogwarts Story EQ (parser, models, validation, future UI).

- **Key responsibilities**
  - **core.config** – user settings, theme.
  - **core.loader** – ContextLoader, load_context().
  - **core.explorer** – interactive flows, menus, visualizations hook.
  - **[story_eq](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0)** – parses .ini-like story files to [StoryContext](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/models.py:74:0-121:47), validates, later visualizes.
  - **[.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0)** – project‑local “what to look at” list (we’ve already started this).

---

## 3. Phase 1 – Context-driven “health check” scenarios

Think in *scenarios*, not just files. For each scenario, you’ll later attach debug tasks / breakpoints.

- **Scenario A: Start DataKit normally**
  - Command: python datakit.py 
  - Expected:
    - Default context loads (Circle of Fifths).
    - Main menu shows without tracebacks.
  - Debug focus:
    - core.config.get_config() 
    - core.loader.ContextLoader default data directory.
    - core.explorer.InteractiveExplorer.run() entry.

- **Scenario B: Load a specific JSON/YAML context**
  - Command: python datakit.py -c data/<file>.json 
  - Debug focus:
    - JSON/YAML decoding errors.
    - _parse_context_data in core.loader.

- **Scenario C: Run a visualization tool directly**
  - Static: python visualizations/static/circle_graph.py --no-show 
  - Static: python visualizations/static/smartdecisor.py --no-show (if you add such a flag later).
  - Debug focus:
    - Path resolution (PROJECT_ROOT, DATA_DIR).
    - Missing optional dependencies (e.g., matplotlib / networkx).

- **Scenario D: Parse a Story EQ .ini file**
  - (Future) python -m full_datakit.story_eq.cli path/to/story.ini 
  - For now: direct use in a REPL:
    ```python
    from pathlib import Path
    from story_eq.parser import parse_story_file
    from story_eq.validation import validate_context

    result = parse_story_file(Path("examples/story_eq_hermione.ini"))
    errs = result.errors
    ```
  - Debug focus:
    - [story_eq.parser.parse_story_file](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/parser.py:55:0-99:48) → [_parse_content](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/parser.py:102:0-189:68) → [_build_context](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/parser.py:207:0-258:54).
    - [story_eq.validation.validate_context](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/validation.py:37:0-58:17).

---

## 4. Phase 2 – Planting observability (logging + debug hooks)

You don’t have to wire logging everywhere at once. Start with *choke points*.

- **Core loader / explorer**
  - **Add optional debug logging** (guarded by a config flag) to:
    - [ContextLoader.__init__](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/visualizations/Hogwarts/hogwarts_toolkit.py:35:4-41:51) (data directory used).
    - ContextLoader.load_json/load_yaml (file path, size, success/failure).
    - InteractiveExplorer.run (context name, mode).
  - Plant: a single DEBUG mode (env var or config flag) that makes these logs print to stdout.

- **Story EQ**
  - In story_eq.parser:
    - Optional “trace parse” flag where each section header and scene index is logged once.
    - When adding [ParseResult.error_summary()](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/errors.py:114:4-131:31), print that in debug mode after parsing.
  - In story_eq.validation:
    - Add a helper debug_validate(path) function (later) that parses + validates + prints a short report.

- **Visualizations**
  - For [smartdecisor.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/visualizations/static/smartdecisor.py:0:0-0:0) (already has a triage log):
    - Treat the existing triage log as a **debug artifact**: ensure it always includes:
      - input_path, number of triage cases, any cases dropped for being out-of-range.

You can drive all of this by a simple convention:

- **Env var** GRID_DEBUG=1 or
- CLI flag --debug at top‑level tools, passed down as needed.

---

## 5. Phase 3 – Per‑subsystem debugging “recipes”

### 5.1 [core](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/core:0:0-0:0) + [datakit.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/datakit.py:0:0-0:0)

- **Debug recipe 1: Context load failures**
  - Attach breakpoints or logging in:
    - ContextLoader.load_json / load_yaml.
    - _parse_context_data.
  - When a context fails to load:
    - Log filepath, exists?, size, and the first ~200 chars of content if decode fails.

- **Debug recipe 2: Exploration crashes**
  - Watch:
    - InteractiveExplorer.run, _show_main_menu, _visualizations.
  - Add a small try/except around “visualizations” dispatch that:
    - Logs the exception type and message.
    - Mentions which visualization was being opened.

### 5.2 [story_eq](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0) backend (already mostly in place)

- **Parser**
  - [ErrorSeverity](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/errors.py:18:0-23:19) + [ValidationError](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/errors.py:26:0-61:42) + [ParseResult](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/errors.py:64:0-131:31) are good foundations.
  - Debug focus:
    - Unrecognized lines → captured with line number, section, source.
    - Missing [profile] → we already return an error [ParseResult(context=None, errors=..)](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/errors.py:64:0-131:31).
  - Plant:
    - A tiny helper in a REPL / scratch file:
      ```python
      from story_eq.parser import parse_story_file
      print(parse_story_file(PATH).error_summary())
      ```

- **Models**
  - [Trait.__post_init__](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/models.py:43:4-45:51) and [Scene.__post_init__](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/models.py:66:4-71:9) already clamp values and normalize; these are “automatic fixes”.
  - Plant:
    - If you need to debug weird trait ranges, you can add a temporary assert/log in [__post_init__](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/models.py:43:4-45:51) to see raw inputs.

- **Validation**
  - [validate_context](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/validation.py:37:0-58:17) and [is_valid](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/validation.py:207:0-218:69) already encapsulate semantic checks.
  - Plant:
    - When integrating with a future UI, call [validate_context(ctx)](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/validation.py:37:0-58:17) once and show:
      - Errors in red.
      - Warnings in yellow.
      - Info as subtle hints.

### 5.3 story_eq.ui (future)

- Current state:
  - [story_eq/ui/__init__.py](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/ui/__init__.py:0:0-0:0)’s lazy exports reference window.py, timeline_canvas.py, panels.py that don’t exist yet. That’s marked as a **red bug** in [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0).
- Debug planting for later:
  - For each UI module (window.py, timeline_canvas.py):
    - Implement a [main()](cci:1://file:///e:/grid/light_of_the_seven/full_datakit/visualizations/static/smartdecisor.py:613:0-708:52) or demo() function that:
      - Loads a tiny demo [StoryContext](cci:2://file:///e:/grid/light_of_the_seven/full_datakit/story_eq/models.py:74:0-121:47) (hardcoded or from [examples/](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/examples:0:0-0:0)).
      - Opens the window and draws once.
    - Add a [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0) entry for “Run Story EQ demo window”.

---

## 6. Phase 4 – Tooling: [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0) and test seeds

You already saw how we used [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0) as a **map of problems**. You can extend this as a **map of debug tasks**.

- **For each key scenario**, consider adding one entry with:
  - color: "yellow" for “run this to inspect behavior”.
  - A short message describing the scenario.
  - Optional notes with the exact command to run.

Examples you might add later (manually):

- **DataKit context list**
  ```json
  {
    "color": "yellow",
    "type": "task",
    "file": "datakit.py",
    "line": 473,
    "message": "List available DataKit contexts to verify loader wiring.",
    "notes": "Run: python datakit.py --list"
  }
  ```

- **Story EQ parser smoke test**
  ```json
  {
    "color": "yellow",
    "type": "task",
    "file": "story_eq/parser.py",
    "line": 56,
    "message": "Parse demo Hermione Story EQ file and print error summary.",
    "notes": "In REPL: from story_eq.parser import parse_story_file; from pathlib import Path; print(parse_story_file(Path('examples/story_eq_hermione.ini')).error_summary())"
  }
  ```

---

## 7. How to use this plan

- **Short term**:
  - Keep [.zed/debug.json](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/.zed/debug.json:0:0-0:0) as your **live index** of:
    - Red: real breakage risks.
    - Yellow: design/lint/doc mismatches worth attention.
  - Use the scenarios in Phase 1 as your “go‑to” when something feels off.

- **Medium term**:
  - As you implement [story_eq](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0) UI and more visualizations, always:
    - Add one small debug entry.
    - Add one tiny demo context or CLI path.
  - This keeps insights about execution close to where the code lives.

- **Long term**:
  - If something breaks, first ask:
    - Which layer? (datakit CLI, [core](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/core:0:0-0:0), [visualizations](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/visualizations:0:0-0:0), [story_eq](cci:7://file:///e:/grid/light_of_the_seven/full_datakit/story_eq:0:0-0:0)?)  
    - Which scenario from Phase 1 best matches?  
    - What logs / debug seeds exist there?
