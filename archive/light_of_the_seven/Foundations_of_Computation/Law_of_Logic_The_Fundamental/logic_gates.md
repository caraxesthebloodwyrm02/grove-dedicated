# Law of Logic: The Fundamental Gates

## Overview

Logic gates are the physical building blocks of digital circuits. They implement Boolean operations in hardware, transforming electrical signals according to logical rules. Understanding gates is essential for bridging abstract Boolean algebra with concrete circuit implementation.

## Internal Map

- **Fundamental_Logic_Gates/**
  Overview of all gate types and their relationships

- **AND_OR_NOT_Gates/**
  The three basic gates that directly implement Boolean operations

- **NAND_NOR_Gates/**
  Inverted gates with special properties

- **XOR_XNOR_Gates/**
  Exclusive operations for parity and comparison

- **Universal_Gates/**
  How NAND and NOR can implement any Boolean function

## Role in the Directional-Derivative Workflow

From `directional_direvative.md`:

- **Gate Selection → RTL Implementation**
  - Choose gate types based on technology library
  - Map Boolean expressions to physical gates
  - Consider fan-in, fan-out, and timing

- **Universal Gates → Manufacturing Simplicity**
  - NAND-only or NOR-only designs simplify fabrication
  - Reduce mask count and process complexity

**Net effect:** This subtree provides the **physical vocabulary** for implementing the Boolean netlists from the algebra layer.

## Gate Summary Table

| Gate | Symbol | Expression | Output = 1 when... |
|------|--------|------------|-------------------|
| AND | · | A·B | All inputs are 1 |
| OR | + | A+B | Any input is 1 |
| NOT | ' | A' | Input is 0 |
| NAND | ⊼ | (A·B)' | Any input is 0 |
| NOR | ⊽ | (A+B)' | All inputs are 0 |
| XOR | ⊕ | A⊕B | Odd number of 1s |
| XNOR | ⊙ | (A⊕B)' | Even number of 1s |

## Design Insights

- **NAND/NOR are universal**: Any circuit can be built with just one type
- **XOR detects differences**: Essential for comparators and arithmetic
- **Gate delays add up**: Minimize logic depth for speed
- **Fan-out affects timing**: More loads = slower transitions

## Suggested Learning Path

1. **AND_OR_NOT_Gates** - Master the basic three
2. **Fundamental_Logic_Gates** - See the complete picture
3. **NAND_NOR_Gates** - Understand inversion and universality
4. **XOR_XNOR_Gates** - Learn exclusive operations
5. **Universal_Gates** - Implement anything with one gate type

---

**Status**: Framework established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
