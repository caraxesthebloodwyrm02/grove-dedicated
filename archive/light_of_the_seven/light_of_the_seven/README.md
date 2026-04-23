# light_of_the_seven

A research workbench exploring the directional derivative of computation: from foundational theory to hardware implementation. This repository traces a path through information theory, cognitive architecture, AI frameworks, and hardware design.

## Repository Structure

### Core Python Utilities
- `structured_geometry.py` + `test_structured_geometry.py`
  - SVG generator for phase/sub-phase visualization
  - Unit tests with XML namespace handling
- `custom_sort_algorithm.py`
  - Deterministic, single-pass `wyrm_sort` algorithm
  - Handles complex data with structural clarity
- `version_structure.py`
  - Data models and SVG helpers for version insights

### Research Branches

#### 1. Foundations_of_Computation/
- Information Theory (entropy, compression, error correction)
- Logic Laws and Boolean Algebra
- Core mathematical principles

#### 2. Structure_of_Programming_and_Cognitive_Architecture/
- Cognitive Process Analysis
- Language Structure and Compilation
- Mental Models and Problem Solving

#### 3. The_AI_Swift_and_Cognitive_Framework/
- Deep Personalized Systems
- Learning Process Implementation
- Adaptive and Context-Aware Systems

#### 4. The_Logistic_Field_Hardware_Domain/
- AI Knowledge and Expert Systems
- NLP Process Dialog
- Computing Theory Implementation
- Hardware Design and Development

### Documentation
- `circle_of_fifths.md`: Musical theory as computational framework
- `directional_direvative.md`: Core concept map and implementation path
- Various research notes and architectural drafts

## Quick start

### Requirements

- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/irfankabir02/light-of-the-seven.git
cd light-of-the-seven

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev tools
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/ -v
```

### Generate an example SVG

```bash
python -c "from light_of_the_seven.geometry import create_svg; create_svg('example.svg', ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'])"
```

## 📚 Documentation

- **[LEARNING_PATH.md](./LEARNING_PATH.md)** - Guided educational journey through the four research branches
- **[API_REFERENCE.md](./docs/API_REFERENCE.md)** - Complete API documentation with examples
- **[DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Developer setup guide and contribution workflow
- **[INSTALLATION.md](./INSTALLATION.md)** - Platform-specific installation instructions
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines
- **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)** - Community standards
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history and breaking changes

## Platform Integrations

Light of the Seven includes optional integrations with enterprise and high-performance platforms:

### IBM Watson (`ibm` extra)

```python
from light_of_the_seven.integration import IBMWatsonIntegration

watson = IBMWatsonIntegration(api_key="...", url="...")
watson.connect()
models = watson.list_foundation_models()
```

Install: `pip install -e ".[ibm]"`

### NVIDIA CUDA (`cuda` extra)

```python
from light_of_the_seven.integration import NVIDIACUDAIntegration

cuda = NVIDIACUDAIntegration()
info = cuda.get_device_info()
result = cuda.demonstrate_saxpy(n=1000000)
```

Install: `pip install -e ".[cuda]"`

### Check Environment

```python
from light_of_the_seven.integration import check_environment

env = check_environment()
# {'ibm_watson': bool, 'nvidia_cuda': bool, 'pytorch': bool, 'pytorch_cuda': bool}
```

---

## Continuous Integration & Testing

All code is tested automatically on:
- Python 3.9, 3.10, 3.11, 3.12
- Multiple operating systems
- With and without optional dependencies

**Status:** [![Tests](https://img.shields.io/github/actions/workflow/status/irfankabir02/light-of-the-seven/tests.yml?branch=main&label=tests)](https://github.com/irfankabir02/light-of-the-seven/actions)

**View workflows:**
- [Tests](https://github.com/irfankabir02/light-of-the-seven/actions/workflows/tests.yml)
- [Lint & Type Check](https://github.com/irfankabir02/light-of-the-seven/actions/workflows/lint.yml)
- [Documentation](https://github.com/irfankabir02/light-of-the-seven/actions/workflows/docs.yml)

---

## Versioning

Tags/releases are intended to follow SemVer (e.g., `v0.1.0`).

## License

See `LICENSE`.

## Contributing

See `CONTRIBUTING.md`.

## Code of Conduct

See `CODE_OF_CONDUCT.md`.

## Development Path

This repository follows a **directional derivative** approach to development:

1. **Root: Foundations_of_Computation/**
   - Start with information theory and logic
   - Build mathematical foundations
   - Define core abstractions

2. **Structure_of_Programming_and_Cognitive_Architecture/**
   - Map theory to cognitive models
   - Design language structures
   - Create programming frameworks

3. **The_AI_Swift_and_Cognitive_Framework/**
   - Implement learning systems
   - Build adaptive frameworks
   - Create personalized interfaces

4. **Leaf: The_Logistic_Field_Hardware_Domain/**
   - Design hardware implementations
   - Create expert systems
   - Deploy concrete solutions

## Concept Map

### Circle of Fifths as Computational Framework
See `circle_of_fifths.md` for an example of mapping musical theory to:
- Boolean algebra and logic gates
- Finite state machines
- Quantum computing concepts
- AI/ML implementations

### Directional Derivative Implementation
See `directional_direvative.md` for the complete path from theory to silicon:
- Information budgets and constraints
- Cognitive architecture design
- AI framework selection
- Hardware implementation specs

## Complete Directory Structure

```
light_of_the_seven/
├── Foundations_of_Computation/
│   ├── Information_Theory/
│   │   ├── Data_Compression/
│   │   ├── Entropy_and_Information/
│   │   ├── Error_Correction_Codes/
│   │   ├── Information_Measures/
│   │   └── Shannons_Theory/
│   ├── Law_of_Logic_Boolean_Algebra/
│   │   ├── Boolean_Algebra_Basics/
│   │   ├── Boolean_Algebra_Identities/
│   │   ├── Boolean_Algebra_Theorems/
│   │   ├── Karnaugh_Maps/
│   │   └── Simplification_Techniques/
│   ├── Law_of_Logic_The_Fundamental/
│   │   ├── AND_OR_NOT_Gates/
│   │   ├── Fundamental_Logic_Gates/
│   │   ├── NAND_NOR_Gates/
│   │   ├── Universal_Gates/
│   │   └── XOR_XNOR_Gates/
│   └── Logic_of_Propositions/
│       ├── Laws_of_Logic/
│       ├── Logical_Equivalence/
│       ├── Propositional_Calculus/
│       ├── Propositional_Logic/
│       ├── Tautologies_and_Contradictions/
│       └── Truth_Tables/
├── Structure_of_Programming_and_Cognitive_Architecture/
│   ├── Cognitive_Process/
│   │   ├── Cognitive_Load_Theory/
│   │   ├── Decision_Making/
│   │   ├── Human_Computer_Interaction/
│   │   ├── Mental_Models/
│   │   └── Problem_Solving/
│   └── Language_Structure/
│       ├── Compiler_Design/
│       ├── Interpreter_Design/
│       ├── Lexical_Analysis/
│       ├── Parsing_Techniques/
│       └── Syntax_and_Semantics/
├── The_AI_Swift_and_Cognitive_Framework/
│   ├── Deep_Personalized_Systems_Framework/
│   │   ├── Adaptive_Learning_Systems/
│   │   ├── Context_Aware_Systems/
│   │   ├── Personalized_Interfaces/
│   │   ├── Personalized_Recommendations/
│   │   └── User_Modeling/
│   └── Learning_Process/
│       ├── Deep_Learning/
│       ├── Machine_Learning/
│       ├── Reinforcement_Learning/
│       ├── Supervised_Learning/
│       └── Unsupervised_Learning/
├── The_Logistic_Field_Hardware_Domain/
│   ├── AI_Knowledge/
│   │   ├── Expert_Systems/
│   │   ├── Inference_Engines/
│   │   ├── Knowledge_Acquisition/
│   │   ├── Knowledge_Engineering/
│   │   └── Knowledge_Representation/
│   ├── AI_NLP_Process_Dialog/
│   │   ├── Machine_Translation/
│   │   ├── Natural_Language_Processing/
│   │   ├── Parsing_Techniques/
│   │   ├── Speech_Recognition/
│   │   └── Syntax_and_Semantics/
│   ├── Computing_Theory/
│   │   ├── Context_Free_Grammars/
│   │   ├── Finite_Automata/
│   │   ├── Pushdown_Automata/
│   │   ├── Regular_Expressions/
│   │   └── Turing_Machines/
│   └── Design_and_Development_Hardware_Level/
│       ├── ASIC_and_FPGA_Design/
│       ├── Digital_Circuit_Design/
│       ├── Embedded_Systems/
│       ├── Microprocessor_Architecture/
│       └── VLSI_Design/
└── [Root files]
    ├── structured_geometry.py
    ├── custom_sort_algorithm.py
    ├── version_structure.py
    ├── circle_of_fifths.md
    ├── directional_direvative.md
    └── ...
```

## Navigation

Each branch contains:
- **Overview document** (`.md` at branch root): Explains the branch's role in the directional derivative
- **README.md** in each leaf directory: Detailed documentation with concepts, examples, and exercises
- **Executive_Report/** directories: Cross-reference JSON files for concept mappings

---

**Last Updated**: December 2025
**Maintainer**: GRID Research Team
# All CI/CD workflows passing!
