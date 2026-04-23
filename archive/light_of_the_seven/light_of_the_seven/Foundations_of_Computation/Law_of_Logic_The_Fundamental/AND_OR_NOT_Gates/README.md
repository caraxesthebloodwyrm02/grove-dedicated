# AND, OR, NOT Gates

## Overview

AND, OR, and NOT are the three fundamental logic gates that directly implement the basic Boolean operations. Every other gate and every digital circuit can be constructed from combinations of these three primitives.

## AND Gate

### Definition
Outputs 1 only when ALL inputs are 1.

### Truth Table (2-input)

| A | B | A AND B |
|---|---|---------|
| 0 | 0 |    0    |
| 0 | 1 |    0    |
| 1 | 0 |    0    |
| 1 | 1 |    1    |

### Boolean Expression
```
Y = A · B  (also written as AB or A ∧ B)
```

### Symbol
```
    A ──┬──╮
        │  D──── Y
    B ──┴──╯
```
(Flat back, curved front)

### Characteristics
- **Identity**: A · 1 = A
- **Null**: A · 0 = 0
- **Idempotent**: A · A = A
- **Complement**: A · A' = 0

### Applications
- **Enable signals**: Gate passes data only when enabled
- **Masking**: Select specific bits
- **Coincidence detection**: Both conditions must be true

### N-Input AND
```
Y = A · B · C · D · ...
```
Output = 1 only if ALL inputs = 1

## OR Gate

### Definition
Outputs 1 when ANY input is 1.

### Truth Table (2-input)

| A | B | A OR B |
|---|---|--------|
| 0 | 0 |   0    |
| 0 | 1 |   1    |
| 1 | 0 |   1    |
| 1 | 1 |   1    |

### Boolean Expression
```
Y = A + B  (also written as A ∨ B)
```

### Symbol
```
    A ──╮
        ├)──── Y
    B ──╯
```
(Curved back, pointed front)

### Characteristics
- **Identity**: A + 0 = A
- **Null**: A + 1 = 1
- **Idempotent**: A + A = A
- **Complement**: A + A' = 1

### Applications
- **Interrupt handling**: Any source triggers response
- **Fault detection**: Any error raises alarm
- **Signal merging**: Combine multiple sources

### N-Input OR
```
Y = A + B + C + D + ...
```
Output = 1 if ANY input = 1

## NOT Gate (Inverter)

### Definition
Outputs the complement of the input.

### Truth Table

| A | NOT A |
|---|-------|
| 0 |   1   |
| 1 |   0   |

### Boolean Expression
```
Y = A'  (also written as Ā or ¬A)
```

### Symbol
```
    A ──▷○──── Y
```
(Triangle with bubble)

### Characteristics
- **Involution**: (A')' = A
- **Single input**: Only gate with one input
- **No identity**: Always changes the value

### Applications
- **Signal inversion**: Convert active-high to active-low
- **Complement generation**: Create A' from A
- **Level shifting**: Invert logic sense

## CMOS Implementation

### NOT Gate (Inverter)
```
        VDD
         │
        ┌┴┐
    A ──┤P├──┬── Y
        └┬┘  │
        ┌┴┐  │
    A ──┤N├──┘
        └┬┘
         │
        GND
```
- PMOS pulls up when A=0
- NMOS pulls down when A=1

### NAND Gate (AND requires inverter)
```
        VDD
         │
    ┌────┴────┐
   ┌┴┐       ┌┴┐
A──┤P├───┬───┤P├──B
   └┬┘   │   └┬┘
    └────┼────┘
         │
        ┌┴┐
    A ──┤N├
        └┬┘
        ┌┴┐
    B ──┤N├
        └┬┘
         │
        GND
```
AND = NAND + NOT (requires extra inverter)

### NOR Gate (OR requires inverter)
Similar structure with series PMOS, parallel NMOS.
OR = NOR + NOT

## Combining the Three Gates

### Any Function from AND, OR, NOT
Every Boolean function can be expressed in:
- **Sum of Products (SOP)**: AND gates feeding OR gate
- **Product of Sums (POS)**: OR gates feeding AND gate

### Example: XOR from AND, OR, NOT
```
A XOR B = A'B + AB'
        = (A + B) · (A' + B')
```

Implementation:
```
A ──┬──[NOT]──┬──[AND]──┐
    │         │         │
B ──┼────────┬┘         [OR]── Y
    │        │          │
A ──┼──[AND]─┼──────────┘
    │        │
B ──┴──[NOT]─┘
```

## Timing Analysis

### Propagation Delays (typical CMOS)
| Gate | tPLH | tPHL |
|------|------|------|
| NOT  | 1ns  | 1ns  |
| AND  | 2ns  | 2ns  |
| OR   | 2ns  | 2ns  |

Note: AND and OR typically implemented as NAND/NOR + NOT

### Critical Path
Total delay = sum of gate delays along longest path

## Exercises

1. Build a 3-input AND using 2-input ANDs
2. Implement f = AB + C using AND, OR, NOT
3. Count transistors for 2-input AND in CMOS
4. Calculate delay for: Y = (A·B) + (C·D)
5. Design enable circuit: Y = EN · DATA

## Key Insights

- **Three gates suffice**: AND, OR, NOT can build anything
- **NOT is cheapest**: Single inverter in CMOS
- **AND/OR need inversion**: NAND/NOR are more natural in CMOS
- **Completeness**: {AND, NOT} or {OR, NOT} alone are complete

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
