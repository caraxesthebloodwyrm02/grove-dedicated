"""
Chord Progression Generator for the Circle of Fifths.

This script generates chord progressions based on the Circle of Fifths
data structure, demonstrating various progression patterns commonly
used in Western music.

Can be run standalone or imported as a module.
"""

import csv
import json
import os
import random
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports when run standalone
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Default Circle of Fifths keys (fallback if JSON not available)
DEFAULT_KEYS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]

# Default relationships (perfect fifths clockwise, perfect fourths counterclockwise)
DEFAULT_RELATIONSHIPS = {
    "C": ["G", "F"],
    "G": ["D", "C"],
    "D": ["A", "G"],
    "A": ["E", "D"],
    "E": ["B", "A"],
    "B": ["F#", "E"],
    "F#": ["C#", "B"],
    "C#": ["G#", "F#"],
    "G#": ["D#", "C#"],
    "D#": ["A#", "G#"],
    "A#": ["F", "D#"],
    "F": ["C", "A#"],
}


class ChordProgressionGenerator:
    """
    Generates chord progressions based on the Circle of Fifths.

    This class provides various methods for generating musical chord
    progressions using the relationships defined in the Circle of Fifths.
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the generator.

        Args:
            data_path: Path to the circle_of_fifths.json file.
                      If None, uses default location or fallback data.
        """
        self.keys: List[str] = []
        self.relationships: Dict[str, List[str]] = {}
        self.common_progressions: Dict[str, Dict] = {}

        # Try to load data from JSON
        self._load_data(data_path)

    def _load_data(self, data_path: Optional[str] = None):
        """Load Circle of Fifths data from JSON file or use defaults."""
        if data_path is None:
            data_path = PROJECT_ROOT / "data" / "circle_of_fifths.json"

        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.keys = data.get("keys", DEFAULT_KEYS)
            self.relationships = data.get("relationships", DEFAULT_RELATIONSHIPS)
            self.common_progressions = data.get("common_progressions", {})
            print(f"✅ Loaded data from: {data_path}")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️  Could not load JSON data: {e}")
            print("   Using default Circle of Fifths data.")
            self.keys = DEFAULT_KEYS
            self.relationships = DEFAULT_RELATIONSHIPS
            self.common_progressions = {}

    def get_key_index(self, key: str) -> int:
        """Get the index of a key in the circle."""
        try:
            return self.keys.index(key)
        except ValueError:
            return 0  # Default to C if key not found

    def get_relative_key(self, key: str, steps: int) -> str:
        """
        Get a key relative to the given key by moving around the circle.

        Args:
            key: Starting key
            steps: Number of steps (positive = clockwise, negative = counterclockwise)

        Returns:
            The key at the specified position
        """
        idx = self.get_key_index(key)
        new_idx = (idx + steps) % len(self.keys)
        return self.keys[new_idx]

    def generate_random_progression(
        self, start_key: Optional[str] = None, length: int = 4
    ) -> List[str]:
        """
        Generate a random chord progression following circle relationships.

        Args:
            start_key: Starting key (random if None)
            length: Number of chords in the progression

        Returns:
            List of keys in the progression
        """
        if start_key is None:
            start_key = random.choice(self.keys)

        progression = [start_key]
        current_key = start_key

        for _ in range(length - 1):
            # Get related keys and pick one randomly
            related = self.relationships.get(current_key, [])
            if related:
                next_key = random.choice(related)
            else:
                # Fallback: move by perfect fifth
                next_key = self.get_relative_key(current_key, 1)

            progression.append(next_key)
            current_key = next_key

        return progression

    def generate_I_IV_V_I(self, key: str) -> List[str]:
        """
        Generate the classic I-IV-V-I progression in the given key.

        Args:
            key: The root key

        Returns:
            List of 4 keys forming the I-IV-V-I progression
        """
        idx = self.get_key_index(key)

        # I = root
        # IV = counterclockwise 1 step (or clockwise 11 steps)
        # V = clockwise 1 step
        I = self.keys[idx]
        IV = self.keys[(idx - 1) % len(self.keys)]  # Counterclockwise
        V = self.keys[(idx + 1) % len(self.keys)]  # Clockwise

        return [I, IV, V, I]

    def generate_ii_V_I(self, key: str) -> List[str]:
        """
        Generate the jazz ii-V-I progression in the given key.

        Args:
            key: The root key (target I chord)

        Returns:
            List of 3 keys forming the ii-V-I progression
        """
        idx = self.get_key_index(key)

        # I = root
        # V = clockwise 1 step
        # ii = clockwise 2 steps (relative to V)
        I = self.keys[idx]
        V = self.keys[(idx + 1) % len(self.keys)]
        ii = self.keys[(idx + 2) % len(self.keys)]

        return [ii, V, I]

    def generate_fifths_walk(self, start_key: str, length: int = 5) -> List[str]:
        """
        Generate a progression walking through perfect fifths.

        Args:
            start_key: Starting key
            length: Number of steps

        Returns:
            List of keys walking around the circle
        """
        progression = []
        idx = self.get_key_index(start_key)

        for i in range(length):
            progression.append(self.keys[(idx + i) % len(self.keys)])

        return progression

    def generate_batch(
        self, num_progressions: int = 10, length: int = 5
    ) -> List[List[str]]:
        """
        Generate multiple random progressions.

        Args:
            num_progressions: Number of progressions to generate
            length: Length of each progression

        Returns:
            List of progressions
        """
        progressions = []
        for _ in range(num_progressions):
            progression = self.generate_random_progression(length=length)
            progressions.append(progression)
        return progressions

    def save_to_csv(self, progressions: List[List[str]], filepath: str):
        """
        Save progressions to a CSV file.

        Args:
            progressions: List of progressions to save
            filepath: Output file path
        """
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Progression", "Start Key", "Length"])
            for progression in progressions:
                writer.writerow(
                    [" → ".join(progression), progression[0], len(progression)]
                )
        print(f"✅ Saved {len(progressions)} progressions to: {filepath}")

    def print_progression(self, progression: List[str], name: str = ""):
        """Print a progression in a nice format."""
        prog_str = " → ".join(progression)
        if name:
            print(f"  🎵 {name}: {prog_str}")
        else:
            print(f"  🎵 {prog_str}")


def interactive_mode(generator: ChordProgressionGenerator):
    """Run the generator in interactive mode."""
    print("\n" + "=" * 50)
    print("🎹 Chord Progression Generator")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  [1] Generate random progression")
        print("  [2] Generate I-IV-V-I")
        print("  [3] Generate ii-V-I (Jazz)")
        print("  [4] Walk through fifths")
        print("  [5] Generate batch & save to CSV")
        print("  [6] Show all keys")
        print("  [q] Quit")

        choice = input("\nEnter choice: ").strip().lower()

        if choice == "1":
            key = input("Starting key (or Enter for random): ").strip().upper() or None
            length = input("Length (default 4): ").strip() or "4"
            prog = generator.generate_random_progression(key, int(length))
            print("\nGenerated progression:")
            generator.print_progression(prog, "Random")

        elif choice == "2":
            key = input("Key (e.g., C, G, D): ").strip().upper() or "C"
            prog = generator.generate_I_IV_V_I(key)
            print(f"\nI-IV-V-I in {key}:")
            generator.print_progression(prog, "Classic")

        elif choice == "3":
            key = input("Target key (e.g., C, G, D): ").strip().upper() or "C"
            prog = generator.generate_ii_V_I(key)
            print(f"\nii-V-I resolving to {key}:")
            generator.print_progression(prog, "Jazz")

        elif choice == "4":
            key = input("Starting key (e.g., C): ").strip().upper() or "C"
            length = input("Steps (default 5): ").strip() or "5"
            prog = generator.generate_fifths_walk(key, int(length))
            print(f"\nFifths walk from {key}:")
            generator.print_progression(prog, "Circle Walk")

        elif choice == "5":
            num = input("Number of progressions (default 10): ").strip() or "10"
            progressions = generator.generate_batch(int(num))

            # Save to data directory
            output_path = PROJECT_ROOT / "data" / "chord_progressions.csv"
            generator.save_to_csv(progressions, str(output_path))

            print("\nGenerated progressions:")
            for i, prog in enumerate(progressions[:5], 1):
                generator.print_progression(prog, f"#{i}")
            if len(progressions) > 5:
                print(f"  ... and {len(progressions) - 5} more")

        elif choice == "6":
            print("\nCircle of Fifths keys (clockwise):")
            print("  " + " → ".join(generator.keys))

        elif choice == "q":
            print("\n👋 Thanks for using the Chord Generator!")
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    """Main entry point for the script."""
    print("🎵 Circle of Fifths - Chord Progression Generator")
    print("-" * 50)

    # Create generator
    generator = ChordProgressionGenerator()

    # Check if running interactively
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        # Batch mode: generate and save
        num = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        progressions = generator.generate_batch(num)
        output_path = PROJECT_ROOT / "data" / "chord_progressions.csv"
        generator.save_to_csv(progressions, str(output_path))
    else:
        # Interactive mode
        interactive_mode(generator)


if __name__ == "__main__":
    main()
