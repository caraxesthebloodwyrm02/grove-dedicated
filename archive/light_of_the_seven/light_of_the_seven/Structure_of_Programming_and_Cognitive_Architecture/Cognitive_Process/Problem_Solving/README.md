# Problem Solving

## Overview

Problem solving is the cognitive process of finding solutions to difficult or complex issues. In programming and engineering, effective problem-solving skills are essential for debugging, algorithm design, and system architecture.

## Problem-Solving Frameworks

### Polya's Four Steps
1. **Understand the problem**
   - What is unknown?
   - What is given?
   - What are the constraints?

2. **Devise a plan**
   - Have you seen a similar problem?
   - Can you restate the problem?
   - Can you solve a simpler version?

3. **Carry out the plan**
   - Execute step by step
   - Check each step
   - Can you prove correctness?

4. **Look back**
   - Can you check the result?
   - Can you derive it differently?
   - Can you use it for other problems?

### Computational Thinking
- **Decomposition**: Break into smaller parts
- **Pattern Recognition**: Find similarities
- **Abstraction**: Focus on essential details
- **Algorithm Design**: Create step-by-step solution

## Problem-Solving Strategies

### 1. Divide and Conquer
Break problem into independent subproblems.

```
Problem: Sort a list
Approach:
1. Divide list in half
2. Sort each half (recursively)
3. Merge sorted halves
```

### 2. Working Backwards
Start from goal, work toward start.

```
Problem: Find path from A to Z
Approach:
1. What leads to Z?
2. What leads to those?
3. Continue until reaching A
```

### 3. Simplification
Solve a simpler version first.

```
Problem: Handle arbitrary input
Approach:
1. Solve for specific simple case
2. Generalize solution
3. Handle edge cases
```

### 4. Analogy
Apply solution from similar problem.

```
Problem: Find shortest path in graph
Analogy: Like finding shortest route on map
Apply: Dijkstra's algorithm
```

### 5. Brainstorming
Generate many ideas without judgment.

```
Rules:
- No criticism during generation
- Quantity over quality initially
- Build on others' ideas
- Encourage wild ideas
```

### 6. Means-Ends Analysis
Reduce difference between current and goal state.

```
Current: Unsorted list
Goal: Sorted list
Difference: Order
Operator: Swap elements
Repeat until difference = 0
```

## Problem Representation

### Problem Space
- **Initial state**: Starting conditions
- **Goal state**: Desired outcome
- **Operators**: Actions that change state
- **Constraints**: Limitations on actions

### Representation Matters
Same problem, different representations:

```
Mutilated Checkerboard Problem:
- Visual: Hard to solve
- Parity argument: Easy to prove impossible
```

### External Representations
- Diagrams and sketches
- Tables and matrices
- Pseudocode
- State diagrams

## Debugging as Problem Solving

### Scientific Method for Debugging
1. **Observe**: What is the bug?
2. **Hypothesize**: What might cause it?
3. **Predict**: If hypothesis true, what should happen?
4. **Test**: Check prediction
5. **Conclude**: Refine understanding

### Debugging Strategies

#### Binary Search
```
1. Find midpoint in code/data
2. Check if bug before or after
3. Repeat in relevant half
4. Narrow to exact location
```

#### Wolf Fence
```
"There's a wolf in Alaska. Build fence across middle.
 Wolf howls. Which side? Repeat."
```

#### Rubber Duck Debugging
Explain code line-by-line to inanimate object.
Often reveals assumptions and errors.

### Common Bug Patterns
- Off-by-one errors
- Null pointer dereference
- Race conditions
- Resource leaks
- Incorrect assumptions

## Obstacles to Problem Solving

### Functional Fixedness
Seeing objects only in typical use.

**Example**: Using a coin as a screwdriver

**In programming**: Using data structures only in "standard" ways

### Mental Set
Applying previously successful approach inappropriately.

**Example**: Always using loops when recursion is cleaner

### Confirmation Bias
Seeking evidence that confirms hypothesis.

**In debugging**: Only testing cases that should work

### Einstellung Effect
First idea blocks better solutions.

**Mitigation**: Generate multiple solutions before evaluating

## Expert vs. Novice Problem Solving

| Aspect | Novice | Expert |
|--------|--------|--------|
| Representation | Surface features | Deep structure |
| Strategy | Trial and error | Pattern matching |
| Knowledge | Isolated facts | Organized schemas |
| Monitoring | Poor metacognition | Strong self-regulation |
| Transfer | Limited | Broad application |

### Developing Expertise
- Deliberate practice
- Study worked examples
- Reflect on solutions
- Learn from errors
- Build pattern library

## Collaborative Problem Solving

### Pair Programming
- Driver: Writes code
- Navigator: Reviews, thinks ahead
- Regular role switching

### Code Review
- Fresh perspective
- Knowledge sharing
- Error detection
- Standard enforcement

### Design Reviews
- Multiple viewpoints
- Challenge assumptions
- Identify risks
- Improve solutions

## Exercises

1. Apply Polya's steps to a coding challenge
2. Use binary search to find a bug
3. Solve a problem two different ways
4. Explain code to a rubber duck
5. Identify functional fixedness in your approach

## Key Insights

- **Representation is half the battle**: Right framing makes problems tractable
- **Strategies are learnable**: Problem-solving improves with practice
- **Experts see patterns**: Build your pattern library
- **Obstacles are predictable**: Awareness helps overcome them

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
