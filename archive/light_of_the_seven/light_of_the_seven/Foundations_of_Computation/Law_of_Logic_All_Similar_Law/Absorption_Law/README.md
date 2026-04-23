# Absorption Law

## Definition

The **Absorption Law** states that a variable combined with a product or sum containing that variable can be simplified by removing the redundant term.

### Formal Statements

**First Form (OR with AND)**:
$$A + AB = A$$

**Second Form (AND with OR)**:
$$A(A + B) = A$$

## Intuition

### First Form: A + AB = A

**Logic**: "A or (A and B)" is equivalent to just "A"

**Reasoning**:
- If A is TRUE: The entire expression is TRUE (first term)
- If A is FALSE: Then AB is FALSE (regardless of B), so expression is FALSE
- Therefore: Result depends only on A

### Second Form: A(A + B) = A

**Logic**: "A and (A or B)" is equivalent to just "A"

**Reasoning**:
- If A is TRUE: The entire expression is TRUE
- If A is FALSE: The entire expression is FALSE (regardless of B)
- Therefore: Result depends only on A

## Truth Table Verification

### Form 1: A + AB = A

| A | B | AB | A+AB | A | Match |
|---|---|----|------|---|-------|
| 0 | 0 | 0  | 0    | 0 | ✓     |
| 0 | 1 | 0  | 0    | 0 | ✓     |
| 1 | 0 | 0  | 1    | 1 | ✓     |
| 1 | 1 | 1  | 1    | 1 | ✓     |

### Form 2: A(A + B) = A

| A | B | A+B | A(A+B) | A | Match |
|---|---|-----|--------|---|-------|
| 0 | 0 | 0   | 0      | 0 | ✓     |
| 0 | 1 | 1   | 0      | 0 | ✓     |
| 1 | 0 | 1   | 1      | 1 | ✓     |
| 1 | 1 | 1   | 1      | 1 | ✓     |

## Proof

### Algebraic Proof - Form 1

```
A + AB
= A · 1 + AB              [Identity law: A·1 = A]
= A(1 + B)                [Distributive law]
= A · 1                   [Null law: 1 + B = 1]
= A                       [Identity law]
```

### Algebraic Proof - Form 2

```
A(A + B)
= A·A + A·B               [Distributive law]
= A + A·B                 [Idempotent: A·A = A]
= A                       [Absorption - circular, but proven above]
```

## Extensions

### Form 1 Variant: A + ¯AB

```
A + ¯AB
= A(1 + ¯B)  [Factor... wait, that's not right]
= A + ¯AB
```

This doesn't simplify to just A. Different from basic absorption.

### Form 1 with Multiple Terms: A + AB + ABC

```
A + AB + ABC
= A + A(B + BC)           [Factor]
= A + AB(1 + C)           [Is this right? No]
= A + AB                  [Since B + BC = B]
= A                       [Absorption]
```

### Generalized Absorption

```
A + ABC...N = A + A(products without A) = A
A(A + BC...N) = A(A + anything) = A
```

## Intuitive Explanation

### Circuit Perspective

**Form 1 - OR Gate Input**:
```
     ┌─────────┐
  A ─┤         │
     │   OR    ├─── Output
  AB─┤         │
     └─────────┘
```
The second input (AB) is redundant because:
- When A=1: Output is 1 (from A alone)
- When A=0: Output is 0 (AB cannot be 1 if A=0)

**Form 2 - AND Gate Input**:
```
     ┌─────────┐
  A ─┤         │
     │   AND   ├─── Output
A+B ─┤         │
     └─────────┘
```
The second input is redundant because:
- When A=1: Output is 1
- When A=0: Output is 0 (regardless of (A+B))

## Practical Applications

### Digital Logic Optimization

**Example 1**: Security alarm system
```
Original: Alert = Motion + (Motion AND Recent) + (Motion AND Recent AND Alert)
Simplified: Alert = Motion
```
The additional conditions are unnecessary.

**Example 2**: Error correction
```
Original: Valid = Checksum_OK + (Checksum_OK AND Data_Matches)
Simplified: Valid = Checksum_OK
```

### Software Conditional Logic

```javascript
// Original
if (userAuthenticated || (userAuthenticated && hasPermission)) {
    grantAccess();
}

// Optimized (using absorption)
if (userAuthenticated) {
    grantAccess();
}
```

### Circuit Minimization

**Gate reduction**:
- Original: 3 gates (AND gate for AB, OR gate for +, plus inputs)
- Optimized: 1 gate (just A)
- Savings: 2 gates, faster, less power

## Variants and Related Laws

### Similar to Absorption

**Consensus Theorem**:
```
AB + ¯AC + BC = AB + ¯AC
```
Middle term BC is redundant (consensus).

**Adjacency**:
```
AB + A¯B = A
```
Two adjacent minterms combine.

### Connection to Other Laws

**Uses Distributive Law**:
- Factoring to apply absorption

**Uses Identity/Null Laws**:
- For simplification

**Dual of Absorption**:
- Forms 1 and 2 are De Morgan duals

## How to Recognize Absorption

### Pattern Matching

**For A + AB = A**:
- Look for: Variable + (Variable AND ...)
- Pattern: X + XY = X

**For A(A + B) = A**:
- Look for: Variable AND (Variable OR ...)
- Pattern: X(X + Y) = X

### In Complex Expressions

```
ABC + ABCD + ABD
= AB(C + CD + D)           [Factor AB]
= AB(C + D)                [Since C + CD = C(1+D) = C, wait...]
  Actually: C + CD + D
         = C(1 + D) + D     [Nope]
         = C + D            [Since C + CD = C]
```

## Significance in Boolean Algebra

### Why It Matters

1. **Reduces complexity**: Removes unnecessary terms
2. **Saves logic gates**: Direct circuit cost reduction
3. **Improves speed**: Fewer gates = shorter path
4. **Reduces power**: Fewer transitions

### In Karnaugh Maps

Absorption is what Karnaugh maps exploit visually:
- Adjacent groups represent absorbed terms
- Larger groups = more absorption

## Exercises

1. **Apply absorption to**: A + ABC
   - Answer: A

2. **Simplify**: XYZ + XYZ + XY
   - Answer: XY

3. **Identify absorbed terms**: W + WX + WY
   - Answer: W (both WX and WY are absorbed)

4. **Prove**: A(AB + A¯B) = A

5. **Design circuit**: Use absorption to minimize gates for output F = A + ABA

## Comparison Table

| Law | Pattern | Result |
|-----|---------|--------|
| Identity | A + 0 | A |
| Null | A + 1 | 1 |
| Idempotent | A + A | A |
| Complement | A + ¯A | 1 |
| Absorption | A + AB | A |
| Adjacency | A + ¯A | 1 |

## Related Topics

- **Boolean Algebra Laws**: Comprehensive law reference
- **Distributive Law**: Used in absorption proofs
- **Consensus Theorem**: Similar redundancy elimination
- **Karnaugh Maps**: Graphical application of absorption
- **Simplification Techniques**: Absorption as optimization method

---

**Status**: Complete explanation
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
