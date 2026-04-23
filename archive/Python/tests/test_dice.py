"""Unit tests for dice rolling module."""

import pytest

from src.dice import DiceRoller


class TestDiceRollerInitialization:
    """Test suite for DiceRoller initialization."""

    def test_dice_roller_creates_without_seed(self) -> None:
        """Test DiceRoller instantiation without seed."""
        roller = DiceRoller()
        assert roller is not None
        assert isinstance(roller, DiceRoller)

    def test_dice_roller_creates_with_seed(self) -> None:
        """Test DiceRoller instantiation with seed."""
        roller = DiceRoller(seed=42)
        assert roller is not None

    def test_dice_roller_constants(self) -> None:
        """Test that dice face constants are correctly defined."""
        assert DiceRoller.MIN_FACE == 1
        assert DiceRoller.MAX_FACE == 6


class TestSingleRoll:
    """Test suite for single die rolls."""

    def test_roll_returns_integer(self, dice_roller: DiceRoller) -> None:
        """Test that roll() returns an integer."""
        result = dice_roller.roll()
        assert isinstance(result, int)

    def test_roll_within_range(self, dice_roller: DiceRoller) -> None:
        """Test that roll() returns value between 1 and 6."""
        for _ in range(100):
            result = dice_roller.roll()
            assert 1 <= result <= 6

    def test_roll_reproducibility(self) -> None:
        """Test that seeded rolls are reproducible."""
        roller1 = DiceRoller(seed=12345)
        rolls1 = [roller1.roll() for _ in range(10)]

        roller2 = DiceRoller(seed=12345)
        rolls2 = [roller2.roll() for _ in range(10)]

        assert rolls1 == rolls2

    def test_roll_randomness_across_seeds(self) -> None:
        """Test that different seeds produce different sequences."""
        roller1 = DiceRoller(seed=1)
        roller2 = DiceRoller(seed=2)

        rolls1 = [roller1.roll() for _ in range(10)]
        rolls2 = [roller2.roll() for _ in range(10)]

        # Extremely unlikely to be identical with different seeds
        assert rolls1 != rolls2


class TestMultipleRolls:
    """Test suite for rolling multiple times."""

    def test_roll_multiple_returns_list(self, dice_roller: DiceRoller) -> None:
        """Test that roll_multiple() returns a list."""
        result = dice_roller.roll_multiple(5)
        assert isinstance(result, list)

    def test_roll_multiple_correct_count(self, dice_roller: DiceRoller) -> None:
        """Test that roll_multiple() returns correct number of rolls."""
        for count in [1, 5, 10, 100]:
            result = dice_roller.roll_multiple(count)
            assert len(result) == count

    def test_roll_multiple_all_valid(self, dice_roller: DiceRoller) -> None:
        """Test that all rolls in roll_multiple() are valid."""
        rolls = dice_roller.roll_multiple(50)
        assert all(1 <= roll <= 6 for roll in rolls)

    def test_roll_multiple_zero_raises_error(self, dice_roller: DiceRoller) -> None:
        """Test that roll_multiple(0) raises ValueError."""
        with pytest.raises(ValueError):
            dice_roller.roll_multiple(0)

    def test_roll_multiple_negative_raises_error(self, dice_roller: DiceRoller) -> None:
        """Test that roll_multiple with negative count raises ValueError."""
        with pytest.raises(ValueError):
            dice_roller.roll_multiple(-5)

    def test_roll_multiple_reproducibility(self) -> None:
        """Test that multiple rolls are reproducible with seed."""
        roller1 = DiceRoller(seed=999)
        rolls1 = roller1.roll_multiple(20)

        roller2 = DiceRoller(seed=999)
        rolls2 = roller2.roll_multiple(20)

        assert rolls1 == rolls2


class TestStatistics:
    """Test suite for statistics calculation."""

    def test_calculate_stats_returns_dict(self, sample_rolls: list) -> None:
        """Test that calculate_stats() returns a dictionary."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        assert isinstance(stats, dict)

    def test_calculate_stats_has_required_keys(self, sample_rolls: list) -> None:
        """Test that stats dict contains all required keys."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        required_keys = {"count", "min", "max", "sum", "mean"}
        assert required_keys.issubset(stats.keys())

    def test_calculate_stats_count(self, sample_rolls: list) -> None:
        """Test that count in stats is correct."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        assert stats["count"] == len(sample_rolls)

    def test_calculate_stats_min(self, sample_rolls: list) -> None:
        """Test that min in stats is correct."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        assert stats["min"] == min(sample_rolls)

    def test_calculate_stats_max(self, sample_rolls: list) -> None:
        """Test that max in stats is correct."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        assert stats["max"] == max(sample_rolls)

    def test_calculate_stats_sum(self, sample_rolls: list) -> None:
        """Test that sum in stats is correct."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        assert stats["sum"] == sum(sample_rolls)

    def test_calculate_stats_mean(self, sample_rolls: list) -> None:
        """Test that mean in stats is calculated correctly."""
        stats = DiceRoller.calculate_stats(sample_rolls)
        expected_mean = sum(sample_rolls) / len(sample_rolls)
        assert stats["mean"] == expected_mean

    def test_calculate_stats_empty_list_raises_error(self) -> None:
        """Test that calculate_stats() on empty list raises ValueError."""
        with pytest.raises(ValueError):
            DiceRoller.calculate_stats([])

    def test_calculate_stats_single_value(self) -> None:
        """Test statistics with single roll."""
        rolls = [4]
        stats = DiceRoller.calculate_stats(rolls)
        assert stats["count"] == 1
        assert stats["min"] == 4
        assert stats["max"] == 4
        assert stats["sum"] == 4
        assert stats["mean"] == 4.0

    def test_calculate_stats_all_same(self) -> None:
        """Test statistics with all identical rolls."""
        rolls = [3, 3, 3, 3, 3]
        stats = DiceRoller.calculate_stats(rolls)
        assert stats["min"] == 3
        assert stats["max"] == 3
        assert stats["mean"] == 3.0

    def test_calculate_stats_extremes(self) -> None:
        """Test statistics with extreme values (all 1s and 6s)."""
        rolls = [1, 1, 6, 6]
        stats = DiceRoller.calculate_stats(rolls)
        assert stats["min"] == 1
        assert stats["max"] == 6
        assert stats["sum"] == 14
        assert stats["mean"] == 3.5


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_roll_and_calculate_stats(self, seeded_roller: DiceRoller) -> None:
        """Test rolling multiple dice and calculating statistics."""
        rolls = seeded_roller.roll_multiple(10)
        stats = DiceRoller.calculate_stats(rolls)

        # Verify stats are coherent with rolls
        assert stats["count"] == len(rolls)
        assert stats["min"] == min(rolls)
        assert stats["max"] == max(rolls)
        assert stats["sum"] == sum(rolls)

    def test_multiple_roll_sessions(self) -> None:
        """Test that roll sessions continue sequentially with same seed."""
        import random

        # Reset random for consistent behavior
        random.seed(100)
        roller1 = DiceRoller(seed=100)
        rolls1_session1 = roller1.roll_multiple(5)
        rolls1_session2 = roller1.roll_multiple(5)

        # Create fresh roller with same seed
        random.seed(100)
        roller2 = DiceRoller(seed=100)
        rolls2_session1 = roller2.roll_multiple(5)
        rolls2_session2 = roller2.roll_multiple(5)

        # Verify both sessions match
        assert rolls1_session1 == rolls2_session1
        assert rolls1_session2 == rolls2_session2
