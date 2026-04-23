# Mental Models

## Overview

Mental models are internal representations of how things work. In programming and system design, mental models determine how developers understand code, predict system behavior, and debug problems. Aligning system design with user mental models is key to usability.

## What Are Mental Models?

### Definition
A mental model is a cognitive representation of:
- How something works
- What it does
- Why it behaves as it does
- How to interact with it

### Characteristics
- **Incomplete**: Never capture full complexity
- **Unstable**: Change with experience
- **Unscientific**: May contain misconceptions
- **Parsimonious**: Simplified for cognitive efficiency

### Formation
Mental models form through:
- Direct experience
- Instruction and documentation
- Analogy to familiar systems
- Trial and error

## Mental Models in Programming

### Code Comprehension

#### Novice Mental Model of Variables
```
x = 5      # "x is 5"
x = x + 1  # Confusion: "x equals x plus 1?"
```

#### Expert Mental Model of Variables
```
x = 5      # "Bind name 'x' to value 5"
x = x + 1  # "Rebind 'x' to current value plus 1"
```

### Program Execution

#### Sequential Model
```python
a = 1
b = 2
c = a + b  # Mental simulation: a=1, b=2, so c=3
```

#### Concurrent Model (More Complex)
```python
# Thread 1        # Thread 2
x = 1             y = 1
print(y)          print(x)
# Possible outputs: (1,1), (0,1), (1,0), (0,0)
```

### Memory Models

#### Value Semantics (Copying)
```
a = [1, 2, 3]
b = a          # Mental model: b gets a copy
b.append(4)    # Surprise: a is also modified!
```

#### Reference Semantics (Aliasing)
```
a = [1, 2, 3]
b = a          # Mental model: b points to same list
b.append(4)    # Expected: both a and b show [1,2,3,4]
```

## Types of Mental Models

### Structural Models
How components are organized.

**Example**: File system as hierarchy
```
/
├── home/
│   └── user/
│       └── documents/
└── etc/
```

### Functional Models
What the system does.

**Example**: Compiler as transformer
```
Source Code → [Compiler] → Machine Code
```

### Causal Models
Why things happen.

**Example**: Garbage collection
```
Object unreachable → GC detects → Memory freed
```

## Mental Model Mismatches

### Common Mismatches

#### Floating Point
```python
0.1 + 0.2 == 0.3  # False!
# Mental model: Decimal arithmetic
# Reality: Binary floating point
```

#### Equality vs. Identity
```python
a = [1, 2]
b = [1, 2]
a == b   # True (equal values)
a is b   # False (different objects)
```

#### Scope
```python
x = 10
def f():
    print(x)  # Works: reads global
    x = 20    # Error if this line added!
              # Python sees assignment, assumes local
```

### Consequences of Mismatches
- Bugs that are hard to find
- Incorrect predictions of behavior
- Frustration and confusion
- Inefficient debugging

## Designing for Mental Models

### Principles

#### 1. Match Existing Models
Design systems that work like users expect.

```
# Good: Familiar file operations
file.open()
file.read()
file.close()

# Confusing: Unfamiliar pattern
file.activate()
file.extract()
file.terminate()
```

#### 2. Provide Clear Conceptual Models
Help users build accurate mental models.

- Good documentation
- Consistent behavior
- Meaningful error messages
- Visual representations

#### 3. Make the Invisible Visible
Show internal state when helpful.

- Debugger variable views
- Network request inspectors
- Memory profilers
- Execution traces

#### 4. Support Model Refinement
Help users correct misconceptions.

- Informative errors
- Interactive tutorials
- Sandbox environments
- Immediate feedback

### Metaphors and Analogies

#### Effective Metaphors
- **Desktop**: Files, folders, trash
- **Shopping cart**: E-commerce
- **Clipboard**: Copy/paste

#### Metaphor Limitations
Metaphors break down at edges:
- Desktop files don't have "versions"
- Shopping carts don't have "undo"
- Clipboard only holds one thing (usually)

## Mental Models and Debugging

### Expert Debugging Process
1. **Observe** unexpected behavior
2. **Hypothesize** based on mental model
3. **Predict** what should happen if hypothesis true
4. **Test** prediction
5. **Refine** mental model based on results

### Common Mental Model Bugs

#### Off-by-One
```python
for i in range(10):  # 0-9, not 1-10
    print(i)
```

#### Null/None Handling
```python
result = find_user(id)
print(result.name)  # Crash if user not found
```

#### Async Timing
```javascript
let data;
fetch(url).then(r => data = r);
console.log(data);  // undefined! Async not complete
```

## Exercises

1. Identify your mental model of how Git branching works
2. Find a mental model mismatch in a language you use
3. Design an error message that helps correct a misconception
4. Create a visual representation of a complex system
5. Interview a novice about their mental model of recursion

## Key Insights

- **Models are personal**: Different users have different models
- **Models are learnable**: Experience refines mental models
- **Design shapes models**: Good design builds good models
- **Mismatches cause bugs**: Many bugs are model failures

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
