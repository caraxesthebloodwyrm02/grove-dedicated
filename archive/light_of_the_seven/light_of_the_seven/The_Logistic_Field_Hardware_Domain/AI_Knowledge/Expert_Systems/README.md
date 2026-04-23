# Expert Systems

## Overview

Expert systems are AI programs that emulate the decision-making ability of human experts. They use knowledge bases and inference engines to solve complex problems in specific domains.

## Architecture

```
┌─────────────────────────────────────────┐
│           User Interface                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Inference Engine                │
│   (Forward/Backward Chaining)           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Knowledge Base                  │
│   ┌─────────────┬─────────────┐        │
│   │   Rules     │   Facts     │        │
│   └─────────────┴─────────────┘        │
└─────────────────────────────────────────┘
```

## Knowledge Representation

### Production Rules
```
IF condition1 AND condition2 THEN action

Example:
IF temperature > 100°C
AND pressure > 10 atm
THEN alarm = critical
```

### Rule Format
```python
class Rule:
    def __init__(self, conditions, action, confidence=1.0):
        self.conditions = conditions  # List of predicates
        self.action = action          # Conclusion or action
        self.confidence = confidence  # Certainty factor
```

### Facts
```python
facts = {
    'temperature': 105,
    'pressure': 12,
    'system_status': 'running'
}
```

## Inference Mechanisms

### Forward Chaining (Data-Driven)
Start with facts, apply rules to derive conclusions.

```python
def forward_chain(rules, facts):
    changed = True
    while changed:
        changed = False
        for rule in rules:
            if rule.conditions_met(facts) and not rule.already_fired:
                new_facts = rule.fire()
                facts.update(new_facts)
                rule.already_fired = True
                changed = True
    return facts
```

### Backward Chaining (Goal-Driven)
Start with goal, work backward to find supporting facts.

```python
def backward_chain(rules, facts, goal):
    if goal in facts:
        return True

    for rule in rules:
        if rule.conclusion == goal:
            subgoals = rule.conditions
            if all(backward_chain(rules, facts, sg) for sg in subgoals):
                facts[goal] = rule.fire()
                return True

    return False
```

## Uncertainty Handling

### Certainty Factors
```python
def combine_cf(cf1, cf2):
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1 - cf1)
    elif cf1 < 0 and cf2 < 0:
        return cf1 + cf2 * (1 + cf1)
    else:
        return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))
```

### Bayesian Reasoning
```python
def bayesian_update(prior, likelihood, evidence):
    posterior = (likelihood * prior) / evidence
    return posterior
```

## Example: Design Rule Checker

```python
class DesignRuleChecker:
    def __init__(self):
        self.rules = [
            Rule(
                conditions=['mac_array_size > 4096'],
                action='require_two_level_interconnect',
                confidence=1.0
            ),
            Rule(
                conditions=['clock_frequency > 1GHz', 'process_node < 14nm'],
                action='require_clock_tree_synthesis',
                confidence=0.95
            ),
            Rule(
                conditions=['power_budget < 10W', 'performance_target > 1TOPS'],
                action='recommend_quantization',
                confidence=0.8
            )
        ]

    def check_design(self, design_params):
        violations = []
        recommendations = []

        for rule in self.rules:
            if rule.evaluate(design_params):
                if rule.is_violation:
                    violations.append(rule.action)
                else:
                    recommendations.append((rule.action, rule.confidence))

        return violations, recommendations
```

## Applications

### Hardware Design
- Design rule checking
- Synthesis optimization
- Verification planning

### Diagnostics
- Fault diagnosis
- Troubleshooting guides
- Root cause analysis

### Configuration
- System configuration
- Product selection
- Constraint satisfaction

## Advantages and Limitations

### Advantages
- Captures expert knowledge explicitly
- Explanations available (trace reasoning)
- Easy to modify rules
- Consistent decisions

### Limitations
- Knowledge acquisition bottleneck
- Brittleness at domain boundaries
- Difficulty with uncertainty
- Maintenance challenges

## Exercises

1. Build simple rule-based expert system
2. Implement forward and backward chaining
3. Add certainty factors to rules
4. Create design rule checker for hardware
5. Build explanation facility

## Key Insights

- **Knowledge is explicit**: Rules capture expertise directly
- **Inference is traceable**: Can explain reasoning
- **Domain-specific**: Works best in narrow domains
- **Maintenance matters**: Rules need updating

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
