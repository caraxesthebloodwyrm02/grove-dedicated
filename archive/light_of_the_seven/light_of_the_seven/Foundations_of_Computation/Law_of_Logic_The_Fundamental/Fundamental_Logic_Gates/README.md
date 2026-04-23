# Fundamental Logic Gates

## Overview

Logic gates are electronic circuits that perform Boolean operations on one or more inputs to produce a single output. They are the fundamental building blocks of all digital systems, from simple calculators to complex processors.

## The Seven Basic Gates

### Classification

#### Basic Gates (3)
- **AND**: Conjunction
- **OR**: Disjunction
- **NOT**: Negation/Inversion

#### Inverted Gates (2)
- **NAND**: NOT-AND
- **NOR**: NOT-OR

#### Exclusive Gates (2)
- **XOR**: Exclusive OR
- **XNOR**: Exclusive NOR

## Gate Characteristics

### Electrical Properties

| Property | Description |
|----------|-------------|
| **Fan-in** | Number of inputs a gate can accept |
| **Fan-out** | Number of gates an output can drive |
| **Propagation Delay** | Time for input change to affect output |
| **Power Consumption** | Static and dynamic power usage |
| **Noise Margin** | Tolerance to signal degradation |

### Logic Levels

| Level | Voltage (TTL) | Voltage (CMOS 3.3V) |
|-------|---------------|---------------------|
| Logic 0 | 0 - 0.8V | 0 - 1.0V |
| Logic 1 | 2.0 - 5.0V | 2.3 - 3.3V |
| Undefined | 0.8 - 2.0V | 1.0 - 2.3V |

## Truth Tables Summary

### 2-Input Gates

| A | B | AND | OR | NAND | NOR | XOR | XNOR |
|---|---|-----|-----|------|-----|-----|------|
| 0 | 0 |  0  |  0  |  1   |  1  |  0  |  1   |
| 0 | 1 |  0  |  1  |  1   |  0  |  1  |  0   |
| 1 | 0 |  0  |  1  |  1   |  0  |  1  |  0   |
| 1 | 1 |  1  |  1  |  0   |  0  |  0  |  1   |

### NOT Gate

| A | NOT |
|---|-----|
| 0 |  1  |
| 1 |  0  |

## Gate Symbols

### IEEE/ANSI Standard
- Distinctive shapes for each gate type
- AND: Flat back, curved front
- OR: Curved back, pointed front
- NOT: Triangle with bubble

### IEC Standard
- Rectangular symbols with function labels
- More uniform, less intuitive
- Used in some international contexts

## Implementation Technologies

### TTL (Transistor-Transistor Logic)
- Bipolar transistors
- Fast switching
- Higher power consumption
- 5V supply typical

### CMOS (Complementary Metal-Oxide-Semiconductor)
- NMOS and PMOS transistors
- Low static power
- Scalable to small geometries
- Dominant technology today

### Other Technologies
- **ECL**: Emitter-Coupled Logic (very fast, high power)
- **RTL**: Resistor-Transistor Logic (historical)
- **DTL**: Diode-Transistor Logic (historical)

## Multi-Input Gates

### Extending to N Inputs

**AND Gate (N inputs)**
- Output = 1 only if ALL inputs = 1
- A · B · C · D · ... · N

**OR Gate (N inputs)**
- Output = 1 if ANY input = 1
- A + B + C + D + ... + N

**XOR Gate (N inputs)**
- Output = 1 if ODD number of inputs = 1
- Parity function

### Practical Limits
- Physical gates typically limited to 2-8 inputs
- Larger functions built from cascaded gates
- Trade-off: fewer levels vs. simpler gates

## Timing Considerations

### Propagation Delay
- **tPLH**: Low-to-High transition time
- **tPHL**: High-to-Low transition time
- Critical for determining maximum clock frequency

### Setup and Hold Times
- Relevant for sequential circuits
- Input must be stable before and after clock edge

### Glitches and Hazards
- Transient incorrect outputs during transitions
- Static hazard: momentary wrong output
- Dynamic hazard: multiple transitions

## Applications

### Combinational Logic
- Arithmetic circuits (adders, multipliers)
- Multiplexers and decoders
- Comparators
- Code converters

### Sequential Logic
- Flip-flops and latches
- Registers and counters
- State machines
- Memory elements

### Special Functions
- Parity generators/checkers (XOR)
- Enable/disable control (AND)
- Signal routing (multiplexers)

## Exercises

1. Draw the symbol for each of the 7 basic gates
2. Verify the truth table for a 3-input AND gate
3. Calculate total propagation delay for a 4-level circuit
4. Design a circuit using only 2-input gates for: f = ABCD
5. Compare power consumption of CMOS vs TTL

## Key Insights

- **Seven gates cover all needs**: Any Boolean function implementable
- **Technology affects performance**: Choose based on requirements
- **Timing is critical**: Propagation delays limit speed
- **Physical constraints matter**: Fan-in, fan-out, power

---

**Status**: Foundation established
**Last Updated**: December 2025
**Maintainer**: GRID Foundations Team
