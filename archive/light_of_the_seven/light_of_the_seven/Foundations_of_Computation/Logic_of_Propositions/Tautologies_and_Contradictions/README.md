# Tautologies and Contradictions

## Overview

Tautologies and contradictions are special types of compound propositions with fixed truth values regardless of their component propositions. Understanding these concepts is essential for logical reasoning and proof techniques.

## Definitions

### Tautology
A **tautology** is a compound proposition that is **always true**, regardless of the truth values of its component propositions.

- Symbol: Often denoted as ⊤ or T
- Every row in truth table has value T
- Also called: logically valid, logically true

### Contradiction
A **contradiction** is a compound proposition that is **always false**, regardless of the truth values of its component propositions.

- Symbol: Often denoted as ⊥ or F
- Every row in truth table has value F
- Also called: logically false, unsatisfiable

### Contingency
A **contingency** is a compound proposition that is **neither a tautology nor a contradiction**.

- Has at least one T and at least one F in truth table
- Truth value depends on component values
- Most propositions are contingencies

## Examples of Tautologies

### Law of Excluded Middle
```
p ∨ ¬p
```
| p | ¬p | p ∨ ¬p |
|---|-----|--------|
| T |  F  |   T    |
| F |  T  |   T    |

### Implication Tautology
```
p → p
```
| p | p → p |
|---|-------|
| T |   T   |
| F |   T   |

### Modus Ponens Form
```
((p → q) ∧ p) → q
```
Always true - the foundation of logical inference.

### De Morgan Equivalence
```
¬(p ∧ q) ↔ (¬p ∨ ¬q)
```
Biconditional of equivalent statements is always true.

### Contrapositive Equivalence
```
(p → q) ↔ (¬q → ¬p)
```

## Examples of Contradictions

### Law of Non-Contradiction
```
p ∧ ¬p
```
| p | ¬p | p ∧ ¬p |
|---|-----|--------|
| T |  F  |   F    |
| F |  T  |   F    |

### Negation of Tautology
```
¬(p ∨ ¬p)
```
The negation of any tautology is a contradiction.

### Impossible Implication
```
(p → q) ∧ (p → ¬q) ∧ p
```
Requires p to imply both q and ¬q while p is true.

## Properties

### Tautology Properties
1. **Negation**: ¬(tautology) is a contradiction
2. **Conjunction**: tautology ∧ p ≡ p
3. **Disjunction**: tautology ∨ p ≡ tautology
4. **Implication**: tautology → p ≡ p

### Contradiction Properties
1. **Negation**: ¬(contradiction) is a tautology
2. **Conjunction**: contradiction ∧ p ≡ contradiction
3. **Disjunction**: contradiction ∨ p ≡ p
4. **Implication**: contradiction → p ≡ tautology (vacuously true)

### Duality
- Tautologies and contradictions are duals
- Swap ∧/∨ and T/F to convert between them

## Testing Methods

### Truth Table Method
1. Build complete truth table
2. Check output column:
   - All T → Tautology
   - All F → Contradiction
   - Mixed → Contingency

### Algebraic Method
1. Apply logical equivalences
2. Simplify to T (tautology) or F (contradiction)
3. If neither, it's a contingency

### Counterexample Method
- To disprove tautology: find one F row
- To disprove contradiction: find one T row

## Important Tautologies

### Logical Laws as Tautologies

| Name | Tautology |
|------|-----------|
| Identity | p ↔ p |
| Excluded Middle | p ∨ ¬p |
| Double Negation | p ↔ ¬¬p |
| Contrapositive | (p → q) ↔ (¬q → ¬p) |
| De Morgan | ¬(p ∧ q) ↔ (¬p ∨ ¬q) |
| Exportation | ((p ∧ q) → r) ↔ (p → (q → r)) |

### Inference Rules as Tautologies

| Rule | Tautology Form |
|------|----------------|
| Modus Ponens | ((p → q) ∧ p) → q |
| Modus Tollens | ((p → q) ∧ ¬q) → ¬p |
| Hypothetical Syllogism | ((p → q) ∧ (q → r)) → (p → r) |
| Disjunctive Syllogism | ((p ∨ q) ∧ ¬p) → q |
| Constructive Dilemma | ((p → q) ∧ (r → s) ∧ (p ∨ r)) → (q ∨ s) |

## Applications

### Proof by Contradiction
1. Assume ¬p (negation of what you want to prove)
2. Derive a contradiction
3. Conclude p must be true

### Validity Testing
An argument is valid if:
```
(premise₁ ∧ premise₂ ∧ ... ∧ premiseₙ) → conclusion
```
is a tautology.

### Satisfiability
- Tautology: satisfiable (always true)
- Contradiction: unsatisfiable (never true)
- Contingency: satisfiable (sometimes true)

### Circuit Design
- Tautology → output always 1 (can simplify to constant)
- Contradiction → output always 0 (can simplify to constant)
- Contingency → actual logic needed

## Exercises

1. Prove tautology: (p → q) ∨ (q → p)
2. Prove contradiction: (p → q) ∧ (p → ¬q) ∧ p
3. Classify: (p → q) → (¬p → ¬q)
4. Find counterexample: p → (q → p)
5. Simplify using tautology/contradiction rules: (p ∧ ¬p) ∨ q

## Key Insights

- **Tautologies are always safe**: Can be added to any argument
- **Contradictions prove anything**: From F, anything follows (principle of explosion)
- **Testing is mechanical**: Truth tables always work
- **Logical laws are tautologies**: The rules of logic are themselves tautologies

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
