# Computing Theory

## Overview

Computing theory establishes the mathematical foundations of computation. It defines what can be computed, how efficiently, and with what resources.

## Internal Map

- **Finite_Automata/** - Simplest computational model
- **Regular_Expressions/** - Pattern specification language
- **Pushdown_Automata/** - Automata with stack memory
- **Context_Free_Grammars/** - Language generation rules
- **Turing_Machines/** - Universal computation model

## Chomsky Hierarchy

| Type | Language | Automaton | Example |
|------|----------|-----------|---------|
| 3 | Regular | Finite Automata | a*b* |
| 2 | Context-Free | Pushdown Automata | aⁿbⁿ |
| 1 | Context-Sensitive | Linear Bounded | aⁿbⁿcⁿ |
| 0 | Recursively Enumerable | Turing Machine | Any computable |

---

**Status**: Framework established
**Last Updated**: December 2025
