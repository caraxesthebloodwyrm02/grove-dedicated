# Boolean Algebra Theorems

## Overview

Boolean algebra theorems are proven statements that extend the basic identities to more complex relationships. These theorems provide powerful tools for simplifying and transforming Boolean expressions.

## De Morgan's Theorems

The most important theorems in Boolean algebra, enabling conversion between AND and OR operations.

### First Theorem
The complement of a product equals the sum of the complements.

```
(A · B)' = A' + B'
```

**Proof by Truth Table:**
| A | B | A·B | (A·B)' | A' | B' | A'+B' |
|---|---|-----|--------|----|----|-------|
| 0 | 0 |  0  |   1    | 1  | 1  |   1   |
| 0 | 1 |  0  |   1    | 1  | 0  |   1   |
| 1 | 0 |  0  |   1    | 0  | 1  |   1   |
| 1 | 1 |  1  |   0    | 0  | 0  |   0   |

### Second Theorem
The complement of a sum equals the product of the complements.

```
(A + B)' = A' · B'
```

### Generalized De Morgan's
Extends to any number of variables:
```
(A · B · C · ... · N)' = A' + B' + C' + ... + N'
(A + B + C + ... + N)' = A' · B' · C' · ... · N'
```

## Consensus Theorem

A redundant term can be eliminated when it is "covered" by other terms.

### Standard Form
```
AB + A'C + BC = AB + A'C
```

The term BC is the **consensus term** and is redundant.

### Dual Form
```
(A + B)(A' + C)(B + C) = (A + B)(A' + C)
```

### Proof
```
AB + A'C + BC
= AB + A'C + BC(A + A')           (Complement: A + A' = 1)
= AB + A'C + ABC + A'BC           (Distributive)
= AB(1 + C) + A'C(1 + B)          (Factoring)
= AB + A'C                         (Null: 1 + X = 1)
```

## Absorption Theorems

### Simple Absorption
```
A + AB = A
A(A + B) = A
```

### Absorption with Complement
```
A + A'B = A + B
A(A' + B) = AB
```

**Proof of A + A'B = A + B:**
```
A + A'B = (A + A')(A + B)         (Distributive: OR over AND)
        = 1 · (A + B)             (Complement)
        = A + B                    (Identity)
```

## Simplification Theorems

### Combining Theorem
```
AB + AB' = A
```

Two terms differing in one variable can be combined.

### Elimination Theorem
```
A + A'B = A + B
```

### Redundancy Theorem
```
A + AB = A
```

## Expansion Theorems

### Shannon's Expansion (Cofactor Expansion)
Any Boolean function can be expanded around a variable:

```
f(A, B, C, ...) = A · f(1, B, C, ...) + A' · f(0, B, C, ...)
```

This is fundamental for:
- Binary decision diagrams (BDDs)
- Circuit decomposition
- Functional verification

### Canonical Forms

#### Sum of Products (SOP)
```
f = Σm(minterms where f=1)
Example: f = A'B + AB' + AB
```

#### Product of Sums (POS)
```
f = ΠM(maxterms where f=0)
Example: f = (A + B)(A' + B')
```

## Duality Theorem

Every Boolean theorem has a dual obtained by:
1. Interchanging AND (·) and OR (+)
2. Interchanging 0 and 1

If a theorem is true, its dual is also true.

**Example:**
- Original: A + 0 = A
- Dual: A · 1 = A

## Transposition Theorem

```
AB + A'C = (A + C)(A' + B)
```

Useful for converting between SOP and POS forms.

## Applications

### Circuit Design
- Convert between gate types (NAND/NOR implementation)
- Minimize gate count
- Balance propagation delays

### Logic Optimization
- Reduce expression complexity
- Identify redundant terms
- Prepare for technology mapping

### Formal Verification
- Prove circuit equivalence
- Validate transformations
- Check design correctness

## Worked Examples

### Example 1: Apply De Morgan's
Simplify: ((AB)'C)'
```
((AB)'C)' = (AB)'' + C'    (De Morgan)
          = AB + C'         (Involution)
```

### Example 2: Apply Consensus
Simplify: XY + X'Z + YZ
```
XY + X'Z + YZ = XY + X'Z    (Consensus: YZ is redundant)
```

### Example 3: Shannon Expansion
Expand f(A,B) = AB + A'B' around A:
```
f = A · f(1,B) + A' · f(0,B)
  = A · (1·B + 0) + A' · (0 + 1·B')
  = A · B + A' · B'
```

## Exercises

1. Apply De Morgan's to: (A + B + C)'
2. Use consensus to simplify: PQ + P'R + QR
3. Prove: (A + B)(A + B') = A
4. Expand f = AB + BC around variable B
5. Convert to POS: f = A'B + AB'

## Key Insights

- **De Morgan's is universal**: Enables any AND-OR to NAND-NOR conversion
- **Consensus identifies redundancy**: Look for terms covered by others
- **Shannon expansion is systematic**: Works for any function, any variable
- **Duality halves the work**: Prove one theorem, get its dual free

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
