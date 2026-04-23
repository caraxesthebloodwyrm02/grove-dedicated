#!/usr/bin/env python
"""
Locus of Control Demo: Agency Mechanism

Demonstrates how the dials restore user agency and manufacture certainty
through the act of control. Each dial turn is a micro-affirmation of control.
"""

import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[5]
GREP_EQ_SPECTRUM_ROOT = REPO_ROOT / "light_of_the_seven" / "full_datakit" / "At the rate" / "grep_eq_spectrum"

sys.path.insert(0, str(GREP_EQ_SPECTRUM_ROOT))

from workspace.dials_and_knobs import DialsAndKnobs
from core.models import EmotionalValence, DrivePolicy

def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def demonstrate_helplessness():
    """Show the panic state: no control."""
    print_section("SCENARIO 1: HELPLESSNESS (No Control)")
    
    print("\nUser observes market data passively:")
    print("  • Market is falling")
    print("  • Volatility is high")
    print("  • News is contradictory")
    print("  → User feels: 'I can't do anything'")
    print("  → Result: PANIC, PARALYSIS")
    
    print("\nWithout GRID:")
    print("  Input: Ambiguous market signals")
    print("  Process: Black-box analysis")
    print("  Output: 'Trust me, sell now'")
    print("  User State: Uncertain, helpless, panicked")

def demonstrate_agency_through_dials():
    """Show how dials restore agency."""
    print_section("SCENARIO 2: AGENCY RESTORED (Dials as Control)")
    
    dk = DialsAndKnobs(smoothing=0.3)
    policy = DrivePolicy()
    
    print("\nUser takes control through dials:")
    print("  Step 1: Acknowledge current state")
    
    # Current state: panic
    dk.set_dials(valence=-0.6, arousal=0.8, dominance=0.2)
    for _ in range(3): dk.tick()
    snap1 = dk.snapshot(label="Panic State")
    
    print(f"    Valence: {snap1.valence:.2f} (negative, scared)")
    print(f"    Arousal: {snap1.arousal:.2f} (high, activated)")
    print(f"    Dominance: {snap1.depth:.2f} (low, helpless)")
    print(f"    Drive: {snap1.drive:.4f} ({policy.classify_drive(snap1.drive)})")
    print(f"    → Feeling: 'I'm losing control'")
    
    print("\n  Step 2: User turns Dominance dial UP (agency affirmation)")
    print("    'I choose to take control of this situation'")
    
    dk.set_dials(valence=-0.6, arousal=0.8, dominance=0.7)
    for _ in range(3): dk.tick()
    snap2 = dk.snapshot(label="Taking Control")
    
    print(f"    Valence: {snap2.valence:.2f} (still negative, but...)")
    print(f"    Arousal: {snap2.arousal:.2f} (still high, but...)")
    print(f"    Dominance: {snap2.depth:.2f} (HIGH, I'm in control)")
    print(f"    Drive: {snap2.drive:.4f} ({policy.classify_drive(snap2.drive)})")
    print(f"    → Feeling: 'I'm managing this'")
    
    print("\n  Step 3: User turns Arousal dial DOWN (calming)")
    print("    'I choose to calm down and think clearly'")
    
    dk.set_dials(valence=-0.6, arousal=0.3, dominance=0.7)
    for _ in range(3): dk.tick()
    snap3 = dk.snapshot(label="Calm Control")
    
    print(f"    Valence: {snap3.valence:.2f} (still negative, but...)")
    print(f"    Arousal: {snap3.arousal:.2f} (low, calm)")
    print(f"    Dominance: {snap3.depth:.2f} (high, in control)")
    print(f"    Drive: {snap3.drive:.4f} ({policy.classify_drive(snap3.drive)})")
    print(f"    → Feeling: 'I'm calm and in control'")
    
    print("\n  Step 4: User turns Valence dial UP (optimism)")
    print("    'I choose to see the opportunity in this'")
    
    dk.set_dials(valence=0.3, arousal=0.3, dominance=0.7)
    for _ in range(3): dk.tick()
    snap4 = dk.snapshot(label="Optimistic Control")
    
    print(f"    Valence: {snap4.valence:.2f} (positive, hopeful)")
    print(f"    Arousal: {snap4.arousal:.2f} (low, calm)")
    print(f"    Dominance: {snap4.depth:.2f} (high, in control)")
    print(f"    Drive: {snap4.drive:.4f} ({policy.classify_drive(snap4.drive)})")
    print(f"    → Feeling: 'I'm calm, in control, and optimistic'")
    
    print("\n  Step 5: User COMMITS to action (HIGH_POSITIVE band)")
    print("    'I'm ready to execute with confidence'")
    
    dk.set_dials(valence=0.6, arousal=0.5, dominance=0.8)
    for _ in range(3): dk.tick()
    snap5 = dk.snapshot(label="Execute with Certainty")
    
    print(f"    Valence: {snap5.valence:.2f} (positive, confident)")
    print(f"    Arousal: {snap5.arousal:.2f} (engaged, ready)")
    print(f"    Dominance: {snap5.depth:.2f} (HIGH, full control)")
    print(f"    Drive: {snap5.drive:.4f} ({policy.classify_drive(snap5.drive)})")
    print(f"    → Feeling: 'I'm executing with certainty'")
    print(f"    → Band: HIGH_POSITIVE → Pipeline mode: ACCELERATE")
    
    print("\n  TRANSFORMATION:")
    print(f"    Start:  Drive = {snap1.drive:.4f} (panic, NEUTRAL)")
    print(f"    End:    Drive = {snap5.drive:.4f} (certainty, HIGH_POSITIVE)")
    print(f"    Change: {snap5.drive - snap1.drive:+.4f}")
    print(f"    → User moved from HELPLESSNESS to AGENCY to ACTION")

def demonstrate_psychological_layers():
    """Show the four layers of control."""
    print_section("PSYCHOLOGICAL LAYERS OF CONTROL")
    
    dk = DialsAndKnobs(smoothing=0.3)
    
    print("\nLayer 1: MECHANICAL (I can change things)")
    print("  Action: Turn dial from 0.2 to 0.7")
    dk.set_dials(valence=0.0, arousal=0.2, dominance=0.2)
    for _ in range(2): dk.tick()
    print(f"  Result: Dominance changed to {dk.depth_dial.value:.2f}")
    print("  Feeling: 'My action had an effect'")
    
    print("\nLayer 2: COGNITIVE (My actions have measurable impact)")
    print("  Observation: Drive coefficient updated")
    dk.set_dials(valence=0.0, arousal=0.5, dominance=0.7)
    for _ in range(2): dk.tick()
    drive = dk.drive
    print(f"  Result: Drive = {drive:.4f}")
    print("  Feeling: 'I can see the impact quantified'")
    
    print("\nLayer 3: EMOTIONAL (I can preserve good states)")
    print("  Action: Snapshot current state")
    snap = dk.snapshot(label="Good State")
    print(f"  Result: State saved at {snap.timestamp}")
    print("  Feeling: 'I can hold onto this good feeling'")
    
    print("\nLayer 4: STRATEGIC (My control maps to outcomes)")
    print("  Observation: Policy band determines action")
    policy = DrivePolicy()
    band = policy.classify_drive(drive)
    print(f"  Result: Drive {drive:.4f} → {band} band")
    print(f"  Action: {get_action_for_band(band)}")
    print("  Feeling: 'My control leads to real outcomes'")

def get_action_for_band(band):
    """Get recommended action for drive band."""
    actions = {
        "HIGH_POSITIVE": "Accelerate, take opportunities",
        "NEUTRAL": "Hold steady, monitor situation",
        "HIGH_NEGATIVE": "De-escalate, seek support"
    }
    return actions.get(band, "Unknown")

def demonstrate_certainty_manufacturing():
    """Show how certainty is manufactured step by step."""
    print_section("CERTAINTY MANUFACTURING PIPELINE")
    
    dk = DialsAndKnobs(smoothing=0.3)
    policy = DrivePolicy()
    
    print("\nStep 1: RAW AMBIGUITY")
    print("  Input: 'I feel uneasy about this situation'")
    print("  Problem: Ambiguous, unmeasurable, triggers panic")
    
    print("\nStep 2: QUANTIZATION (V×A×D)")
    dk.set_dials(valence=-0.3, arousal=0.4, dominance=0.5)
    for _ in range(2): dk.tick()
    print(f"  Valence: {dk.valence_dial.value:.2f}")
    print(f"  Arousal: {dk.arousal_dial.value:.2f}")
    print(f"  Dominance: {dk.depth_dial.value:.2f}")
    print("  Result: Ambiguity → Precise Numbers")
    
    print("\nStep 3: CLASSIFICATION (Policy Bands)")
    drive = dk.drive
    band = policy.classify_drive(drive)
    print(f"  Drive: {drive:.4f}")
    print(f"  Band: {band}")
    print("  Result: Numbers → Actionable Category")
    
    print("\nStep 4: ACTION MAPPING")
    action = get_action_for_band(band)
    print(f"  Recommended: {action}")
    print("  Result: Category → Specific Action")
    
    print("\nStep 5: AGENCY RESTORATION")
    print("  User can adjust dials to change action")
    print("  Result: Action → User Control")
    
    print("\nFINAL STATE: STRUCTURED CERTAINTY")
    print(f"  'My unease is: slightly negative sentiment ({dk.valence_dial.value:.2f}),")
    print(f"   moderate activation ({dk.arousal_dial.value:.2f}),")
    print(f"   reasonable control ({dk.depth_dial.value:.2f}).'")
    print(f"  Recommended action: {action}")
    print("  User state: CALM, INFORMED, IN CONTROL")

def main():
    """Run all demonstrations."""
    print("\n" + "█" * 70)
    print("█  LOCUS OF CONTROL DEMO: Agency as Certainty Mechanism")
    print("█" * 70)
    
    demonstrate_helplessness()
    demonstrate_agency_through_dials()
    demonstrate_psychological_layers()
    demonstrate_certainty_manufacturing()
    
    print_section("KEY INSIGHT")
    print("\nThe dials are not just UI controls—they are AGENCY ARTIFACTS.")
    print("\nEach dial turn is a micro-affirmation:")
    print("  • Mechanical: 'I can change things'")
    print("  • Cognitive: 'My actions have measurable impact'")
    print("  • Emotional: 'I can preserve good states'")
    print("  • Strategic: 'My control maps to outcomes'")
    print("\nResult: Panic → Certainty through RESTORED AGENCY")
    
    print("\n" + "=" * 70)
    print("  Certainty is manufactured when users regain control.")
    print("  GRID manufactures certainty by restoring agency.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
