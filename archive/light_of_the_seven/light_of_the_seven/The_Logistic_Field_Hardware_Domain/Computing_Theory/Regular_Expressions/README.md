# Regular Expressions

## Overview

Regular expressions are a declarative language for specifying patterns. They are equivalent in power to finite automata and are fundamental to text processing.

## Basic Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| a | Literal character | a matches "a" |
| . | Any character | a.c matches "abc" |
| * | Zero or more | a* matches "", "a", "aa" |
| + | One or more | a+ matches "a", "aa" |
| ? | Zero or one | a? matches "", "a" |
| \| | Alternation | a\|b matches "a" or "b" |
| [] | Character class | [abc] matches "a", "b", "c" |
| () | Grouping | (ab)+ matches "ab", "abab" |

## Extended Syntax

```
\d  - Digit [0-9]
\w  - Word character [a-zA-Z0-9_]
\s  - Whitespace
^   - Start of string
$   - End of string
{n} - Exactly n times
{n,m} - Between n and m times
```

## Regex to NFA (Thompson's Construction)

Each regex operator maps to NFA fragment:
- Concatenation: Connect fragments
- Alternation: ε-transitions to both
- Kleene star: Loop with ε-transitions

## Applications

- Text search and validation
- Lexical analysis
- Data extraction
- Find and replace

---

**Status**: Foundation established
**Last Updated**: December 2025
