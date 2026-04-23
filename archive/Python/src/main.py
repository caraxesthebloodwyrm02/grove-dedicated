"""CLI entry point for hello-app."""

import argparse
import sys

from src.dice import DiceRoller
from src.logger import setup_logger


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    logger = setup_logger(__name__)

    parser = argparse.ArgumentParser(
        description="Enterprise-grade dice rolling application.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m src.main                  # Roll once\n"
            "  python -m src.main --rolls 10       # Roll 10 times\n"
            "  python -m src.main --seed 42 --rolls 5"
            "  # Reproducible rolls\n"
        ),
    )

    parser.add_argument(
        "--rolls",
        type=int,
        default=1,
        help="Number of rolls to perform (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible results (optional)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug-level logging",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display statistics (min, max, mean) for rolls",
    )

    args = parser.parse_args()

    # Adjust logging level
    if args.verbose:
        logger.setLevel(1)  # DEBUG level

    logger.info("Starting hello-app dice roller")

    try:
        # Validate input
        if args.rolls < 1:
            logger.error("Roll count must be at least 1")
            return 1

        # Create roller and execute
        roller = DiceRoller(seed=args.seed)
        rolls = roller.roll_multiple(args.rolls)

        # Display results
        logger.info("Rolls: %s", rolls)

        if args.stats:
            stats = DiceRoller.calculate_stats(rolls)
            logger.info(
                "Statistics - Count: %s, Min: %s, Max: %s, Sum: %s, Mean: %.2f",
                stats["count"],
                stats["min"],
                stats["max"],
                stats["sum"],
                stats["mean"],
            )

        logger.info("Completed successfully")
        return 0

    except ValueError as e:
        logger.error("Invalid input: %s", e)
        return 1
    except RuntimeError as e:
        logger.exception("Unexpected error: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
