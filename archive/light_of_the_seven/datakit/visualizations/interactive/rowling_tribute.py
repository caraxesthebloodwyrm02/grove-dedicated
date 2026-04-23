#!/usr/bin/env python3
"""
JK Rowling Tribute Visualization
================================

An interactive tribute to JK Rowling, celebrating her journey
from struggling writer to world-renowned author.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

# Project paths (no sys.path modifications)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_appreciation_data() -> Dict[str, Any]:
    """Load the JK Rowling appreciation context data."""
    json_path = DATA_DIR / "jk_rowling_appreciation.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Loaded tribute data from: {json_path}")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️  Could not load JSON: {e}")
        return {}


def build_impact_perspective(data: Dict[str, Any]) -> Dict[str, Any]:
    """Build the core impact perspective JSON for JK Rowling.

    This returns a dictionary in the following structure:

    {
      "role_model": "JK Rowling",
      "description": "A tribute to the creator of Harry Potter - exploring her journey, craft, and cultural impact",
      "emotional_purpose": "To honor storytelling that shaped minds and offered refuge",
      "statistics": { ... },
      "fun_facts": [ ... ],
      "themes": [ ... ]
    }
    """

    metadata = data.get("metadata", {})
    narrative = data.get("narrative_segments", {})
    ripple = narrative.get("global_ripple", {})
    statistics = ripple.get("statistics", {})

    fun_facts = data.get("fun_facts", [])

    craft = narrative.get("craft_elements", {})
    moral = craft.get("elements", {}).get("moral_structure", {})
    themes = moral.get("core_themes", [])

    return {
        "role_model": metadata.get("name", "JK Rowling").replace(" Appreciation", ""),
        "description": metadata.get(
            "description",
            "A tribute to the creator of Harry Potter - exploring her journey, craft, and cultural impact",
        ),
        "emotional_purpose": metadata.get(
            "emotional_purpose",
            "To honor storytelling that shaped minds and offered refuge",
        ),
        "statistics": statistics,
        "fun_facts": fun_facts,
        "themes": themes,
    }


def display_banner():
    """Display the tribute banner."""
    banner = r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   ✨  A TRIBUTE TO J.K. ROWLING  ✨                              ║
    ║                                                                  ║
    ║   "It does not do to dwell on dreams and forget to live."       ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_journey_timeline(data: Dict[str, Any]):
    """Display the author's journey timeline."""
    print("\n📜 THE JOURNEY\n" + "=" * 50)
    
    origins = data.get("narrative_segments", {}).get("origins", {})
    timeline = origins.get("timeline", [])
    
    for event in timeline:
        year = event.get("year", "")
        description = event.get("event", "")
        print(f"  {year} │ {description}")
    
    print("\n" + origins.get("levels", {}).get("reflection", ""))


def display_books(data: Dict[str, Any]):
    """Display the Harry Potter book milestones."""
    print("\n📚 THE BOOKS\n" + "=" * 50)
    
    books = data.get("knowledge_blocks", {}).get("book_milestones", [])
    
    for book in books:
        title = book.get("title", "")
        year = book.get("year", "")
        theme = book.get("theme", "")
        pages = book.get("pages", "")
        print(f"  ⚡ {title} ({year})")
        print(f"     Theme: {theme} | Pages: {pages}")


def display_hogwarts_houses(data: Dict[str, Any]):
    """Display Hogwarts house information."""
    print("\n🏰 HOGWARTS HOUSES\n" + "=" * 50)
    
    houses = data.get("knowledge_blocks", {}).get("hogwarts_houses", {})
    
    house_emojis = {
        "Gryffindor": "🦁",
        "Slytherin": "🐍",
        "Ravenclaw": "🦅",
        "Hufflepuff": "🦡"
    }
    
    for house, info in houses.items():
        emoji = house_emojis.get(house, "✨")
        trait = info.get("trait", "")
        element = info.get("element", "")
        founder = info.get("founder", "")
        print(f"  {emoji} {house}")
        print(f"     Trait: {trait} | Element: {element}")
        print(f"     Founder: {founder}\n")


def display_personal_resonance(data: Dict[str, Any]):
    """Display why this tribute matters."""
    print("\n💝 WHY THIS MATTERS\n" + "=" * 50)
    
    resonance = data.get("narrative_segments", {}).get("personal_resonance", {})
    levels = resonance.get("levels", {})
    
    print(f"\n  {levels.get('summary', '')}\n")
    print(f"  {levels.get('deeper', '')}\n")
    print(f"  ✨ {levels.get('reflection', '')}")


def display_gratitude():
    """Display closing gratitude message."""
    print("\n" + "=" * 50)
    print("""
    Thank you, J.K. Rowling, for:
    
    ✨ Giving us Hogwarts as a second home
    ✨ Teaching us that love is the most powerful magic
    ✨ Showing that ordinary people can be heroes
    ✨ Creating a world where the awkward belong
    ✨ Proving that perseverance creates magic
    
    "Happiness can be found even in the darkest of times,
     if one only remembers to turn on the light."
    """)
    print("=" * 50 + "\n")


def display_impact_perspective(data: Dict[str, Any]):
    """Display the core impact perspective (role_model, stats, fun facts, themes)."""
    print("\n📊 IMPACT OVERVIEW\n" + "=" * 50)

    perspective = build_impact_perspective(data)

    print(f"\n  Role model: {perspective['role_model']}")
    print(f"  Description: {perspective['description']}")
    print(f"  Emotional purpose: {perspective['emotional_purpose']}\n")

    print("  Key statistics:")
    stats = perspective.get("statistics", {})
    for key, value in stats.items():
        print(f"    • {key.replace('_', ' ').title()}: {value}")

    print("\n  Fun facts:")
    for fact in perspective.get("fun_facts", []):
        print(f"    • {fact}")

    print("\n  Core themes:")
    for theme in perspective.get("themes", []):
        print(f"    • {theme}")


def interactive_menu(data: Dict[str, Any]):
    """Run an interactive tribute menu."""
    while True:
        print("\n🪄 TRIBUTE MENU")
        print("-" * 30)
        print("  [1] View Journey Timeline")
        print("  [2] Explore the Books")
        print("  [3] Discover Hogwarts Houses")
        print("  [4] Why This Matters")
        print("  [5] Show Gratitude")
        print("  [6] Impact Overview")
        print("  [a] Show All")
        print("  [q] Exit")
        
        choice = input("\n> ").strip().lower()
        
        if choice == "1":
            display_journey_timeline(data)
        elif choice == "2":
            display_books(data)
        elif choice == "3":
            display_hogwarts_houses(data)
        elif choice == "4":
            display_personal_resonance(data)
        elif choice == "5":
            display_gratitude()
        elif choice == "6":
            display_impact_perspective(data)
        elif choice == "a":
            display_journey_timeline(data)
            display_books(data)
            display_hogwarts_houses(data)
            display_personal_resonance(data)
            display_gratitude()
            display_impact_perspective(data)
        elif choice == "q":
            print("\n✨ Mischief Managed! ✨\n")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main entry point for the tribute visualization."""
    display_banner()
    data = load_appreciation_data()
    
    if not data:
        print("Unable to load tribute data. Please check the data file.")
        return
    
    interactive_menu(data)


if __name__ == "__main__":
    main()
