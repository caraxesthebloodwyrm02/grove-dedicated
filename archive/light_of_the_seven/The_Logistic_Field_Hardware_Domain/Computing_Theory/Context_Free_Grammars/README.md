# Context-Free Grammars

## Overview

Context-free grammars (CFGs) generate context-free languages through production rules. They are the foundation for programming language syntax and natural language parsing.

## Definition

CFG = (V, Σ, R, S)
- V: Variables (non-terminals)
- Σ: Terminals
- R: Production rules
- S: Start symbol

## Example: Arithmetic Expressions

```
E → E + T | E - T | T
T → T * F | T / F | F
F → ( E ) | id | num
```

## Derivations

**Leftmost**: Always expand leftmost variable
**Rightmost**: Always expand rightmost variable

```
E ⇒ E + T ⇒ T + T ⇒ F + T ⇒ id + T ⇒ id + F ⇒ id + num
```

## Parse Trees

Visual representation of derivation structure.

## Normal Forms

### Chomsky Normal Form (CNF)
All rules: A → BC or A → a

### Greibach Normal Form (GNF)
All rules: A → aα (terminal first)

## Ambiguity

Grammar is ambiguous if some string has multiple parse trees.

```
# Ambiguous:
E → E + E | E * E | id

# Unambiguous (with precedence):
E → E + T | T
T → T * F | F
F → id
```

## CFG ↔ PDA Equivalence

Every CFG has equivalent PDA and vice versa.

---

**Status**: Foundation established
**Last Updated**: December 2025
