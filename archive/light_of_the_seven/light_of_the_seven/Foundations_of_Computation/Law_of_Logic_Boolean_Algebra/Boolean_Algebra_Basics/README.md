# Boolean Algebra Basics

## Overview

Boolean algebra operates on binary values (0 and 1, or FALSE and TRUE) using three fundamental operations. It forms the mathematical basis for all digital logic circuits and computer operations.

## Fundamental Concepts

### Binary Variables
- **Values**: Only two possible states: 0 (FALSE) or 1 (TRUE)
- **Representation**: Can represent voltage levels, switch states, or logical conditions
- **Notation**: Variables typically denoted as A, B, C, X, Y, Z

### The Three Basic Operations

#### 1. AND Operation (Conjunction)
- **Symbol**: · or ∧
- **Notation**: A · B or AB or A ∧ B
- **Definition**: Output is 1 only when ALL inputs are 1

| A | B | A · B |
|---|---|-------|
| 0 | 0 |   0   |
| 0 | 1 |   0   |
| 1 | 0 |   0   |
| 1 | 1 |   1   |

#### 2. OR Operation (Disjunction)
- **Symbol**: + or ∨
- **Notation**: A + B or A ∨ B
- **Definition**: Output is 1 when ANY input is 1

| A | B | A + B |
|---|---|-------|
| 0 | 0 |   0   |
| 0 | 1 |   1   |
| 1 | 0 |   1   |
| 1 | 1 |   1   |

#### 3. NOT Operation (Negation/Complement)
- **Symbol**: ' or ¬ or overbar
- **Notation**: A' or ¬A or Ā
- **Definition**: Inverts the input value

| A | A' |
|---|-----|
| 0 |  1  |
| 1 |  0  |

## Boolean Constants

- **0 (Zero/FALSE)**: The additive identity; A + 0 = A
- **1 (One/TRUE)**: The multiplicative identity; A · 1 = A

## Boolean Expressions

### Definition
A Boolean expression is a combination of:
- Boolean variables (A, B, C, ...)
- Boolean constants (0, 1)
- Boolean operators (AND, OR, NOT)

### Examples
- Simple: `A + B`
- Compound: `(A · B) + C`
- Complex: `(A + B') · (C + D)`

### Operator Precedence
1. **NOT** (highest priority)
2. **AND**
3. **OR** (lowest priority)

Example: `A + B · C'` = `A + (B · (C'))`

## Duality Principle

Every Boolean theorem has a dual obtained by:
- Swapping AND (·) with OR (+)
- Swapping 0 with 1

Example:
- Original: A + 0 = A
- Dual: A · 1 = A

## Practical Applications

### Digital Circuits
- Logic gates implement Boolean operations
- Combinational circuits are Boolean functions
- Sequential circuits add memory to Boolean logic

### Computer Programming
- Conditional statements use Boolean logic
- Bitwise operations apply Boolean ops to bits
- Control flow depends on Boolean evaluation

### Database Queries
- WHERE clauses use Boolean conditions
- Search filters combine Boolean operators
- Set operations map to Boolean algebra

## Exercises

1. Evaluate: (1 · 0) + (1 · 1)
2. Simplify: A · A
3. Find the complement of: A + B
4. Write truth table for: A · (B + C)
5. Express in Boolean: "Either A is true, or both B and C are true"

## Key Insights

- **Binary is fundamental**: All digital computation reduces to 0s and 1s
- **Three operations suffice**: AND, OR, NOT can express any Boolean function
- **Precedence matters**: Always clarify with parentheses when in doubt
- **Duality provides shortcuts**: Prove one theorem, get another free

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
