#!/usr/bin/env python3
"""
DataKit - Interactive Learning System
======================================

A fun and engaging way to learn about any topic through
immersive, interactive exploration.

This is the main entry point for the DataKit learning system.
Run this script to start exploring!

Usage:
    python datakit.py                  # Interactive mode
    python datakit.py --context FILE   # Load specific context
    python datakit.py --tour           # Start guided tour directly
    python datakit.py --help           # Show help
"""

import argparse
import os
import sys
from pathlib import Path

# Add the project root to the path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config import DataKitConfig, get_config
from core.explorer import InteractiveExplorer
from core.loader import Context, ContextLoader
from core.control import get_control_plane

# ASCII Art Banner
BANNER = r"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║     ██████╗  █████╗ ████████╗ █████╗ ██╗  ██╗██╗████████╗            ║
║     ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║ ██╔╝██║╚══██╔══╝            ║
║     ██║  ██║███████║   ██║   ███████║█████╔╝ ██║   ██║               ║
║     ██║  ██║██╔══██║   ██║   ██╔══██║██╔═██╗ ██║   ██║               ║
║     ██████╔╝██║  ██║   ██║   ██║  ██║██║  ██╗██║   ██║               ║
║     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝               ║
║                                                                       ║
║            🚀 Interactive Learning System 🚀                          ║
║                                                                       ║
║         Load • Explore • Learn • Have Fun!                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

MINI_BANNER = """
╭─────────────────────────────────────╮
│  📚 DataKit - Learn Interactively  │
╰─────────────────────────────────────╯
"""


class DataKit:
    """
    Main DataKit application class.

    This class orchestrates the entire learning experience,
    from loading contexts to running the interactive explorer.
    """

    def __init__(self, config: DataKitConfig | None = None):
        """
        Initialize DataKit.

        Args:
            config: Configuration object (uses default if None)
        """
        self.config = config or get_config()
        self.loader = ContextLoader(PROJECT_ROOT / "data")
        self.control_plane = get_control_plane()
        self.current_context: Context | None = None
        self.explorer: InteractiveExplorer | None = None

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self, mini: bool = False) -> None:
        """Print the DataKit banner."""
        if mini:
            print(MINI_BANNER)
        else:
            print(BANNER)

    def color_text(self, text: str, color: str) -> str:
        """Apply ANSI color to text, depending on config."""
        if not self.config.theme.use_colors:
            return text
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

    def get_input(self, prompt: str = "> ") -> str:
        """Get user input with styled prompt."""
        try:
            return input(self.color_text(prompt, "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            # Treat abrupt termination as a request to quit
            return "q"

    def list_available_contexts(self) -> list[str]:
        """Get list of available context files."""
        return self.loader.list_available_contexts()

    def load_context(self, filepath: str) -> bool:
        """
        Load a context from file.

        Args:
            filepath: Path to the context file

        Returns:
            True if loading was successful
        """
        try:
            if filepath.endswith(".json"):
                self.current_context = self.loader.load_json(filepath)
            elif filepath.endswith((".yaml", ".yml")):
                self.current_context = self.loader.load_yaml(filepath)
            else:
                # Try JSON by default
                self.current_context = self.loader.load_json(filepath)
            return True
        except Exception as e:
            print(self.color_text(f"Error loading context: {e}", "red"))
            return False

    def load_default_context(self) -> bool:
        """Load the default context (Circle of Fifths)."""
        return self.load_context(self.config.default_context_file)

    def create_custom_context(self) -> None:
        """Interactive wizard to create a custom context."""
        self.clear_screen()
        print(self.color_text("\n📝 Create Custom Learning Context\n", "cyan"))
        print("Let's create a new topic to explore!\n")

        # Get basic info
        name = self.get_input("Topic name: ")
        if not name:
            print("Cancelled.")
            return

        description = self.get_input("Brief description: ")

        # Get optional introduction
        print("\nEnter an introduction (press Enter twice to finish):")
        intro_lines: list[str] = []
        while True:
            line = self.get_input("")
            if not line:
                break
            intro_lines.append(line)
        introduction = "\n".join(intro_lines) if intro_lines else None

        # Get fun facts
        print("\nEnter some fun facts (one per line, empty line to finish):")
        fun_facts: list[str] = []
        while True:
            fact = self.get_input(f"Fact {len(fun_facts) + 1}: ")
            if not fact:
                break
            fun_facts.append(fact)

        # Create the context
        self.current_context = self.loader.create_custom_context(
            name=name,
            description=description,
            introduction=introduction,
            fun_facts=fun_facts,
        )

        print(self.color_text(f"\n✅ Created context: {name}", "green"))
        input("\nPress Enter to continue...")

    def show_main_menu(self) -> None:
        """Display the main menu and handle selection."""
        while True:
            self.clear_screen()
            self.print_banner(mini=True)

            print(self.color_text("Main Menu", "yellow"))
            print("=" * 40)

            # Show current context if loaded
            if self.current_context:
                print(
                    f"\n📚 Current: "
                    f"{self.color_text(self.current_context.name, 'green')}"
                )
                desc = self.current_context.description or ""
                short_desc = (desc[:47] + "...") if len(desc) > 50 else desc
                print(f"   {short_desc}")

            print("\n  [1] 📂 Load a Context")
            print("  [2] 📝 Create Custom Context")
            if self.current_context:
                print("  [3] 🚀 Start Exploring!")
                print("  [4] ℹ️  View Context Info")
            print("  [5] ⚙️  Settings")
            print("  [q] 👋 Exit")
            print()

            choice = self.get_input().lower()

            if choice == "1":
                self.show_context_loader()
            elif choice == "2":
                self.create_custom_context()
            elif choice == "3" and self.current_context:
                self.start_exploration()
            elif choice == "4" and self.current_context:
                self.show_context_info()
            elif choice == "5":
                self.show_settings()
            elif choice in ("q", "quit", "exit"):
                self.exit_app()
                break
            elif choice:
                # Invalid choice - show brief feedback
                print(self.color_text(f"\n  Invalid option: '{choice}'", "yellow"))
                input("  Press Enter to continue...")

    def show_context_loader(self) -> None:
        """Show the context loading menu."""
        self.clear_screen()
        print(self.color_text("\n📂 Load Learning Context\n", "cyan"))

        # List available contexts
        available = self.list_available_contexts()

        if available:
            print("Available contexts:")
            print("-" * 40)
            for i, ctx in enumerate(available, 1):
                print(f"  [{i}] {ctx}")
        else:
            print("No context files found in the data directory.")

        print("\n  [c] Enter custom file path")
        print("  [m] Back to main menu")
        print()

        choice = self.get_input().lower()

        if choice in ("m", "back", "q"):
            return
        elif choice == "c":
            filepath = self.get_input("Enter file path: ")
            if filepath:
                self.load_context(filepath)
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(available) and self.load_context(available[idx]):
                    context_name = (
                        self.current_context.name if self.current_context else "Unknown"
                    )
                    print(self.color_text(f"\n✅ Loaded: {context_name}", "green"))
            except ValueError:
                pass

        input("\nPress Enter to continue...")

    def show_context_info(self) -> None:
        """Display information about the current context."""
        self.clear_screen()
        print(self.color_text("\nℹ️  Context Information\n", "cyan"))

        if not self.current_context:
            print("No context loaded.")
            input("\nPress Enter to continue...")
            return

        ctx = self.current_context
        print(f"Name: {self.color_text(ctx.name, 'green')}")
        print(f"Description: {ctx.description}")
        print(f"Version: {ctx.version}")
        print(f"Author: {ctx.author}")
        print(f"Type: {ctx.topic_type}")
        print()
        print(f"📖 Learning Modules: {len(ctx.modules)}")
        for module in ctx.modules:
            print(f"   • {module.title} ({module.difficulty})")
        print()
        print(f"🎯 Challenges: {len(ctx.challenges)}")
        for challenge in ctx.challenges:
            print(f"   • {challenge.title}")
        print()
        print(f"💡 Fun Facts: {len(ctx.fun_facts)}")

        if ctx.source_path:
            print(f"\nSource: {ctx.source_path}")

        input("\nPress Enter to continue...")

    def start_exploration(self) -> None:
        """Start the interactive exploration session."""
        if not self.current_context:
            print(self.color_text("No context loaded!", "red"))
            input("\nPress Enter to continue...")
            return

        # Create and run the explorer
        self.explorer = InteractiveExplorer(
            context=self.current_context,
            use_colors=self.config.theme.use_colors,
        )
        self.explorer.run()

    def show_settings(self) -> None:
        """Show and modify settings."""
        while True:
            self.clear_screen()
            print(self.color_text("\n⚙️  Settings\n", "cyan"))

            print(
                f"  [1] Colors: "
                f"{'✅ Enabled' if self.config.theme.use_colors else '❌ Disabled'}"
            )
            print(
                f"  [2] Emoji: "
                f"{'✅ Enabled' if self.config.theme.use_emoji else '❌ Disabled'}"
            )
            print(
                f"  [3] Show Hints: "
                f"{'✅ Yes' if self.config.exploration.show_hints else '❌ No'}"
            )
            print(f"  [4] Default Context: {self.config.default_context_file}")
            print("  [5] Reset to Defaults")
            print("\n  [s] Save Settings")
            print("  [m] Back to Main Menu")
            print()

            choice = self.get_input().lower()

            if choice == "1":
                self.config.theme.use_colors = not self.config.theme.use_colors
            elif choice == "2":
                self.config.theme.use_emoji = not self.config.theme.use_emoji
            elif choice == "3":
                self.config.exploration.show_hints = (
                    not self.config.exploration.show_hints
                )
            elif choice == "4":
                new_default = self.get_input("Enter default context filename: ")
                if new_default:
                    self.config.default_context_file = new_default
            elif choice == "5":
                self.config.reset_to_defaults()
                print(self.color_text("Settings reset to defaults.", "green"))
                input("\nPress Enter to continue...")
            elif choice == "s":
                if self.config.save():
                    print(self.color_text("Settings saved!", "green"))
                else:
                    print(self.color_text("Failed to save settings.", "red"))
                input("\nPress Enter to continue...")
            elif choice in ("m", "back", "q"):
                break

    def exit_app(self) -> None:
        """Exit the application."""
        self.clear_screen()
        print(self.color_text("\n👋 Thanks for using DataKit!", "cyan"))
        print("\nKeep learning, keep exploring! 🚀\n")

    def run(
        self,
        context_file: str | None = None,
        start_tour: bool = False,
        start_explore: bool = False,
    ) -> None:
        """
        Run the DataKit application.

        Args:
            context_file: Optional context file to load at startup
            start_tour: If True, starts guided tour directly
            start_explore: If True, starts exploration directly
        """
        # Load context if specified
        if context_file:
            if not self.load_context(context_file):
                print("Failed to load specified context.")
                return
        else:
            # Try to load default context
            self.load_default_context()

        # Direct mode: start tour or explore immediately
        if (start_tour or start_explore) and self.current_context:
            self.explorer = InteractiveExplorer(
                context=self.current_context,
                use_colors=self.config.theme.use_colors,
            )
            self.explorer.run()
        else:
            # Interactive mode: show main menu
            self.show_main_menu()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="DataKit - Interactive Learning System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python datakit.py                     # Start interactive mode
  python datakit.py -c mydata.json      # Load specific context
  python datakit.py --tour              # Start guided tour directly
  python datakit.py --list              # List available contexts
        """,
    )

    parser.add_argument(
        "-c",
        "--context",
        metavar="FILE",
        help="Load a specific context file",
    )

    parser.add_argument(
        "-t",
        "--tour",
        action="store_true",
        help="Start the guided tour directly",
    )

    parser.add_argument(
        "-e",
        "--explore",
        action="store_true",
        help="Start free exploration directly",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List available context files",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="DataKit 1.0.0",
    )

    parser.add_argument(
        "-s",
        "--spreadsheet",
        action="store_true",
        help="View the Control Plane (active flags)",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_arguments()

    # Create configuration
    config = get_config()

    if args.no_color:
        config.theme.use_colors = False

    # Create DataKit instance
    app = DataKit(config)

    # Handle list command
    if args.list:
        print("\nAvailable context files:")
        print("-" * 40)
        for ctx in app.list_available_contexts():
            print(f"  • {ctx}")
        print()
        print()
        return

    # Handle spreadsheet command
    if args.spreadsheet:
        app.control_plane.print_spreadsheet()
        return

    # Run the app
    app.run(
        context_file=args.context,
        start_tour=args.tour,
        start_explore=args.explore,
    )


if __name__ == "__main__":
    main()
