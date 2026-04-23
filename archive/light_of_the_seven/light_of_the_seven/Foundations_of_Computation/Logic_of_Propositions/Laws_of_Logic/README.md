# Laws of Logic

## Overview

The laws of logic are fundamental principles that govern valid reasoning. These laws are tautologies - they are true regardless of the truth values of their component propositions. They form the foundation for all logical deduction and proof.

## The Three Classical Laws

### 1. Law of Identity
**Statement**: A thing is identical to itself.
```
p → p
p ↔ p
```
- Every proposition implies itself
- A proposition is equivalent to itself

### 2. Law of Non-Contradiction
**Statement**: A proposition cannot be both true and false simultaneously.
```
¬(p ∧ ¬p)
```
- No proposition and its negation can both be true
- Contradictions are always false

### 3. Law of Excluded Middle
**Statement**: A proposition is either true or false; there is no middle ground.
```
p ∨ ¬p
```
- Every proposition has a definite truth value
- No third truth value exists

## Equivalence Laws

### Double Negation
```
¬(¬p) ≡ p
```
Negating twice returns the original.

### Commutative Laws
```
p ∧ q ≡ q ∧ p
p ∨ q ≡ q ∨ p
```
Order of operands doesn't matter.

### Associative Laws
```
(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)
(p ∨ q) ∨ r ≡ p ∨ (q ∨ r)
```
Grouping of operands doesn't matter.

### Distributive Laws
```
p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)
p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)
```
Distribution of one connective over another.

## Identity and Domination Laws

### Identity Laws
```
p ∧ T ≡ p
p ∨ F ≡ p
```
T is identity for AND; F is identity for OR.

### Domination Laws
```
p ∧ F ≡ F
p ∨ T ≡ T
```
F dominates AND; T dominates OR.

### Idempotent Laws
```
p ∧ p ≡ p
p ∨ p ≡ p
```
Combining with self yields self.

## Complement Laws

### Complement
```
p ∧ ¬p ≡ F
p ∨ ¬p ≡ T
```

### De Morgan's Laws
```
¬(p ∧ q) ≡ ¬p ∨ ¬q
¬(p ∨ q) ≡ ¬p ∧ ¬q
```
Negation distributes by swapping AND/OR.

## Absorption Laws

### Standard Absorption
```
p ∧ (p ∨ q) ≡ p
p ∨ (p ∧ q) ≡ p
```

### Absorption with Negation
```
p ∨ (¬p ∧ q) ≡ p ∨ q
p ∧ (¬p ∨ q) ≡ p ∧ q
```

## Implication Laws

### Material Implication
```
p → q ≡ ¬p ∨ q
```

### Contrapositive
```
p → q ≡ ¬q → ¬p
```

### Exportation
```
(p ∧ q) → r ≡ p → (q → r)
```

### Negation of Implication
```
¬(p → q) ≡ p ∧ ¬q
```

## Biconditional Laws

### Definition
```
p ↔ q ≡ (p → q) ∧ (q → p)
```

### Alternative Forms
```
p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)
p ↔ q ≡ (¬p ∨ q) ∧ (p ∨ ¬q)
```

### Negation
```
¬(p ↔ q) ≡ p ↔ ¬q ≡ ¬p ↔ q
```

## Inference Rules

### Modus Ponens
```
p → q, p ⊢ q
```
If p implies q, and p is true, then q is true.

### Modus Tollens
```
p → q, ¬q ⊢ ¬p
```
If p implies q, and q is false, then p is false.

### Hypothetical Syllogism
```
p → q, q → r ⊢ p → r
```
Chain of implications.

### Disjunctive Syllogism
```
p ∨ q, ¬p ⊢ q
```
If one disjunct is false, the other is true.

### Conjunction Introduction
```
p, q ⊢ p ∧ q
```

### Conjunction Elimination
```
p ∧ q ⊢ p
p ∧ q ⊢ q
```

### Disjunction Introduction
```
p ⊢ p ∨ q
```

### Resolution
```
p ∨ q, ¬p ∨ r ⊢ q ∨ r
```

## Summary Table

| Law | AND Form | OR Form |
|-----|----------|---------|
| Identity | p ∧ T ≡ p | p ∨ F ≡ p |
| Domination | p ∧ F ≡ F | p ∨ T ≡ T |
| Idempotent | p ∧ p ≡ p | p ∨ p ≡ p |
| Complement | p ∧ ¬p ≡ F | p ∨ ¬p ≡ T |
| Commutative | p ∧ q ≡ q ∧ p | p ∨ q ≡ q ∨ p |
| Associative | (p∧q)∧r ≡ p∧(q∧r) | (p∨q)∨r ≡ p∨(q∨r) |
| Distributive | p∧(q∨r) ≡ (p∧q)∨(p∧r) | p∨(q∧r) ≡ (p∨q)∧(p∨r) |
| Absorption | p ∧ (p∨q) ≡ p | p ∨ (p∧q) ≡ p |
| De Morgan | ¬(p∧q) ≡ ¬p∨¬q | ¬(p∨q) ≡ ¬p∧¬q |

## Applications

### Proof Construction
Use laws to derive conclusions from premises.

### Expression Simplification
Apply laws to reduce complex expressions.

### Circuit Optimization
Minimize gate count using Boolean algebra laws.

### Program Verification
Prove program correctness using logical laws.

## Exercises

1. Prove using laws: ¬(p → q) ≡ p ∧ ¬q
2. Simplify: (p ∧ q) ∨ (p ∧ ¬q) ∨ (¬p ∧ q)
3. Derive q from: p → q, r → p, r
4. Prove: (p → q) ∧ (p → r) ≡ p → (q ∧ r)
5. Apply De Morgan to: ¬(p ∨ (q ∧ r))

## Key Insights

- **Laws are tools**: Use them to transform and simplify
- **Duality exists**: Most laws come in AND/OR pairs
- **Inference is mechanical**: Apply rules systematically
- **Foundation of reasoning**: All valid arguments use these laws

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
