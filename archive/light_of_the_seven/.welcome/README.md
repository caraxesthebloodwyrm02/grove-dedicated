# 🗂️ GRID Workspace — Startup Dashboard

```
   ██████╗ ██████╗ ██╗██████╗     ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗  ██████╗███████╗
  ██╔════╝ ██╔══██╗██║██╔══██╗    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
  ██║  ███╗██████╔╝██║██║  ██║    ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗██████╔╝███████║██║     █████╗  
  ██║   ██║██╔══██╗██║██║  ██║    ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝  
  ╚██████╔╝██║  ██║██║██████╔╝    ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║     ██║  ██║╚██████╗███████╗
   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝      ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝
```

> **Welcome to the GRID master workspace!**  
> This dashboard provides navigation, quick-start commands, and key insights for productive development.

---

## ⚡ Quick Start (30 Seconds)

```bash
# 1️⃣ Initialize environment (verify Python)
Ctrl+Shift+P → Tasks: Run Task → █ STARTUP · Initialize Environment

# 2️⃣ Install dependencies
Ctrl+Shift+P → Tasks: Run Task → █ INSTALL · GRID (Editable)

# 3️⃣ Start the API server
Ctrl+Shift+P → Tasks: Run Task → █ SERVER · Circuits API (8002)

# 4️⃣ Check workspace health
Ctrl+Shift+P → Tasks: Run Task → █ STARTUP · Workspace Status
```

---

## 🏛️ Workspace as Event Venue (Floors)

**Basement (Registry):** Sign-in/out so sessions stay coherent.

- **Check-in task:** `🏛️ EVENT · Check In (Basement)`
- **Check-out task:** `🏛️ EVENT · Check Out (Basement)`
- **Recent log:** `🏛️ EVENT · Recent Check-Ins (Tail)`
- **Log file:** `logs/sessions/checkins.jsonl`

**2nd Floor (Research Lab):** Exploration without pressure.

- `src/light_of_the_seven/`, `archival/` (experiments, prototypes, notebooks)

**4th Floor (Documentation):** Clear maps and orientation.

- `.welcome/`, `docs/`, `.claude/`

**7th Floor (Governance):** Rules that keep it calm, not crowded.

- `.windsurf/rules/`

**8th Floor (Quality):** Tests + workflows to keep the line stable.

- `tests/`, `workflows/`, `.github/workflows/`

**16th Floor (Core Runtime):** Where execution lives.

- `grid/`, `application/`

---

## 🎯 Workspace Tier System

| Tier | Color | Purpose | Key Folders |
|:----:|:-----:|---------|-------------|
| **1** | 🟦 | **Core Systems** | `grid/` `src/` |
| **2** | 🟪 | **Infrastructure** | `backend/` `AGENT/` `agent_service/` `mothership/` |
| **3** | 🟫 | **Tools & Schemas** | `schemas/` `tools/` |
| **4** | 🟧 | **Documentation** | `light_of_the_seven/` `docs/` `.claude/` `.windsurf/` |
| **5** | 🟩 | **Quality** | `tests/` `workflows/` `demos/` |
| **6** | 🟦 | **Operations** | `scripts/` `infra/` |
| **7** | 🟨 | **Integrations** | `integrations/` `schemas/` |

---

## 🔗 Platform Integration Layer

GRID integrates with multiple platforms through a structured resonance schema.

### Active Platform Integrations
| Platform | Tier | Primary Component | Connection Path |
|----------|:----:|-------------------|-----------------|
| **Windsurf** | 7 | Intelligence | `.windsurf/rules/` |
| **Databricks** | 2 | Infrastructure | `backend/databricks/` |
| **Claude** | 4 | Documentation | `.claude/` |

### Adding a New Platform
1.  **Define Schema**: Create `integrations/<name>/integration.json`.
2.  **Verify Resonance**: Run `█ TEST · Integration <name>`.
3.  **Sync Branch**: Use `git-topic` with `--theme <name>`.

See `.windsurf/rules/grid-platform-integration.md` for full governance.

---

## 📚 Key Resources & Scaffolds

### 🤖 AI Context (`.claude/`)
| File | Purpose |
|------|---------|
| `QUICK_START.md` | Rapid onboarding guide |
| `ARCHITECTURE_REFERENCE.md` | System design overview |
| `INDEX.md` | Master index of all documentation |
| `context.json` | Structured context for AI agents |
| `opus_context.md` | Extended context for Claude Opus |

### 🏄 Windsurf Config (`.windsurf/`)
| Folder | Purpose |
|--------|---------|
| `rules/` | Custom rules and conventions |
| `workflows/` | Automated workflow definitions |

### 🤖 Agent System (`AGENT/` + `agent_service/`)
| Component | Description |
|-----------|-------------|
| `AGENT/api/router.py` | Agent API endpoints |
| `agent_service/main.py` | Agent runtime service |
| Pattern analysis | Entity extraction & relationship mapping |

### 🔄 Workflows (`workflows/`)
| File | Purpose |
|------|---------|
| `update.ps1` | Daily update automation |
| Various YAML | CI/CD pipeline definitions |

### 🔧 Tools (`tools/`)
| Tool | Description |
|------|-------------|
| `pulse_monitor.py` | System health monitoring |
| `ambient_sound.py` | Audio generation tools |
| `zoology_mapper.py` | Entity classification |

---

## 🚀 Essential Tasks (By Category)

### 📦 Installation
| Task | Description |
|------|-------------|
| `█ INSTALL · GRID (Editable)` | Install package in dev mode |
| `█ INSTALL · Dependencies` | Install from requirements.txt |
| `█ INSTALL · Dev Tools` | Install pytest, ruff, pyright |

### 🌐 Servers
| Task | Port | Description |
|------|:----:|-------------|
| `█ SERVER · Circuits API` | 8002 | Main API server |
| `█ SERVER · Grid Portal` | 8000 | Web portal |

### 🧪 Testing
| Task | Description |
|------|-------------|
| `█ TEST · Run All` | Full test suite |
| `█ TEST · Run Fast` | Skip slow tests |
| `█ TEST · Current File` | Test active file only |
| `█ TEST · Coverage` | Generate coverage report |

### 🔍 Quality
| Task | Description |
|------|-------------|
| `█ LINT · Ruff Check` | Check for issues |
| `█ LINT · Ruff Fix` | Auto-fix issues |
| `█ FORMAT · Ruff Format` | Format all code |
| `█ TYPE · Pyright` | Static type checking |
| `█ QUALITY · Full Check` | Lint + Type + Test |

### 📈 Benchmarks
| Task | Description |
|------|-------------|
| `█ BENCHMARK · Performance` | Standard benchmark |
| `█ BENCHMARK · Heavy Load` | Stress test |
| `█ BENCHMARK · Generate Report` | Create report |

---

## 🛡️ Startup Guardrails

### Environment Variables (Auto-configured)
```
PYTHONPATH     → Includes all source directories
GRID_HOME      → ${workspaceFolder}
GRID_DATA      → ${workspaceFolder}/data
GRID_LOGS      → ${workspaceFolder}/logs
ALLOW_ENTRY    → 1 (enables API access)
```

### Pre-flight Checks
1. **Python Version**: Requires Python 3.11+
2. **Virtual Environment**: `.venv/` recommended
3. **Dependencies**: Run `█ INSTALL · GRID (Editable)` first
4. **Git Hooks**: Run `█ GIT · Setup Hooks` for quality gates

### Quality Gates (Git Hooks)
- **Pre-commit**: Ruff lint, format check, syntax validation
- **Pre-push**: Schema validation, fast tests, type check

---

## 📁 Project Structure Overview

```
grid/
├── 📖 .welcome/          ← YOU ARE HERE
│   └── README.md         ← This startup guide
├── 🤖 .claude/           ← AI context & documentation
├── 🏄 .windsurf/         ← Windsurf rules & workflows
│
├── 🧠 grid/              ← Core intelligence module
│   ├── api/              ← REST API endpoints
│   ├── pattern/          ← Pattern matching engine
│   └── programs/         ← NER & analysis services
│
├── 📦 src/               ← V2 Source Code
│   └── light_of_the_seven/ ← Educational Package
│
├── 🤖 AGENT/             ← Agent platform
│   └── api/router.py     ← Agent endpoints
├── 🤖 agent_service/     ← Agent runtime
│
├── 📐 schemas/           ← JSON schemas
├── 🔧 tools/             ← Utility modules
├── 📊 mothership/        ← Dashboard UI
│
├── 🧪 tests/             ← Test suite
│
├── 📄 docs/              ← Documentation
└── 🔄 workflows/         ← Process automation
```

---

## ⌨️ Keyboard Shortcuts

| Action | Windows | Description |
|--------|---------|-------------|
| Command Palette | `Ctrl+Shift+P` | Access all commands |
| Quick Open | `Ctrl+P` | Open files by name |
| Terminal | `` Ctrl+` `` | Toggle integrated terminal |
| Run Task | `Ctrl+Shift+P` → "Run Task" | Execute workspace tasks |
| Search Files | `Ctrl+Shift+F` | Search across workspace |
| Go to Symbol | `Ctrl+Shift+O` | Navigate to functions/classes |

---

## 🔥 Hot Paths (Most Used)

### Daily Development Flow
```
1. █ STARTUP · Workspace Status     → Check health
2. █ SERVER · Circuits API (8002)   → Start server
3. █ TEST · Run Fast                → Quick validation
4. █ LINT · Ruff Fix                → Clean up code
```

### Before Commit
```
1. █ QUALITY · Full Check           → Lint + Type + Test
2. █ FORMAT · Ruff Format           → Ensure formatting
```

### Investigation & Debugging
```
1. █ TEST · Current File            → Debug specific test
2. █ BENCHMARK · Performance        → Check performance
3. █ STARTUP · Workspace Status     → Review overall state
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Import errors** | Run `█ INSTALL · GRID (Editable)` |
| **Tests not found** | Check PYTHONPATH in terminal |
| **API won't start** | Ensure `ALLOW_ENTRY=1` |
| **Slow startup** | Run `█ CLEAN · Build Artifacts` |
| **Type errors** | Run `█ TYPE · Pyright Check` |

### Reset Everything
```bash
# Clean artifacts
python -c "import shutil; [shutil.rmtree(p, True) for p in ['dist', 'build', '__pycache__', '.pytest_cache']]"

# Reinstall
pip install -e ".[dev]"

# Verify
python scripts/workspace_status.py --format full
```

---

## 📊 Status Indicators

Run `█ STARTUP · Workspace Status` to see:

```
╔══════════════════════════════════════════════════════════╗
║           🗂️  GRID Workspace Status                      ║
╠══════════════════════════════════════════════════════════╣
║ 🔀 GIT STATUS      → Branch, changes, sync state        ║
║ 🧪 TEST STATUS     → Pass/fail counts                   ║
║ 📊 BENCHMARK       → Performance metrics                ║
║ 🌡️  ENVIRONMENT    → Config validation                  ║
║ 💚 HEALTH          → Overall workspace health           ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🎨 Visual Theme

The workspace uses a **Navy/Amber** color scheme:
- **Navy** (`#0d1b2a`) — Sidebar, panels, terminal
- **Blue** (`#1e3a5f`) — Status bar, active tabs
- **Amber** (`#ffb300`) — Accents, badges, highlights

---

## 📚 Further Reading

| Resource | Path | Description |
|----------|------|-------------|
| Architecture | `.claude/ARCHITECTURE_REFERENCE.md` | System design |
| Quick Start | `.claude/QUICK_START.md` | Onboarding |
| Contributing | `CONTRIBUTING.md` | How to contribute |
| Changelog | `CHANGELOG.md` | Version history |
| API Docs | `docs/` | API documentation |

---

<div align="center">

**🚀 Ready to build something amazing!**

*Press `Ctrl+Shift+P` → `Tasks: Run Task` → `█ STARTUP · Initialize Environment` to begin*

---

Built with 💙 by the GRID Team | Last updated: Auto-generated

</div>