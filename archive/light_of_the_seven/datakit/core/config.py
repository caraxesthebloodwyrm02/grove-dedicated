"""
Configuration Module for DataKit Learning System.

This module provides configuration management for the DataKit system,
including user preferences, theme settings, and system defaults.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ThemeConfig:
    """Configuration for visual themes."""

    name: str = "default"
    use_colors: bool = True
    use_emoji: bool = True
    primary_color: str = "cyan"
    secondary_color: str = "yellow"
    success_color: str = "green"
    error_color: str = "red"
    warning_color: str = "yellow"


@dataclass
class ExplorationConfig:
    """Configuration for exploration behavior."""

    auto_advance: bool = False
    show_hints: bool = True
    typewriter_effect: bool = False
    typewriter_speed: float = 0.02
    clear_screen_between_steps: bool = True
    confirm_exit: bool = True


@dataclass
class ProgressConfig:
    """Configuration for progress tracking."""

    track_progress: bool = True
    save_progress: bool = True
    progress_file: str = "progress.json"
    show_completion_percentage: bool = True
    celebrate_milestones: bool = True


@dataclass
class DataKitConfig:
    """
    Main configuration class for the DataKit Learning System.

    This class manages all configuration settings and provides
    methods for loading, saving, and modifying settings.
    """

    # Sub-configurations
    theme: ThemeConfig = field(default_factory=ThemeConfig)
    exploration: ExplorationConfig = field(default_factory=ExplorationConfig)
    progress: ProgressConfig = field(default_factory=ProgressConfig)

    # General settings
    default_data_directory: str = "data"
    default_context_file: str = "circle_of_fifths.json"
    language: str = "en"
    verbose_mode: bool = False
    debug_mode: bool = False

    # Session settings
    session_timeout_minutes: int = 60
    auto_save_interval_seconds: int = 300

    # Paths
    config_directory: Optional[str] = None
    _config_file_path: Optional[str] = field(default=None, repr=False)

    def __post_init__(self):
        """Initialize configuration after dataclass creation."""
        if self.config_directory is None:
            # Default to user's home directory
            self.config_directory = str(Path.home() / ".datakit")

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "DataKitConfig":
        """
        Load configuration from a JSON file.

        Args:
            config_path: Path to the configuration file.
                        If None, uses default location.

        Returns:
            A DataKitConfig instance with loaded settings.
        """
        if config_path is None:
            config_path = str(Path.home() / ".datakit" / "config.json")

        if not os.path.exists(config_path):
            # Return default configuration if file doesn't exist
            config = cls()
            config._config_file_path = config_path
            return config

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            config = cls._from_dict(data)
            config._config_file_path = config_path
            return config

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            config = cls()
            config._config_file_path = config_path
            return config

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "DataKitConfig":
        """Create a DataKitConfig from a dictionary."""
        # Parse nested configs
        theme_data = data.pop("theme", {})
        exploration_data = data.pop("exploration", {})
        progress_data = data.pop("progress", {})

        theme = ThemeConfig(**theme_data) if theme_data else ThemeConfig()
        exploration = (
            ExplorationConfig(**exploration_data)
            if exploration_data
            else ExplorationConfig()
        )
        progress = (
            ProgressConfig(**progress_data) if progress_data else ProgressConfig()
        )

        # Remove internal fields if present
        data.pop("_config_file_path", None)

        return cls(
            theme=theme,
            exploration=exploration,
            progress=progress,
            **data,
        )

    def save(self, config_path: Optional[str] = None) -> bool:
        """
        Save configuration to a JSON file.

        Args:
            config_path: Path to save the configuration.
                        If None, uses the path from which config was loaded.

        Returns:
            True if save was successful, False otherwise.
        """
        if config_path is None:
            config_path = self._config_file_path or str(
                Path.home() / ".datakit" / "config.json"
            )

        # Ensure directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        try:
            data = self.to_dict()
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True

        except IOError as e:
            print(f"Warning: Could not save config to {config_path}: {e}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to a dictionary."""
        data = asdict(self)
        # Remove internal fields
        data.pop("_config_file_path", None)
        return data

    def reset_to_defaults(self):
        """Reset all settings to their default values."""
        default = DataKitConfig()
        self.theme = default.theme
        self.exploration = default.exploration
        self.progress = default.progress
        self.default_data_directory = default.default_data_directory
        self.default_context_file = default.default_context_file
        self.language = default.language
        self.verbose_mode = default.verbose_mode
        self.debug_mode = default.debug_mode

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Supports dot notation for nested values (e.g., 'theme.use_colors').

        Args:
            key: The configuration key
            default: Default value if key is not found

        Returns:
            The configuration value or default
        """
        parts = key.split(".")
        value = self

        try:
            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                elif isinstance(value, dict):
                    value = value[part]
                else:
                    return default
            return value
        except (KeyError, AttributeError):
            return default

    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration value by key.

        Supports dot notation for nested values (e.g., 'theme.use_colors').

        Args:
            key: The configuration key
            value: The value to set

        Returns:
            True if successful, False otherwise
        """
        parts = key.split(".")

        if len(parts) == 1:
            if hasattr(self, key):
                setattr(self, key, value)
                return True
            return False

        # Navigate to the parent object
        obj = self
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return False

        # Set the final attribute
        final_key = parts[-1]
        if hasattr(obj, final_key):
            setattr(obj, final_key, value)
            return True

        return False

    def validate(self) -> List[str]:
        """
        Validate the configuration.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate theme
        valid_colors = [
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
        ]
        if self.theme.primary_color not in valid_colors:
            errors.append(f"Invalid primary_color: {self.theme.primary_color}")
        if self.theme.secondary_color not in valid_colors:
            errors.append(f"Invalid secondary_color: {self.theme.secondary_color}")

        # Validate exploration
        if self.exploration.typewriter_speed <= 0:
            errors.append("typewriter_speed must be positive")

        # Validate session settings
        if self.session_timeout_minutes <= 0:
            errors.append("session_timeout_minutes must be positive")
        if self.auto_save_interval_seconds <= 0:
            errors.append("auto_save_interval_seconds must be positive")

        return errors


# Predefined theme configurations
THEMES = {
    "default": ThemeConfig(),
    "dark": ThemeConfig(
        name="dark",
        primary_color="cyan",
        secondary_color="magenta",
    ),
    "light": ThemeConfig(
        name="light",
        primary_color="blue",
        secondary_color="green",
    ),
    "high_contrast": ThemeConfig(
        name="high_contrast",
        primary_color="white",
        secondary_color="yellow",
    ),
    "minimal": ThemeConfig(
        name="minimal",
        use_colors=False,
        use_emoji=False,
    ),
}


def get_theme(theme_name: str) -> ThemeConfig:
    """
    Get a predefined theme by name.

    Args:
        theme_name: Name of the theme

    Returns:
        ThemeConfig for the requested theme (default if not found)
    """
    return THEMES.get(theme_name, THEMES["default"])


# Global configuration instance
_global_config: Optional[DataKitConfig] = None


def get_config() -> DataKitConfig:
    """
    Get the global configuration instance.

    Creates a new instance with defaults if one doesn't exist.

    Returns:
        The global DataKitConfig instance
    """
    global _global_config
    if _global_config is None:
        _global_config = DataKitConfig.load()
    return _global_config


def set_config(config: DataKitConfig):
    """
    Set the global configuration instance.

    Args:
        config: The configuration to use globally
    """
    global _global_config
    _global_config = config


def reset_config():
    """Reset the global configuration to defaults."""
    global _global_config
    _global_config = DataKitConfig()
