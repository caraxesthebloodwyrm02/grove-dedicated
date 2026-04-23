# Digital Circuit Design

## Overview

Digital circuit design transforms Boolean logic into physical hardware using logic gates, flip-flops, and interconnects.

## Combinational Circuits

Output depends only on current inputs.

### Building Blocks
- **Multiplexer**: Select one of N inputs
- **Decoder**: N inputs → 2ᴺ outputs
- **Encoder**: 2ᴺ inputs → N outputs
- **Adder**: Arithmetic addition
- **Comparator**: Compare two values
- **ALU**: Arithmetic Logic Unit

### Design Process
1. Truth table or Boolean expression
2. Minimize (K-map, Quine-McCluskey)
3. Map to gates
4. Optimize for area/speed/power

## Sequential Circuits

Output depends on current inputs AND history (state).

### Storage Elements
- **Latch**: Level-sensitive
- **Flip-Flop**: Edge-triggered (D, JK, T)
- **Register**: Multiple flip-flops

### Finite State Machines
```
State Register → Next State Logic → Output Logic
      ↑                    |
      └────────────────────┘
```

### Design Process
1. State diagram
2. State encoding
3. Next-state equations
4. Output equations
5. Implementation

## Timing Analysis

- **Setup time**: Data stable before clock edge
- **Hold time**: Data stable after clock edge
- **Propagation delay**: Input to output delay
- **Clock-to-Q**: Clock edge to output change

## Design for Testability

- Scan chains
- Built-in self-test (BIST)
- Boundary scan (JTAG)

---

**Status**: Foundation established
**Last Updated**: December 2025
