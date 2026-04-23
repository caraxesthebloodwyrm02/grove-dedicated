"""
Interactive Explorer Module for DataKit Learning System.

This module provides an immersive, interactive learning experience
for exploring loaded contexts. It offers multiple exploration modes:
- Guided Tour: Step-by-step walkthrough
- Free Exploration: Open-ended discovery
- Challenge Mode: Test your knowledge
- Quick Facts: Random interesting tidbits

The explorer adapts to the loaded context and provides
a fun, engaging way to learn about any topic.
"""

import os
import random
import sys
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

from .loader import Challenge, Context, LearningModule
from .pack_schema import resolve_data_path


class ExplorationMode(Enum):
    """Available exploration modes."""

    GUIDED_TOUR = auto()
    FREE_EXPLORATION = auto()
    CHALLENGE_MODE = auto()
    QUICK_FACTS = auto()
    VISUALIZE = auto()


@dataclass
class ExplorationState:
    """Tracks the current state of exploration."""

    current_module_index: int = 0
    completed_modules: List[str] = field(default_factory=list)
    completed_challenges: List[str] = field(default_factory=list)
    score: int = 0
    facts_seen: int = 0
    session_start_time: float = field(default_factory=time.time)

    @property
    def session_duration_minutes(self) -> float:
        """Get the duration of the current session in minutes."""
        return (time.time() - self.session_start_time) / 60


class InteractiveExplorer:
    """
    Main class for interactive exploration of learning contexts.

    The InteractiveExplorer provides a rich, menu-driven interface
    for learning about any loaded topic/context.
    """

    # ANSI color codes for terminal output
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "underline": "\033[4m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }

    # Emoji icons for visual flair
    ICONS = {
        "book": "📚",
        "star": "⭐",
        "rocket": "🚀",
        "lightbulb": "💡",
        "target": "🎯",
        "trophy": "🏆",
        "music": "🎵",
        "sparkles": "✨",
        "check": "✅",
        "cross": "❌",
        "arrow_right": "➡️",
        "arrow_left": "⬅️",
        "question": "❓",
        "info": "ℹ️",
        "warning": "⚠️",
        "chart": "📊",
        "gear": "⚙️",
        "home": "🏠",
        "wave": "👋",
        "brain": "🧠",
        "fire": "🔥",
        "compass": "🧭",
    }

    def __init__(self, context: Optional[Context] = None, use_colors: bool = True):
        """
        Initialize the InteractiveExplorer.

        Args:
            context: The learning context to explore (can be set later)
            use_colors: Whether to use ANSI colors in output
        """
        self.context = context
        self.use_colors = use_colors and self._supports_color()
        self.state = ExplorationState()
        self._custom_handlers: Dict[str, Callable] = {}
        self._navigation_items: Dict[str, Dict[str, Any]] = {}
        self._running = False

    def _supports_color(self) -> bool:
        """Check if the terminal supports colors."""
        # Check for Windows without proper terminal
        if sys.platform == "win32":
            return os.environ.get("TERM") is not None or os.environ.get(
                "WT_SESSION"
            )  # Windows Terminal
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def _color(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.use_colors:
            return text
        color_code = self.COLORS.get(color, "")
        reset = self.COLORS["reset"]
        return f"{color_code}{text}{reset}"

    def _bold(self, text: str) -> str:
        """Make text bold."""
        return self._color(text, "bold")

    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def _print_header(self, title: str, subtitle: str = ""):
        """Print a formatted header."""
        width = 60
        print("\n" + "=" * width)
        print(
            self._color(
                f" {self.ICONS['sparkles']} {title} {self.ICONS['sparkles']}", "cyan"
            )
        )
        if subtitle:
            print(self._color(f"    {subtitle}", "dim"))
        print("=" * width + "\n")

    def _print_menu(self, options: List[Tuple[str, str]], title: str = "Options"):
        """
        Print a numbered menu.

        Args:
            options: List of (key, description) tuples
            title: Title for the menu
        """
        print(self._color(f"\n{title}:", "yellow"))
        print("-" * 40)
        for i, (key, description) in enumerate(options, 1):
            print(f"  [{self._color(str(i), 'green')}] {description}")
        print("-" * 40)

    def _get_input(self, prompt: str = "> ") -> str:
        """Get user input with a styled prompt."""
        try:
            return input(self._color(prompt, "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            return "q"

    def _pause(self, message: str = "Press Enter to continue..."):
        """Pause and wait for user input."""
        self._get_input(f"\n{message}")

    def _type_effect(self, text: str, delay: float = 0.02):
        """Print text with a typewriter effect."""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()

    def set_context(self, context: Context):
        """Set or change the current learning context."""
        self.context = context
        self.state = ExplorationState()  # Reset state for new context

    def register_handler(self, name: str, handler: Callable):
        """Register a custom handler for context-specific functionality."""
        self._custom_handlers[name] = handler

    def run(self):
        """
        Start the interactive exploration session.

        This is the main entry point for the explorer.
        """
        if not self.context:
            print(self._color("Error: No context loaded!", "red"))
            return

        self._running = True
        self._clear_screen()
        self._show_welcome()

        while self._running:
            self._show_main_menu()

    def stop(self):
        """Stop the exploration session."""
        self._running = False

    def _show_welcome(self):
        """Display the welcome screen with introduction."""
        self._print_header(
            f"Welcome to: {self.context.name}",
            self.context.description[:50] + "..."
            if len(self.context.description) > 50
            else self.context.description,
        )

        print(f"{self.ICONS['wave']} Hello, curious learner!\n")

        if self.context.introduction:
            print(self._color("Introduction:", "bold"))
            print(self.context.introduction)
            print()
        else:
            print(f"You're about to explore {self._bold(self.context.name)}.")
            print("This interactive journey will help you understand this topic")
            print("through multiple engaging learning modes.\n")

        # Show quick stats
        print(self._color("What's inside:", "yellow"))
        print(f"  {self.ICONS['book']} {len(self.context.modules)} Learning Modules")
        print(f"  {self.ICONS['target']} {len(self.context.challenges)} Challenges")
        print(f"  {self.ICONS['lightbulb']} {len(self.context.fun_facts)} Fun Facts")

        self._pause()

    def _show_main_menu(self):
        """Display the main exploration menu."""
        self._clear_screen()
        self._print_header(self.context.name, "Main Menu")

        # Show current progress
        if self.state.completed_modules:
            progress = (
                len(self.state.completed_modules)
                / max(len(self.context.modules), 1)
                * 100
            )
            print(
                f"{self.ICONS['chart']} Progress: {progress:.0f}% | Score: {self.state.score} pts"
            )
            print()

        options = [
            (
                "1",
                f"{self.ICONS['compass']} Guided Tour - Step-by-step learning journey",
            ),
            (
                "2",
                f"{self.ICONS['rocket']} Free Exploration - Explore at your own pace",
            ),
            ("3", f"{self.ICONS['target']} Challenge Mode - Test your knowledge"),
            (
                "4",
                f"{self.ICONS['lightbulb']} Quick Facts - Random interesting tidbits",
            ),
            ("5", f"{self.ICONS['chart']} Visualizations - Interactive visual tools"),
            ("6", f"{self.ICONS['info']} About This Topic - Detailed information"),
            ("7", f"{self.ICONS['gear']} Settings"),
            ("q", f"{self.ICONS['home']} Exit"),
        ]

        self._print_menu(options, "Choose your adventure")

        choice = self._get_input()

        if choice == "1":
            self._guided_tour()
        elif choice == "2":
            self._free_exploration()
        elif choice == "3":
            self._challenge_mode()
        elif choice == "4":
            self._quick_facts()
        elif choice == "5":
            self._visualizations()
        elif choice == "6":
            self._about_topic()
        elif choice == "7":
            self._settings()
        elif choice.lower() == "q":
            self._exit_session()

    def _guided_tour(self):
        """Run the guided tour mode."""
        self._clear_screen()
        self._print_header("Guided Tour", "Learn step by step")

        if not self.context.modules:
            print(
                f"{self.ICONS['warning']} No learning modules available for this topic."
            )
            self._pause()

            return

        current_idx = self.state.current_module_index

        while current_idx < len(self.context.modules):
            module = self.context.modules[current_idx]

            self._clear_screen()
            print(
                f"\n{self.ICONS['book']} Module {current_idx + 1}/{len(self.context.modules)}"
            )
            print("=" * 50)
            print(self._bold(module.title))
            print(f"Difficulty: {self._format_difficulty(module.difficulty)}")
            print(f"Estimated time: {module.duration_minutes} minutes")
            print("=" * 50)
            print()
            print(module.description)
            print()

            # Show content if available
            if module.content:
                print(self._color("Content:", "cyan"))
                print(module.content)
                print()

            # Show related data from context if applicable
            self._show_module_data(module)

            # Navigation
            print("\n" + "-" * 40)
            nav_options = []
            if current_idx > 0:
                nav_options.append(f"[p] Previous")
            nav_options.append("[n] Next")
            nav_options.append("[m] Main Menu")
            print(" | ".join(nav_options))

            choice = self._get_input()

            if choice.lower() == "n":
                if module.id not in self.state.completed_modules:
                    self.state.completed_modules.append(module.id)
                current_idx += 1
            elif choice.lower() == "p" and current_idx > 0:
                current_idx -= 1
            elif choice.lower() == "m":
                break

        self.state.current_module_index = min(
            current_idx, len(self.context.modules) - 1
        )

        if current_idx >= len(self.context.modules):
            self._show_tour_complete()

    def _show_module_data(self, module: LearningModule):
        """Show relevant data from the context for a module."""
        # This can be customized based on context type
        if self.context.topic_type == "music_theory_computational":
            self._show_music_module_data(module)
        elif module.id in self._custom_handlers:
            self._custom_handlers[module.id](self, module)

    def _show_music_module_data(self, module: LearningModule):
        """Show music-specific module data."""
        data = self.context.data

        if module.id == "fsm" and "computational_models" in data:
            fsm = data["computational_models"].get("finite_state_machine", {})
            if fsm:
                print(self._color("\n🔧 FSM Properties:", "yellow"))
                props = fsm.get("properties", {})
                for key, value in props.items():
                    print(f"   • {key}: {value}")

        elif module.id == "boolean" and "computational_models" in data:
            boolean = data["computational_models"].get("boolean_algebra", {})
            if boolean:
                encoding = boolean.get("encoding", {})
                print(self._color("\n💾 Binary Encoding (first 6 keys):", "yellow"))
                for i, (key, binary) in enumerate(encoding.items()):
                    if i >= 6:
                        break
                    print(f"   {key} = {binary}")

        elif module.id == "hands_on" and "common_progressions" in data:
            print(self._color("\n🎹 Try these common progressions:", "yellow"))
            for name, prog in list(data["common_progressions"].items())[:3]:
                example = prog.get("example_in_C", [])
                print(f"   {name}: {' → '.join(example)}")

    def _show_tour_complete(self):
        """Show completion message for guided tour."""
        self._clear_screen()
        self._print_header("Tour Complete!", "Congratulations!")

        print(f"{self.ICONS['trophy']} Amazing! You've completed the guided tour!")
        print()
        print(f"Modules completed: {len(self.state.completed_modules)}")
        print(f"Time spent: {self.state.session_duration_minutes:.1f} minutes")
        print()
        print("What would you like to do next?")
        print("  [1] Try Challenge Mode")
        print("  [2] Free Exploration")
        print("  [m] Main Menu")

        choice = self._get_input()
        if choice == "1":
            self._challenge_mode()
        elif choice == "2":
            self._free_exploration()

    def _free_exploration(self):
        """Run free exploration mode."""
        self._clear_screen()
        self._print_header("Free Exploration", "Discover at your own pace")

        if not self.context.data:
            print(f"{self.ICONS['warning']} Limited data available for exploration.")
            self._pause()
            return

        # Build exploration options from context data
        explorable_items = self._get_explorable_items()

        while True:
            self._clear_screen()
            print(f"\n{self.ICONS['compass']} What would you like to explore?\n")

            for i, (key, description) in enumerate(explorable_items, 1):
                print(f"  [{i}] {description}")
            print(f"  [m] Back to Main Menu")

            choice = self._get_input()

            if choice.lower() == "m":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(explorable_items):
                    key, _ = explorable_items[idx]
                    self._explore_item(key)
            except ValueError:
                pass

    def _render_generic_view(self, view: Dict[str, Any]) -> None:
        if not self.context:
            return

        pack = self.context.data
        vtype = view.get("type")
        title = view.get("title")
        if not isinstance(title, str) or not title:
            title = "View"

        source = view.get("source", "$")
        if not isinstance(source, str) or not source:
            source = "$"

        ok, resolved = resolve_data_path(pack, source)
        if not ok:
            self._clear_screen()
            self._print_header(title, "Invalid source")
            print(f"{self.ICONS['warning']} Invalid source path: {source}")
            self._pause()
            return

        if vtype == "tree":
            self._view_tree(resolved, title)
        elif vtype == "table":
            columns = view.get("columns")
            if not (
                isinstance(columns, list) and columns and all(isinstance(c, str) for c in columns)
            ):
                columns = None

            max_rows = view.get("max_rows")
            if not isinstance(max_rows, int) or max_rows <= 0:
                max_rows = 20

            self._view_table(resolved, title, columns, max_rows)
        else:
            self._clear_screen()
            self._print_header(title)
            print(f"{self.ICONS['warning']} Unknown view type: {vtype}")
            self._pause()

    def _summarize_node(self, node: Any) -> str:
        if isinstance(node, dict):
            return f"(object {len(node)})"
        if isinstance(node, list):
            return f"(list {len(node)})"
        if node is None:
            return "= null"
        if isinstance(node, bool):
            return f"= {str(node).lower()}"
        if isinstance(node, (int, float)):
            return f"= {node}"
        if isinstance(node, str):
            s = node.replace("\n", " ").strip()
            if len(s) > 60:
                s = s[:57] + "..."
            return f"= {s}"
        s = str(node)
        if len(s) > 60:
            s = s[:57] + "..."
        return f"= {s}"

    def _view_tree(self, root: Any, title: str) -> None:
        stack: List[Tuple[str, Any]] = [("$", root)]
        max_items = 30

        while True:
            path, node = stack[-1]
            self._clear_screen()
            self._print_header(title, path)

            if isinstance(node, dict):
                keys = list(node.keys())
                if not keys:
                    print("(empty object)")
                else:
                    shown = keys[:max_items]
                    for i, k in enumerate(shown, 1):
                        summary = self._summarize_node(node.get(k))
                        print(f"  [{i}] {k} {summary}")
                    if len(keys) > max_items:
                        print(f"\n{self.ICONS['info']} Showing {max_items}/{len(keys)} items")

                print("\n  [u] Up  |  [m] Back")
                choice = self._get_input()
                if choice.lower() == "m":
                    return
                if choice.lower() == "u":
                    if len(stack) > 1:
                        stack.pop()
                    continue

                try:
                    idx = int(choice) - 1
                except ValueError:
                    continue

                if 0 <= idx < min(len(keys), max_items):
                    k = keys[idx]
                    stack.append((f"{path}.{k}", node.get(k)))

            elif isinstance(node, list):
                if not node:
                    print("(empty list)")
                else:
                    shown = node[:max_items]
                    for i, item in enumerate(shown, 1):
                        summary = self._summarize_node(item)
                        print(f"  [{i}] [{i - 1}] {summary}")
                    if len(node) > max_items:
                        print(f"\n{self.ICONS['info']} Showing {max_items}/{len(node)} items")

                print("\n  [u] Up  |  [m] Back")
                choice = self._get_input()
                if choice.lower() == "m":
                    return
                if choice.lower() == "u":
                    if len(stack) > 1:
                        stack.pop()
                    continue

                try:
                    idx = int(choice) - 1
                except ValueError:
                    continue

                if 0 <= idx < min(len(node), max_items):
                    stack.append((f"{path}[{idx}]", node[idx]))

            else:
                if isinstance(node, str):
                    print(node)
                else:
                    print(repr(node))

                print("\n  [u] Up  |  [m] Back")
                choice = self._get_input()
                if choice.lower() == "m":
                    return
                if choice.lower() == "u":
                    if len(stack) > 1:
                        stack.pop()

    def _format_table_cell(self, value: Any, width: int) -> str:
        if value is None:
            s = ""
        elif isinstance(value, bool):
            s = str(value).lower()
        elif isinstance(value, (int, float)):
            s = str(value)
        elif isinstance(value, str):
            s = value.replace("\n", " ")
        else:
            s = str(value)

        s = s.strip()
        if len(s) > width:
            if width <= 3:
                return s[:width]
            return s[: width - 3] + "..."
        return s

    def _view_table(
        self,
        root: Any,
        title: str,
        columns: Optional[List[str]],
        max_rows: int,
    ) -> None:
        if isinstance(root, list):
            raw_rows: List[Any] = root
        elif isinstance(root, dict):
            raw_rows = [{"key": k, "value": v} for k, v in root.items()]
        else:
            self._clear_screen()
            self._print_header(title)
            print(f"{self.ICONS['warning']} Table view source must be a list or object")
            self._pause()
            return

        while True:
            display_rows = raw_rows[: max_rows or 20]
            normalized: List[Dict[str, Any]] = []
            for r in display_rows:
                if isinstance(r, dict):
                    normalized.append(r)
                else:
                    normalized.append({"value": r})

            self._clear_screen()
            self._print_header(title)

            if not normalized:
                print("(no rows)")
                self._pause()
                return

            cols: List[str]
            if columns is None:
                cols = list(normalized[0].keys())
            else:
                cols = list(columns)

            max_width = 28
            widths: Dict[str, int] = {}
            for c in cols:
                w = len(c)
                for row in normalized:
                    cell = self._format_table_cell(row.get(c, ""), max_width)
                    w = max(w, len(cell))
                widths[c] = min(w, max_width)

            header = " | ".join(c.ljust(widths[c]) for c in cols)
            sep = "-+-".join("-" * widths[c] for c in cols)
            print("    " + header)
            print("    " + sep)
            for i, row in enumerate(normalized, 1):
                line = " | ".join(
                    self._format_table_cell(row.get(c, ""), widths[c]).ljust(widths[c])
                    for c in cols
                )
                print(f"{i:>3} {line}")

            if len(raw_rows) > len(display_rows):
                print(f"\n{self.ICONS['info']} Showing {len(display_rows)}/{len(raw_rows)} rows")

            print("\n  [#] Open row  |  [m] Back")
            choice = self._get_input()
            if choice.lower() == "m":
                return

            try:
                idx = int(choice) - 1
            except ValueError:
                continue

            if 0 <= idx < len(display_rows):
                self._view_tree(display_rows[idx], f"{title} (Row {idx + 1})")

    def _get_explorable_items(self) -> List[Tuple[str, str]]:
        """Get a list of explorable items from the context."""
        items: List[Tuple[str, str]] = []
        data = self.context.data
        self._navigation_items = {}

        navigation = data.get("navigation") if isinstance(data, dict) else None
        if isinstance(navigation, dict):
            free = navigation.get("free_exploration")
            if isinstance(free, list) and free:
                for i, item in enumerate(free, 1):
                    if not isinstance(item, dict):
                        continue
                    label = item.get("label")
                    if not isinstance(label, str) or not label:
                        label = f"Item {i}"
                    key = f"nav_{i}"
                    self._navigation_items[key] = item
                    items.append((key, label))

                items.append(("__pack_tree__", f"{self.ICONS['info']} Browse Pack Data"))
                return items

        # Add standard items based on data structure
        if "keys" in data:
            items.append(("keys", f"{self.ICONS['music']} Musical Keys"))
        if "relationships" in data:
            items.append(
                ("relationships", f"{self.ICONS['arrow_right']} Key Relationships")
            )
        if "common_progressions" in data:
            items.append(("progressions", f"{self.ICONS['music']} Common Progressions"))
        if "computational_models" in data:
            items.append(("models", f"{self.ICONS['brain']} Computational Models"))
        if "key_signatures" in data:
            items.append(("signatures", f"{self.ICONS['star']} Key Signatures"))
        if "intervals" in data:
            items.append(("intervals", f"{self.ICONS['chart']} Intervals"))

        items.append(("__pack_tree__", f"{self.ICONS['info']} Browse Pack Data"))

        return items

    def _explore_item(self, key: str):
        """Explore a specific item from the context."""
        self._clear_screen()
        data = self.context.data

        if key in self._navigation_items:
            nav_item = self._navigation_items[key]
            label = nav_item.get("label")
            if not isinstance(label, str) or not label:
                label = "View"

            view_spec: Any = None
            view_id = nav_item.get("view_id")
            if isinstance(view_id, str) and view_id:
                views = data.get("views")
                if isinstance(views, list):
                    for v in views:
                        if isinstance(v, dict) and v.get("id") == view_id:
                            view_spec = v
                            break

            if view_spec is None:
                view_inline = nav_item.get("view")
                if isinstance(view_inline, dict):
                    view_spec = view_inline

            if not isinstance(view_spec, dict):
                print(f"{self.ICONS['warning']} Invalid navigation item: missing view")
                self._pause()
                return

            view_copy = dict(view_spec)
            if not isinstance(view_copy.get("title"), str) or not view_copy.get("title"):
                view_copy["title"] = label

            self._render_generic_view(view_copy)
            return

        if key == "__pack_tree__":
            self._render_generic_view({"type": "tree", "title": "Pack Data", "source": "$"})
            return

        if key == "keys":
            keys = data.get("keys", [])
            print(f"\n{self.ICONS['music']} The 12 Keys of the Circle:\n")
            print("  " + " → ".join(keys))
            print("\n  (Arranged clockwise by perfect fifths)")

        elif key == "relationships":
            relationships = data.get("relationships", {})
            print(f"\n{self.ICONS['arrow_right']} Key Relationships:\n")
            print("  Each key connects to its neighbors by perfect fifth/fourth:\n")
            for k, neighbors in list(relationships.items())[:6]:
                print(f"  {k}: → {neighbors[0]} (fifth) | → {neighbors[1]} (fourth)")

        elif key == "progressions":
            progressions = data.get("common_progressions", {})
            print(f"\n{self.ICONS['music']} Common Chord Progressions:\n")
            for name, prog in progressions.items():
                print(f"  {self._bold(name)}")
                print(f"    {prog.get('description', '')}")
                example = prog.get("example_in_C", [])
                print(f"    Example: {' → '.join(example)}")
                genres = prog.get("genre", [])
                print(f"    Genres: {', '.join(genres)}")
                print()

        elif key == "models":
            models = data.get("computational_models", {})
            print(f"\n{self.ICONS['brain']} Computational Models:\n")
            for model_name, model_data in models.items():
                print(f"  {self._bold(model_name.replace('_', ' ').title())}")
                print(f"    {model_data.get('description', '')}")
                print()

        elif key == "signatures":
            signatures = data.get("key_signatures", {})
            print(f"\n{self.ICONS['star']} Key Signatures:\n")
            for k, sig in list(signatures.items())[:7]:
                sharps = sig.get("sharps", 0)
                flats = sig.get("flats", 0)
                acc = sig.get("accidentals", [])
                if sharps > 0:
                    print(f"  {k}: {sharps} sharp(s) - {', '.join(acc)}")
                elif flats > 0:
                    print(f"  {k}: {flats} flat(s) - {', '.join(acc)}")
                else:
                    print(f"  {k}: No sharps or flats")

        elif key == "intervals":
            intervals = data.get("intervals", {})
            print(f"\n{self.ICONS['chart']} Intervals:\n")
            for interval_name, interval_data in intervals.items():
                print(f"  {self._bold(interval_name.replace('_', ' ').title())}")
                print(f"    Semitones: {interval_data.get('semitones', 'N/A')}")
                print(f"    Direction: {interval_data.get('direction', 'N/A')}")
                print(f"    {interval_data.get('description', '')}")
                print()

        self._pause()

    def _challenge_mode(self):
        """Run challenge mode."""
        self._clear_screen()
        self._print_header("Challenge Mode", "Test your knowledge!")

        if not self.context.challenges:
            print(f"{self.ICONS['warning']} No challenges available for this topic.")
            print("\nBut here's a quick quiz based on the content!\n")
            self._quick_quiz()
            return

        print(f"Available challenges: {len(self.context.challenges)}\n")

        for i, challenge in enumerate(self.context.challenges, 1):
            status = (
                self.ICONS["check"]
                if challenge.id in self.state.completed_challenges
                else "  "
            )
            print(f"  [{i}] {status} {challenge.title}")
            print(
                f"      {self._format_difficulty(challenge.difficulty)} | {challenge.points} pts"
            )

        print(f"\n  [m] Back to Main Menu")

        choice = self._get_input()

        if choice.lower() != "m":
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.context.challenges):
                    self._run_challenge(self.context.challenges[idx])
            except ValueError:
                pass

    def _quick_quiz(self):
        """Generate a quick quiz from context data."""
        data = self.context.data
        questions = []

        # Generate questions based on available data
        if "keys" in data:
            keys = data["keys"]
            questions.append(
                {
                    "question": f"How many keys are in the Circle of Fifths?",
                    "answer": str(len(keys)),
                    "type": "number",
                }
            )

        if "common_progressions" in data:
            prog_name = list(data["common_progressions"].keys())[0]
            prog = data["common_progressions"][prog_name]
            questions.append(
                {
                    "question": f"The {prog_name} progression is common in which genres?",
                    "answer": ", ".join(prog.get("genre", [])),
                    "type": "info",
                }
            )

        if questions:
            q = random.choice(questions)
            print(f"{self.ICONS['question']} {q['question']}")
            user_answer = self._get_input("Your answer: ")
            print(f"\n{self.ICONS['info']} The answer is: {q['answer']}")

        self._pause()

    def _run_challenge(self, challenge: Challenge):
        """Run a specific challenge."""
        self._clear_screen()
        print(f"\n{self.ICONS['target']} Challenge: {challenge.title}\n")
        print(f"Type: {challenge.challenge_type}")
        print(f"Difficulty: {self._format_difficulty(challenge.difficulty)}")
        print(f"Points: {challenge.points}")
        print()
        print(challenge.description)
        print()

        # Placeholder for actual challenge logic
        # This would be customized based on challenge type and context
        print("This challenge will be implemented based on the topic specifics.")
        print("For now, mark as complete?")
        print("  [y] Yes, I've practiced this")
        print("  [n] Not yet")

        if self._get_input().lower() == "y":
            if challenge.id not in self.state.completed_challenges:
                self.state.completed_challenges.append(challenge.id)
                self.state.score += challenge.points
                print(f"\n{self.ICONS['trophy']} +{challenge.points} points!")

        self._pause()

    def _quick_facts(self):
        """Show random fun facts."""
        self._clear_screen()
        self._print_header("Quick Facts", "Did you know?")

        if not self.context.fun_facts:
            print(f"{self.ICONS['warning']} No fun facts available for this topic.")
            self._pause()
            return

        while True:
            fact = random.choice(self.context.fun_facts)
            self.state.facts_seen += 1

            print(f"\n{self.ICONS['lightbulb']} Fun Fact #{self.state.facts_seen}:\n")
            print(f"  {fact}")
            print()
            print("-" * 40)
            print("  [n] Another fact")
            print("  [m] Back to Main Menu")

            choice = self._get_input()
            if choice.lower() == "m":
                break

            self._clear_screen()
            self._print_header("Quick Facts", "Did you know?")

    def _visualizations(self):
        """Access visualization tools."""
        self._clear_screen()
        self._print_header("Visualizations", "See it to understand it")

        print("Available visualizations:\n")
        print(f"  [1] {self.ICONS['chart']} Static Circle Graph (matplotlib)")
        print(f"  [2] {self.ICONS['sparkles']} Interactive Circle (Plotly)")
        print(f"  [3] {self.ICONS['rocket']} D3.js Web Visualization")
        print(f"  [4] {self.ICONS['fire']} Animated Manim Visualization")
        print(f"\n  [m] Back to Main Menu")

        choice = self._get_input()

        if choice == "1":
            print("\nTo generate static visualization, run:")
            print("  python visualizations/static/circle_graph.py")
        elif choice == "2":
            print("\nTo generate interactive Plotly visualization, run:")
            print("  python visualizations/interactive/plotly_circle.py")
        elif choice == "3":
            print("\nOpen in browser:")
            print("  visualizations/interactive/d3_circle.html")
        elif choice == "4":
            print("\nTo render Manim animation, run:")
            print("  manim -pql visualizations/animated/manim_circle.py CircleOfFifths")

        if choice in ["1", "2", "3", "4"]:
            self._pause()

    def _about_topic(self):
        """Show detailed information about the topic."""
        self._clear_screen()
        self._print_header("About This Topic", "In-depth information")

        print(self.context.summary())
        print()

        if self.context.source_path:
            print(f"Source: {self.context.source_path}")

        print()
        print(f"Author: {self.context.author}")
        print(f"Version: {self.context.version}")
        print(f"Type: {self.context.topic_type}")

        self._pause()

    def _settings(self):
        """Show settings menu."""
        self._clear_screen()
        self._print_header("Settings", "Customize your experience")

        print(f"  [1] Colors: {'Enabled' if self.use_colors else 'Disabled'}")
        print(f"  [2] Reset Progress")
        print(f"\n  [m] Back to Main Menu")

        choice = self._get_input()

        if choice == "1":
            self.use_colors = not self.use_colors
            print(f"\nColors {'enabled' if self.use_colors else 'disabled'}.")
            self._pause()
        elif choice == "2":
            self.state = ExplorationState()
            print("\nProgress reset.")
            self._pause()

    def _exit_session(self):
        """Exit the exploration session."""
        self._clear_screen()
        print(f"\n{self.ICONS['wave']} Thanks for exploring {self.context.name}!\n")
        print(f"Session Summary:")
        print(f"  • Time spent: {self.state.session_duration_minutes:.1f} minutes")
        print(f"  • Modules completed: {len(self.state.completed_modules)}")
        print(f"  • Challenges completed: {len(self.state.completed_challenges)}")
        print(f"  • Facts learned: {self.state.facts_seen}")
        print(f"  • Total score: {self.state.score}")
        print()
        print("See you next time! Keep learning! 🚀")
        print()
        self._running = False

    def _format_difficulty(self, difficulty: str) -> str:
        """Format difficulty level with color."""
        colors = {
            "beginner": "green",
            "intermediate": "yellow",
            "advanced": "red",
        }
        color = colors.get(difficulty.lower(), "white")
        return self._color(difficulty.capitalize(), color)


# Convenience function for quick exploration
def explore(context: Context):
    """
    Quick function to start exploring a context.

    Args:
        context: The Context object to explore
    """
    explorer = InteractiveExplorer(context)
    explorer.run()
