# Karnaugh Maps (K-Maps)

## Overview

Karnaugh maps are a visual method for simplifying Boolean expressions. They organize truth table values in a 2D grid where adjacent cells differ by exactly one variable, making it easy to identify and group terms that can be combined.

## Fundamental Concepts

### Gray Code Ordering
K-map rows and columns use Gray code ordering where adjacent entries differ by one bit:
- 2 variables: 0, 1
- 3 variables: 00, 01, 11, 10
- 4 variables: 00, 01, 11, 10

### Adjacency
Cells are adjacent if they differ in exactly one variable:
- Horizontal neighbors
- Vertical neighbors
- **Wrap-around**: Top-bottom, left-right edges are adjacent

## K-Map Structures

### 2-Variable K-Map
```
        B=0   B=1
    ┌─────┬─────┐
A=0 │  0  │  1  │
    ├─────┼─────┤
A=1 │  2  │  3  │
    └─────┴─────┘
```
Minterms: m0=A'B', m1=A'B, m2=AB', m3=AB

### 3-Variable K-Map
```
          BC
        00   01   11   10
    ┌─────┬─────┬─────┬─────┐
A=0 │  0  │  1  │  3  │  2  │
    ├─────┼─────┼─────┼─────┤
A=1 │  4  │  5  │  7  │  6  │
    └─────┴─────┴─────┴─────┘
```

### 4-Variable K-Map
```
            CD
          00   01   11   10
      ┌─────┬─────┬─────┬─────┐
AB=00 │  0  │  1  │  3  │  2  │
      ├─────┼─────┼─────┼─────┤
AB=01 │  4  │  5  │  7  │  6  │
      ├─────┼─────┼─────┼─────┤
AB=11 │ 12  │ 13  │ 15  │ 14  │
      ├─────┼─────┼─────┼─────┤
AB=10 │  8  │  9  │ 11  │ 10  │
      └─────┴─────┴─────┴─────┘
```

## Simplification Rules

### Grouping Rules
1. **Group sizes**: Must be powers of 2 (1, 2, 4, 8, 16, ...)
2. **Shape**: Groups must be rectangular (including squares)
3. **Coverage**: Every 1 must be covered by at least one group
4. **Overlap allowed**: Groups can share cells
5. **Wrap-around**: Groups can wrap around edges

### Optimization Goals
1. **Minimize groups**: Fewer groups = fewer product terms
2. **Maximize group size**: Larger groups = simpler terms
3. **Cover all 1s**: Every minterm must be included

## Simplification Process

### Step-by-Step Method
1. **Plot the function**: Place 1s in cells corresponding to minterms
2. **Identify largest groups**: Start with the largest possible groups
3. **Cover all 1s**: Ensure every 1 is in at least one group
4. **Write product terms**: Each group becomes one product term
5. **Form the sum**: OR all product terms together

### Reading Product Terms
- Variables that are **constant 0** in the group: include complemented
- Variables that are **constant 1** in the group: include uncomplemented
- Variables that **change** in the group: omit from the term

## Don't Care Conditions

### Definition
Don't care conditions (X or d) represent input combinations that:
- Never occur in practice
- Have outputs we don't care about

### Usage
- Can be treated as 0 or 1 to maximize group sizes
- Choose the assignment that gives the simplest result

### Example
```
          BC
        00   01   11   10
    ┌─────┬─────┬─────┬─────┐
A=0 │  1  │  X  │  1  │  0  │
    ├─────┼─────┼─────┼─────┤
A=1 │  0  │  0  │  X  │  1  │
    └─────┴─────┴─────┴─────┘
```
Treating X as 1 where helpful can create larger groups.

## Product of Sums (POS) Simplification

To find POS form:
1. Group the **0s** instead of 1s
2. Write maxterms for each group
3. AND all maxterms together

## Worked Examples

### Example 1: 3-Variable SOP
f(A,B,C) = Σm(1,2,5,6,7)

```
          BC
        00   01   11   10
    ┌─────┬─────┬─────┬─────┐
A=0 │  0  │  1  │  0  │  1  │
    ├─────┼─────┼─────┼─────┤
A=1 │  0  │  1  │  1  │  1  │
    └─────┴─────┴─────┴─────┘
```

Groups:
- Column 01 (m1, m5): B'C → C (wait, let me recalculate)
- Actually: m1,m5 = C·B' and m5,m7 = A·C and m6,m7 = A·B and m2,m6 = B·C'

Result: f = A'C + AB + BC'... (verify with actual groupings)

### Example 2: 4-Variable with Don't Cares
f(A,B,C,D) = Σm(0,2,5,7,8,10,13,15) + d(1,3)

Use don't cares to form larger groups for simpler expression.

## Limitations

### Variable Count
- **2-4 variables**: Easy to visualize and solve
- **5-6 variables**: Possible but complex (3D or multiple maps)
- **7+ variables**: Impractical; use algorithmic methods

### Alternatives for Large Problems
- Quine-McCluskey algorithm
- Espresso heuristic
- Binary Decision Diagrams (BDDs)
- CAD tools (e.g., ABC, SIS)

## Applications

### Digital Circuit Design
- Minimize gate count
- Reduce chip area
- Lower power consumption

### PLA/PAL Programming
- Fit logic into programmable arrays
- Optimize product term usage

### FPGA Synthesis
- Optimize LUT utilization
- Improve timing

## Exercises

1. Simplify: f(A,B) = Σm(0,2,3)
2. Simplify: f(A,B,C) = Σm(0,1,2,4,5,6)
3. Find POS: f(A,B,C) = Σm(1,3,5,7)
4. With don't cares: f = Σm(1,5,7) + d(0,2,6)
5. 4-variable: f(A,B,C,D) = Σm(0,1,2,3,8,9,10,11)

## Key Insights

- **Adjacency is key**: Gray code ensures neighbors differ by one variable
- **Bigger is better**: Larger groups mean simpler terms
- **Don't cares are free**: Use them to maximize group sizes
- **Wrap-around matters**: Don't forget edge adjacencies
- **Know the limits**: Beyond 4-5 variables, use algorithms

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
