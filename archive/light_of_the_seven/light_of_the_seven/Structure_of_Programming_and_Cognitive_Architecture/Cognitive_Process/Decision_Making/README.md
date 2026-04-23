# Decision Making

## Overview

Decision making is the cognitive process of selecting a course of action from multiple alternatives. In engineering and software development, understanding decision-making processes helps create better tools, design more effective systems, and make sound architectural choices.

## Decision-Making Models

### 1. Rational Decision Model
Classical approach assuming perfect information and rationality.

**Steps:**
1. Identify the problem
2. Generate alternatives
3. Evaluate alternatives
4. Select best alternative
5. Implement decision
6. Evaluate results

**Limitations:**
- Requires complete information
- Assumes unlimited cognitive capacity
- Ignores time constraints
- Unrealistic in practice

### 2. Bounded Rationality (Simon)
Recognizes cognitive limitations.

**Key Concepts:**
- **Satisficing**: Accept "good enough" rather than optimal
- **Heuristics**: Mental shortcuts for quick decisions
- **Limited search**: Stop when satisfactory option found

**Application**: Design-space exploration with time constraints

### 3. Naturalistic Decision Making
How experts make decisions in real-world conditions.

**Recognition-Primed Decision (RPD):**
1. Recognize situation as familiar
2. Recall typical response
3. Mental simulation to verify
4. Execute or modify

**Application**: Debugging by experienced programmers

### 4. Dual-Process Theory
Two systems for thinking and deciding.

| System 1 (Fast) | System 2 (Slow) |
|-----------------|-----------------|
| Automatic | Deliberate |
| Intuitive | Analytical |
| Low effort | High effort |
| Parallel | Serial |
| Unconscious | Conscious |

## Decision-Making in Engineering

### Design-Space Exploration

#### Weighted Decision Matrix
```
Criteria        Weight  Option A  Option B  Option C
-------------------------------------------------
Performance     0.4     8 (3.2)   6 (2.4)   9 (3.6)
Power           0.3     7 (2.1)   9 (2.7)   5 (1.5)
Area            0.2     6 (1.2)   8 (1.6)   7 (1.4)
Risk            0.1     8 (0.8)   7 (0.7)   4 (0.4)
-------------------------------------------------
Total                   7.3       7.4       6.9
```

#### Pareto Analysis
- Identify non-dominated solutions
- Trade-off curves between objectives
- No single "best" when objectives conflict

### Architecture Decisions

#### Architecture Decision Records (ADRs)
```markdown
# ADR-001: Use NAND-only implementation

## Status: Accepted

## Context
Need to choose gate library for accelerator logic.

## Decision
Use NAND-only implementation.

## Consequences
+ Simpler manufacturing
+ Easier testing
- May require more gates
- Slightly higher area
```

### Risk-Based Decisions

#### Expected Value
```
EV = Σ (probability × outcome)
```

#### Decision Trees
- Nodes: Decision points or chance events
- Branches: Options or outcomes
- Leaves: Final outcomes with values

## Cognitive Biases in Decision Making

### Confirmation Bias
Seeking information that confirms existing beliefs.

**Mitigation**: Actively seek disconfirming evidence

### Anchoring
Over-relying on first piece of information.

**Mitigation**: Consider multiple reference points

### Sunk Cost Fallacy
Continuing because of past investment.

**Mitigation**: Focus on future costs and benefits only

### Availability Heuristic
Judging probability by ease of recall.

**Mitigation**: Use actual data, not memorable examples

### Overconfidence
Excessive confidence in own judgments.

**Mitigation**: Calibration training, seek outside views

### Groupthink
Conformity pressure in groups.

**Mitigation**: Devil's advocate, anonymous input

## Decision Support Tools

### Quantitative Tools
- **Spreadsheets**: Weighted matrices, sensitivity analysis
- **Optimization**: Linear programming, constraint satisfaction
- **Simulation**: Monte Carlo, discrete event
- **Machine Learning**: Prediction, classification

### Qualitative Tools
- **Pro/con lists**: Simple comparison
- **SWOT analysis**: Strengths, weaknesses, opportunities, threats
- **Six Thinking Hats**: Multiple perspectives
- **Delphi method**: Expert consensus

### Visualization
- **Decision trees**: Structure and outcomes
- **Influence diagrams**: Dependencies
- **Trade-off plots**: Pareto frontiers
- **Sensitivity charts**: Parameter impact

## Group Decision Making

### Advantages
- More information and perspectives
- Error checking
- Buy-in and commitment

### Challenges
- Coordination costs
- Groupthink
- Dominant personalities
- Diffusion of responsibility

### Techniques
- **Nominal Group Technique**: Independent then combined
- **Delphi Method**: Anonymous iterative consensus
- **Voting**: Various schemes (majority, ranked, etc.)
- **Consensus Building**: Discussion until agreement

## Decisions Under Uncertainty

### Types of Uncertainty
- **Risk**: Known probabilities
- **Uncertainty**: Unknown probabilities
- **Ambiguity**: Unclear problem definition

### Strategies
- **Maximin**: Maximize minimum outcome (pessimistic)
- **Maximax**: Maximize maximum outcome (optimistic)
- **Minimax Regret**: Minimize worst-case regret
- **Expected Value**: Probability-weighted average

### Real Options
- Delay decisions to gather information
- Create flexibility for future choices
- Value of optionality

## Exercises

1. Create a weighted decision matrix for choosing a programming language
2. Identify cognitive biases in a past technical decision
3. Draw a decision tree for a build-vs-buy choice
4. Apply satisficing to a design problem
5. Document an architecture decision using ADR format

## Key Insights

- **Perfect decisions are rare**: Satisficing is often appropriate
- **Biases are universal**: Awareness helps mitigation
- **Process matters**: Good process improves outcomes
- **Document decisions**: Future you will thank present you

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
