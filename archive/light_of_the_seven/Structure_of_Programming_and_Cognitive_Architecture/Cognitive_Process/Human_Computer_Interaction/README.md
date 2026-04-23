# Human-Computer Interaction

## Overview

Human-Computer Interaction (HCI) studies how people interact with computers and designs interfaces that are effective, efficient, and satisfying. For programming tools and development environments, HCI principles are essential for productivity and usability.

## Foundations of HCI

### The Human Processor Model (Card, Moran, Newell)
Three interacting systems:
1. **Perceptual System**: Senses and buffers (~100ms cycle)
2. **Cognitive System**: Working memory and processing (~70ms cycle)
3. **Motor System**: Physical actions (~70ms cycle)

### Fitts's Law
Time to acquire a target:
```
MT = a + b × log₂(2D/W)
```
- MT: Movement time
- D: Distance to target
- W: Width of target
- a, b: Constants

**Implication**: Make targets large and close

### Hick's Law
Decision time increases with choices:
```
RT = a + b × log₂(n)
```
- RT: Reaction time
- n: Number of choices

**Implication**: Reduce options or organize hierarchically

## Usability Principles

### Nielsen's 10 Heuristics

1. **Visibility of system status**
   - Keep users informed
   - Progress indicators, status bars

2. **Match between system and real world**
   - Use familiar language and concepts
   - Follow real-world conventions

3. **User control and freedom**
   - Undo and redo
   - Clear exit paths

4. **Consistency and standards**
   - Same words mean same things
   - Follow platform conventions

5. **Error prevention**
   - Prevent errors before they occur
   - Confirmation for destructive actions

6. **Recognition rather than recall**
   - Make options visible
   - Reduce memory load

7. **Flexibility and efficiency of use**
   - Shortcuts for experts
   - Customization options

8. **Aesthetic and minimalist design**
   - Remove unnecessary elements
   - Focus on essential information

9. **Help users recognize, diagnose, and recover from errors**
   - Clear error messages
   - Constructive solutions

10. **Help and documentation**
    - Easy to search
    - Task-focused

### Norman's Design Principles

- **Affordances**: Perceived possible actions
- **Signifiers**: Indicators of where action should occur
- **Constraints**: Limiting possible actions
- **Mappings**: Relationship between controls and effects
- **Feedback**: Information about action results
- **Conceptual Models**: User's understanding of how it works

## HCI for Development Tools

### IDE Design

#### Code Editor
- **Syntax highlighting**: Visual parsing aid
- **Auto-completion**: Reduce typing, prevent errors
- **Error squiggles**: Immediate feedback
- **Code folding**: Manage complexity
- **Multiple cursors**: Efficient editing

#### Navigation
- **Go to definition**: Quick code exploration
- **Find references**: Understand usage
- **Breadcrumbs**: Location awareness
- **File tree**: Project structure

#### Debugging
- **Breakpoints**: Visual markers
- **Variable inspection**: Current state
- **Call stack**: Execution context
- **Step controls**: Execution control

### Command-Line Interfaces

#### Good CLI Design
- **Consistent syntax**: Predictable patterns
- **Helpful errors**: Suggest corrections
- **Tab completion**: Reduce typing
- **Man pages**: Accessible documentation
- **Sensible defaults**: Work out of box

#### Example: Git
```bash
# Good: Clear, consistent
git commit -m "message"
git push origin main

# Helpful error
fatal: not a git repository
hint: Run 'git init' to create one
```

### Visual Programming

#### Advantages
- Lower barrier to entry
- Immediate visual feedback
- Prevents syntax errors
- Shows data flow

#### Challenges
- Scalability (large programs)
- Version control
- Text search
- Expert efficiency

## Accessibility

### WCAG Principles (Web Content Accessibility Guidelines)

1. **Perceivable**: Information must be presentable
2. **Operable**: Interface must be operable
3. **Understandable**: Information must be understandable
4. **Robust**: Content must be robust for assistive technologies

### Developer Tool Accessibility
- Screen reader compatibility
- Keyboard navigation
- High contrast modes
- Adjustable font sizes
- Color-blind friendly palettes

## User Research Methods

### Formative (Design Phase)
- **Interviews**: Deep understanding
- **Contextual inquiry**: Observe in context
- **Card sorting**: Information architecture
- **Prototyping**: Test concepts early

### Summative (Evaluation Phase)
- **Usability testing**: Task completion
- **A/B testing**: Compare alternatives
- **Analytics**: Usage patterns
- **Surveys**: User satisfaction

### Metrics
- **Effectiveness**: Task completion rate
- **Efficiency**: Time on task
- **Satisfaction**: User ratings
- **Learnability**: Improvement over time
- **Memorability**: Performance after absence

## Interaction Paradigms

### WIMP
Windows, Icons, Menus, Pointer
- Desktop standard
- Mature and familiar
- Mouse-centric

### Touch
- Direct manipulation
- Gestures
- Mobile-first

### Voice
- Natural language
- Hands-free
- Accessibility

### AR/VR
- Spatial computing
- Immersive
- 3D interaction

## Exercises

1. Evaluate an IDE against Nielsen's heuristics
2. Calculate Fitts's Law for a toolbar button
3. Design a CLI with good error messages
4. Conduct a think-aloud usability test
5. Create an accessibility checklist for a dev tool

## Key Insights

- **Users are not designers**: Test with real users
- **Consistency reduces learning**: Follow conventions
- **Feedback is essential**: Users need to know what happened
- **Errors will happen**: Design for recovery

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
