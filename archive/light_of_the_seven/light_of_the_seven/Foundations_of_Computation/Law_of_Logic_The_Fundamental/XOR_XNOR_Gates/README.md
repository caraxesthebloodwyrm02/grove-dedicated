# XOR and XNOR Gates

## Overview

XOR (Exclusive OR) and XNOR (Exclusive NOR) gates perform comparison and parity operations. Unlike AND/OR which are "inclusive," XOR/XNOR are "exclusive" - they distinguish between having exactly one input true versus having multiple inputs true.

## XOR Gate (Exclusive OR)

### Definition
Outputs 1 when inputs are **different** (odd number of 1s).

### Truth Table (2-input)

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 |    0    |
| 0 | 1 |    1    |
| 1 | 0 |    1    |
| 1 | 1 |    0    |

### Boolean Expressions
```
Y = A ⊕ B
  = A'B + AB'           (Sum of Products)
  = (A + B)(A' + B')    (Product of Sums)
  = (A + B)(AB)'        (Alternative form)
```

### Symbol
```
    A ──╮
        ╞)──── Y
    B ──╯
```
(OR symbol with extra curved line at input)

### Key Properties
- **Commutative**: A ⊕ B = B ⊕ A
- **Associative**: (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)
- **Identity**: A ⊕ 0 = A
- **Self-inverse**: A ⊕ A = 0
- **Complement**: A ⊕ 1 = A'

## XNOR Gate (Exclusive NOR)

### Definition
Outputs 1 when inputs are **same** (even number of 1s, including zero).

### Truth Table (2-input)

| A | B | A XNOR B |
|---|---|----------|
| 0 | 0 |    1     |
| 0 | 1 |    0     |
| 1 | 0 |    0     |
| 1 | 1 |    1     |

### Boolean Expressions
```
Y = A ⊙ B = (A ⊕ B)'
  = AB + A'B'           (Sum of Products)
  = (A + B')(A' + B)    (Product of Sums)
```

### Symbol
```
    A ──╮
        ╞)○──── Y
    B ──╯
```
(XOR symbol with bubble on output)

### Key Properties
- **Equivalence**: Outputs 1 when A equals B
- **Complement of XOR**: A ⊙ B = (A ⊕ B)'
- **Identity**: A ⊙ 1 = A
- **Self-inverse**: A ⊙ A = 1

## Relationship Between XOR and XNOR

```
XNOR = NOT(XOR)
A ⊙ B = (A ⊕ B)'

Also:
A ⊙ B = A'B' + AB    (same values)
A ⊕ B = A'B + AB'    (different values)
```

## N-Input XOR/XNOR

### N-Input XOR
Outputs 1 when **odd number** of inputs are 1.

| A | B | C | A⊕B⊕C |
|---|---|---|-------|
| 0 | 0 | 0 |   0   |
| 0 | 0 | 1 |   1   |
| 0 | 1 | 0 |   1   |
| 0 | 1 | 1 |   0   |
| 1 | 0 | 0 |   1   |
| 1 | 0 | 1 |   0   |
| 1 | 1 | 0 |   0   |
| 1 | 1 | 1 |   1   |

### N-Input XNOR
Outputs 1 when **even number** of inputs are 1 (including zero).

### Parity Function
- **Odd parity**: XOR of all bits
- **Even parity**: XNOR of all bits (or XOR inverted)

## Implementation

### XOR from Basic Gates
```
A ⊕ B = A'B + AB'

    A ──┬──[NOT]──[AND]──┐
        │         ↑      │
        │         B      [OR]── Y
        │                │
        └──[AND]─────────┘
            ↑
        B──[NOT]
```

### XOR from NAND Gates
Requires 4 NAND gates:
```
         ┌─[NAND]─┐
    A ───┤        ├─[NAND]─┐
         └────────┘        │
    A ───┐                 ├─[NAND]── Y
         ├─[NAND]──────────┘
    B ───┘
         ┌─[NAND]─┐
    B ───┤        │
         └────────┘
```

### Transmission Gate XOR (CMOS)
More efficient implementation using pass transistors.

## Applications

### Arithmetic Circuits

#### Half Adder
```
Sum = A ⊕ B
Carry = A · B
```

#### Full Adder
```
Sum = A ⊕ B ⊕ Cin
Cout = AB + Cin(A ⊕ B)
```

### Parity Generator/Checker
- **Generator**: XOR all data bits to create parity bit
- **Checker**: XOR all bits including parity; 0 = no error

### Comparator
```
A = B  when  A ⊙ B = 1
A ≠ B  when  A ⊕ B = 1
```

### Controlled Inverter
```
Y = A ⊕ Control
- Control = 0: Y = A (pass through)
- Control = 1: Y = A' (invert)
```

### Cryptography
- **Stream ciphers**: XOR plaintext with keystream
- **One-time pad**: XOR with random key
- **Self-inverse property**: Encrypt and decrypt are same operation

### Error Detection
- **CRC (Cyclic Redundancy Check)**: Based on XOR operations
- **Checksum**: XOR-based error detection
- **RAID**: XOR for parity calculation

## Special Properties

### Cancellation
```
A ⊕ A = 0
A ⊕ 0 = A
```
XORing a value with itself cancels it.

### Swap Without Temporary
```
A = A ⊕ B
B = A ⊕ B  (now B = original A)
A = A ⊕ B  (now A = original B)
```

### Linear Function
XOR is the only gate that is a linear function over GF(2).

## Exercises

1. Implement XNOR using only NAND gates
2. Design a 4-bit parity generator
3. Build a 2-bit comparator using XOR/XNOR
4. Prove: A ⊕ B ⊕ C = A ⊕ (B ⊕ C)
5. Design controlled inverter with enable

## Key Insights

- **XOR detects difference**: Essential for comparison
- **XNOR detects equality**: Natural for matching
- **Parity is XOR**: Odd 1s detection
- **Self-inverse enables crypto**: XOR twice returns original
- **Linear over GF(2)**: Unique algebraic property

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
