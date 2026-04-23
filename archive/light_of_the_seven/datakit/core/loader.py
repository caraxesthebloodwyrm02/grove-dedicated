"""
Context Loader Module for DataKit Learning System.

This module provides functionality to load, parse, and manage different
learning contexts (topics/datasets) that can be explored interactively.

Supports:
- JSON data files
- YAML configuration
- Custom topic definitions
- Dynamic context switching
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

# Type alias for path-like arguments
PathLike = Union[str, Path]


@dataclass
class LearningModule:
    """Represents a single learning module within a context."""

    id: str
    title: str
    description: str
    duration_minutes: int = 10
    difficulty: str = "beginner"
    content: Optional[str] = None
    interactive: bool = False


@dataclass
class Challenge:
    """Represents an interactive challenge."""

    id: str
    title: str
    description: str
    challenge_type: str = "quiz"
    difficulty: str = "beginner"
    points: int = 10


@dataclass
class Context:
    """
    Represents a complete learning context/topic.

    A context contains all the data, modules, and metadata needed
    to provide an immersive learning experience on a specific topic.
    """

    name: str
    description: str
    version: str = "1.0.0"
    author: str = "DataKit"
    topic_type: str = "general"

    # Core data
    data: Dict[str, Any] = field(default_factory=dict)

    # Learning components
    modules: List[LearningModule] = field(default_factory=list)
    challenges: List[Challenge] = field(default_factory=list)
    fun_facts: List[str] = field(default_factory=list)

    # Custom introduction
    introduction: Optional[str] = None

    # Source file path
    source_path: Optional[str] = None

    def get_module(self, module_id: str) -> Optional[LearningModule]:
        """Get a specific learning module by ID."""
        for module in self.modules:
            if module.id == module_id:
                return module
        return None

    def get_challenge(self, challenge_id: str) -> Optional[Challenge]:
        """Get a specific challenge by ID."""
        for challenge in self.challenges:
            if challenge.id == challenge_id:
                return challenge
        return None

    def get_random_fact(self) -> Optional[str]:
        """Get a random fun fact."""
        if not self.fun_facts:
            return None
        import random

        return random.choice(self.fun_facts)

    def summary(self) -> str:
        """Get a summary of this context."""
        return (
            f"📚 {self.name}\n"
            f"   {self.description}\n"
            f"   📖 {len(self.modules)} learning modules\n"
            f"   🎯 {len(self.challenges)} challenges\n"
            f"   💡 {len(self.fun_facts)} fun facts\n"
            f"   🏷️  Type: {self.topic_type} | Version: {self.version}"
        )


class ContextLoader:
    """
    Loads and manages learning contexts from various sources.

    The ContextLoader is the primary interface for loading topic data
    and creating Context objects that can be explored interactively.
    """

    def __init__(self, data_directory: Optional[PathLike] = None):
        """
        Initialize the ContextLoader.

        Args:
            data_directory: Default directory to look for data files.
                           Accepts str or Path. If None, uses './data' relative to this file.
        """
        if data_directory is None:
            # Default to the data directory in the project
            self.data_directory = Path(__file__).parent.parent / "data"
        else:
            self.data_directory = Path(data_directory)

        self._loaded_contexts: Dict[str, Context] = {}
        self._custom_parsers: Dict[str, Callable] = {}

    def load_json(self, filepath: Union[str, Path]) -> Context:
        """
        Load a context from a JSON file.

        Args:
            filepath: Path to the JSON file (absolute or relative to data_directory)

        Returns:
            A Context object populated with the loaded data.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        # Resolve filepath
        path = Path(filepath)
        if not path.is_absolute():
            path = self.data_directory / path

        if not path.exists():
            raise FileNotFoundError(f"Context file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self._parse_context_data(data, str(path))

    def load_yaml(self, filepath: Union[str, Path]) -> Context:
        """
        Load a context from a YAML file.

        Args:
            filepath: Path to the YAML file

        Returns:
            A Context object populated with the loaded data.
        """
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "PyYAML is required for YAML support. Install with: pip install pyyaml"
            )

        path = Path(filepath)
        if not path.is_absolute():
            path = self.data_directory / path

        if not path.exists():
            raise FileNotFoundError(f"Context file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return self._parse_context_data(data, str(path))

    def load_from_dict(
        self, data: Dict[str, Any], name: str = "Custom Context"
    ) -> Context:
        """
        Create a context from a dictionary.

        Useful for creating contexts programmatically or from API responses.

        Args:
            data: Dictionary containing context data
            name: Name for the context if not specified in data

        Returns:
            A Context object.
        """
        if "metadata" not in data:
            data["metadata"] = {"name": name}
        return self._parse_context_data(data, None)

    def create_custom_context(
        self,
        name: str,
        description: str,
        introduction: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        modules: Optional[List[Dict[str, Any]]] = None,
        fun_facts: Optional[List[str]] = None,
        challenges: Optional[List[Dict[str, Any]]] = None,
    ) -> Context:
        """
        Create a custom context from individual components.

        This is the easiest way to create a new learning context
        without needing a pre-existing data file.

        Args:
            name: Name of the learning topic
            description: Brief description of the topic
            introduction: Custom introduction text
            data: Core data dictionary
            modules: List of learning module definitions
            fun_facts: List of interesting facts
            challenges: List of challenge definitions

        Returns:
            A fully configured Context object.
        """
        # Parse modules
        parsed_modules = []
        if modules:
            for m in modules:
                parsed_modules.append(
                    LearningModule(
                        id=m.get("id", f"module_{len(parsed_modules)}"),
                        title=m.get("title", "Untitled Module"),
                        description=m.get("description", ""),
                        duration_minutes=m.get("duration_minutes", 10),
                        difficulty=m.get("difficulty", "beginner"),
                        content=m.get("content"),
                        interactive=m.get("interactive", False),
                    )
                )

        # Parse challenges
        parsed_challenges = []
        if challenges:
            for c in challenges:
                parsed_challenges.append(
                    Challenge(
                        id=c.get("id", f"challenge_{len(parsed_challenges)}"),
                        title=c.get("title", "Untitled Challenge"),
                        description=c.get("description", ""),
                        challenge_type=c.get("type", "quiz"),
                        difficulty=c.get("difficulty", "beginner"),
                        points=c.get("points", 10),
                    )
                )

        return Context(
            name=name,
            description=description,
            introduction=introduction,
            data=data or {},
            modules=parsed_modules,
            challenges=parsed_challenges,
            fun_facts=fun_facts or [],
        )

    def _parse_context_data(
        self, data: Dict[str, Any], source_path: Optional[str]
    ) -> Context:
        """
        Parse raw data dictionary into a Context object.

        Args:
            data: Raw data dictionary
            source_path: Path to the source file (if any)

        Returns:
            A Context object.
        """
        # Extract metadata
        metadata = data.get("metadata", {})

        # Parse learning modules
        modules = []
        for m in data.get("learning_modules", []):
            modules.append(
                LearningModule(
                    id=m.get("id", f"module_{len(modules)}"),
                    title=m.get("title", "Untitled"),
                    description=m.get("description", ""),
                    duration_minutes=m.get("duration_minutes", 10),
                    difficulty=m.get("difficulty", "beginner"),
                    content=m.get("content"),
                    interactive=m.get("interactive", False),
                )
            )

        # Parse challenges
        challenges = []
        for c in data.get("challenges", []):
            challenges.append(
                Challenge(
                    id=c.get("id", f"challenge_{len(challenges)}"),
                    title=c.get("title", "Untitled"),
                    description=c.get("description", ""),
                    challenge_type=c.get("type", "quiz"),
                    difficulty=c.get("difficulty", "beginner"),
                    points=c.get("points", 10),
                )
            )

        # Create and return context
        context = Context(
            name=metadata.get("name", "Unknown Topic"),
            description=metadata.get("description", "No description available"),
            version=metadata.get("version", "1.0.0"),
            author=metadata.get("author", "Unknown"),
            topic_type=metadata.get("topic_type", "general"),
            data=data,
            modules=modules,
            challenges=challenges,
            fun_facts=data.get("fun_facts", []),
            source_path=source_path,
        )

        return context

    def list_available_contexts(self) -> List[str]:
        """
        List all available context files in the data directory.

        Returns:
            List of filenames (without path) that can be loaded.
        """
        if not self.data_directory.exists():
            return []

        contexts = []
        for ext in ["*.json", "*.yaml", "*.yml"]:
            contexts.extend([p.name for p in self.data_directory.glob(ext)])

        return sorted(contexts)

    def register_parser(self, extension: str, parser: Callable[[str], Dict[str, Any]]):
        """
        Register a custom parser for a file extension.

        Args:
            extension: File extension (e.g., '.xml')
            parser: Function that takes a file path and returns a dictionary
        """
        self._custom_parsers[extension.lower()] = parser

    def cache_context(self, key: str, context: Context):
        """Cache a loaded context for quick retrieval."""
        self._loaded_contexts[key] = context

    def get_cached_context(self, key: str) -> Optional[Context]:
        """Retrieve a cached context."""
        return self._loaded_contexts.get(key)

    def clear_cache(self):
        """Clear all cached contexts."""
        self._loaded_contexts.clear()


# Alias for backward compatibility
DataKitContext = Context


# Convenience function for quick loading
def load_context(filepath: str) -> Context:
    """
    Quick function to load a context from a file.

    Args:
        filepath: Path to the context file

    Returns:
        A Context object
    """
    loader = ContextLoader()

    if filepath.endswith(".json"):
        return loader.load_json(filepath)
    elif filepath.endswith((".yaml", ".yml")):
        return loader.load_yaml(filepath)
    else:
        # Try JSON by default
        return loader.load_json(filepath)


# Module-level default loader
_default_loader: Optional[ContextLoader] = None


def get_default_loader() -> ContextLoader:
    """Get or create the default ContextLoader instance."""
    global _default_loader
    if _default_loader is None:
        _default_loader = ContextLoader()
    return _default_loader
