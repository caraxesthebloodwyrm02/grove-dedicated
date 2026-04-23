# Parsing Techniques

## Overview

Parsing (syntax analysis) transforms a token stream into a parse tree or abstract syntax tree (AST). The parser verifies that the input conforms to the grammar and builds a structured representation for further processing.

## Context-Free Grammars

### Definition
A context-free grammar G = (V, Σ, R, S) where:
- V: Set of non-terminals
- Σ: Set of terminals (tokens)
- R: Set of production rules
- S: Start symbol

### BNF Notation
```
<expr>   ::= <term> (('+' | '-') <term>)*
<term>   ::= <factor> (('*' | '/') <factor>)*
<factor> ::= NUMBER | '(' <expr> ')'
```

### EBNF Extensions
- `*`: Zero or more
- `+`: One or more
- `?`: Optional
- `|`: Alternative
- `()`: Grouping

## Parse Trees vs. AST

### Parse Tree
Full grammar structure, includes all tokens.

```
        expr
       / | \
    term '+' term
     |       |
  factor   factor
     |       |
    '3'     '5'
```

### Abstract Syntax Tree
Simplified, semantically meaningful.

```
    BinaryOp(+)
      /    \
   Num(3)  Num(5)
```

## Top-Down Parsing

### Recursive Descent
Each non-terminal becomes a function.

```python
def parse_expr():
    left = parse_term()
    while current_token in ['+', '-']:
        op = current_token
        advance()
        right = parse_term()
        left = BinaryOp(op, left, right)
    return left

def parse_term():
    left = parse_factor()
    while current_token in ['*', '/']:
        op = current_token
        advance()
        right = parse_factor()
        left = BinaryOp(op, left, right)
    return left

def parse_factor():
    if current_token.type == NUMBER:
        value = current_token.value
        advance()
        return Num(value)
    elif current_token == '(':
        advance()
        expr = parse_expr()
        expect(')')
        return expr
```

### LL(k) Parsing
- **L**: Left-to-right scan
- **L**: Leftmost derivation
- **k**: k tokens lookahead

### LL(1) Constraints
- No left recursion
- No common prefixes (left factoring needed)
- FIRST sets must be disjoint

### Left Recursion Elimination
```
# Left recursive (bad for LL):
expr ::= expr '+' term | term

# Transformed:
expr  ::= term expr'
expr' ::= '+' term expr' | ε
```

### Left Factoring
```
# Common prefix (bad for LL):
stmt ::= 'if' expr 'then' stmt
       | 'if' expr 'then' stmt 'else' stmt

# Factored:
stmt  ::= 'if' expr 'then' stmt else_part
else_part ::= 'else' stmt | ε
```

## Bottom-Up Parsing

### Shift-Reduce Parsing
Two operations:
- **Shift**: Push token onto stack
- **Reduce**: Replace stack top with non-terminal

### Example
Input: `3 + 5 * 2`

```
Stack           Input           Action
[]              3 + 5 * 2 $     Shift
[3]             + 5 * 2 $       Reduce (factor → 3)
[factor]        + 5 * 2 $       Reduce (term → factor)
[term]          + 5 * 2 $       Reduce (expr → term)
[expr]          + 5 * 2 $       Shift
[expr +]        5 * 2 $         Shift
[expr + 5]      * 2 $           Reduce (factor → 5)
[expr + factor] * 2 $           Reduce (term → factor)
[expr + term]   * 2 $           Shift (precedence!)
[expr + term *] 2 $             Shift
[expr + term * 2] $             Reduce (factor → 2)
[expr + term * factor] $        Reduce (term → term * factor)
[expr + term]   $               Reduce (expr → expr + term)
[expr]          $               Accept
```

### LR Parsing Variants
- **LR(0)**: No lookahead
- **SLR**: Simple LR, uses FOLLOW sets
- **LALR**: Lookahead LR (most common)
- **LR(1)**: Full canonical LR

### Parser Generator Tools
- **Yacc/Bison**: Classic LALR generators
- **ANTLR**: LL(*) with predicates
- **PEG parsers**: Parsing Expression Grammars

## Operator Precedence

### Precedence Climbing
Handle precedence without grammar changes.

```python
def parse_expr(min_prec=0):
    left = parse_atom()

    while is_binary_op(current_token) and \
          precedence(current_token) >= min_prec:
        op = current_token
        advance()

        if is_right_assoc(op):
            right = parse_expr(precedence(op))
        else:
            right = parse_expr(precedence(op) + 1)

        left = BinaryOp(op, left, right)

    return left
```

### Pratt Parsing
Elegant precedence handling.

```python
def parse_expr(rbp=0):
    token = current_token
    advance()
    left = nud(token)  # Null denotation (prefix)

    while rbp < lbp(current_token):
        token = current_token
        advance()
        left = led(token, left)  # Left denotation (infix)

    return left
```

## Error Handling

### Error Detection
Parser detects when input doesn't match grammar.

### Error Recovery Strategies

#### Panic Mode
Skip tokens until synchronization point.

```python
def synchronize():
    advance()
    while not at_end():
        if previous().type == SEMICOLON:
            return
        if current_token.type in [CLASS, FUN, VAR, FOR, IF, WHILE, RETURN]:
            return
        advance()
```

#### Phrase-Level Recovery
Insert/delete tokens to continue.

#### Error Productions
Add grammar rules for common errors.

### Good Error Messages
```
Error: Expected ')' after expression
  --> main.py:10:15
   |
10 |     result = (a + b
   |                    ^
   |                    Expected ')' here
   |
   = note: '(' opened at line 10, column 14
```

## Ambiguity

### Ambiguous Grammar
Multiple parse trees for same input.

```
# Dangling else ambiguity:
stmt ::= 'if' expr 'then' stmt
       | 'if' expr 'then' stmt 'else' stmt

# Input: if a then if b then s1 else s2
# Which 'if' does 'else' belong to?
```

### Resolution
- Rewrite grammar
- Use precedence/associativity declarations
- Semantic actions to disambiguate

## Exercises

1. Write recursive descent parser for arithmetic
2. Eliminate left recursion from a grammar
3. Implement Pratt parsing for expressions
4. Add error recovery to a parser
5. Build parser for a simple programming language

## Key Insights

- **Grammar defines structure**: Formal specification of syntax
- **Top-down is intuitive**: Easy to write by hand
- **Bottom-up is powerful**: Handles more grammars
- **Error recovery matters**: Users make mistakes

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
