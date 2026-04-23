# Pushdown Automata

## Overview

Pushdown automata (PDA) extend finite automata with a stack, enabling recognition of context-free languages like balanced parentheses and programming language syntax.

## Definition

PDA = (Q, Σ, Γ, δ, q₀, Z₀, F)
- Q: States
- Σ: Input alphabet
- Γ: Stack alphabet
- δ: Transition function
- q₀: Initial state
- Z₀: Initial stack symbol
- F: Accept states

## Transitions

δ(q, a, X) = {(p, γ), ...}
- In state q, reading input a, with X on stack top
- Move to state p, replace X with string γ

## Example: Balanced Parentheses

```
Accept strings like "()", "(())", "()()"

States: {q0, q1}
Stack alphabet: {Z, (}

Transitions:
  (q0, '(', Z) → (q0, (Z)   // Push
  (q0, '(', () → (q0, (()   // Push
  (q0, ')', () → (q0, ε)    // Pop
  (q0, ε, Z)  → (q1, Z)     // Accept

Accept by reaching q1 with Z on stack
```

## Deterministic vs Non-Deterministic

- DPDA: Deterministic, less powerful
- NPDA: Non-deterministic, recognizes all CFLs
- Unlike FA, DPDA ⊊ NPDA

## Applications

- Parsing programming languages
- XML/HTML validation
- Expression evaluation

---

**Status**: Foundation established
**Last Updated**: December 2025
