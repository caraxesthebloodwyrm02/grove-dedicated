# Propositional Logic

## Overview

Propositional logic is the study of propositions and their combinations using logical connectives. It forms the foundation of mathematical logic and is essential for computer science, digital circuit design, and formal reasoning.

## Propositions

### Definition
A **proposition** is a declarative sentence that is either true or false, but not both.

### Examples of Propositions
- "Paris is the capital of France" (True)
- "2 + 3 = 6" (False)
- "It is raining" (True or False, depending on conditions)

### Non-Propositions
- "What time is it?" (Question)
- "Please close the door" (Command)
- "x + 1 = 2" (Contains variable - not a proposition until x is specified)
- "This statement is false" (Paradox - neither true nor false)

### Propositional Variables
Letters (p, q, r, ...) represent propositions whose truth values may vary.

## Logical Connectives

### Negation (NOT)
- **Symbol**: ¬, ~, or '
- **Meaning**: "It is not the case that..."
- **Truth**: Reverses the truth value

| p | ¬p |
|---|-----|
| T |  F  |
| F |  T  |

### Conjunction (AND)
- **Symbol**: ∧, ·, or &
- **Meaning**: "Both...and..."
- **Truth**: True only when both operands are true

| p | q | p ∧ q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   F   |
| F | F |   F   |

### Disjunction (OR)
- **Symbol**: ∨ or +
- **Meaning**: "Either...or...or both"
- **Truth**: True when at least one operand is true

| p | q | p ∨ q |
|---|---|-------|
| T | T |   T   |
| T | F |   T   |
| F | T |   T   |
| F | F |   F   |

### Implication (IMPLIES)
- **Symbol**: →, ⇒, or ⊃
- **Meaning**: "If...then..."
- **Truth**: False only when antecedent is true and consequent is false

| p | q | p → q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   T   |
| F | F |   T   |

**Key insight**: A false antecedent makes the implication vacuously true.

### Biconditional (IFF)
- **Symbol**: ↔, ⇔, or ≡
- **Meaning**: "If and only if"
- **Truth**: True when both operands have the same truth value

| p | q | p ↔ q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   F   |
| F | F |   T   |

## Compound Propositions

### Formation Rules
1. Any propositional variable is a well-formed formula (wff)
2. If φ is a wff, then ¬φ is a wff
3. If φ and ψ are wffs, then (φ ∧ ψ), (φ ∨ ψ), (φ → ψ), (φ ↔ ψ) are wffs
4. Nothing else is a wff

### Operator Precedence
1. ¬ (highest)
2. ∧
3. ∨
4. →
5. ↔ (lowest)

**Example**: p ∨ q ∧ r means p ∨ (q ∧ r)

### Parentheses
Use parentheses to override precedence or clarify meaning:
- (p ∨ q) ∧ r ≠ p ∨ (q ∧ r)

## Translating Natural Language

### Common Patterns

| Natural Language | Logical Form |
|-----------------|--------------|
| "p and q" | p ∧ q |
| "p or q" | p ∨ q |
| "not p" | ¬p |
| "if p then q" | p → q |
| "p only if q" | p → q |
| "p if q" | q → p |
| "p if and only if q" | p ↔ q |
| "neither p nor q" | ¬p ∧ ¬q |
| "p unless q" | ¬q → p |

### Ambiguity in Natural Language
"You can have cake or ice cream"
- **Inclusive OR**: p ∨ q (can have both)
- **Exclusive OR**: (p ∨ q) ∧ ¬(p ∧ q) (exactly one)

Context determines interpretation.

## Applications

### Digital Logic
- Propositions map to signal values (0/1)
- Connectives map to logic gates
- Compound propositions map to circuits

### Programming
- Boolean expressions in conditions
- Control flow (if-then-else)
- Loop conditions

### Databases
- SQL WHERE clauses
- Query optimization
- Constraint specification

### Formal Verification
- Specification of properties
- Assertion checking
- Model checking

## Exercises

1. Determine if these are propositions:
   - "The moon is made of cheese"
   - "x > 5"
   - "Hello!"

2. Translate to logical form:
   - "If it rains, then the ground is wet"
   - "I will go unless it snows"

3. Evaluate: (T ∧ F) ∨ (¬F → T)

4. Write the negation of: "If p then q"

5. Express XOR using basic connectives

## Key Insights

- **Binary truth values**: Every proposition is exactly true or false
- **Connectives are functions**: Map truth values to truth values
- **Implication is tricky**: False antecedent makes it true
- **Natural language is ambiguous**: Formal logic removes ambiguity

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
