# Turing Machines

## Overview

Turing machines are the most powerful computational model, capable of computing anything that is computable. They define the limits of algorithmic computation.

## Definition

TM = (Q, Σ, Γ, δ, q₀, qaccept, qreject)
- Q: States
- Σ: Input alphabet
- Γ: Tape alphabet (Σ ⊂ Γ, includes blank)
- δ: Q × Γ → Q × Γ × {L, R}
- q₀: Initial state
- qaccept, qreject: Halting states

## Operation

1. Read symbol under head
2. Write new symbol
3. Move head left or right
4. Change state
5. Repeat until halt

## Church-Turing Thesis

Any function computable by an algorithm can be computed by a Turing machine.

## Decidability

- **Decidable**: TM always halts with yes/no
- **Recognizable**: TM halts on "yes", may loop on "no"
- **Undecidable**: No TM can decide (e.g., Halting Problem)

## Halting Problem

Cannot determine if arbitrary TM halts on given input.

**Proof**: Assume H(M, w) decides halting. Construct D that:
- Runs H(M, M)
- Does opposite of H's answer
- D(D) leads to contradiction

## Complexity Classes

- **P**: Decidable in polynomial time
- **NP**: Verifiable in polynomial time
- **PSPACE**: Decidable in polynomial space

## Applications

- Computability limits
- Complexity theory
- Programming language theory
- Formal verification

---

**Status**: Foundation established
**Last Updated**: December 2025
