# ASIC and FPGA Design

## Overview

ASICs (Application-Specific Integrated Circuits) and FPGAs (Field-Programmable Gate Arrays) are two approaches to implementing custom digital logic.

## ASIC Design

### Characteristics
- Custom silicon for specific application
- Highest performance and efficiency
- High NRE (non-recurring engineering) cost
- Long development time
- No post-fabrication changes

### Design Flow
```
Specification → RTL → Synthesis → Physical Design → Tape-out → Fabrication → Testing
```

### When to Use
- High volume production
- Maximum performance needed
- Lowest power required
- Cost amortized over units

## FPGA Design

### Characteristics
- Programmable logic fabric
- Rapid prototyping
- Lower NRE cost
- Reconfigurable
- Lower performance than ASIC

### Architecture
```
┌─────────────────────────────────────┐
│  CLB   CLB   CLB   CLB   CLB   CLB  │
│  CLB   CLB   CLB   CLB   CLB   CLB  │
│  CLB   BRAM  CLB   DSP   CLB   CLB  │
│  CLB   CLB   CLB   CLB   CLB   CLB  │
│  I/O   I/O   I/O   I/O   I/O   I/O  │
└─────────────────────────────────────┘
CLB: Configurable Logic Block
BRAM: Block RAM
DSP: Digital Signal Processing
```

### Design Flow
```
RTL → Synthesis → Place & Route → Bitstream Generation → Programming
```

### When to Use
- Prototyping before ASIC
- Low volume production
- Flexibility needed
- Faster time-to-market

## Comparison

| Aspect | ASIC | FPGA |
|--------|------|------|
| Performance | Highest | Lower |
| Power | Lowest | Higher |
| NRE Cost | High | Low |
| Unit Cost | Low (volume) | Higher |
| Time to Market | Long | Short |
| Flexibility | None | High |

## For AI Accelerators

### FPGA Prototyping
1. Implement RTL on FPGA
2. Validate functionality
3. Measure performance
4. Iterate design

### ASIC Production
1. Finalize RTL from FPGA validation
2. Full VLSI flow
3. Tape-out to foundry
4. Silicon bring-up

---

**Status**: Foundation established
**Last Updated**: December 2025
