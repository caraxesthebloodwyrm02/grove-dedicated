# Truth Tables

## Overview

A truth table is a systematic way to list all possible combinations of truth values for propositional variables and determine the resulting truth value of a compound proposition. Truth tables are fundamental tools for analyzing logical expressions.

## Structure of Truth Tables

### Components
1. **Input columns**: One for each propositional variable
2. **Intermediate columns**: Optional, for sub-expressions
3. **Output column**: Final truth value of the expression

### Row Count
For n propositional variables: 2ⁿ rows

| Variables | Rows |
|-----------|------|
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 5 | 32 |
| n | 2ⁿ |

### Standard Ordering
List combinations in binary counting order:
- 2 variables: 00, 01, 10, 11
- 3 variables: 000, 001, 010, 011, 100, 101, 110, 111

## Building Truth Tables

### Step-by-Step Method

1. **Identify variables**: List all propositional variables
2. **Create rows**: 2ⁿ rows for n variables
3. **Fill input columns**: Binary counting pattern
4. **Evaluate sub-expressions**: Work from innermost to outermost
5. **Compute final result**: Apply main connective

### Example: (p → q) ∧ (q → r)

| p | q | r | p → q | q → r | (p → q) ∧ (q → r) |
|---|---|---|-------|-------|-------------------|
| T | T | T |   T   |   T   |         T         |
| T | T | F |   T   |   F   |         F         |
| T | F | T |   F   |   T   |         F         |
| T | F | F |   F   |   T   |         F         |
| F | T | T |   T   |   T   |         T         |
| F | T | F |   T   |   F   |         F         |
| F | F | T |   T   |   T   |         T         |
| F | F | F |   T   |   T   |         T         |

## Truth Tables for Basic Connectives

### Negation (¬p)
| p | ¬p |
|---|-----|
| T |  F  |
| F |  T  |

### Conjunction (p ∧ q)
| p | q | p ∧ q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   F   |
| F | F |   F   |

### Disjunction (p ∨ q)
| p | q | p ∨ q |
|---|---|-------|
| T | T |   T   |
| T | F |   T   |
| F | T |   T   |
| F | F |   F   |

### Implication (p → q)
| p | q | p → q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   T   |
| F | F |   T   |

### Biconditional (p ↔ q)
| p | q | p ↔ q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   F   |
| F | F |   T   |

## Applications of Truth Tables

### 1. Determining Logical Type

**Tautology**: All rows are T
| p | ¬p | p ∨ ¬p |
|---|-----|--------|
| T |  F  |   T    |
| F |  T  |   T    |

**Contradiction**: All rows are F
| p | ¬p | p ∧ ¬p |
|---|-----|--------|
| T |  F  |   F    |
| F |  T  |   F    |

**Contingency**: Mix of T and F

### 2. Testing Logical Equivalence

Two expressions are equivalent if they have identical truth tables.

**Example**: p → q ≡ ¬p ∨ q

| p | q | p → q | ¬p | ¬p ∨ q |
|---|---|-------|-----|--------|
| T | T |   T   |  F  |   T    |
| T | F |   F   |  F  |   F    |
| F | T |   T   |  T  |   T    |
| F | F |   T   |  T  |   T    |

Columns 3 and 5 are identical ✓

### 3. Testing Validity of Arguments

An argument is valid if: whenever all premises are true, the conclusion is true.

**Example**: Modus Ponens
- Premise 1: p → q
- Premise 2: p
- Conclusion: q

| p | q | p → q | Premises True? | q |
|---|---|-------|----------------|---|
| T | T |   T   | Yes (T,T)      | T ✓ |
| T | F |   F   | No             | - |
| F | T |   T   | No             | - |
| F | F |   T   | No             | - |

When premises are all true (row 1), conclusion is true. Valid! ✓

### 4. Finding Satisfying Assignments

Find input combinations that make expression true.

**Example**: (p ∨ q) ∧ ¬p

| p | q | p ∨ q | ¬p | (p ∨ q) ∧ ¬p |
|---|---|-------|-----|--------------|
| T | T |   T   |  F  |      F       |
| T | F |   T   |  F  |      F       |
| F | T |   T   |  T  |      T       | ← Satisfying
| F | F |   F   |  T  |      F       |

Satisfying assignment: p = F, q = T

## Shortcuts and Efficiency

### Short-Circuit Evaluation
- **AND**: If first operand is F, result is F
- **OR**: If first operand is T, result is T

### Dominant Values
- 0 dominates AND (0 ∧ x = 0)
- 1 dominates OR (1 ∨ x = 1)

### Partial Tables
For large expressions, evaluate only needed rows:
- To prove tautology: try to find a row with F (if none, tautology)
- To prove satisfiability: find one row with T

## Limitations

### Exponential Growth
- 10 variables: 1,024 rows
- 20 variables: 1,048,576 rows
- 30 variables: over 1 billion rows

### Alternatives for Large Problems
- **BDDs**: Binary Decision Diagrams
- **SAT solvers**: Algorithmic satisfiability checking
- **Semantic methods**: Proof without enumeration

## Connection to Digital Logic

### Truth Table to Circuit
1. Identify rows where output = 1
2. Write minterm for each such row
3. OR all minterms together (SOP form)
4. Implement with gates

### Circuit to Truth Table
1. Enumerate all input combinations
2. Trace through circuit for each
3. Record output values

## Exercises

1. Build truth table for: ¬(p ∧ q) ↔ (¬p ∨ ¬q)
2. Determine if tautology: (p → q) → (¬q → ¬p)
3. Find all satisfying assignments: (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ ¬r)
4. Test equivalence: p → (q → r) and (p ∧ q) → r
5. Verify validity: p → q, q → r ⊢ p → r

## Key Insights

- **Exhaustive method**: Covers all possibilities
- **Mechanical process**: No creativity needed
- **Exponential cost**: Impractical for many variables
- **Foundation for logic**: Defines meaning of connectives

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
