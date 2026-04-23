# VLSI Design

## Overview

Very Large Scale Integration (VLSI) design creates integrated circuits with millions to billions of transistors. It bridges logical design and physical fabrication.

## Design Flow

```
RTL → Synthesis → Floorplanning → Placement → Clock Tree → Routing → Verification → Tape-out
```

## Logic Synthesis

Convert RTL to gate-level netlist.

```
RTL (Verilog/VHDL) → Synthesis Tool → Gate Netlist
```

### Optimization Goals
- Area minimization
- Timing closure
- Power reduction

## Physical Design

### Floorplanning
- Arrange major blocks
- Plan power distribution
- Estimate routing congestion

### Placement
- Position standard cells
- Optimize for timing and congestion

### Clock Tree Synthesis
- Distribute clock with minimal skew
- Buffer insertion
- Clock gating for power

### Routing
- Connect all signals
- Meet timing constraints
- Avoid DRC violations

## Verification

### Design Rule Check (DRC)
Verify physical rules (spacing, width, etc.)

### Layout vs. Schematic (LVS)
Verify layout matches netlist

### Static Timing Analysis (STA)
Verify timing constraints met

### Power Analysis
- IR drop analysis
- Electromigration check
- Thermal analysis

## Process Technology

- Node size (7nm, 5nm, 3nm)
- FinFET transistors
- Multiple metal layers
- Standard cell libraries

## Tape-out

Final GDSII file sent to foundry for fabrication.

---

**Status**: Foundation established
**Last Updated**: December 2025
