# Grid/Circuits: Strategic Plan

**Version:** 1.0
**Date:** 2025
**Scope:** Scaling, Income Diversification, Research Facilitation, Workspace Restructuring

---

## Executive Summary

Grid/Circuits is a research platform studying **information propagation as measurable force**. To sustain long-term research while building toward the sensory Goldilocks zone, the project needs:

1. **Scalable architecture** that supports both research and commercial applications
2. **Diversified income streams** that fund research without compromising it
3. **Workspace restructuring** that reflects the project's multi-domain nature

This plan proposes a path where commercial applications and research reinforce each other.

---

## Part 1: Scaling Strategy

### Current State Assessment

The project has multiple domains operating in parallel:

| Domain | Current Location | Purpose | Maturity |
|--------|------------------|---------|----------|
| Core Intelligence | `grid/`, `circuits/` | Information dynamics engine | High |
| Visualization | `light_of_the_seven/`, `mothership/` | Educational + research viz | Medium |
| Agent Services | `AGENT/`, `agent_service/` | AI agent infrastructure | Early |
| Tooling | `SEGA/`, `scripts/` | Utilities + automation | Medium |
| Sensory Layers | `schemas/` | Sound + Vision specs | Defined, not implemented |

### Scaling Priorities

#### Phase 1: Consolidate (Months 1-3)
- Unify the intelligence layer (`grid/` + `circuits/`) as the **single source of truth**
- Implement sound and vision renderers from the schemas we defined
- Create clean API boundaries between domains

#### Phase 2: Productize (Months 4-8)
- Package discrete capabilities as standalone tools:
  - **Relationship Intelligence API** — `/ner/analyze` as a service
  - **Pattern Detection Engine** — real-time anomaly detection
  - **Sensory Dashboard** — vision + sound monitoring interface
- Build embeddable widgets for integration into other platforms

#### Phase 3: Platform (Months 9-12)
- Open the platform for third-party integrations
- Marketplace for sensory "presets" (sound mappings, visualization themes)
- Research collaboration portal

---

## Part 2: Income Diversification

### Revenue Model Framework

The key insight: **research and commerce are not opposites**. The same infrastructure serves both. The question is packaging.

```
┌─────────────────────────────────────────────────────────────────┐
│                     GRID/CIRCUITS ECOSYSTEM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │  RESEARCH   │    │  PRODUCTS   │    │  SERVICES   │        │
│   │  (Mission)  │◄──►│  (Revenue)  │◄──►│  (Revenue)  │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            │                                    │
│                     ┌──────▼──────┐                             │
│                     │   SHARED    │                             │
│                     │   CORE      │                             │
│                     │ (grid/circ) │                             │
│                     └─────────────┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Income Streams

#### Stream 1: Developer Tools (B2D)
**Target:** Developers building applications that need relationship/influence analysis

| Product | Pricing Model | Revenue Potential |
|---------|---------------|-------------------|
| Relationship Analysis API | Per-call + monthly cap | $50-500/mo per customer |
| Pattern Detection SDK | License + support | $200-2000/mo |
| Embeddable Widgets | Freemium + white-label | $100-1000/mo |

**Implementation:**
- Spin off `circuits/` API as a hosted service (Vercel, Railway, or self-hosted)
- Create SDK wrappers (Python, JS, Go)
- Documentation portal with interactive examples

#### Stream 2: Sensory Monitoring Dashboard (B2B)
**Target:** Operations teams, trading floors, crisis response centers

| Product | Pricing Model | Revenue Potential |
|---------|---------------|-------------------|
| Basic Dashboard | SaaS subscription | $200-500/mo |
| Custom Sound Mappings | One-time + maintenance | $1000-5000 |
| Enterprise Integration | Annual license | $10k-50k/year |

**Implementation:**
- Build web dashboard consuming `vision_layer_schema.json` + `sound_layer_schema.json`
- Real-time WebSocket feeds from Grid API
- Custom theming and alert configuration

#### Stream 3: Educational Content (B2C)
**Target:** Learners interested in information dynamics, data visualization, systems thinking

| Product | Pricing Model | Revenue Potential |
|---------|---------------|-------------------|
| Interactive Courses | One-time purchase | $50-200 per course |
| Visualization Toolkit | Freemium + premium | $10-50/mo |
| Workshop Series | Live + recorded | $100-500 per workshop |

**Implementation:**
- Leverage `light_of_the_seven/` educational content
- Build on the Circle of Fifths / directional derivative pedagogy
- Interactive notebooks (Jupyter, Observable)

#### Stream 4: Research Consulting (B2B/B2G)
**Target:** Organizations needing bespoke information dynamics analysis

| Service | Pricing Model | Revenue Potential |
|---------|---------------|-------------------|
| Custom Analysis | Project-based | $5k-50k per project |
| Integration Consulting | Hourly + retainer | $150-300/hr |
| Research Partnerships | Grant + revenue share | Variable |

**Implementation:**
- Build case studies from internal research
- Publish findings to establish credibility
- Network with academic and government institutions

#### Stream 5: Open Source + Sponsorship
**Target:** Community contributions, corporate sponsors

| Model | Approach | Revenue Potential |
|-------|----------|-------------------|
| GitHub Sponsors | Tier-based perks | $500-5000/mo |
| Corporate Sponsorship | Logo placement, priority support | $1k-10k/mo |
| Grants | Research foundations, government | Variable |

---

## Part 3: The Zoology Scope

### Why Zoology?

The project's goal is finding the **sensory Goldilocks zone** — where five senses achieve coherence. Zoology provides critical insights because:

1. **Alternative Sensory Configurations**
   - Dogs: olfactory-dominant (smell as primary information channel)
   - Eagles: visual-dominant (extreme acuity, motion detection)
   - Bats: auditory-dominant (echolocation as spatial mapping)
   - Sharks: electroreception (sensing electrical fields)

2. **Evolved Coherence States**
   - Animals have optimized sensory integration over millions of years
   - Their "Goldilocks zones" are battle-tested by survival
   - We can study what coherence looks like in different configurations

3. **Cross-Species Patterns**
   - Do certain information dynamics trigger universal responses?
   - Are there common "threat signatures" across sensory modalities?
   - What can we learn from predator-prey dynamics about information propagation?

### Zoology Research Directions

#### Direction 1: Sensory Configuration Mapping
Map different species' sensory configurations to our framework:

```
Species         Primary     Secondary    Tertiary    Configuration Type
────────────────────────────────────────────────────────────────────────
Human           Vision      Hearing      Touch       Balanced Visual
Dog             Smell       Hearing      Vision      Olfactory Dominant
Owl             Hearing     Vision       Touch       Auditory Spatial
Octopus         Touch       Vision       Chemo       Distributed Tactile
```

**Application:** Inform alternative sensory mappings for different use cases (e.g., auditory-dominant for visually impaired users).

#### Direction 2: Information Threat Response
Study how different species respond to information signals:

- **Startle Response Timing:** How quickly do different species react to novel stimuli?
- **False Positive Tolerance:** How do animals balance sensitivity vs. alarm fatigue?
- **Group Information Propagation:** How does information spread through flocks, herds, schools?

**Application:** Improve alert system design, reduce false positives, model organizational dynamics.

#### Direction 3: Coherence State Indicators
Identify physiological markers of sensory coherence:

- Heart rate variability (calm vs. stressed)
- Eye movement patterns (focused vs. scanning)
- Breathing rhythms
- Posture and muscle tension

**Application:** Build biofeedback integration for Goldilocks zone detection.

### Zoology Integration Points

| Research Area | Grid/Circuits Component | Application |
|---------------|-------------------------|-------------|
| Sensory configs | Sound/Vision layers | Alternative mapping presets |
| Threat response | Alert channel spec | Optimized alert timing |
| Group dynamics | Relationship analyzer | Multi-entity propagation models |
| Coherence markers | (Future) Biofeedback layer | Real-time state detection |

---

## Part 4: Workspace Restructuring

### Current Problems

1. **Flat hierarchy:** Too many top-level folders without clear categorization
2. **Duplicate concepts:** `grid/grid/`, `circuits/programs/`, `SEGA/` have overlapping code
3. **Missing boundaries:** No clear separation between research, product, and infrastructure
4. **Inconsistent naming:** Mix of snake_case, PascalCase, and SCREAMING_CASE

### Proposed Structure

```
grid/
├── .claude/                    # AI model context (KEEP)
├── .vscode/                    # Editor config (KEEP)
│
├── core/                       # RESEARCH CORE
│   ├── intelligence/           # Information dynamics engine
│   │   ├── entities/           # Entity extraction (NER)
│   │   ├── relationships/      # Influence vector analysis
│   │   ├── patterns/           # Resonance detection
│   │   └── propagation/        # Information flow modeling
│   │
│   ├── sensory/                # Sensory layers
│   │   ├── sound/              # Sound layer implementation
│   │   ├── vision/             # Vision layer implementation
│   │   └── schemas/            # Layer schemas (from /schemas)
│   │
│   └── research/               # Research-specific
│       ├── zoology/            # Cross-species studies
│       ├── psychology/         # Human perception studies
│       └── experiments/        # Experimental code
│
├── platform/                   # PRODUCT PLATFORM
│   ├── api/                    # FastAPI service (from circuits/)
│   │   ├── routers/
│   │   ├── middleware/
│   │   └── schemas/
│   │
│   ├── dashboard/              # Web dashboard
│   │   ├── components/
│   │   ├── visualizations/
│   │   └── audio/
│   │
│   └── sdk/                    # Client SDKs
│       ├── python/
│       ├── javascript/
│       └── go/
│
├── education/                  # EDUCATIONAL CONTENT
│   ├── light_of_the_seven/     # (Relocated)
│   ├── courses/
│   ├── workshops/
│   └── interactive/
│
├── tools/                      # UTILITIES
│   ├── cli/                    # Command-line tools
│   ├── scripts/                # Automation scripts
│   ├── benchmarks/             # Performance testing
│   └── migrations/             # Data migrations
│
├── infrastructure/             # DEPLOYMENT
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   └── ci/
│
├── docs/                       # DOCUMENTATION (KEEP)
│   ├── research/
│   ├── api/
│   ├── guides/
│   └── strategic/              # This document
│
├── tests/                      # TESTING (KEEP)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── data/                       # DATA (gitignored mostly)
│   ├── samples/
│   ├── fixtures/
│   └── exports/
│
└── artifacts/                  # BUILD OUTPUTS (gitignored)
```

### Migration Path

#### Phase 1: Reorganize Without Breaking
1. Create new folder structure alongside existing
2. Add symlinks/aliases for backward compatibility
3. Update imports gradually

#### Phase 2: Consolidate Duplicates
1. Merge `grid/grid/programs/` + `circuits/programs/` → `core/intelligence/`
2. Merge `SEGA/` utilities → `tools/`
3. Relocate `mothership/` → `platform/dashboard/`
4. Relocate `light_of_the_seven/` → `education/`

#### Phase 3: Clean Up
1. Remove deprecated folders
2. Update all documentation
3. Update workspace file

### Updated Workspace Configuration

```json
{
  "folders": [
    {
      "path": ".",
      "name": "🌐 GRID - Root"
    },
    {
      "path": "core/intelligence",
      "name": "🧠 Core - Intelligence"
    },
    {
      "path": "core/sensory",
      "name": "👁️ Core - Sensory"
    },
    {
      "path": "core/research",
      "name": "🔬 Core - Research"
    },
    {
      "path": "platform/api",
      "name": "⚡ Platform - API"
    },
    {
      "path": "platform/dashboard",
      "name": "📊 Platform - Dashboard"
    },
    {
      "path": "platform/sdk",
      "name": "📦 Platform - SDK"
    },
    {
      "path": "education",
      "name": "📚 Education"
    },
    {
      "path": "tools",
      "name": "🔧 Tools"
    },
    {
      "path": "infrastructure",
      "name": "🏗️ Infrastructure"
    },
    {
      "path": "docs",
      "name": "📄 Documentation"
    },
    {
      "path": "tests",
      "name": "🧪 Tests"
    }
  ]
}
```

---

## Part 5: Interesting Tools to Build

### Tool 1: Information Pulse Monitor
**Purpose:** Real-time visualization of information dynamics across a network.

```python
# tools/pulse_monitor.py
"""
Real-time terminal-based information pulse monitor.
Shows polarity, confidence, and event rate as animated ASCII.
"""

class PulseMonitor:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.history = deque(maxlen=60)  # 60 seconds of history

    def render_bar(self, value: float, width: int = 40) -> str:
        """Render a value as a terminal bar."""
        filled = int((value + 1) / 2 * width)  # Normalize -1..1 to 0..width
        return "█" * filled + "░" * (width - filled)

    async def run(self):
        """Main loop - poll API and update display."""
        while True:
            data = await self.fetch_metrics()
            self.history.append(data)
            self.render(data)
            await asyncio.sleep(0.2)

    def render(self, data: dict):
        """Render current state to terminal."""
        clear_screen()
        print("╔══════════════════════════════════════════════════════╗")
        print("║           INFORMATION PULSE MONITOR                  ║")
        print("╠══════════════════════════════════════════════════════╣")
        print(f"║ Polarity:   {self.render_bar(data['polarity_mean'])} ║")
        print(f"║ Confidence: {self.render_bar(data['confidence_mean'])} ║")
        print(f"║ Risk:       {self.render_bar(data['risk_index'])} ║")
        print(f"║ Event Rate: {data['event_rate']:>6.1f}/s                        ║")
        print("╚══════════════════════════════════════════════════════╝")
```

### Tool 2: Relationship Web Generator
**Purpose:** Generate interactive relationship graphs from text input.

```python
# tools/relationship_web.py
"""
Generate interactive D3.js relationship graphs from arbitrary text.
Exports to HTML for browser viewing.
"""

class RelationshipWebGenerator:
    def __init__(self, api_client):
        self.api = api_client

    async def generate(self, text: str, output_path: str):
        """Analyze text and generate interactive web visualization."""
        # Extract entities and relationships
        result = await self.api.analyze(text)

        # Build graph data
        graph = {
            "nodes": [
                {"id": e["text"], "type": e.get("type", "entity")}
                for e in result["entities"]
            ],
            "links": [
                {
                    "source": r["source"],
                    "target": r["target"],
                    "polarity": r["polarity_score"],
                    "confidence": r["confidence"]
                }
                for r in result["relationships"]
            ]
        }

        # Generate HTML with embedded D3
        html = self.render_template(graph)
        Path(output_path).write_text(html)
        return output_path
```

### Tool 3: Ambient Sound Generator
**Purpose:** Generate ambient soundscapes from information dynamics.

```python
# tools/ambient_sound.py
"""
Real-time ambient sound generation based on information state.
Uses the sound_layer_schema.json spec.
"""

import numpy as np
import sounddevice as sd

class AmbientSoundGenerator:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.phase = 0.0

    def generate_frame(self, metrics: dict, duration_ms: int = 200) -> np.ndarray:
        """Generate audio samples for one frame."""
        samples = int(self.sample_rate * duration_ms / 1000)

        # Map polarity to frequency (200Hz - 600Hz)
        freq = 400 + metrics["polarity_mean"] * 200

        # Map confidence to amplitude (0.1 - 0.5)
        amplitude = 0.1 + metrics["confidence_mean"] * 0.4

        # Map risk to harmonic content
        risk = metrics["risk_index"]

        # Generate base sine wave
        t = np.linspace(0, duration_ms / 1000, samples, endpoint=False)
        wave = amplitude * np.sin(2 * np.pi * freq * t + self.phase)

        # Add harmonics based on risk
        if risk > 0.3:
            wave += (risk * 0.3) * np.sin(2 * np.pi * freq * 2 * t)
        if risk > 0.6:
            wave += (risk * 0.2) * np.sin(2 * np.pi * freq * 3 * t)

        # Update phase for continuity
        self.phase += 2 * np.pi * freq * duration_ms / 1000
        self.phase %= 2 * np.pi

        return wave.astype(np.float32)

    def stream(self, metrics_source):
        """Stream audio continuously from metrics source."""
        with sd.OutputStream(samplerate=self.sample_rate, channels=1) as stream:
            while True:
                metrics = metrics_source.get_current()
                audio = self.generate_frame(metrics)
                stream.write(audio)
```

### Tool 4: Pattern Deviation Alerter
**Purpose:** CLI tool that watches for pattern deviations and sends notifications.

```python
# tools/deviation_alerter.py
"""
Watch information stream and alert on significant deviations.
Supports desktop notifications, Slack, and Discord.
"""

class DeviationAlerter:
    def __init__(self, api_url: str, threshold: float = 0.7):
        self.api_url = api_url
        self.threshold = threshold
        self.baseline = None
        self.notifiers = []

    def add_notifier(self, notifier):
        """Add a notification channel."""
        self.notifiers.append(notifier)

    async def watch(self):
        """Main watch loop."""
        async for event in self.stream_events():
            if event["kind"] == "deviation_detected":
                if event["salience"] >= self.threshold:
                    await self.send_alert(event)

    async def send_alert(self, event: dict):
        """Send alert to all notifiers."""
        message = f"⚠️ Pattern Deviation Detected\n"
        message += f"Salience: {event['salience']:.2f}\n"
        message += f"Details: {event['payload'].get('label', 'Unknown')}"

        for notifier in self.notifiers:
            await notifier.send(message)
```

### Tool 5: Zoology Sensory Mapper
**Purpose:** Interactive tool for mapping animal sensory configurations.

```python
# tools/zoology_mapper.py
"""
Interactive tool for exploring and mapping animal sensory configurations
to the Grid sensory layer framework.
"""

SENSORY_CONFIGS = {
    "human": {
        "primary": "vision",
        "secondary": "hearing",
        "tertiary": "touch",
        "config_type": "balanced_visual",
        "notes": "Standard reference configuration"
    },
    "dog": {
        "primary": "smell",
        "secondary": "hearing",
        "tertiary": "vision",
        "config_type": "olfactory_dominant",
        "notes": "300M olfactory receptors vs human 6M"
    },
    "owl": {
        "primary": "hearing",
        "secondary": "vision",
        "tertiary": "touch",
        "config_type": "auditory_spatial",
        "notes": "Asymmetric ears for 3D sound localization"
    },
    "shark": {
        "primary": "electroreception",
        "secondary": "smell",
        "tertiary": "vision",
        "config_type": "electromagnetic",
        "notes": "Ampullae of Lorenzini detect electrical fields"
    }
}

class ZoologyMapper:
    def generate_sound_mapping(self, species: str) -> dict:
        """Generate sound layer mapping optimized for a species' sensory config."""
        config = SENSORY_CONFIGS.get(species, SENSORY_CONFIGS["human"])

        # Adjust mappings based on primary sense
        if config["config_type"] == "olfactory_dominant":
            # More emphasis on timbre (chemical → texture)
            return {
                "pitch": {"metric": "novelty_score", "weight": 0.3},
                "loudness": {"metric": "confidence_mean", "weight": 0.2},
                "timbre": {"metric": "polarity_mean", "weight": 0.5}
            }
        elif config["config_type"] == "auditory_spatial":
            # More emphasis on spatial/pitch
            return {
                "pitch": {"metric": "polarity_mean", "weight": 0.5},
                "loudness": {"metric": "risk_index", "weight": 0.3},
                "stereo_pan": {"metric": "confidence_mean", "weight": 0.2}
            }
        else:
            # Default human-centric mapping
            return {
                "pitch": {"metric": "polarity_mean", "weight": 0.4},
                "loudness": {"metric": "confidence_mean", "weight": 0.3},
                "timbre": {"metric": "risk_index", "weight": 0.3}
            }
```

---

## Part 6: Implementation Roadmap

### Quarter 1: Foundation
- [ ] Restructure workspace (Phase 1)
- [ ] Implement sound layer renderer (basic)
- [ ] Implement vision layer renderer (basic)
- [ ] Build Pulse Monitor tool
- [ ] Set up hosted API (basic tier)

### Quarter 2: Product
- [ ] Launch Relationship Analysis API (public beta)
- [ ] Build web dashboard (MVP)
- [ ] Create Python SDK
- [ ] Restructure workspace (Phase 2)
- [ ] First educational content release

### Quarter 3: Growth
- [ ] Launch paid API tiers
- [ ] Dashboard goes GA
- [ ] JavaScript SDK
- [ ] Zoology research module (v1)
- [ ] Pattern Deviation Alerter tool

### Quarter 4: Scale
- [ ] Enterprise features
- [ ] Research partnerships
- [ ] Marketplace (sensory presets)
- [ ] Biofeedback integration (research)
- [ ] Workspace restructure (Phase 3)

---

## Summary

The path forward balances three forces:

1. **Research** — The core mission (information dynamics, sensory coherence, zoology insights)
2. **Products** — Revenue generators (API, dashboard, SDK, education)
3. **Infrastructure** — The foundation (workspace, CI/CD, hosting)

They work in unison when:
- Products are **thin wrappers** around research capabilities
- Revenue funds research **without distorting it**
- Infrastructure serves **both research and products**

The zoology scope isn't a distraction — it's a **research multiplier**. Cross-species insights inform better sensory design, which improves products, which funds more research.

The workspace restructuring isn't cosmetic — it's **cognitive infrastructure**. Clear boundaries reduce overhead, enable collaboration, and prevent technical debt.

---

**Next Action:** Review this plan, prioritize one phase, and execute incrementally.

---

*This document lives at `docs/STRATEGIC_PLAN.md` and should be updated quarterly.*