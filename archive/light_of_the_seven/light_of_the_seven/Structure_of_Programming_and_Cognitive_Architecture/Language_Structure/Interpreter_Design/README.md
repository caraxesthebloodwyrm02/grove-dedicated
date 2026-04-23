# Interpreter Design

## Overview

An interpreter executes programs directly without producing separate machine code. Understanding interpreter design is essential for scripting languages, REPLs, and embedded language implementations.

## Interpreter vs. Compiler

| Aspect | Interpreter | Compiler |
|--------|-------------|----------|
| Execution | Direct | Via generated code |
| Startup | Fast | Slow (compilation) |
| Runtime | Slower | Faster |
| Debugging | Easier | Harder |
| Portability | High | Target-specific |

## Interpreter Architectures

### 1. Tree-Walking Interpreter
Execute AST nodes directly.

```python
def evaluate(node):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, BinaryOp):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.op == '+':
            return left + right
        elif node.op == '*':
            return left * right
```

**Pros**: Simple, easy to implement
**Cons**: Slow, poor cache locality

### 2. Bytecode Interpreter
Compile to bytecode, then interpret.

```
Source → Bytecode Compiler → Bytecode → VM
```

**Bytecode Example**:
```
LOAD_CONST 5
LOAD_CONST 3
BINARY_ADD
STORE_NAME x
```

**Pros**: Faster than tree-walking, portable
**Cons**: More complex implementation

### 3. Threaded Code
Bytecode with direct threading.

- **Direct threading**: Jump table of code addresses
- **Indirect threading**: Pointers to handler routines
- **Subroutine threading**: Call/return to handlers

### 4. JIT Compilation
Compile hot paths at runtime.

```
Interpret → Profile → Compile Hot Code → Execute Native
```

**Examples**: V8 (JavaScript), PyPy (Python), HotSpot (Java)

## Virtual Machine Design

### Stack-Based VM
Operations use implicit stack.

```
PUSH 5      ; Stack: [5]
PUSH 3      ; Stack: [5, 3]
ADD         ; Stack: [8]
POP x       ; Stack: [], x = 8
```

**Pros**: Simple, compact bytecode
**Cons**: More instructions, stack manipulation overhead

### Register-Based VM
Operations use explicit registers.

```
LOAD R1, 5
LOAD R2, 3
ADD R3, R1, R2
STORE x, R3
```

**Pros**: Fewer instructions, closer to hardware
**Cons**: Larger bytecode, register allocation needed

### Comparison
| Aspect | Stack-Based | Register-Based |
|--------|-------------|----------------|
| Code size | Smaller | Larger |
| Dispatch | More | Fewer |
| Operands | Implicit | Explicit |
| Examples | JVM, Python | Lua, Dalvik |

## Bytecode Design

### Instruction Format
```
[Opcode][Operand1][Operand2]...
```

### Common Instructions
- **LOAD_CONST**: Push constant
- **LOAD_NAME**: Push variable value
- **STORE_NAME**: Pop and store to variable
- **BINARY_OP**: Pop two, push result
- **JUMP**: Unconditional jump
- **JUMP_IF_FALSE**: Conditional jump
- **CALL**: Function call
- **RETURN**: Return from function

### Constant Pool
Store literals and names separately.

```
Constants: [42, 3.14, "hello"]
Names: ["x", "y", "print"]
Bytecode: LOAD_CONST 0  ; Load 42
```

## Execution Loop

### Basic Dispatch Loop
```python
def run(bytecode):
    ip = 0  # Instruction pointer
    stack = []

    while ip < len(bytecode):
        opcode = bytecode[ip]
        ip += 1

        if opcode == LOAD_CONST:
            value = constants[bytecode[ip]]
            ip += 1
            stack.append(value)
        elif opcode == BINARY_ADD:
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right)
        # ... more opcodes
```

### Dispatch Optimization
- **Switch dispatch**: Simple but branch misprediction
- **Computed goto**: Direct jump (GCC extension)
- **Threaded code**: Inline next dispatch
- **JIT**: Eliminate dispatch entirely

## Memory Management

### Reference Counting
```python
class Object:
    def __init__(self):
        self.refcount = 1

    def incref(self):
        self.refcount += 1

    def decref(self):
        self.refcount -= 1
        if self.refcount == 0:
            self.free()
```

**Pros**: Immediate cleanup, predictable
**Cons**: Cycles, overhead on every assignment

### Garbage Collection
- **Mark-and-sweep**: Mark reachable, sweep unreachable
- **Copying**: Copy live objects, reclaim rest
- **Generational**: Young/old generations
- **Incremental**: Spread work over time

## Scope and Environment

### Environment Chain
```python
class Environment:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(name)

    def set(self, name, value):
        self.bindings[name] = value
```

### Closures
Capture environment at function creation.

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

## Function Calls

### Call Stack
```
┌─────────────────┐
│ Frame: main     │
│   locals: {x:5} │
│   return addr   │
├─────────────────┤
│ Frame: foo      │
│   locals: {y:3} │
│   return addr   │
├─────────────────┤
│ Frame: bar      │
│   locals: {z:1} │
│   return addr   │
└─────────────────┘
```

### Tail Call Optimization
Reuse frame for tail calls.

```python
def factorial(n, acc=1):
    if n <= 1:
        return acc
    return factorial(n-1, n*acc)  # Tail call
```

## Error Handling

### Exception Implementation
- Maintain exception handler stack
- On throw, unwind to matching handler
- Preserve stack trace for debugging

### Error Messages
- Source location (file, line, column)
- Context (surrounding code)
- Suggestion (if possible)

## Exercises

1. Implement a tree-walking interpreter for arithmetic
2. Design bytecode for a simple language
3. Build a stack-based VM with 10 opcodes
4. Add closures to an interpreter
5. Implement mark-and-sweep garbage collection

## Key Insights

- **Simplicity vs. speed**: Tree-walking is simple, bytecode is faster
- **JIT bridges the gap**: Interpret first, compile hot paths
- **Memory management matters**: GC strategy affects performance
- **Good errors help users**: Invest in error messages

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
