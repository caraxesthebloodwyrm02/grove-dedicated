# Syntax and Semantics

## Overview

Syntax defines the form of valid programs (what they look like), while semantics defines their meaning (what they do). Together, they provide a complete specification of a programming language.

## Syntax

### Levels of Syntax

#### Lexical Syntax
Rules for forming tokens from characters.
```
identifier = letter (letter | digit)*
number = digit+
```

#### Phrase Syntax
Rules for forming phrases from tokens.
```
expr ::= term (('+' | '-') term)*
stmt ::= 'if' expr 'then' stmt ('else' stmt)?
```

### Concrete vs. Abstract Syntax

#### Concrete Syntax
What programmers write, including all punctuation.
```
if (x > 0) { return x; } else { return -x; }
```

#### Abstract Syntax
Essential structure, omitting syntactic sugar.
```
If(
  condition: BinaryOp(>, Var(x), Num(0)),
  then_branch: Return(Var(x)),
  else_branch: Return(UnaryOp(-, Var(x)))
)
```

### Syntax Design Principles

#### Readability
- Meaningful keywords
- Consistent notation
- Visual structure

#### Writability
- Concise expressions
- Sensible defaults
- Orthogonality

#### Unambiguity
- Clear precedence
- No parsing ambiguities
- Deterministic interpretation

## Semantics

### Types of Semantics

#### 1. Operational Semantics
Defines meaning by describing execution.

**Small-Step (Structural)**
```
         e₁ → e₁'
    ─────────────────
    e₁ + e₂ → e₁' + e₂

    ─────────────────
      v₁ + v₂ → v₃
    (where v₃ = v₁ + v₂)
```

**Big-Step (Natural)**
```
    e₁ ⇓ v₁    e₂ ⇓ v₂
    ─────────────────────
       e₁ + e₂ ⇓ v₃
    (where v₃ = v₁ + v₂)
```

#### 2. Denotational Semantics
Maps programs to mathematical objects.

```
⟦n⟧ = n                           (number literal)
⟦e₁ + e₂⟧ = ⟦e₁⟧ + ⟦e₂⟧          (addition)
⟦x⟧ρ = ρ(x)                       (variable lookup)
⟦let x = e₁ in e₂⟧ρ = ⟦e₂⟧ρ[x ↦ ⟦e₁⟧ρ]  (let binding)
```

#### 3. Axiomatic Semantics
Defines meaning through logical assertions.

**Hoare Triple**: {P} S {Q}
- P: Precondition
- S: Statement
- Q: Postcondition

```
{x = 5} x := x + 1 {x = 6}

    {P[e/x]} x := e {P}     (Assignment)

    {P} S₁ {Q}    {Q} S₂ {R}
    ─────────────────────────  (Sequence)
         {P} S₁; S₂ {R}
```

## Type Systems

### Purpose
- Prevent runtime errors
- Document intent
- Enable optimization
- Catch bugs early

### Static vs. Dynamic Typing

| Static | Dynamic |
|--------|---------|
| Types checked at compile time | Types checked at runtime |
| More verbose | More concise |
| Errors caught early | More flexible |
| Better optimization | Easier prototyping |

### Type Checking Rules

```
    Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
    ─────────────────────────────
         Γ ⊢ e₁ + e₂ : int

    Γ ⊢ e : bool    Γ ⊢ s₁ : τ    Γ ⊢ s₂ : τ
    ──────────────────────────────────────────
         Γ ⊢ if e then s₁ else s₂ : τ
```

### Type Inference
Deduce types without explicit annotations.

```
let f = fun x -> x + 1
// Inferred: f : int -> int
```

**Algorithm W (Hindley-Milner)**
1. Assign type variables
2. Generate constraints
3. Unify constraints
4. Substitute solution

## Binding and Scope

### Static (Lexical) Scoping
Names resolved by textual structure.

```python
x = 10
def f():
    return x  # x = 10 (from enclosing scope)
```

### Dynamic Scoping
Names resolved by call stack.

```
x = 10
def f():
    return x  # x depends on caller's scope

def g():
    x = 20
    return f()  # Returns 20 with dynamic scoping
```

### Scope Rules
```
Γ, x:τ ⊢ e : τ'
─────────────────────────
Γ ⊢ let x = v in e : τ'
```

## Evaluation Strategies

### Strict (Eager) Evaluation
Arguments evaluated before function call.

```
f(expensive_computation())  // Computed even if unused
```

### Non-Strict (Lazy) Evaluation
Arguments evaluated only when needed.

```
f(expensive_computation())  // Computed only if f uses it
```

### Call-by-Value vs. Call-by-Reference

| Call-by-Value | Call-by-Reference |
|---------------|-------------------|
| Copy argument | Pass address |
| Changes don't affect caller | Changes affect caller |
| Safer | More efficient for large data |

## Control Flow Semantics

### Sequential Composition
```
⟦S₁; S₂⟧σ = ⟦S₂⟧(⟦S₁⟧σ)
```

### Conditional
```
⟦if e then S₁ else S₂⟧σ =
    if ⟦e⟧σ = true then ⟦S₁⟧σ else ⟦S₂⟧σ
```

### Loop
```
⟦while e do S⟧σ =
    if ⟦e⟧σ = false then σ
    else ⟦while e do S⟧(⟦S⟧σ)
```

## Formal Verification

### Proving Program Properties
Use axiomatic semantics to prove correctness.

**Example**: Prove loop computes factorial
```
{n ≥ 0}
i := 1; f := 1;
while i ≤ n do
    f := f * i;
    i := i + 1
{f = n!}
```

### Loop Invariants
Property that holds before and after each iteration.

```
Invariant: f = (i-1)! ∧ i ≤ n+1
```

## Exercises

1. Write operational semantics for a simple language
2. Prove a Hoare triple for assignment
3. Implement type checking for expressions
4. Compare static and dynamic scoping
5. Define denotational semantics for conditionals

## Key Insights

- **Syntax is surface**: What programs look like
- **Semantics is meaning**: What programs do
- **Multiple approaches exist**: Operational, denotational, axiomatic
- **Types prevent errors**: Static checking catches bugs early

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
