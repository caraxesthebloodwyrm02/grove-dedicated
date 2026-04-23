"""
Interactive guided tour of the Circle of Fifths.

This script provides a step-by-step walkthrough of the Circle of Fifths,
explaining its logic-based analogies and computational framework.

Can be run standalone or imported as a module.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports when run standalone
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Define the Circle of Fifths (clockwise)
CIRCLE_OF_FIFTHS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]

# Define guided tour steps
TOUR_STEPS = [
    {
        "title": "Introduction to the Circle of Fifths",
        "content": (
            "The Circle of Fifths is a visual representation of the relationships "
            "among the 12 tones of the chromatic scale, their corresponding key signatures, "
            "and the associated major and minor keys.\n\n"
            "In this guided tour, we'll explore how the Circle of Fifths can be "
            "represented as a computational framework, including:\n"
            "- Finite State Machines (FSM)\n"
            "- Boolean Algebra\n"
            "- Graph Theory\n"
            "- Quantum Computing Analogies"
        ),
    },
    {
        "title": "The Circle as a Finite State Machine (FSM)",
        "content": (
            "The Circle of Fifths can be modeled as a finite state machine (FSM), where:\n"
            "- Each key is a **state** (e.g., C, G, D).\n"
            "- Transitions between keys are **perfect fifths** (e.g., C → G).\n"
            "- Moving clockwise adds sharps, while moving counterclockwise adds flats.\n\n"
            "This makes it useful for hardware implementations (e.g., FPGA-based music generators)."
        ),
    },
    {
        "title": "Boolean Algebra and the Circle",
        "content": (
            "The Circle of Fifths can also be represented using Boolean algebra:\n"
            "- Each key is a **binary state** (e.g., C = 0000, G = 0001).\n"
            "- Sharps and flats are **bit flips** (e.g., adding a sharp flips a bit).\n"
            "- Chord progressions can be modeled as **logic gates** (e.g., AND, OR).\n\n"
            "This is useful for algorithmic music generation and computational music theory."
        ),
    },
    {
        "title": "Graph Theory and the Circle",
        "content": (
            "The Circle of Fifths is a **graph**, where:\n"
            "- Nodes represent keys (e.g., C, G, D).\n"
            "- Edges represent intervals (e.g., perfect fifths).\n"
            "- Chord progressions are **paths** through the graph.\n\n"
            "This allows us to use graph traversal algorithms to generate music."
        ),
    },
    {
        "title": "Quantum Computing Analogies",
        "content": (
            "The Circle of Fifths can be mapped to quantum computing concepts:\n"
            "- Each key is a **qubit state** (e.g., C = |0⟩, G = |1⟩).\n"
            "- Superposition represents a 'fuzzy' key (e.g., (|C⟩ + |G⟩)/√2).\n"
            "- Entanglement represents harmonic relationships between keys.\n\n"
            "This opens up possibilities for quantum music generation."
        ),
    },
    {
        "title": "AI and the Circle of Fifths",
        "content": (
            "The Circle of Fifths can be used in AI-driven music generation:\n"
            "- Markov chains can model chord progressions.\n"
            "- Reinforcement learning can optimize harmonic transitions.\n"
            "- Neural networks can generate music based on the Circle's rules.\n\n"
            "This enables AI to compose music like a jazz musician."
        ),
    },
    {
        "title": "Hands-On: Generate a Chord Progression",
        "content": (
            "Let's generate a chord progression using the Circle of Fifths.\n"
            "We'll use the I-IV-V-I progression, which is common in Western music.\n\n"
            "Example: In the key of C, the progression is C → F → G → C."
        ),
        "interactive": True,
    },
    {
        "title": "Conclusion",
        "content": (
            "The Circle of Fifths is more than just a music theory tool—it's a "
            "**computational framework** that can be applied to:\n"
            "- Hardware design (e.g., FPGA-based music generators).\n"
            "- Software development (e.g., algorithmic music generation).\n"
            "- AI and machine learning (e.g., reinforcement learning for composition).\n"
            "- Quantum computing (e.g., qubit-based music generation).\n\n"
            "This guided tour is just the beginning. Explore the other scripts in this "
            "datakit to dive deeper into the computational power of the Circle of Fifths!"
        ),
    },
]


def load_circle_data() -> Dict[str, Any]:
    """
    Load Circle of Fifths data from JSON file.

    Returns:
        A dictionary containing circle data.
    """
    data_path = PROJECT_ROOT / "data" / "circle_of_fifths.json"
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def color_text(text: str, color: str) -> str:
    """Apply ANSI color to text."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
        "bold": "\033[1m",
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def generate_chord_progression(start_key: str) -> List[str]:
    """
    Generate a I-IV-V-I chord progression for the given key.

    Args:
        start_key: The starting key (e.g., "C").

    Returns:
        A list of keys representing the progression.
    """
    start_idx = CIRCLE_OF_FIFTHS.index(start_key)
    progression = [
        CIRCLE_OF_FIFTHS[start_idx],  # I
        CIRCLE_OF_FIFTHS[(start_idx - 3) % len(CIRCLE_OF_FIFTHS)],  # IV
        CIRCLE_OF_FIFTHS[(start_idx + 1) % len(CIRCLE_OF_FIFTHS)],  # V
        CIRCLE_OF_FIFTHS[start_idx],  # I
    ]
    return progression


def run_guided_tour(use_colors: bool = True):
    """
    Run the interactive guided tour.

    Args:
        use_colors: Whether to use ANSI colors in output
    """
    # Load additional data from JSON
    circle_data = load_circle_data()

    clear_screen()

    # Welcome header
    print("\n" + "=" * 60)
    if use_colors:
        print(color_text("  🎵 Circle of Fifths: Interactive Guided Tour 🎵", "cyan"))
    else:
        print("  🎵 Circle of Fifths: Interactive Guided Tour 🎵")
    print("=" * 60)
    print("\nWelcome to the interactive guided tour!")
    print("You'll learn how the Circle of Fifths can be represented")
    print("as various computational frameworks.\n")

    # Show fun fact if available
    if circle_data.get("fun_facts"):
        import random

        fact = random.choice(circle_data["fun_facts"])
        print(f"💡 Did you know? {fact}\n")

    input("Press Enter to begin the tour...")

    for i, step in enumerate(TOUR_STEPS):
        clear_screen()

        # Progress indicator
        progress = f"[{i + 1}/{len(TOUR_STEPS)}]"
        print(f"\n{progress}")
        print("=" * 60)

        if use_colors:
            print(color_text(f"🎵 {step['title']}", "yellow"))
        else:
            print(f"🎵 {step['title']}")
        print("=" * 60)
        print()
        print(step["content"])
        print()

        # Show extra data based on step
        if step["title"].find("FSM") >= 0 and circle_data.get("computational_models"):
            fsm_data = circle_data["computational_models"].get(
                "finite_state_machine", {}
            )
            if fsm_data:
                print("\n📊 From the data:")
                apps = fsm_data.get("applications", [])
                if apps:
                    print(f"   Applications: {', '.join(apps[:3])}")

        elif step["title"].find("Boolean") >= 0 and circle_data.get(
            "computational_models"
        ):
            bool_data = circle_data["computational_models"].get("boolean_algebra", {})
            if bool_data:
                encoding = bool_data.get("encoding", {})
                print("\n📊 Binary encodings:")
                for key, binary in list(encoding.items())[:4]:
                    print(f"   {key} = {binary}")

        if step.get("interactive", False):
            print("\n" + "-" * 40)
            print("🎹 Let's generate a chord progression!")
            start_key = input("Enter a starting key (e.g., C, G, D): ").strip().upper()

            if start_key not in CIRCLE_OF_FIFTHS:
                print("Invalid key. Defaulting to C.")
                start_key = "C"

            progression = generate_chord_progression(start_key)

            if use_colors:
                print(
                    f"\nChord Progression: {color_text(' → '.join(progression), 'green')}"
                )
            else:
                print(f"\nChord Progression: {' → '.join(progression)}")
            print(f"This is a classic I-IV-V-I progression in the key of {start_key}")

            # Show common progressions from data
            if circle_data.get("common_progressions"):
                print("\n💡 Other common progressions:")
                for name, prog in list(circle_data["common_progressions"].items())[:3]:
                    example = prog.get("example_in_C", [])
                    print(f"   {name}: {' → '.join(example)}")

        print("\n" + "-" * 40)
        print("  [n] Next  |  [p] Previous  |  [q] Quit")

        choice = input("\n> ").strip().lower()

        if choice == "q":
            break
        elif choice == "p" and i > 0:
            # Go back (handled by loop structure - would need refactoring for true back)
            pass
        # Default: continue to next step

    clear_screen()
    print("\n" + "=" * 60)
    if use_colors:
        print(color_text("  🎉 Guided Tour Complete! 🎉", "green"))
    else:
        print("  🎉 Guided Tour Complete! 🎉")
    print("=" * 60)
    print("\nThank you for exploring the Circle of Fifths!")
    print("The Circle is more than music theory—it's a computational framework.\n")

    print("What's next?")
    print("  • Run the AI Composer: python scripts/ai_composer.py")
    print("  • Generate progressions: python scripts/chord_generator.py")
    print("  • Launch DataKit: python datakit.py")
    print()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Circle of Fifths Guided Tour")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    args = parser.parse_args()

    run_guided_tour(use_colors=not args.no_color)


if __name__ == "__main__":
    main()
