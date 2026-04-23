"""
termporal.py

Definition:
In the architecture of a modern Digital Audio Workstation (DAW), tempo refers to the rate at which the underlying musical clock advances, typically measured in beats per minute (BPM). Tempo acts as a timing framework, influencing how musical events (MIDI notes, audio clips, effects) are quantized and synchronized within the DAW, but does not inherently define the content or structure of the music itself.
"""

import time
import random

class TempoEngine:
    """Simulates tempo-based and freeform DAW timing behavior."""

    def __init__(self, bpm: int = 120, toggle: bool = True):
        self.bpm = bpm
        self.toggle = toggle
        self.beat_interval = 60 / bpm  # seconds per beat

    def toggle_tempo(self, state: bool):
        self.toggle = state

    def get_structure_description(self) -> str:
        if self.toggle:
            return "quantized to BPM grid, predictable sequencing"
        return "freeform: timing is fluid, sequencing based on manual arrangement or external cues"

    def simulate_sequence(self, beats: int = 8):
        print("\n--- Tempo Simulation ---")
        print(f"Tempo Active: {self.toggle} | BPM: {self.bpm}")
        print(f"Structure: {self.get_structure_description()}\n")

        if self.toggle:
            for i in range(beats):
                print(f"Beat {i + 1}: Snap to grid")
                time.sleep(self.beat_interval / 10)  # reduced for demonstration
        else:
            for i in range(beats):
                interval = random.uniform(self.beat_interval * 0.5, self.beat_interval * 1.5)
                print(f"Event {i + 1}: Freeform timing ({interval:.2f}s)")
                time.sleep(interval / 10)

        print("\n--- Simulation Complete ---\n")


def interpret_tempo_perception(toggle: bool):
    if toggle:
        return (
            "Tempo functions as a rigid controller — music aligns to quantized grids."
        )
    else:
        return (
            "Tempo operates as a flexible guideline — expressive, organic sequencing emerges."
        )


def demo():
    print("\nTempo Interpretation and Demonstration")
    print("--------------------------------------")

    # Case 1: Tempo ON
    daw_on = TempoEngine(bpm=120, toggle=True)
    print(interpret_tempo_perception(daw_on.toggle))
    daw_on.simulate_sequence(beats=4)

    # Case 2: Tempo OFF
    daw_off = TempoEngine(bpm=120, toggle=False)
    print(interpret_tempo_perception(daw_off.toggle))
    daw_off.simulate_sequence(beats=4)


if __name__ == "__main__":
    demo()

"""
This Python demonstration interprets the conceptual DAW tempo logic:
- Simulates tempo-locked and freeform timing.
- Validates the conditional toggle logic.
- Illustrates how perception shifts behavior between quantized and expressive time.
"""
