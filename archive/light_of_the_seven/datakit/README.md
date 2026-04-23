# 📚 DataKit - Interactive Learning System

> **Load • Explore • Learn • Have Fun!**

## Production setup notes (best practices)

This repo is designed to run locally, but you can run it safely in staging/production by following these rules:

- **Never commit secrets** (API keys). Use environment variables or a secret manager.
- Use **separate staging vs production** credentials/projects and enforce spend/rate limits.
- Keep requests **bounded** (timeouts, small token budgets) and prefer **smaller models** where they meet quality needs.
- Use caching and batching where appropriate; implement retry/backoff for transient errors.

See `PRODUCTION.md` for a checklist and guidance.

### Environment configuration

A template is provided at `config/.env.example`. In real production, inject these via your platform’s secret manager.

Minimum required for OpenAI smoke test:
- `OPENAI_API_KEY`

Optional:
- `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID`
- `OPENAI_DEFAULT_MODEL`, `OPENAI_TIMEOUT_SECONDS`, `OPENAI_MAX_OUTPUT_TOKENS`

### Production readiness checks (offline by default)

Run the doctor (no network calls):
```bash
python scripts/doctor.py
```

Run the doctor with a **minimal bounded** OpenAI live call (uses credits):
```bash
python scripts/doctor.py --live
```

### OpenAI smoke test (opt-in live)

Offline (default):
```bash
python scripts/openai_smoketest.py
```

Live (bounded, uses credits):
```bash
python scripts/openai_smoketest.py --live
```

DataKit is an immersive, interactive learning system built in Python. It transforms any topic or dataset into an engaging exploration experience through guided tours, challenges, visualizations, and fun facts.

---

## 🌟 Overview

This project started as documentation for the **Circle of Fifths** - a fundamental concept in music theory. During the documentation process, an interesting realization emerged: the Circle of Fifths can be represented as various computational frameworks:

- **Finite State Machines (FSM)** - Keys as states, intervals as transitions
- **Boolean Algebra** - Binary encoding of musical keys
- **Graph Theory** - Nodes, edges, and traversal algorithms
- **Quantum Computing** - Qubits, superposition, and entanglement analogies
- **AI/ML** - Markov chains and reinforcement learning for composition

This sparked the idea: *"Why not create a tool that makes learning about ANY topic this engaging?"*

---

## 🚀 Quick Start

### Installation

**Note:** This project is run directly from the repository (it is not packaged for `pip install`).
Run commands from the `full_datakit/` directory so imports like `core` and `story_eq` resolve correctly.

1. Clone or download this repository
2. Navigate to the `full_datakit` directory
3. Install dependencies:

```bash
pip install -r requirements-core.txt
```

Optional (ML / viz extras):
```bash
pip install -r requirements-ml.txt
pip install -r requirements-viz.txt
```

### Running DataKit

**Interactive Mode (Recommended):**
```bash
python datakit.py
```

**Load a Specific Context:**
```bash
python datakit.py -c circle_of_fifths.json
```

**Start Guided Tour Directly:**
```bash
python datakit.py --tour
```

**List Available Contexts:**
```bash
python datakit.py --list
```

---

## 📁 Project Structure

```
full_datakit/
├── datakit.py              # Main entry point & launcher
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── core/                  # Core modules
│   ├── __init__.py
│   ├── loader.py          # Context loading & parsing
│   ├── explorer.py        # Interactive exploration engine
│   └── config.py          # Configuration management
│
├── data/                  # Learning contexts (JSON/YAML)
│   └── circle_of_fifths.json
│
├── scripts/               # Utility scripts
│   ├── ai_composer.py     # AI-driven music generation
│   ├── chord_generator.py # Chord progression generator
│   └── guided_tour.py     # Standalone guided tour
│
├── templates/             # Web interface
│   ├── index.html         # Main HTML interface
│   └── style.css          # Styling
│
└── visualizations/        # Visual representations
    ├── static/            # Matplotlib graphs
    ├── interactive/       # Plotly & D3.js
    └── animated/          # Manim animations
```

---

## 🎮 Features

### 🧭 Guided Tour
Step-by-step walkthrough of the loaded topic with:
- Progressive difficulty
- Interactive examples
- Real-time data exploration

### 🚀 Free Exploration
Discover at your own pace:
- Browse different aspects of the topic
- Dive deep into specific areas
- Follow your curiosity

### 🎯 Challenge Mode
Test your knowledge with:
- Quizzes and puzzles
- Point-based scoring
- Progress tracking

### 💡 Quick Facts
Random interesting tidbits to keep you engaged and learning!

### 📊 Visualizations
Multiple visualization options:
- **Static**: Matplotlib graphs (PNG output)
- **Interactive**: Plotly and D3.js web visualizations
- **Animated**: Manim mathematical animations

---

## 📝 Creating Custom Contexts

DataKit is designed to learn about ANY topic! You can create your own learning context in two ways:

### 1. Interactive Creation
Run DataKit and select "Create Custom Context" from the menu.

### 2. JSON File
Create a JSON file in the `data/` directory:

```json
{
  "metadata": {
    "name": "Your Topic Name",
    "description": "Brief description of the topic",
    "version": "1.0.0",
    "author": "Your Name",
    "topic_type": "general"
  },
  "learning_modules": [
    {
      "id": "intro",
      "title": "Introduction",
      "description": "Getting started with this topic",
      "duration_minutes": 10,
      "difficulty": "beginner"
    }
  ],
  "fun_facts": [
    "Interesting fact #1",
    "Interesting fact #2"
  ],
  "challenges": [
    {
      "id": "quiz_1",
      "title": "Basic Quiz",
      "description": "Test your fundamental understanding",
      "type": "quiz",
      "difficulty": "beginner",
      "points": 10
    }
  ]
}
```

### 3. Programmatic Creation

```python
from core.loader import ContextLoader

loader = ContextLoader()
context = loader.create_custom_context(
    name="My Topic",
    description="Learn about something amazing",
    introduction="Welcome to this fascinating subject!",
    fun_facts=["Fact 1", "Fact 2", "Fact 3"],
    modules=[
        {
            "id": "mod1",
            "title": "Getting Started",
            "description": "The basics",
            "difficulty": "beginner"
        }
    ]
)
```

---

## 🔧 Configuration

DataKit saves configuration to `~/.datakit/config.json`. Settings include:

- **Theme**: Colors, emoji support
- **Exploration**: Hints, typewriter effects
- **Progress**: Tracking, auto-save

Access settings through the main menu or programmatically:

```python
from core.config import get_config, DataKitConfig

config = get_config()
config.theme.use_colors = True
config.exploration.show_hints = True
config.save()
```

---

## 🎵 Circle of Fifths (Default Context)

The included Circle of Fifths context demonstrates DataKit's capabilities:

### What's Included:
- **12 Musical Keys** with relationships and signatures
- **Common Progressions** (I-IV-V-I, ii-V-I, Pop progression, etc.)
- **Computational Models**:
  - Finite State Machine representation
  - Boolean algebra encoding
  - Graph theory properties
  - Quantum computing analogies
  - Markov chain models

### Visualizations:
- `visualizations/static/circle_graph.py` - Matplotlib circle graph
- `visualizations/interactive/plotly_circle.py` - Interactive Plotly
- `visualizations/interactive/d3_circle.html` - D3.js web visualization
- `visualizations/animated/manim_circle.py` - Animated explanation

### Scripts:
- `scripts/ai_composer.py` - Generate chord progressions using:
  - Markov Chains
  - Reinforcement Learning
  - Neural Networks (placeholder)
- `scripts/chord_generator.py` - Simple chord progression generator
- `scripts/guided_tour.py` - Standalone CLI guided tour

---

## 🛠️ Development

### Running Tests

```bash
python -m unittest discover tests -v
```

### Running Visualizations

**Static Graph:**
```bash
python visualizations/static/circle_graph.py
```

**Interactive Plotly:**
```bash
python visualizations/interactive/plotly_circle.py
```

**D3.js Visualization:**
Open `visualizations/interactive/d3_circle.html` in a browser.

**Manim Animation:**
```bash
manim -pql visualizations/animated/manim_circle.py CircleOfFifths
```

### Running Scripts

**AI Composer:**
```bash
python scripts/ai_composer.py
```

**Chord Generator:**
```bash
python scripts/chord_generator.py
```

---

## 📦 Dependencies

- **matplotlib** - Static visualizations
- **networkx** - Graph structures
- **plotly** - Interactive visualizations
- **numpy** - Numerical operations
- **markovify** - Markov chain generation (for AI composer)

Optional:
- **tensorflow** - Neural network composition (advanced)
- **manim** - Mathematical animations
- **pyyaml** - YAML context file support

---

## 🎯 Roadmap

- [ ] Web interface integration
- [ ] More built-in contexts (Programming, Science, History)
- [ ] Spaced repetition learning mode
- [ ] Multi-language support
- [ ] Cloud sync for progress
- [ ] Plugin system for custom visualizations

---

## 💡 Philosophy

Learning should be:
1. **Interactive** - Not just reading, but doing
2. **Fun** - Engaging challenges and discoveries
3. **Visual** - Multiple representations for different learning styles
4. **Flexible** - Learn any topic with the same engaging framework
5. **Progressive** - Build from fundamentals to advanced concepts

---

## 🤝 Contributing

Want to add a new context or feature? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Add your context/feature
4. Submit a pull request

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🙏 Acknowledgments

- The Circle of Fifths - A brilliant piece of music theory that inspired this project
- All the learners who believe that education can be fun

---

**Happy Learning! 🚀📚✨**