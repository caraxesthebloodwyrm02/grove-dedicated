"""
Pytest fixtures and configuration.

This module provides shared test utilities and fixtures for the test suite.
"""

from typing import List

import pytest

from src.dice import DiceRoller


@pytest.fixture
def dice_roller() -> DiceRoller:
    """Provide a standard dice roller instance for tests."""
    return DiceRoller()


@pytest.fixture
def seeded_roller() -> DiceRoller:
    """Provide a deterministic dice roller with fixed seed."""
    return DiceRoller(seed=42)

@pytest.fixture
def sample_rolls() -> List[int]:
    """Provide sample roll data for statistics tests."""
    return [1, 2, 3, 4, 5, 6, 1, 2, 3]
