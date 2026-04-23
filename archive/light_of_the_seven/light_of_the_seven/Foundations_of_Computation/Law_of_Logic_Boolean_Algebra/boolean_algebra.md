# Law of Logic: Boolean Algebra

## Overview

Boolean algebra is the mathematical foundation of digital logic and computation. It provides a formal system for representing and manipulating logical statements using binary variables (0 and 1) and logical operations.

## Internal Map

- **Boolean_Algebra_Basics/**
  Fundamental concepts: variables, constants, and basic operations (AND, OR, NOT)

- **Boolean_Algebra_Identities/**
  Core identities: Identity, Commutative, Associative, Distributive laws

- **Boolean_Algebra_Theorems/**
  Key theorems including De Morgan's laws and absorption theorems

- **Karnaugh_Maps/**
  Visual method for simplifying Boolean expressions using 2D truth table grids

- **Simplification_Techniques/**
  Algebraic and systematic methods for reducing Boolean expressions

## Role in the Directional-Derivative Workflow

From `directional_direvative.md`:

- **Boolean_Algebra_Identities → Logic Minimisation**
  - Derive optimised gate-level Boolean expressions for MAC (multiply-accumulate) datapath
  - Apply Karnaugh maps for systematic minimisation
  - Reduces transistor count → lower power & area

- **De Morgan's Laws → Control Logic Simplification**
  - Simplify power-gating and clock-gating blocks
  - Enable aggressive dynamic power management

**Net effect:** This subtree produces the **optimised Boolean netlist** that directly feeds into RTL implementation and VLSI design.

## Core Laws

### Identity Law
- A + 0 = A
- A · 1 = A

### Commutative Law
- A · B = B · A
- A + B = B + A

### Associative Law
- (A · B) · C = A · (B · C)
- (A + B) + C = A + (B + C)

### Distributive Law
- A · (B + C) = (A · B) + (A · C)
- A + (B · C) = (A + B) · (A + C)

### Complement Law
- A + A' = 1
- A · A' = 0

### De Morgan's Theorems
- (A · B)' = A' + B'
- (A + B)' = A' · B'

## Design Insights

- **Minimisation is not optional.** Every redundant gate costs power, area, and propagation delay.
- **De Morgan enables flexibility.** Convert between AND-OR and NAND-NOR implementations freely.
- **K-maps scale poorly.** Beyond 4-5 variables, use Quine-McCluskey or software tools.
- **Don't-cares are opportunities.** Unspecified outputs can be assigned to simplify logic.

## Suggested Learning Path

1. **Boolean_Algebra_Basics** - Master the three operations and truth tables
2. **Boolean_Algebra_Identities** - Memorise and apply the fundamental laws
3. **Boolean_Algebra_Theorems** - Understand De Morgan's and absorption
4. **Karnaugh_Maps** - Learn visual simplification for 2-4 variables
5. **Simplification_Techniques** - Apply systematic reduction methods

---

**Status**: Framework established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
