"""Core dice rolling logic."""

import random
from typing import Dict, List, Optional

from src.logger import get_logger

logger = get_logger(__name__)


class DiceRoller:
    """Simulates rolling a standard six-sided die."""

    MIN_FACE = 1
    MAX_FACE = 6

    def __init__(self, seed: Optional[int] = None) -> None:
        """
        Initialize the dice roller.

        Args:
            seed: Optional seed for reproducible rolls
        """
        if seed is not None:
            random.seed(seed)
            logger.debug("Dice roller seeded with %s", seed)

    def roll(self) -> int:
        """
        Roll a single die (1-6).

        Returns:
            Integer between 1 and 6 (inclusive)
        """
        result = random.randint(self.MIN_FACE, self.MAX_FACE)
        logger.debug("Rolled: %s", result)
        return result

    def roll_multiple(self, count: int) -> List[int]:
        """
        Roll the die multiple times.

        Args:
            count: Number of rolls to perform

        Returns:
            List of roll results

        Raises:
            ValueError: If count is negative or zero
        """
        if count <= 0:
            raise ValueError("Roll count must be a positive integer")

        rolls = [self.roll() for _ in range(count)]
        logger.info("Performed %s rolls: %s", count, rolls)
        return rolls

    @staticmethod
    def calculate_stats(rolls: List[int]) -> Dict[str, float]:
        """
        Calculate statistics for a list of rolls.

        Args:
            rolls: List of roll results

        Returns:
            Dictionary with min, max, mean, sum statistics

        Raises:
            ValueError: If rolls list is empty
        """
        if not rolls:
            raise ValueError("Cannot calculate stats for empty roll list")

        stats: Dict[str, float] = {
            "count": float(len(rolls)),
            "min": float(min(rolls)),
            "max": float(max(rolls)),
            "sum": float(sum(rolls)),
            "mean": sum(rolls) / len(rolls),
        }

        logger.debug("Statistics calculated: %s", stats)
        return stats
