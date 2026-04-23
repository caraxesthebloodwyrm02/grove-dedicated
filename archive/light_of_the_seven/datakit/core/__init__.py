"""
DataKit Core Module
===================

This module provides the core functionality for the DataKit learning system,
including context loading, interactive exploration, and configuration management.
"""

from .config import DataKitConfig
from .explorer import InteractiveExplorer
from .loader import ContextLoader, DataKitContext

__all__ = [
    "ContextLoader",
    "DataKitContext",
    "InteractiveExplorer",
    "DataKitConfig",
]

__version__ = "1.0.0"
