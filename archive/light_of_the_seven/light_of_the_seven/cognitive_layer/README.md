# Cognitive Decision Support Layer for GRID

## Overview

The Cognitive Decision Support Layer integrates decision support principles (bounded rationality, dual-process theory) with GRID's existing modules, enabling cognitive-aware processing that adapts to user mental models and decision-making patterns.

## Architecture

The cognitive layer is organized into four main components:

### 1. Decision Support (`decision_support/`)

Implements decision-making mechanisms:

- **Bounded Rationality Engine**: Satisficing, heuristics, limited search
- **Dual-Process Router**: System 1 (fast) vs System 2 (slow) routing
- **Decision Matrix Generator**: Weighted decision matrices
- **Choice Architecture**: Framing, defaults, nudges, progressive disclosure

### 2. Mental Models (`mental_models/`)

Manages user mental models:

- **Model Tracker**: Infers and tracks user mental models over time
- **Alignment Checker**: Compares grid behavior with user expectations
- **Model Builder**: Constructs mental models from user interactions

### 3. Cognitive Load (`cognitive_load/`)

Manages cognitive load:

- **Load Estimator**: Estimates cognitive load of operations
- **Information Chunker**: Organizes information into manageable chunks
- **Scaffolding Manager**: Progressive disclosure based on expertise

### 4. Integration (`integration/`)

Bridges with GRID modules:

- **Grid Bridge**: Connects to grid/essence, grid/awareness, grid/patterns
- **Pipeline Adapter**: Adapts GRID processing pipeline with cognitive awareness
- **Context Enricher**: Enriches GRID context with cognitive factors

## Usage

### Basic Example

```python
from light_of_the_seven.cognitive_layer import (
    CognitiveState,
    DecisionContext,
    UserCognitiveProfile,
    BoundedRationalityEngine,
    DualProcessRouter,
)

# Create user profile
user_profile = UserCognitiveProfile(
    user_id="user123",
    expertise_level="intermediate",
    decision_style="balanced",
)

# Create decision context
decision_context = DecisionContext(
    decision_id="decision1",
    decision_type="tactical",
    options=[
        {"id": "opt1", "name": "Option 1", "score": 0.8},
        {"id": "opt2", "name": "Option 2", "score": 0.6},
    ],
    criteria=[
        {"name": "performance", "evaluate": lambda o: o.get("score", 0.0)},
    ],
)

# Use bounded rationality engine
engine = BoundedRationalityEngine()
result = engine.evaluate_with_bounded_rationality(
    decision_context,
    decision_context.options,
    lambda o: o.get("score", 0.0)
)

# Use dual-process router
router = DualProcessRouter()
processing_result = router.process(decision_context, user_profile)
```

### Integration with GRID

```python
from light_of_the_seven.cognitive_layer.integration import GridBridge, PipelineAdapter
from light_of_the_seven.cognitive_layer import CognitiveState

# Create bridge and adapter
bridge = GridBridge()
adapter = PipelineAdapter(bridge)

# Set cognitive state
cognitive_state = CognitiveState(
    estimated_load=5.0,
    processing_mode="system_1",
)

adapter.set_cognitive_state(cognitive_state)
adapter.set_user_profile(user_profile)

# Adapt a pipeline stage
def ner_function(text):
    # Original NER implementation
    pass

# Wrap with cognitive awareness
cognitive_ner = adapter.wrap_pipeline_stage("ner", ner_function)
result = cognitive_ner("Sample text")
```

## Design Principles

1. **Cognitive-First**: All decisions respect human cognitive limitations
2. **Transparency**: Users understand why decisions were made
3. **Adaptability**: System learns from user behavior and preferences
4. **Non-Intrusive**: Cognitive layer enhances, doesn't replace, existing functionality
5. **Modular**: Components can be used independently or together

## Key Features

### Decision Support

- **Satisficing**: Stop search when "good enough" solution found
- **Heuristics**: Apply cognitive shortcuts for common decisions
- **Dual-Process Routing**: Automatic routing to System 1 or System 2
- **Decision Matrices**: Weighted criteria evaluation
- **Choice Architecture**: Framing, defaults, nudges

### Mental Model Management

- **Model Tracking**: Infer and track user mental models
- **Alignment Checking**: Compare expectations with behavior
- **Mismatch Detection**: Flag discrepancies for explanation
- **Model Evolution**: Track how mental models change over time

### Cognitive Load Management

- **Load Estimation**: Estimate cognitive load of operations
- **Chunking**: Organize information into manageable units (Miller's 7±2)
- **Scaffolding**: Progressive disclosure based on expertise
- **Load Reduction**: Suggest ways to reduce cognitive load

## Integration Points

### With grid/essence (State Representation)

- Cognitive state becomes part of essential state
- Decision history tracked in state transformations
- Mental model alignment stored in state

### With grid/awareness (Context)

- Cognitive context enriches awareness layer
- User's decision-making style influences context gathering
- Cognitive load affects context window size

### With grid/patterns (Pattern Recognition)

- Decision patterns recognized alongside spatial/temporal patterns
- Cognitive patterns (e.g., "user prefers quick decisions") detected
- Mental model mismatches flagged as patterns

### With Grid Processing Pipeline

- **NER**: Cognitive-aware entity extraction (respects cognitive load)
- **Pattern Engine**: Decision-aware pattern matching
- **Rules Engine**: Bounded rationality in rule evaluation
- **Relationship Analyzer**: Decision context in relationship judgment

## Data Flow

```
User Interaction
    ↓
Cognitive Layer (Decision Support)
    ├─→ Assess cognitive load
    ├─→ Check mental model alignment
    ├─→ Route to System 1 or System 2
    └─→ Apply bounded rationality heuristics
    ↓
Grid Processing Pipeline
    ├─→ NER (cognitive-aware)
    ├─→ Pattern Engine (decision-aware)
    ├─→ Rules Engine (bounded rationality)
    └─→ Relationship Analyzer (decision context)
    ↓
Cognitive Layer (Post-Processing)
    ├─→ Chunk results for presentation
    ├─→ Check mental model alignment
    └─→ Provide decision rationale
    ↓
User Output (Cognitive-Optimized)
```

## References

This implementation is based on research from:

- `light_of_the_seven/Structure_of_Programming_and_Cognitive_Architecture/Cognitive_Process/Decision_Making/README.md`
- `light_of_the_seven/Structure_of_Programming_and_Cognitive_Architecture/Cognitive_Process/Mental_Models/README.md`
- `light_of_the_seven/Structure_of_Programming_and_Cognitive_Architecture/Cognitive_Process/Cognitive_Load_Theory/README.md`

## Status

**Phase 1-4 Complete**: Foundation, Decision Support, Mental Models, and Cognitive Load modules are implemented.

**Phase 5-6 Pending**: Full integration with GRID pipeline and user profile learning systems.

