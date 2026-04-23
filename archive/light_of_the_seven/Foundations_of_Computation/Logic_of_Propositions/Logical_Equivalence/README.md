# Logical Equivalence

## Overview

Two propositions are **logically equivalent** if they have the same truth value in every possible scenario. Logical equivalence is fundamental for simplifying expressions, proving theorems, and optimizing circuits.

## Definition

### Formal Definition
Propositions p and q are logically equivalent (written p ≡ q) if and only if p ↔ q is a tautology.

### Equivalent Statements
- p ≡ q
- p and q have identical truth tables
- p ↔ q is always true
- p and q are true in exactly the same situations

## Testing for Equivalence

### Method 1: Truth Table Comparison
Build truth tables for both expressions and compare output columns.

**Example**: Show p → q ≡ ¬p ∨ q

| p | q | p → q | ¬p | ¬p ∨ q |
|---|---|-------|-----|--------|
| T | T |   T   |  F  |   T    |
| T | F |   F   |  F  |   F    |
| F | T |   T   |  T  |   T    |
| F | F |   T   |  T  |   T    |

Columns match ✓ Therefore p → q ≡ ¬p ∨ q

### Method 2: Algebraic Transformation
Use known equivalences to transform one expression into the other.

### Method 3: Biconditional Test
Show that p ↔ q is a tautology.

## Fundamental Equivalences

### Double Negation
```
¬(¬p) ≡ p
```

### Commutative Laws
```
p ∧ q ≡ q ∧ p
p ∨ q ≡ q ∨ p
```

### Associative Laws
```
(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)
(p ∨ q) ∨ r ≡ p ∨ (q ∨ r)
```

### Distributive Laws
```
p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)
p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)
```

### Identity Laws
```
p ∧ T ≡ p
p ∨ F ≡ p
```

### Domination Laws
```
p ∧ F ≡ F
p ∨ T ≡ T
```

### Idempotent Laws
```
p ∧ p ≡ p
p ∨ p ≡ p
```

### Complement Laws
```
p ∧ ¬p ≡ F
p ∨ ¬p ≡ T
```

### Absorption Laws
```
p ∧ (p ∨ q) ≡ p
p ∨ (p ∧ q) ≡ p
```

### De Morgan's Laws
```
¬(p ∧ q) ≡ ¬p ∨ ¬q
¬(p ∨ q) ≡ ¬p ∧ ¬q
```

## Equivalences Involving Implication

### Implication as Disjunction
```
p → q ≡ ¬p ∨ q
```

### Contrapositive
```
p → q ≡ ¬q → ¬p
```

### Negation of Implication
```
¬(p → q) ≡ p ∧ ¬q
```

### Biconditional Equivalences
```
p ↔ q ≡ (p → q) ∧ (q → p)
p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)
p ↔ q ≡ ¬(p ⊕ q)  [XOR relation]
```

## Non-Equivalences (Common Mistakes)

### Converse is NOT Equivalent
```
p → q ≢ q → p
```
Example: "If it rains, ground is wet" ≠ "If ground is wet, it rained"

### Inverse is NOT Equivalent
```
p → q ≢ ¬p → ¬q
```

### But Contrapositive IS Equivalent
```
p → q ≡ ¬q → ¬p
```

## Simplification Using Equivalences

### Example 1
Simplify: ¬(p → q)
```
¬(p → q) ≡ ¬(¬p ∨ q)     [Implication]
         ≡ ¬(¬p) ∧ ¬q    [De Morgan]
         ≡ p ∧ ¬q        [Double Negation]
```

### Example 2
Simplify: (p ∧ q) ∨ (p ∧ ¬q)
```
(p ∧ q) ∨ (p ∧ ¬q) ≡ p ∧ (q ∨ ¬q)  [Distributive]
                    ≡ p ∧ T          [Complement]
                    ≡ p              [Identity]
```

### Example 3
Simplify: ¬(¬p ∨ q) ∨ (p ∧ ¬q)
```
¬(¬p ∨ q) ∨ (p ∧ ¬q) ≡ (p ∧ ¬q) ∨ (p ∧ ¬q)  [De Morgan, Double Neg]
                      ≡ p ∧ ¬q               [Idempotent]
```

## Equivalence Classes

### Definition
An equivalence class is a set of all propositions equivalent to each other.

### Examples
- {T, p ∨ ¬p, (p → q) ∨ (q → p), ...} - All tautologies
- {F, p ∧ ¬p, ...} - All contradictions
- {p, ¬¬p, p ∧ T, p ∨ F, ...} - All equivalent to p

## Applications

### Circuit Optimization
Replace complex circuits with simpler equivalent ones.

### Proof Simplification
Transform complex statements into simpler equivalent forms.

### Query Optimization
Rewrite database queries using equivalent but faster forms.

### Program Transformation
Optimize code by replacing expressions with equivalents.

## Exercises

1. Prove: ¬(p ↔ q) ≡ p ⊕ q
2. Simplify: (p → q) ∧ (p → ¬q)
3. Show: p → (q → r) ≡ (p ∧ q) → r
4. Prove: (p → q) ∧ (r → q) ≡ (p ∨ r) → q
5. Simplify: ¬(p → q) ∨ ¬(q → p)

## Key Insights

- **Equivalence preserves meaning**: Equivalent expressions are interchangeable
- **Many forms, one meaning**: Infinitely many equivalent expressions exist
- **Simplification is valuable**: Simpler forms are easier to work with
- **Contrapositive is key**: Often the easiest way to prove implications

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
