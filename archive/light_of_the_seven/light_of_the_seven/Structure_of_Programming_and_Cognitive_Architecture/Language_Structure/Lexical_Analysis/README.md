# Lexical Analysis

## Overview

Lexical analysis (scanning/tokenization) is the first phase of compilation. It converts a stream of characters into a stream of tokens, handling whitespace, comments, and lexical errors.

## Purpose

### Input
Raw source code as character stream:
```
"if (x >= 10) { return x * 2; }"
```

### Output
Token stream:
```
IF, LPAREN, IDENT("x"), GE, NUMBER(10), RPAREN,
LBRACE, RETURN, IDENT("x"), STAR, NUMBER(2),
SEMICOLON, RBRACE
```

## Token Structure

### Token Components
```python
class Token:
    type: TokenType    # IF, IDENT, NUMBER, etc.
    value: Any         # Literal value if applicable
    line: int          # Source location
    column: int
```

### Token Categories

| Category | Examples |
|----------|----------|
| Keywords | `if`, `while`, `return`, `class` |
| Identifiers | `foo`, `myVar`, `_count` |
| Literals | `42`, `3.14`, `"hello"`, `true` |
| Operators | `+`, `-`, `*`, `/`, `==`, `&&` |
| Delimiters | `(`, `)`, `{`, `}`, `;`, `,` |
| Special | `EOF`, `NEWLINE`, `INDENT` |

## Regular Expressions

### Token Patterns
```
IDENT    = [a-zA-Z_][a-zA-Z0-9_]*
NUMBER   = [0-9]+(\.[0-9]+)?
STRING   = "([^"\\]|\\.)*"
COMMENT  = //[^\n]*
WS       = [ \t\n\r]+
```

### Pattern Priority
When multiple patterns match:
1. **Longest match wins**: `ifx` is IDENT, not IF + IDENT
2. **First pattern wins** (for equal length): Keywords before identifiers

## Finite Automata

### DFA for Identifiers
```
        [a-zA-Z_]        [a-zA-Z0-9_]
    ┌──────────────┐    ┌────────────┐
    │              ▼    │            │
→ (S0) ─────────→ ((S1)) ◄──────────┘
                   │
                   │ other
                   ▼
                 ACCEPT
```

### DFA for Numbers
```
        [0-9]           [0-9]
    ┌──────────┐    ┌──────────┐
    │          ▼    │          │
→ (S0) ─────→ ((S1)) ◄─────────┘
               │
               │ '.'
               ▼
              (S2) ──[0-9]──→ ((S3))
                              │    │
                              └────┘
                              [0-9]
```

## Lexer Implementation

### Hand-Written Lexer
```python
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def next_token(self):
        self.skip_whitespace()

        if self.pos >= len(self.source):
            return Token(EOF, None, self.line, self.column)

        char = self.source[self.pos]

        if char.isalpha() or char == '_':
            return self.read_identifier()
        elif char.isdigit():
            return self.read_number()
        elif char == '"':
            return self.read_string()
        elif char == '+':
            self.advance()
            return Token(PLUS, '+', self.line, self.column)
        # ... more cases

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and \
              (self.source[self.pos].isalnum() or
               self.source[self.pos] == '_'):
            self.advance()

        text = self.source[start:self.pos]
        token_type = KEYWORDS.get(text, IDENT)
        return Token(token_type, text, self.line, self.column)
```

### Generated Lexer (Lex/Flex)
```lex
%%
"if"        { return IF; }
"while"     { return WHILE; }
[a-zA-Z_][a-zA-Z0-9_]*  { return IDENT; }
[0-9]+      { return NUMBER; }
[ \t\n]     { /* skip whitespace */ }
.           { return yytext[0]; }
%%
```

## Handling Special Cases

### Keywords vs. Identifiers
```python
KEYWORDS = {
    'if': IF, 'else': ELSE, 'while': WHILE,
    'for': FOR, 'return': RETURN, 'class': CLASS,
}

def read_identifier(self):
    text = self.read_word()
    return Token(KEYWORDS.get(text, IDENT), text)
```

### String Escapes
```python
def read_string(self):
    self.advance()  # Skip opening quote
    result = []
    while self.current() != '"':
        if self.current() == '\\':
            self.advance()
            escape = {
                'n': '\n', 't': '\t', 'r': '\r',
                '\\': '\\', '"': '"'
            }.get(self.current())
            result.append(escape)
        else:
            result.append(self.current())
        self.advance()
    self.advance()  # Skip closing quote
    return Token(STRING, ''.join(result))
```

### Multi-Character Operators
```python
def read_operator(self):
    char = self.current()
    self.advance()

    if char == '=' and self.current() == '=':
        self.advance()
        return Token(EQ, '==')
    elif char == '!':
        if self.current() == '=':
            self.advance()
            return Token(NE, '!=')
        return Token(NOT, '!')
    elif char == '<':
        if self.current() == '=':
            self.advance()
            return Token(LE, '<=')
        return Token(LT, '<')
    # ... more cases
```

### Comments
```python
def skip_whitespace_and_comments(self):
    while True:
        self.skip_whitespace()
        if self.match('//'):
            self.skip_line_comment()
        elif self.match('/*'):
            self.skip_block_comment()
        else:
            break

def skip_line_comment(self):
    while self.current() != '\n' and not self.at_end():
        self.advance()

def skip_block_comment(self):
    while not self.match('*/') and not self.at_end():
        self.advance()
```

## Indentation-Sensitive Languages

### Python-Style Indentation
```python
def handle_newline(self):
    self.emit(NEWLINE)
    indent = 0
    while self.current() == ' ':
        indent += 1
        self.advance()

    if indent > self.indent_stack[-1]:
        self.indent_stack.append(indent)
        self.emit(INDENT)
    else:
        while indent < self.indent_stack[-1]:
            self.indent_stack.pop()
            self.emit(DEDENT)
```

## Error Handling

### Lexical Errors
- Unterminated string
- Invalid character
- Malformed number
- Unterminated comment

### Error Recovery
```python
def next_token(self):
    try:
        return self.scan_token()
    except LexicalError as e:
        self.report_error(e)
        self.synchronize()  # Skip to safe point
        return self.next_token()
```

### Good Error Messages
```
Error: Unterminated string literal
  --> main.py:5:10
   |
 5 |     msg = "hello
   |           ^
   |           String started here but never closed
```

## Performance Considerations

### Buffer Management
- Read file in chunks, not character by character
- Use memory-mapped files for large sources

### Table-Driven Lexer
- Precomputed transition tables
- Faster than switch statements
- Generated by tools like Flex

### Avoiding Backtracking
- Design patterns to be prefix-free when possible
- Use maximal munch (longest match)

## Exercises

1. Write a lexer for a calculator language
2. Handle nested block comments
3. Implement string interpolation lexing
4. Add source location tracking
5. Build an indentation-sensitive lexer

## Key Insights

- **Regular expressions define tokens**: Formal specification
- **DFAs implement recognition**: Efficient execution
- **Longest match resolves ambiguity**: Standard rule
- **Good errors help users**: Invest in error messages

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
