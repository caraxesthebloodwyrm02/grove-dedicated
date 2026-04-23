# Finite Automata

## Overview

Finite automata are the simplest computational models, consisting of states and transitions. They recognize regular languages and form the basis for lexical analysis, pattern matching, and hardware control.

## Deterministic Finite Automata (DFA)

### Definition
DFA = (Q, Σ, δ, q₀, F)
- Q: Finite set of states
- Σ: Input alphabet
- δ: Transition function Q × Σ → Q
- q₀: Initial state
- F: Set of accepting states

### Example: Strings ending in "01"
```
States: {q0, q1, q2}
Alphabet: {0, 1}
Transitions:
  q0 --0--> q1
  q0 --1--> q0
  q1 --0--> q1
  q1 --1--> q2
  q2 --0--> q1
  q2 --1--> q0
Accept: {q2}
```

## Non-Deterministic Finite Automata (NFA)

### Definition
- Multiple transitions for same input
- ε-transitions (no input consumed)
- Accepts if ANY path leads to accept state

### NFA to DFA Conversion (Subset Construction)
Each DFA state = set of NFA states

## Applications

- **Lexical analysis**: Token recognition in compilers
- **Pattern matching**: Text search, grep
- **Protocol verification**: State machine modeling
- **Hardware control**: FSM in digital circuits

## Key Insight

DFA and NFA have equivalent power - both recognize exactly the regular languages.

---

**Status**: Foundation established
**Last Updated**: December 2025
