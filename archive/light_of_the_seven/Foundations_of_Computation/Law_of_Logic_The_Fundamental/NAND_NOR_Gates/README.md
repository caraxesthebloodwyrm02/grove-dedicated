# NAND and NOR Gates

## Overview

NAND (NOT-AND) and NOR (NOT-OR) gates are inverted versions of AND and OR. They have a special property: each is **functionally complete**, meaning any Boolean function can be implemented using only NAND gates or only NOR gates.

## NAND Gate

### Definition
Outputs 0 only when ALL inputs are 1 (inverse of AND).

### Truth Table (2-input)

| A | B | A NAND B |
|---|---|----------|
| 0 | 0 |    1     |
| 0 | 1 |    1     |
| 1 | 0 |    1     |
| 1 | 1 |    0     |

### Boolean Expression
```
Y = (A · B)'  (also written as A ⊼ B)
```

### Symbol
```
    A ──┬──╮
        │  D○──── Y
    B ──┴──╯
```
(AND symbol with bubble on output)

### Key Property
NAND is the **complement of AND**:
- AND outputs 1 when all inputs are 1
- NAND outputs 0 when all inputs are 1

## NOR Gate

### Definition
Outputs 1 only when ALL inputs are 0 (inverse of OR).

### Truth Table (2-input)

| A | B | A NOR B |
|---|---|---------|
| 0 | 0 |    1    |
| 0 | 1 |    0    |
| 1 | 0 |    0    |
| 1 | 1 |    0    |

### Boolean Expression
```
Y = (A + B)'  (also written as A ⊽ B)
```

### Symbol
```
    A ──╮
        ├)○──── Y
    B ──╯
```
(OR symbol with bubble on output)

### Key Property
NOR is the **complement of OR**:
- OR outputs 1 when any input is 1
- NOR outputs 0 when any input is 1

## CMOS Implementation

### NAND Gate
```
        VDD
         │
    ┌────┴────┐
   ┌┴┐       ┌┴┐
A──┤P├───────┤P├──B
   └┬┘       └┬┘
    └────┬────┘
         ├──── Y
        ┌┴┐
    A ──┤N├
        └┬┘
        ┌┴┐
    B ──┤N├
        └┬┘
         │
        GND
```
- **PMOS in parallel**: Either can pull up
- **NMOS in series**: Both needed to pull down
- **Natural in CMOS**: No extra inverter needed

### NOR Gate
```
        VDD
         │
        ┌┴┐
    A ──┤P├
        └┬┘
        ┌┴┐
    B ──┤P├
        └┬┘
         ├──── Y
    ┌────┴────┐
   ┌┴┐       ┌┴┐
A──┤N├───────┤N├──B
   └┬┘       └┬┘
    └────┬────┘
         │
        GND
```
- **PMOS in series**: Both needed to pull up
- **NMOS in parallel**: Either can pull down
- **Natural in CMOS**: No extra inverter needed

## Why NAND/NOR are Preferred in CMOS

### Transistor Count Comparison

| Gate | Transistors (CMOS) |
|------|-------------------|
| NOT  | 2                 |
| NAND | 4                 |
| NOR  | 4                 |
| AND  | 6 (NAND + NOT)    |
| OR   | 6 (NOR + NOT)     |

### Speed Comparison
- NAND/NOR: Single gate delay
- AND/OR: Two gate delays (inverted gate + inverter)

### Conclusion
NAND and NOR are more efficient than AND and OR in CMOS technology.

## De Morgan's Law Connection

### NAND via De Morgan
```
(A · B)' = A' + B'
```
NAND is equivalent to OR with inverted inputs.

### NOR via De Morgan
```
(A + B)' = A' · B'
```
NOR is equivalent to AND with inverted inputs.

### Practical Use
Convert between NAND-NAND and AND-OR implementations:
```
AND-OR: Y = AB + CD
NAND-NAND: Y = ((AB)' · (CD)')'
         = NAND(NAND(A,B), NAND(C,D))
```

## Building Other Gates from NAND

### NOT from NAND
```
A ──┬──╮
    │  D○──── A'
A ──┴──╯
```
Connect both inputs together: (A · A)' = A'

### AND from NAND
```
A ──┬──╮        ┌──╮
    │  D○───┬───│  D○──── A·B
B ──┴──╯    └───┴──╯
```
NAND followed by NOT (another NAND as inverter)

### OR from NAND
```
A ──┬──╮
    │  D○───┐
A ──┴──╯    │   ┌──╮
            ├───│  D○──── A+B
B ──┬──╮    │   └──╯
    │  D○───┘
B ──┴──╯
```
Invert inputs, then NAND: (A')' + (B')' via De Morgan

## Building Other Gates from NOR

### NOT from NOR
```
A ──╮
    ├)○──── A'
A ──╯
```
Connect both inputs together: (A + A)' = A'

### OR from NOR
```
A ──╮         ╮
    ├)○───┬───├)○──── A+B
B ──╯     └───╯
```
NOR followed by NOT

### AND from NOR
```
A ──╮
    ├)○───┐
A ──╯     │   ╮
          ├───├)○──── A·B
B ──╮     │   ╯
    ├)○───┘
B ──╯
```
Invert inputs, then NOR

## Applications

### NAND Flash Memory
- Storage cells use NAND gate structure
- Cells connected in series
- High density, lower cost per bit

### NOR Flash Memory
- Storage cells use NOR gate structure
- Cells connected in parallel
- Faster random access, lower density

### Standard Cell Libraries
- NAND/NOR are basic cells
- Multiple drive strengths available
- Optimized for area, speed, power

## Exercises

1. Implement XOR using only NAND gates
2. Implement XOR using only NOR gates
3. Count NAND gates needed for: f = AB + CD
4. Convert AND-OR to NAND-NAND: f = (A+B)(C+D)
5. Compare transistor count: NAND vs NOR implementation of f = AB + C

## Key Insights

- **NAND/NOR are universal**: Either alone can implement any function
- **CMOS favors inversion**: NAND/NOR are natural, AND/OR need extra inverter
- **De Morgan enables conversion**: Switch between AND-OR and NAND-NOR freely
- **Technology drives choice**: NAND for density, NOR for speed

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
