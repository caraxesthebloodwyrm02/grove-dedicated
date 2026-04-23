# Compiler Design

## Overview

A compiler translates source code from a high-level programming language into a lower-level language (typically machine code or intermediate representation). Understanding compiler design is essential for language implementation, optimization, and tool development.

## Compiler Architecture

### Traditional Phases

```
Source Code
    ↓
┌─────────────────┐
│  Lexical        │  Characters → Tokens
│  Analysis       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Syntax         │  Tokens → Parse Tree
│  Analysis       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Semantic       │  Parse Tree → Annotated Tree
│  Analysis       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Intermediate   │  Annotated Tree → IR
│  Code Gen       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Optimization   │  IR → Optimized IR
│                 │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Code           │  IR → Target Code
│  Generation     │
└─────────────────┘
```

### Front End vs. Back End

| Front End | Back End |
|-----------|----------|
| Language-dependent | Target-dependent |
| Lexer, Parser | Code Generator |
| Semantic Analysis | Register Allocation |
| IR Generation | Instruction Selection |

### Multi-Pass vs. Single-Pass
- **Single-pass**: Process source once (faster, limited optimization)
- **Multi-pass**: Multiple traversals (slower, better optimization)

## Lexical Analysis

### Purpose
Convert character stream into token stream.

### Token Types
- **Keywords**: `if`, `while`, `return`
- **Identifiers**: `foo`, `myVar`
- **Literals**: `42`, `"hello"`, `3.14`
- **Operators**: `+`, `==`, `&&`
- **Punctuation**: `;`, `{`, `}`

### Implementation
- Regular expressions define token patterns
- Finite automata recognize tokens
- Tools: Lex, Flex, ANTLR

## Syntax Analysis (Parsing)

### Purpose
Build parse tree from token stream.

### Grammar Notation (BNF)
```
<expr>   ::= <term> (('+' | '-') <term>)*
<term>   ::= <factor> (('*' | '/') <factor>)*
<factor> ::= NUMBER | '(' <expr> ')'
```

### Parser Types

#### Top-Down (LL)
- Start from root, build down
- Predictive parsing
- LL(k): k tokens lookahead
- Recursive descent implementation

#### Bottom-Up (LR)
- Start from leaves, build up
- Shift-reduce parsing
- LR(k), LALR, SLR variants
- More powerful than LL

### Parse Trees vs. AST
- **Parse Tree**: Full grammar structure
- **AST**: Simplified, semantically meaningful

## Semantic Analysis

### Purpose
Check meaning and gather information.

### Tasks
- **Type checking**: Operand compatibility
- **Scope resolution**: Variable binding
- **Declaration checking**: Define before use
- **Flow analysis**: Reachability, initialization

### Symbol Table
```
Name     | Type    | Scope  | Attributes
---------|---------|--------|------------
x        | int     | global | initialized
foo      | func    | global | params: (int, int)
y        | float   | foo    | local
```

## Intermediate Representation

### Purpose
Machine-independent representation for optimization.

### Types

#### Three-Address Code
```
t1 = a + b
t2 = t1 * c
x = t2
```

#### Static Single Assignment (SSA)
```
x1 = 5
x2 = x1 + 1
y1 = x2 * 2
```
Each variable assigned exactly once.

#### Control Flow Graph (CFG)
Nodes are basic blocks, edges are control flow.

## Optimization

### Levels
- **Local**: Within basic block
- **Global**: Within function
- **Interprocedural**: Across functions
- **Link-time**: Across compilation units

### Common Optimizations

#### Constant Folding
```
x = 2 + 3  →  x = 5
```

#### Dead Code Elimination
```
x = 5      →  (removed if x unused)
```

#### Common Subexpression Elimination
```
a = b + c      a = b + c
d = b + c  →   d = a
```

#### Loop Optimizations
- Loop invariant code motion
- Loop unrolling
- Strength reduction

#### Inlining
Replace function call with function body.

## Code Generation

### Tasks
- **Instruction selection**: Choose target instructions
- **Register allocation**: Map variables to registers
- **Instruction scheduling**: Order for performance

### Register Allocation
- Graph coloring algorithm
- Linear scan (faster, JIT)
- Spilling to memory when needed

### Instruction Selection
- Pattern matching on IR
- Tree covering algorithms
- Peephole optimization

## Domain-Specific Languages (DSLs)

### Characteristics
- Focused on specific domain
- Higher abstraction level
- Often embedded in host language

### Examples
- SQL (databases)
- Regular expressions (text matching)
- Make (build systems)
- TensorFlow/PyTorch (ML)

### Implementation Approaches
- **External DSL**: Separate parser, compiler
- **Internal DSL**: Embedded in host language
- **Language workbenches**: Tools for DSL creation

## Modern Compiler Infrastructure

### LLVM
- Modular compiler infrastructure
- Language-independent IR
- Extensive optimization passes
- Multiple target backends

### GCC
- GNU Compiler Collection
- Multiple front ends (C, C++, Fortran, ...)
- Mature optimization
- Wide platform support

## Exercises

1. Write a lexer for a simple expression language
2. Implement recursive descent parser for arithmetic
3. Build a symbol table with scope handling
4. Convert code to three-address form
5. Implement constant folding optimization

## Key Insights

- **Phases separate concerns**: Each phase has clear responsibility
- **IR enables optimization**: Machine-independent transformations
- **Trade-offs everywhere**: Compile time vs. runtime performance
- **Tools help**: Use parser generators, IR frameworks

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
