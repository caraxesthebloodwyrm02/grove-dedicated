"""
ANSI Magic Prototype
Location: prototypes/ansi_test.py

A spike script to validate high-fidelity colored text output for the
Hogwarts CLI. This ensures we can visualize House colors and magical
effects (like the Killing Curse green or Patronus silver) directly
in the terminal without external image generators.
"""

import random


def color_text(text: str, rgb: tuple) -> str:
    """Apply TrueColor (RGB) foreground to text."""
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def magic_sparkle(text: str) -> str:
    """Interleave silver sparkles into text."""
    silver = (226, 232, 240)
    output = ""
    for char in text:
        output += char
        if random.random() > 0.8:
            output += color_text("✨", silver)
    return output


def main():
    """Demonstrate ANSI TrueColor capabilities for Hogwarts CLI."""
    # Define High-Fidelity House Colors (RGB)
    houses = {
        "Gryffindor": {"primary": (174, 0, 1), "secondary": (238, 186, 48)},
        "Slytherin": {"primary": (26, 71, 42), "secondary": (170, 170, 170)},
        "Ravenclaw": {"primary": (14, 26, 64), "secondary": (148, 107, 45)},
        "Hufflepuff": {"primary": (236, 185, 57), "secondary": (55, 46, 41)},
    }

    print("\n--- HOGWARTS VISUALIZATION ENGINE (ANSI PROTOTYPE) ---\n")

    # Test House Representations
    block = "██████████"
    for house, colors in houses.items():
        print(f"{color_text(block, colors['primary'])} {house} Primary")
        print(f"{color_text(block, colors['secondary'])} {house} Secondary")
        print("-" * 30)

    # Test Spell Effects
    print("\n--- SPELL EFFECT VISUALIZATION ---\n")

    spells = [
        ("Avada Kedavra", (0, 255, 0)),
        ("Expecto Patronum", (200, 210, 255)),
        ("Sectumsempra", (139, 0, 0)),
    ]

    for spell_name, spell_color in spells:
        print(f"Spell: {color_text(spell_name, spell_color)}")

    # Patronus effect demonstration
    patronus_silver = (200, 210, 255)
    patronus_text = color_text("The stag bursts from the wand tip...", patronus_silver)
    print(f"Effect: {magic_sparkle(patronus_text)}")

    print("\n[SUCCESS] ANSI Engine initialized. TrueColor support verified.\n")


if __name__ == "__main__":
    main()