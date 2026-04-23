# Propositional Calculus

## Overview

Propositional calculus (also called propositional logic or sentential calculus) is a formal system for reasoning about propositions. It provides a rigorous framework for constructing proofs and deriving conclusions from premises.

## Components of the Formal System

### 1. Alphabet (Symbols)
- **Propositional variables**: p, q, r, s, ... (infinite supply)
- **Logical connectives**: ¬, ∧, ∨, →, ↔
- **Punctuation**: (, )
- **Constants**: ⊤ (true), ⊥ (false)

### 2. Well-Formed Formulas (WFFs)
Rules for constructing valid expressions:
1. Every propositional variable is a WFF
2. ⊤ and ⊥ are WFFs
3. If φ is a WFF, then (¬φ) is a WFF
4. If φ and ψ are WFFs, then (φ ∧ ψ), (φ ∨ ψ), (φ → ψ), (φ ↔ ψ) are WFFs
5. Nothing else is a WFF

### 3. Axioms
Statements assumed true without proof.

**Łukasiewicz Axiom System:**
1. φ → (ψ → φ)
2. (φ → (ψ → χ)) → ((φ → ψ) → (φ → χ))
3. (¬φ → ¬ψ) → (ψ → φ)

### 4. Inference Rules
Rules for deriving new theorems.

**Modus Ponens (MP):**
```
From φ and φ → ψ, derive ψ
```

## Proof Systems

### Natural Deduction

#### Introduction Rules
| Connective | Rule | Form |
|------------|------|------|
| ∧ | ∧-intro | From φ and ψ, derive φ ∧ ψ |
| ∨ | ∨-intro | From φ, derive φ ∨ ψ |
| → | →-intro | From assumption φ leading to ψ, derive φ → ψ |
| ¬ | ¬-intro | From assumption φ leading to ⊥, derive ¬φ |

#### Elimination Rules
| Connective | Rule | Form |
|------------|------|------|
| ∧ | ∧-elim | From φ ∧ ψ, derive φ (or ψ) |
| ∨ | ∨-elim | From φ ∨ ψ, φ → χ, ψ → χ, derive χ |
| → | →-elim | From φ → ψ and φ, derive ψ (Modus Ponens) |
| ¬ | ¬-elim | From ¬¬φ, derive φ |

### Sequent Calculus

#### Notation
```
Γ ⊢ Δ
```
- Γ: Set of assumptions (antecedent)
- Δ: Set of conclusions (succedent)
- ⊢: "proves" or "entails"

#### Key Rules
- **Weakening**: Add unused assumptions
- **Contraction**: Remove duplicate assumptions
- **Cut**: Chain proofs together

### Hilbert System

#### Characteristics
- Few inference rules (often just MP)
- Many axiom schemas
- Proofs can be long but systematic

#### Example Axioms
```
A1: φ → (ψ → φ)
A2: (φ → (ψ → χ)) → ((φ → ψ) → (φ → χ))
A3: (¬ψ → ¬φ) → (φ → ψ)
```

## Proof Techniques

### Direct Proof
1. Assume premises
2. Apply inference rules
3. Derive conclusion

**Example**: Prove p → r from p → q and q → r
```
1. p → q         (premise)
2. q → r         (premise)
3. Assume p      (for →-intro)
4. q             (→-elim: 1, 3)
5. r             (→-elim: 2, 4)
6. p → r         (→-intro: 3-5)
```

### Proof by Contradiction (Reductio ad Absurdum)
1. Assume negation of goal
2. Derive contradiction
3. Conclude goal is true

**Example**: Prove p from ¬p → ⊥
```
1. ¬p → ⊥        (premise)
2. Assume ¬p     (for contradiction)
3. ⊥             (→-elim: 1, 2)
4. p             (¬-elim from contradiction)
```

### Proof by Cases
1. Have φ ∨ ψ
2. Prove goal from φ
3. Prove goal from ψ
4. Conclude goal

### Conditional Proof
1. Assume antecedent
2. Derive consequent
3. Conclude implication

## Metatheorems

### Soundness
If Γ ⊢ φ (φ is provable from Γ), then Γ ⊨ φ (φ is true whenever all of Γ is true).

**Meaning**: Provable statements are true.

### Completeness
If Γ ⊨ φ (φ is true whenever all of Γ is true), then Γ ⊢ φ (φ is provable from Γ).

**Meaning**: True statements are provable.

### Decidability
There exists an algorithm to determine whether any given WFF is a theorem.

**Method**: Truth tables (exponential but finite)

### Compactness
If every finite subset of Γ is satisfiable, then Γ is satisfiable.

## Formal Proofs

### Proof Format
```
Line | Statement | Justification
-----|-----------|---------------
1    | φ₁        | Premise
2    | φ₂        | Premise
3    | φ₃        | Rule (line references)
...  | ...       | ...
n    | ψ         | Conclusion
```

### Example: Modus Tollens
Prove ¬p from p → q and ¬q

```
1  | p → q      | Premise
2  | ¬q         | Premise
3  | Assume p   | Assumption (for ¬-intro)
4  | q          | →-elim (1, 3)
5  | ⊥          | ¬-elim (2, 4)
6  | ¬p         | ¬-intro (3-5)
```

## Applications

### Automated Theorem Proving
- SAT solvers
- Resolution-based provers
- Tableaux methods

### Program Verification
- Hoare logic
- Precondition/postcondition reasoning
- Loop invariants

### Hardware Verification
- Model checking
- Equivalence checking
- Property verification

### Knowledge Representation
- Expert systems
- Logic programming
- Semantic web

## Exercises

1. Prove: (p → q) → (¬q → ¬p) [Contrapositive]
2. Prove: p ∧ (p → q) → q [Modus Ponens as theorem]
3. Prove: (p → q) ∧ (q → r) → (p → r) [Hypothetical Syllogism]
4. Prove: ¬(p ∧ q) ↔ (¬p ∨ ¬q) [De Morgan]
5. Prove: ((p → q) → p) → p [Peirce's Law]

## Key Insights

- **Syntax vs. Semantics**: Proofs are syntactic; truth is semantic
- **Soundness + Completeness**: Syntax and semantics align perfectly
- **Mechanical verification**: Proofs can be checked by algorithm
- **Foundation for mathematics**: All mathematical proof rests on logic

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
