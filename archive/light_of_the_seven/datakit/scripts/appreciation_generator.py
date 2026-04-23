#!/usr/bin/env python3
"""
Appreciation Generator
======================

A generative engine that creates heartfelt tributes and appreciation content
for role models who have impacted our lives. Uses structured context data
to produce meaningful outputs: tributes, reflections, gratitude letters, and more.

Usage:
    python appreciation_generator.py              # Interactive menu
    python appreciation_generator.py --tribute    # Generate tribute
    python appreciation_generator.py --letter     # Generate gratitude letter
    python appreciation_generator.py --reflection # Generate personal reflection
    python appreciation_generator.py --impact     # Summarize their impact
"""

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, Optional


def load_context() -> Dict[str, Any]:
    """Load the appreciation context data."""
    data_path = Path(__file__).parent.parent / "data" / "jk_rowling_appreciation.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_impact_perspective(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Build the core impact perspective from the master JSON context.

    Structure:
    {
      "role_model": str,
      "description": str,
      "emotional_purpose": str,
      "statistics": Dict[str, Any],
      "fun_facts": List[str],
      "themes": List[str],
    }
    """

    metadata = ctx.get("metadata", {})
    segments = ctx.get("narrative_segments", {})
    ripple = segments.get("global_ripple", {})
    statistics = ripple.get("statistics", {})

    fun_facts = ctx.get("fun_facts", [])

    craft = segments.get("craft_elements", {})
    moral = craft.get("elements", {}).get("moral_structure", {})
    themes = moral.get("core_themes", [])

    return {
        "role_model": metadata.get("name", "JK Rowling").replace(" Appreciation", ""),
        "description": metadata.get(
            "description",
            "A tribute to the creator of Harry Potter – honoring the stories, craft, and quiet acts of courage that helped millions feel less alone.",
        ),
        "emotional_purpose": metadata.get(
            "emotional_purpose",
            "To thank the person whose stories made Hogwarts a second home, offered comfort in difficult times, and gave us language for hope, friendship, and choice.",
        ),
        "statistics": statistics,
        "fun_facts": fun_facts,
        "themes": themes,
    }


class AppreciationGenerator:
    """
    Engine for generating heartfelt appreciation outputs for role models.
    
    This generator helps users articulate gratitude toward people who have
    shaped their lives, providing templates and inspiration for meaningful tributes.
    """

    def __init__(self, context: Dict[str, Any]):
        self.ctx = context
        self._perspective: Optional[Dict[str, Any]] = None

    def _get_perspective(self) -> Dict[str, Any]:
        if self._perspective is None:
            self._perspective = build_impact_perspective(self.ctx)
        return self._perspective

    def generate_tribute(self, focus: Optional[str] = None) -> str:
        """
        Generate a reflective tribute paragraph honoring the role model.

        Args:
            focus: Optional focus area ('craft', 'impact', 'personal')
        
        Returns:
            A heartfelt tribute paragraph expressing gratitude.
        """
        p = self._get_perspective()

        role_model = p["role_model"]
        emotional_purpose = p["emotional_purpose"]
        themes = p.get("themes", [])
        stats = p.get("statistics", {})
        fun_facts = p.get("fun_facts", [])

        theme = random.choice(themes) if themes else None
        stat_key, stat_value = (None, None)
        if stats:
            stat_key, stat_value = random.choice(list(stats.items()))
        fact = random.choice(fun_facts) if fun_facts else None

        parts = []
        parts.append(f"To {role_model}, whose stories made Hogwarts a second home for so many of us.")
        if emotional_purpose:
            parts.append(emotional_purpose)
        if theme:
            parts.append(f"Again and again, your work returns to the theme that {theme.lower()}.")
        if stat_key and stat_value:
            pretty_key = stat_key.replace("_", " ")
            parts.append(f"In simple numbers—{pretty_key}: {stat_value}—but the real measure is how many hearts were changed.")
        if fact:
            parts.append(f"Along the way, we carried details like this with us: {fact}")

        return " " .join(parts)

    def generate_gratitude_letter(self) -> str:
        """
        Generate a personal gratitude letter to the role model.
        
        Returns:
            A formatted gratitude letter expressing appreciation.
        """
        p = self._get_perspective()

        role_model = p["role_model"]
        emotional_purpose = p["emotional_purpose"]
        themes = p.get("themes", [])
        stats = p.get("statistics", {})
        fun_facts = p.get("fun_facts", [])

        theme_line = ""
        if themes:
            theme = random.choice(themes)
            theme_line = f"Your books quietly taught me that {theme.lower()}"

        stat_line = ""
        if stats:
            key, value = random.choice(list(stats.items()))
            pretty_key = key.replace("_", " ")
            stat_line = f"In the wider world, people talk about numbers like {pretty_key}: {value}, but for me the real number is the nights I felt less alone because of your stories."

        fact_line = ""
        if fun_facts:
            fact = random.choice(fun_facts)
            fact_line = f"I still smile at details like this: {fact}"

        letter = f"""Dear {role_model},

I wanted to take a moment to express my gratitude for the way your work has shaped my life.

{emotional_purpose}

{theme_line}

{stat_line}

{fact_line}

Thank you for building a world where many of us found courage, friendship, and a sense of home.

With sincere appreciation,
A grateful reader"""

        return letter

    def generate_impact_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the role model's impact.
        
        Returns:
            A dictionary containing impact statistics and highlights.
        """
        # Return the core perspective object directly so callers see
        # role_model, description, emotional_purpose, statistics,
        # fun_facts, and themes in a consistent structure.
        return self._get_perspective()

    def generate_reflection_prompt(self) -> str:
        """
        Generate a reflection prompt to help articulate personal gratitude.
        
        Returns:
            A thoughtful prompt for personal reflection.
        """
        p = self._get_perspective()
        role_model = p["role_model"]
        themes = p.get("themes", [])

        # Map themes to more specific prompts when possible.
        theme_prompts = {
            "Choice defines us": "Can you recall a choice you made that felt braver because of something you learned from {role_model}?",
            "Friendship sustains and heals": "Which friendship in your life feels a little bit like the friendships in {role_model}'s world?",
            "Found family is real family": "When have you felt a found family around you, the way the books describe it?",
            "Courage despite fear": "Think of a time you acted even while afraid. How did {role_model}'s stories help you see that as real courage?",
        }

        if themes:
            # Try to pick a theme that has a custom prompt; otherwise fall back.
            weighted = [t for t in themes if t in theme_prompts] or themes
            theme = random.choice(weighted)
            base = theme_prompts.get(
                theme,
                "How has {role_model}'s work helped you through difficult times?",
            )
        else:
            base = "What moment first made you realize {role_model}'s impact on your life?"

        return base.format(role_model=role_model)


def _run_interactive(generator: AppreciationGenerator) -> None:
    """Run an interactive appreciation session in the terminal."""
    while True:
        print("\n✨ Appreciation Generator")
        print("-" * 40)
        print("  [1] Generate tribute paragraph")
        print("  [2] Generate gratitude letter")
        print("  [3] Show impact summary")
        print("  [4] Reflection prompt")
        print("  [q] Quit")

        choice = input("\n> ").strip().lower()

        if choice == "1":
            print("\n--- Tribute ---\n")
            print(generator.generate_tribute())
        elif choice == "2":
            print("\n--- Gratitude Letter ---\n")
            print(generator.generate_gratitude_letter())
        elif choice == "3":
            print("\n--- Impact Summary ---\n")
            summary = generator.generate_impact_summary()
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        elif choice == "4":
            print("\n--- Reflection Prompt ---\n")
            print(generator.generate_reflection_prompt())
        elif choice == "q":
            print("\nThank you for taking a moment to appreciate your role model.\n")
            break
        else:
            print("Invalid choice. Please try again.")


def main() -> None:
    """Command-line entrypoint for the appreciation generator."""
    parser = argparse.ArgumentParser(description="Generate appreciation content from structured context data.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tribute", action="store_true", help="Generate a tribute paragraph")
    group.add_argument("--letter", action="store_true", help="Generate a gratitude letter")
    group.add_argument("--impact", action="store_true", help="Show an impact summary (JSON)")
    group.add_argument("--reflection", action="store_true", help="Generate a reflection prompt")

    args = parser.parse_args()

    context = load_context()
    generator = AppreciationGenerator(context)

    if args.tribute:
        print(generator.generate_tribute())
    elif args.letter:
        print(generator.generate_gratitude_letter())
    elif args.impact:
        summary = generator.generate_impact_summary()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    elif args.reflection:
        print(generator.generate_reflection_prompt())
    else:
        _run_interactive(generator)


if __name__ == "__main__":
    main()
