"""NON-CANONICAL: Draw My Life - Visual Biography Generator

This module provides tools for creating visual representations of a person's life,
following the Draw My Life framework. It generates SVG timelines and relationship
graphs from structured life data.

Uses only Python standard library.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class EmotionalValence(Enum):
    """Emotional tone of a life event."""
    TRIUMPH = "triumph"      # Peak moments
    JOY = "joy"              # Happiness
    NEUTRAL = "neutral"      # Regular life
    STRUGGLE = "struggle"    # Challenges
    LOSS = "loss"            # Grief, defeat
    TURNING = "turning"      # Pivotal change


@dataclass
class LifeEvent:
    """A single event in a person's life."""
    date: str  # ISO format or "YYYY" or "~YYYY" for approximate
    title: str
    description: str = ""
    valence: EmotionalValence = EmotionalValence.NEUTRAL
    importance: float = 0.5  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)
    source: str = ""  # Citation for the claim
    
    def year(self) -> int:
        """Extract year from date string."""
        clean = self.date.replace("~", "").replace("?", "")
        return int(clean[:4])


@dataclass
class Relationship:
    """A relationship with another person."""
    person: str
    role: str  # "mentor", "friend", "rival", "family", "love"
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    strength: float = 0.5  # 0.0 to 1.0
    description: str = ""


@dataclass
class LifePhase:
    """A major phase of life."""
    name: str
    start_year: int
    end_year: int
    summary: str = ""
    color: str = "#888888"


@dataclass
class LifeProfile:
    """Complete profile for Draw My Life visualization."""
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    through_line: str = ""  # The essence of this life
    visual_metaphor: str = ""  # e.g., "Silver Doe", "Rising Phoenix"
    events: List[LifeEvent] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    phases: List[LifePhase] = field(default_factory=list)
    
    # Temporal anchors (from TemporalPatronus model)
    past_anchor: str = ""
    present_anchor: str = ""
    future_anchor: str = ""

    def year_range(self) -> Tuple[int, int]:
        """Get the full year range of this life."""
        years = [e.year() for e in self.events]
        if self.birth_year:
            years.append(self.birth_year)
        if self.death_year:
            years.append(self.death_year)
        if not years:
            return (1900, 2000)
        return (min(years), max(years))


# =============================================================================
# Color Palettes
# =============================================================================

VALENCE_COLORS = {
    EmotionalValence.TRIUMPH: "#FFD700",   # Gold
    EmotionalValence.JOY: "#90EE90",       # Light green
    EmotionalValence.NEUTRAL: "#B0C4DE",   # Light steel blue
    EmotionalValence.STRUGGLE: "#CD853F",  # Peru (brown)
    EmotionalValence.LOSS: "#708090",      # Slate gray
    EmotionalValence.TURNING: "#FF6347",   # Tomato red
}

RELATIONSHIP_COLORS = {
    "mentor": "#4169E1",    # Royal blue
    "friend": "#32CD32",    # Lime green
    "rival": "#DC143C",     # Crimson
    "family": "#9370DB",    # Medium purple
    "love": "#FF69B4",      # Hot pink
    "colleague": "#20B2AA", # Light sea green
}


# =============================================================================
# SVG Generation
# =============================================================================

def generate_timeline_svg(
    profile: LifeProfile,
    width: int = 1200,
    height: int = 400,
    margin: int = 60
) -> str:
    """Generate an SVG timeline visualization of a life."""
    
    min_year, max_year = profile.year_range()
    year_span = max(max_year - min_year, 1)
    
    def x_for_year(year: int) -> float:
        return margin + ((year - min_year) / year_span) * (width - 2 * margin)
    
    def y_for_valence(valence: EmotionalValence, importance: float) -> float:
        base_y = height / 2
        # Positive valences go up, negative go down
        if valence in (EmotionalValence.TRIUMPH, EmotionalValence.JOY):
            return base_y - (importance * 100)
        elif valence in (EmotionalValence.LOSS, EmotionalValence.STRUGGLE):
            return base_y + (importance * 100)
        elif valence == EmotionalValence.TURNING:
            return base_y - (importance * 50)  # Slightly elevated
        else:
            return base_y
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<defs>',
        '  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">',
        '    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>',
        '    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        '  </filter>',
        '</defs>',
        
        # Background
        f'<rect width="{width}" height="{height}" fill="#0a0a0f"/>',
        
        # Title
        f'<text x="{width/2}" y="30" text-anchor="middle" fill="#f8e7b7" ',
        f'font-family="Georgia, serif" font-size="20" font-weight="bold">',
        f'{profile.name}: Draw My Life</text>',
        
        # Through-line subtitle
        f'<text x="{width/2}" y="52" text-anchor="middle" fill="#e9c878" ',
        f'font-family="Georgia, serif" font-size="12" font-style="italic">',
        f'"{profile.through_line}"</text>',
        
        # Timeline axis
        f'<line x1="{margin}" y1="{height/2}" x2="{width-margin}" y2="{height/2}" ',
        f'stroke="#f6d37a" stroke-width="2" opacity="0.5"/>',
    ]
    
    # Year markers
    year_step = max(1, year_span // 10)
    for year in range(min_year, max_year + 1, year_step):
        x = x_for_year(year)
        svg_parts.append(
            f'<line x1="{x}" y1="{height/2 - 5}" x2="{x}" y2="{height/2 + 5}" '
            f'stroke="#f6d37a" stroke-width="1" opacity="0.3"/>'
        )
        svg_parts.append(
            f'<text x="{x}" y="{height/2 + 20}" text-anchor="middle" '
            f'fill="#e9c878" font-size="10">{year}</text>'
        )
    
    # Life phases as background bands
    for phase in profile.phases:
        x1 = x_for_year(phase.start_year)
        x2 = x_for_year(phase.end_year)
        svg_parts.append(
            f'<rect x="{x1}" y="60" width="{x2-x1}" height="{height-120}" '
            f'fill="{phase.color}" opacity="0.1"/>'
        )
        svg_parts.append(
            f'<text x="{(x1+x2)/2}" y="{height - 25}" text-anchor="middle" '
            f'fill="{phase.color}" font-size="10" opacity="0.7">{phase.name}</text>'
        )
    
    # Events as connected path
    sorted_events = sorted(profile.events, key=lambda e: e.year())
    if len(sorted_events) > 1:
        path_points = []
        for event in sorted_events:
            x = x_for_year(event.year())
            y = y_for_valence(event.valence, event.importance)
            path_points.append(f"{x},{y}")
        
        svg_parts.append(
            f'<polyline points="{" ".join(path_points)}" '
            f'fill="none" stroke="#f6d37a" stroke-width="2" opacity="0.6"/>'
        )
    
    # Event markers
    for event in sorted_events:
        x = x_for_year(event.year())
        y = y_for_valence(event.valence, event.importance)
        color = VALENCE_COLORS.get(event.valence, "#888888")
        radius = 5 + (event.importance * 10)
        
        # Glow for important events
        if event.importance > 0.7:
            svg_parts.append(
                f'<circle cx="{x}" cy="{y}" r="{radius + 3}" '
                f'fill="{color}" opacity="0.3" filter="url(#glow)"/>'
            )
        
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" '
            f'stroke="#f8e7b7" stroke-width="1"/>'
        )
        
        # Event label (for important events)
        if event.importance > 0.5:
            label_y = y - radius - 8 if y < height/2 else y + radius + 15
            svg_parts.append(
                f'<text x="{x}" y="{label_y}" text-anchor="middle" '
                f'fill="#f8e7b7" font-size="9">{event.title[:20]}</text>'
            )
    
    # Temporal anchors
    anchor_y = height - 10
    if profile.past_anchor:
        svg_parts.append(
            f'<text x="{margin}" y="{anchor_y}" fill="#e9c878" font-size="9">'
            f'Past: {profile.past_anchor[:40]}</text>'
        )
    if profile.future_anchor:
        svg_parts.append(
            f'<text x="{width - margin}" y="{anchor_y}" text-anchor="end" '
            f'fill="#e9c878" font-size="9">Future: {profile.future_anchor[:40]}</text>'
        )
    
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_relationship_svg(
    profile: LifeProfile,
    width: int = 600,
    height: int = 600
) -> str:
    """Generate an SVG relationship constellation."""
    
    center_x, center_y = width / 2, height / 2
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#0a0a0f"/>',
        
        # Title
        f'<text x="{center_x}" y="30" text-anchor="middle" fill="#f8e7b7" ',
        f'font-family="Georgia, serif" font-size="18">{profile.name}: Constellation</text>',
    ]
    
    # Center node (the subject)
    svg_parts.append(
        f'<circle cx="{center_x}" cy="{center_y}" r="30" '
        f'fill="#f6d37a" stroke="#f8e7b7" stroke-width="2"/>'
    )
    svg_parts.append(
        f'<text x="{center_x}" y="{center_y + 5}" text-anchor="middle" '
        f'fill="#0a0a0f" font-size="12" font-weight="bold">{profile.name[:10]}</text>'
    )
    
    # Relationship nodes in a circle
    n_rels = len(profile.relationships)
    for i, rel in enumerate(profile.relationships):
        angle = (2 * math.pi * i / n_rels) - (math.pi / 2)
        distance = 120 + (rel.strength * 80)
        x = center_x + math.cos(angle) * distance
        y = center_y + math.sin(angle) * distance
        
        color = RELATIONSHIP_COLORS.get(rel.role, "#888888")
        
        # Connection line
        line_opacity = 0.3 + (rel.strength * 0.5)
        line_width = 1 + (rel.strength * 2)
        svg_parts.append(
            f'<line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" '
            f'stroke="{color}" stroke-width="{line_width}" opacity="{line_opacity}"/>'
        )
        
        # Relationship node
        radius = 15 + (rel.strength * 10)
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" '
            f'fill="{color}" stroke="#f8e7b7" stroke-width="1" opacity="0.8"/>'
        )
        svg_parts.append(
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" '
            f'fill="#f8e7b7" font-size="10">{rel.person[:12]}</text>'
        )
        svg_parts.append(
            f'<text x="{x}" y="{y + 15 + radius}" text-anchor="middle" '
            f'fill="{color}" font-size="8" opacity="0.7">{rel.role}</text>'
        )
    
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


# =============================================================================
# Presets (Examples)
# =============================================================================

def snape_profile() -> LifeProfile:
    """Create a LifeProfile for Severus Snape."""
    return LifeProfile(
        name="Severus Snape",
        birth_year=1960,
        death_year=1998,
        through_line="Love that could not be expressed, expressed through sacrifice",
        visual_metaphor="The Silver Doe",
        past_anchor="First meeting with Lily by the river",
        present_anchor="Casting the doe Patronus to guide Harry",
        future_anchor="The Pensieve revealing 'Always'",
        phases=[
            LifePhase("Childhood", 1960, 1971, "Neglect, escape into magic", "#4a4a6a"),
            LifePhase("Hogwarts", 1971, 1978, "Friendship, loss, wrong choices", "#2d5a3d"),
            LifePhase("First War", 1978, 1981, "Death Eater, turning point", "#5a2d2d"),
            LifePhase("Interwar", 1981, 1995, "Penance, teaching, waiting", "#3d3d5a"),
            LifePhase("Second War", 1995, 1998, "Double agent, final sacrifice", "#6a4a2d"),
        ],
        events=[
            LifeEvent("1960", "Birth", "Born to Tobias and Eileen Snape", 
                     EmotionalValence.NEUTRAL, 0.3),
            LifeEvent("1967", "Meets Lily", "First encounter by the river",
                     EmotionalValence.JOY, 0.9, source="Deathly Hallows Ch.33"),
            LifeEvent("1971", "Hogwarts Begins", "Sorted into Slytherin; Lily into Gryffindor",
                     EmotionalValence.STRUGGLE, 0.6),
            LifeEvent("1976", "Calls Lily 'Mudblood'", "The friendship ends",
                     EmotionalValence.LOSS, 1.0, source="Order of the Phoenix Ch.28"),
            LifeEvent("1978", "Joins Death Eaters", "Fully commits to the Dark Lord",
                     EmotionalValence.TURNING, 0.8),
            LifeEvent("1980", "Hears the Prophecy", "Brings news to Voldemort",
                     EmotionalValence.TURNING, 0.9),
            LifeEvent("1981", "Lily Dies", "Begs Dumbledore; becomes double agent",
                     EmotionalValence.LOSS, 1.0, source="Deathly Hallows Ch.33"),
            LifeEvent("1991", "Harry Arrives", "Begins protecting Lily's son",
                     EmotionalValence.STRUGGLE, 0.7),
            LifeEvent("1996", "Kills Dumbledore", "Fulfills the Unbreakable Vow",
                     EmotionalValence.TURNING, 1.0, source="Half-Blood Prince Ch.27"),
            LifeEvent("1998", "Death", "Killed by Nagini; gives memories to Harry",
                     EmotionalValence.TRIUMPH, 1.0, source="Deathly Hallows Ch.32"),
        ],
        relationships=[
            Relationship("Lily Evans", "love", 1967, 1976, 1.0, 
                        "The defining relationship of his life"),
            Relationship("Albus Dumbledore", "mentor", 1981, 1997, 0.8,
                        "Master and servant; mutual respect"),
            Relationship("Voldemort", "rival", 1978, 1998, 0.7,
                        "The Dark Lord he betrayed"),
            Relationship("Harry Potter", "family", 1991, 1998, 0.6,
                        "Lily's son; protected and resented"),
            Relationship("James Potter", "rival", 1971, 1981, 0.5,
                        "School rival; took Lily"),
            Relationship("Lucius Malfoy", "colleague", 1971, 1998, 0.4,
                        "Fellow Slytherin and Death Eater"),
        ]
    )


def generate_snape_visualizations(output_dir: Path) -> None:
    """Generate all visualizations for Snape."""
    profile = snape_profile()
    
    timeline_svg = generate_timeline_svg(profile)
    (output_dir / "snape_timeline.svg").write_text(timeline_svg, encoding="utf-8")
    
    constellation_svg = generate_relationship_svg(profile)
    (output_dir / "snape_constellation.svg").write_text(constellation_svg, encoding="utf-8")
    
    print(f"Generated visualizations in {output_dir}")


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    """Run the Draw My Life demo."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Draw My Life - Visual Biography Generator"
    )
    parser.add_argument(
        "preset", nargs="?", default="snape",
        choices=["snape"],
        help="Preset profile to visualize"
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=Path("."),
        help="Output directory for SVG files"
    )
    
    args = parser.parse_args()
    
    if args.preset == "snape":
        generate_snape_visualizations(args.output)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
