#!/usr/bin/env python3
"""
DataKit Quick Start Example
===========================

This script demonstrates how to use the DataKit learning system
programmatically. You can use these examples as a starting point
for integrating DataKit into your own projects.

Usage:
    python examples/quick_start.py
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config import DataKitConfig, get_config
from core.explorer import InteractiveExplorer, explore
from core.loader import Context, ContextLoader


def example_1_load_context():
    """Example 1: Load a context from a JSON file."""
    print("\n" + "=" * 50)
    print("Example 1: Loading a Context")
    print("=" * 50)

    # Create a loader
    loader = ContextLoader()

    # Load the Circle of Fifths context
    context = loader.load_json("circle_of_fifths.json")

    # Print information about the context
    print(f"\nLoaded: {context.name}")
    print(f"Description: {context.description}")
    print(f"Modules: {len(context.modules)}")
    print(f"Challenges: {len(context.challenges)}")
    print(f"Fun Facts: {len(context.fun_facts)}")

    return context


def example_2_explore_data():
    """Example 2: Access data from a loaded context."""
    print("\n" + "=" * 50)
    print("Example 2: Exploring Context Data")
    print("=" * 50)

    loader = ContextLoader()
    context = loader.load_json("circle_of_fifths.json")

    # Access the raw data
    data = context.data

    # Get musical keys
    keys = data.get("keys", [])
    print(f"\nMusical keys in the circle: {', '.join(keys)}")

    # Get relationships
    relationships = data.get("relationships", {})
    print(f"\nKey 'C' connects to: {relationships.get('C', [])}")

    # Get computational models
    models = data.get("computational_models", {})
    print(f"\nComputational models available: {list(models.keys())}")

    # Get a random fun fact
    fact = context.get_random_fact()
    if fact:
        print(f"\n💡 Random fun fact: {fact}")


def example_3_create_custom_context():
    """Example 3: Create a custom learning context."""
    print("\n" + "=" * 50)
    print("Example 3: Creating a Custom Context")
    print("=" * 50)

    loader = ContextLoader()

    # Create a custom context about Python
    context = loader.create_custom_context(
        name="Python Programming Basics",
        description="Learn the fundamentals of Python programming",
        introduction="Welcome to Python! Let's explore this amazing language.",
        fun_facts=[
            "Python was named after Monty Python, not the snake!",
            "Python uses indentation to define code blocks",
            "Python is one of the most popular programming languages",
            "Guido van Rossum created Python in 1991",
        ],
        modules=[
            {
                "id": "intro",
                "title": "What is Python?",
                "description": "An introduction to Python programming",
                "difficulty": "beginner",
                "duration_minutes": 10,
            },
            {
                "id": "variables",
                "title": "Variables and Data Types",
                "description": "Learn about storing and manipulating data",
                "difficulty": "beginner",
                "duration_minutes": 15,
            },
            {
                "id": "functions",
                "title": "Functions",
                "description": "Creating reusable code blocks",
                "difficulty": "intermediate",
                "duration_minutes": 20,
            },
        ],
        challenges=[
            {
                "id": "quiz_basics",
                "title": "Python Basics Quiz",
                "description": "Test your knowledge of Python fundamentals",
                "type": "quiz",
                "difficulty": "beginner",
                "points": 10,
            }
        ],
    )

    print(f"\nCreated context: {context.name}")
    print(f"Modules: {[m.title for m in context.modules]}")
    print(f"Fun facts: {len(context.fun_facts)}")

    # Get a random fact
    print(f"\n💡 {context.get_random_fact()}")

    return context


def example_4_use_configuration():
    """Example 4: Work with configuration."""
    print("\n" + "=" * 50)
    print("Example 4: Configuration Management")
    print("=" * 50)

    # Get the global configuration
    config = get_config()

    # Show current settings
    print(f"\nCurrent settings:")
    print(f"  Colors enabled: {config.theme.use_colors}")
    print(f"  Emoji enabled: {config.theme.use_emoji}")
    print(f"  Show hints: {config.exploration.show_hints}")
    print(f"  Default context: {config.default_context_file}")

    # Modify settings
    config.theme.use_colors = True
    config.exploration.show_hints = True

    # Use dot notation to get values
    primary_color = config.get("theme.primary_color")
    print(f"\n  Primary color: {primary_color}")

    # Validate configuration
    errors = config.validate()
    if errors:
        print(f"\nConfiguration errors: {errors}")
    else:
        print("\nConfiguration is valid!")


def example_5_list_available_contexts():
    """Example 5: List available context files."""
    print("\n" + "=" * 50)
    print("Example 5: Available Contexts")
    print("=" * 50)

    loader = ContextLoader()
    available = loader.list_available_contexts()

    print("\nAvailable context files:")
    for ctx_file in available:
        print(f"  • {ctx_file}")

    if not available:
        print("  (No context files found)")


def example_6_context_from_dict():
    """Example 6: Create context from a dictionary (e.g., API response)."""
    print("\n" + "=" * 50)
    print("Example 6: Context from Dictionary")
    print("=" * 50)

    # Simulate data that might come from an API
    api_data = {
        "metadata": {
            "name": "API-Loaded Topic",
            "description": "This context was loaded from a dictionary",
            "version": "1.0.0",
            "author": "API",
            "topic_type": "example",
        },
        "learning_modules": [
            {
                "id": "mod1",
                "title": "First Module",
                "description": "Learning from API data",
                "difficulty": "beginner",
            }
        ],
        "fun_facts": [
            "This fact came from a dictionary!",
            "DataKit can load data from any source",
        ],
        "challenges": [],
    }

    loader = ContextLoader()
    context = loader.load_from_dict(api_data)

    print(f"\nLoaded from dict: {context.name}")
    print(f"Type: {context.topic_type}")
    print(f"Modules: {[m.title for m in context.modules]}")


def example_7_explore_interactively():
    """Example 7: Start interactive exploration (optional)."""
    print("\n" + "=" * 50)
    print("Example 7: Interactive Exploration")
    print("=" * 50)

    print("\nTo start interactive exploration, you can do:")
    print("""
    from core.loader import ContextLoader
    from core.explorer import explore

    loader = ContextLoader()
    context = loader.load_json("circle_of_fifths.json")

    # This will launch the interactive CLI
    explore(context)
    """)

    response = input("\nWould you like to start exploring now? (y/n): ").strip().lower()
    if response == "y":
        loader = ContextLoader()
        context = loader.load_json("circle_of_fifths.json")
        explore(context)


def main():
    """Run all examples."""
    print("\n" + "🚀" * 20)
    print("     DataKit Quick Start Examples")
    print("🚀" * 20)

    # Run examples
    example_1_load_context()
    example_2_explore_data()
    example_3_create_custom_context()
    example_4_use_configuration()
    example_5_list_available_contexts()
    example_6_context_from_dict()

    # Interactive example is optional
    example_7_explore_interactively()

    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)
    print("\nFor more information, see the README.md file.")
    print("Happy learning! 🎉\n")


if __name__ == "__main__":
    main()
