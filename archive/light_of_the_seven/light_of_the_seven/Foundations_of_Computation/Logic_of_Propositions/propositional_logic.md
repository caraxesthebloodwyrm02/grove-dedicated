# Logic of Propositions

## Overview

Propositional logic (also called sentential logic or statement logic) is the branch of logic that studies ways of combining or altering statements to form more complex statements. It provides the formal foundation for reasoning about truth and falsity.

## Internal Map

- **Propositional_Logic/**
  Basic concepts: propositions, logical connectives, and compound statements

- **Truth_Tables/**
  Systematic method for evaluating all possible truth values

- **Logical_Equivalence/**
  When two statements have the same truth value in all cases

- **Tautologies_and_Contradictions/**
  Statements that are always true or always false

- **Laws_of_Logic/**
  Fundamental rules governing logical reasoning

- **Propositional_Calculus/**
  Formal system for deriving logical conclusions

## Role in the Directional-Derivative Workflow

From `directional_direvative.md`:

- **Propositional Logic → Formal Specification**
  - Express hardware requirements as logical statements
  - Define preconditions and postconditions
  - Specify invariants and assertions

- **Laws of Logic → Verification**
  - Prove correctness of designs
  - Validate transformations
  - Check equivalence of implementations

**Net effect:** This subtree provides the **logical reasoning framework** for specifying, verifying, and proving properties of digital systems.

## Core Concepts

### Propositions
A proposition is a declarative statement that is either true (T/1) or false (F/0).

**Examples:**
- "The sky is blue" - Proposition (can be T or F)
- "2 + 2 = 4" - Proposition (True)
- "Close the door" - NOT a proposition (command)
- "Is it raining?" - NOT a proposition (question)

### Logical Connectives
- **NOT (¬)**: Negation
- **AND (∧)**: Conjunction
- **OR (∨)**: Disjunction
- **IMPLIES (→)**: Conditional
- **IFF (↔)**: Biconditional

## Design Insights

- **Propositions are atomic**: The smallest units of logical reasoning
- **Connectives build complexity**: Combine simple statements into complex ones
- **Truth tables are exhaustive**: Cover all possible cases
- **Equivalence enables optimization**: Replace complex with simple

## Suggested Learning Path

1. **Propositional_Logic** - Understand basic propositions and connectives
2. **Truth_Tables** - Master systematic evaluation
3. **Logical_Equivalence** - Recognize equivalent statements
4. **Tautologies_and_Contradictions** - Identify always-true/false statements
5. **Laws_of_Logic** - Apply fundamental reasoning rules
6. **Propositional_Calculus** - Perform formal derivations

---

**Status**: Framework established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
