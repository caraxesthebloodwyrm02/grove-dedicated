# Inference Engines

## Overview

Inference engines are the reasoning components of knowledge-based systems. They apply logical rules to knowledge bases to derive new information or reach conclusions.

## Types of Inference

### Deductive Inference
From general rules to specific conclusions.

```
Rule: All mammals are warm-blooded
Fact: A dog is a mammal
Conclusion: A dog is warm-blooded
```

### Inductive Inference
From specific observations to general rules.

```
Observations: Swan1 is white, Swan2 is white, Swan3 is white
Generalization: All swans are white (may be wrong!)
```

### Abductive Inference
From observations to best explanation.

```
Observation: The grass is wet
Possible causes: Rain, sprinkler, dew
Best explanation: It rained (given other evidence)
```

## Inference Strategies

### Forward Chaining
Data-driven, bottom-up reasoning.

```python
class ForwardChainingEngine:
    def __init__(self, rules):
        self.rules = rules
        self.agenda = []

    def run(self, facts):
        working_memory = facts.copy()
        fired_rules = set()

        while True:
            applicable = self.find_applicable_rules(working_memory, fired_rules)
            if not applicable:
                break

            rule = self.conflict_resolution(applicable)
            new_facts = rule.execute(working_memory)
            working_memory.update(new_facts)
            fired_rules.add(rule.id)

        return working_memory

    def find_applicable_rules(self, facts, fired):
        return [r for r in self.rules
                if r.id not in fired and r.matches(facts)]

    def conflict_resolution(self, rules):
        # Strategies: specificity, recency, priority
        return max(rules, key=lambda r: r.specificity)
```

### Backward Chaining
Goal-driven, top-down reasoning.

```python
class BackwardChainingEngine:
    def __init__(self, rules):
        self.rules = rules

    def prove(self, goal, facts, depth=0):
        # Check if goal is already known
        if goal in facts:
            return facts[goal]

        # Find rules that conclude this goal
        for rule in self.rules:
            if rule.conclusion == goal:
                # Try to prove all premises
                if self.prove_all(rule.premises, facts, depth + 1):
                    result = rule.execute(facts)
                    facts[goal] = result
                    return result

        # Goal cannot be proven
        return None

    def prove_all(self, premises, facts, depth):
        return all(self.prove(p, facts, depth) for p in premises)
```

## Conflict Resolution

When multiple rules match, choose which to fire.

### Strategies

#### Specificity
More specific rules (more conditions) have priority.

```python
def specificity(rule):
    return len(rule.conditions)
```

#### Recency
Rules matching more recently asserted facts fire first.

```python
def recency(rule, facts):
    return max(facts[c].timestamp for c in rule.conditions)
```

#### Priority
Explicit rule priorities.

```python
def priority(rule):
    return rule.priority  # User-defined
```

#### Refractoriness
Don't fire same rule on same facts twice.

## Rete Algorithm

Efficient pattern matching for production systems.

### Structure
```
Alpha Network: Tests individual conditions
Beta Network: Joins conditions together
Production Nodes: Fire when all conditions match
```

### Optimization
- Shares common condition tests
- Incremental updates on fact changes
- Avoids redundant matching

```python
class ReteNetwork:
    def __init__(self):
        self.alpha_nodes = {}  # Condition -> Node
        self.beta_nodes = []   # Join nodes
        self.productions = []  # Rule terminals

    def add_rule(self, rule):
        # Build alpha nodes for conditions
        alpha_outputs = []
        for condition in rule.conditions:
            if condition not in self.alpha_nodes:
                self.alpha_nodes[condition] = AlphaNode(condition)
            alpha_outputs.append(self.alpha_nodes[condition])

        # Build beta network for joins
        current = alpha_outputs[0]
        for alpha in alpha_outputs[1:]:
            beta = BetaNode(current, alpha)
            self.beta_nodes.append(beta)
            current = beta

        # Add production node
        production = ProductionNode(rule, current)
        self.productions.append(production)
```

## Truth Maintenance

Track dependencies between facts.

```python
class TruthMaintenanceSystem:
    def __init__(self):
        self.facts = {}
        self.justifications = {}  # fact -> set of supporting facts

    def assert_fact(self, fact, justification=None):
        self.facts[fact] = True
        if justification:
            self.justifications[fact] = justification

    def retract_fact(self, fact):
        self.facts[fact] = False
        # Retract dependent facts
        for dependent, justification in self.justifications.items():
            if fact in justification:
                self.retract_fact(dependent)
```

## Applications

### Expert Systems
- Medical diagnosis
- Financial analysis
- Technical support

### Planning Systems
- Goal decomposition
- Action sequencing
- Resource allocation

### Configuration
- Product configuration
- System setup
- Constraint satisfaction

## Exercises

1. Implement forward chaining engine
2. Implement backward chaining engine
3. Add conflict resolution strategies
4. Build simple Rete network
5. Implement truth maintenance

## Key Insights

- **Forward vs. backward**: Choose based on problem structure
- **Efficiency matters**: Rete algorithm for large rule sets
- **Conflict resolution is crucial**: Determines behavior
- **Truth maintenance**: Handle changing facts

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
