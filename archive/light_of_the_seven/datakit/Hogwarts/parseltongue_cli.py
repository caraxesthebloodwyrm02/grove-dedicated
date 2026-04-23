"""The Parseltongue Insight Engine

Where serpent speech meets serpent code.

A CLI that speaks in code, revealing the hidden wisdom of Hogwarts
through Python patterns that embody each house's philosophy.

This file provides a thin, runnable front-end for manifesting
Temporal Patronus presets. Richer utilities (such as Tier 3 provenance
tracking) live in the reusable `hogwarts_toolkit` module.

Usage examples:

    # Snape's eternal doe (default)
    python parseltongue_cli.py
    python parseltongue_cli.py snape

    # Harry's later-years stag
    python parseltongue_cli.py harry

This script is intentionally self-contained and uses only Python's
standard library (argparse, textwrap, sys).
"""

import argparse
import sys
from typing import List, Optional

__all__ = ["TemporalPatronus", "build_parser", "main"]


# ═══════════════════════════════════════════════════════════════════════════════
# ANSI COLOR SUPPORT
# ═══════════════════════════════════════════════════════════════════════════════


def _supports_color() -> bool:
    """Check if the terminal supports ANSI colors."""
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


def _color(text: str, r: int, g: int, b: int) -> str:
    """Apply RGB color to text if supported."""
    if not _supports_color():
        return text
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


# House color palettes
COLORS = {
    "slytherin": (26, 71, 42),  # Emerald green
    "gryffindor": (174, 0, 1),  # Scarlet
    "ravenclaw": (14, 26, 64),  # Blue
    "hufflepuff": (236, 185, 57),  # Yellow
    "patronus": (200, 210, 255),  # Silver-blue
    "gold": (238, 186, 48),  # Gold accent
}


# ═══════════════════════════════════════════════════════════════════════════════
# THE EXPECTO PATRONUM CHRONICLES: A Research into Light Against Darkness
# ═══════════════════════════════════════════════════════════════════════════════


class TemporalPatronus:
    """
    A Patronus that exists across time - Dumbledore's secret discovery.
    The charm travels backwards through time, creating its own history.
    """

    CASTING_SYMPTOMS = [
        "Brief temporal displacement sensation (the 'shimmer' effect)",
        "Memories feeling more vivid than the present moment",
        "Eyes briefly reflecting events not yet occurred",
        "Goosebumps and time-dilation perception",
        "Patronus form revealing future emotional states",
    ]

    def __init__(self, caster: str, memory: str):
        self.caster = caster
        self.memory = memory
        self._form: Optional[str] = None
        self._temporal_anchors: List[str] = []

    def cast(self, form: str) -> "TemporalPatronus":
        """
        Cast the Patronus with a specific form.
        Returns self for method chaining - a Slytherin would approve.
        """
        self._form = form
        self._temporal_anchors.append(f"Present: {self.caster} casts {form}")
        return self

    def anchor_to_past(self, past_event: str) -> "TemporalPatronus":
        """Connect the Patronus to a past emotional anchor."""
        self._temporal_anchors.append(f"Past: {past_event}")
        return self

    def anchor_to_future(self, future_event: str) -> "TemporalPatronus":
        """Connect the Patronus to a future emotional anchor."""
        self._temporal_anchors.append(f"Future: {future_event}")
        return self

    def manifest(self) -> str:
        """Manifest the Patronus across all temporal anchors."""
        if not self._form:
            raise ValueError("Cannot manifest without casting first")

        result = [
            "✨ EXPECTO PATRONUM ✨",
            f"Caster: {self.caster}",
            f"Form: {self._form}",
            f"Powered by: {self.memory}",
            "",
            "Temporal Anchors:",
        ]
        for anchor in self._temporal_anchors:
            result.append(f"  ⏳ {anchor}")

        return "\n".join(result)

    @classmethod
    def snapes_doe(cls) -> "TemporalPatronus":
        """
        'After all this time?' - 'Always.'
        Snape's love existed outside normal time.
        """
        patronus = cls(
            caster="Severus Snape",
            memory="Love for Lily Evans - transcending time itself",
        )
        return (
            patronus.cast("Silver Doe")
            .anchor_to_past("First meeting with Lily")
            .anchor_to_future("Guiding Harry through the Forbidden Forest")
        )

    @classmethod
    def harry_later_years(cls) -> "TemporalPatronus":
        """Harry's first Patronus in the later years, post-war.

        Reflects Harry's life after defeating Voldemort and his
        determination to build a different future alongside his family.
        """
        patronus = cls(
            caster="Harry Potter",
            memory=(
                "Choosing to live beyond the war and build a family after "
                "defeating Voldemort"
            ),
        )
        return (
            patronus.cast("Stag")
            .anchor_to_past("Final duel with Voldemort in the Great Hall")
            .anchor_to_future(
                "Standing with Albus at the edge of time, choosing a different future"
            )
        )

    @classmethod
    def luna_hare(cls) -> "TemporalPatronus":
        """Luna Lovegood's hare Patronus.

        Embodies unconventional wisdom, quiet courage, and belief in the unseen.
        """
        patronus = cls(
            caster="Luna Lovegood",
            memory="Believing in what others cannot see - Thestrals, Nargles, and friendship",
        )
        return (
            patronus.cast("Hare")
            .anchor_to_past("First seeing Thestrals after her mother's death")
            .anchor_to_future("Publishing The Quibbler's truth for generations to come")
        )

    @classmethod
    def dumbledore_phoenix(cls) -> "TemporalPatronus":
        """Albus Dumbledore's phoenix Patronus.

        Represents rebirth, hope, and the triumph of love over death.
        """
        patronus = cls(
            caster="Albus Dumbledore",
            memory="The belief that love is the most powerful magic of all",
        )
        return (
            patronus.cast("Phoenix")
            .anchor_to_past("Defeating Grindelwald at Nurmengard")
            .anchor_to_future("Guiding Harry at King's Cross between life and death")
        )

    @classmethod
    def hermione_otter(cls) -> "TemporalPatronus":
        """Hermione Granger's otter Patronus.

        Embodies playful intelligence, fierce loyalty, and relentless determination.
        """
        patronus = cls(
            caster="Hermione Granger",
            memory="The moment she realized knowledge could save her friends",
        )
        return (
            patronus.cast("Otter")
            .anchor_to_past(
                "Solving the logic puzzle to protect the Philosopher's Stone"
            )
            .anchor_to_future("Reforming magical law as Minister for Magic")
        )


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the Parseltongue CLI."""
    parser = argparse.ArgumentParser(
        prog="parseltongue_cli",
        description=(
            "Manifest canonical temporal Patronus configurations from Hogwarts history."
        ),
    )

    parser.add_argument(
        "preset",
        nargs="?",
        default="snape",
        choices=["snape", "harry", "luna", "dumbledore", "hermione"],
        help=(
            "Which Patronus to manifest: 'snape' (Silver Doe), "
            "'harry' (Stag), 'luna' (Hare), 'dumbledore' (Phoenix), "
            "'hermione' (Otter)."
        ),
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output.",
    )

    return parser


# Preset registry mapping names to factory methods and house colors
PRESET_REGISTRY = {
    "snape": ("snapes_doe", "slytherin"),
    "harry": ("harry_later_years", "gryffindor"),
    "luna": ("luna_hare", "ravenclaw"),
    "dumbledore": ("dumbledore_phoenix", "gryffindor"),
    "hermione": ("hermione_otter", "gryffindor"),
}


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for the Parseltongue CLI.

    Uses argparse to select between canonical TemporalPatronus presets.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.preset not in PRESET_REGISTRY:  # pragma: no cover
        parser.error(f"Unknown preset: {args.preset}")
        return 1

    method_name, house = PRESET_REGISTRY[args.preset]
    patronus = getattr(TemporalPatronus, method_name)()
    output = patronus.manifest()

    # Apply color if not disabled
    if not getattr(args, "no_color", False) and _supports_color():
        house_color = COLORS.get(house, COLORS["patronus"])
        patronus_color = COLORS["patronus"]
        # Color the header
        lines = output.split("\n")
        colored_lines = []
        for line in lines:
            if line.startswith("✨"):
                colored_lines.append(_color(line, *patronus_color))
            elif line.startswith("Caster:") or line.startswith("Form:"):
                colored_lines.append(_color(line, *house_color))
            elif line.startswith("  ⏳"):
                colored_lines.append(_color(line, *COLORS["gold"]))
            else:
                colored_lines.append(line)
        output = "\n".join(colored_lines)

    print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
