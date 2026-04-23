#!/usr/bin/env python3
"""
sora_integration.py - End-to-end Sora video generation workflow.

Complete pipeline: Repo → Concepts → Metaphors → Prompt → Video

Usage:
    python sora_integration.py --repo-path e:/projects/python/hello --budget low --dry-run
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional

from sora_client import (
    AspectRatio,
    SoraClient,
    VideoGenerationRequest,
)
from sora_prompt_generator import (
    PromptOptimizer,
    SoraPromptGenerator,
    TokenBudgetLevel,
)

logger = logging.getLogger(__name__)


class SoraWorkflow:
    """Complete video generation workflow orchestrator."""

    def __init__(
        self,
        repo_path: Path,
        api_key: Optional[str] = None,
        budget_level: TokenBudgetLevel = TokenBudgetLevel.LOW,
        monthly_budget_usd: float = 50.0,
    ):
        """Initialize workflow.

        Args:
            repo_path: Repository to extract concepts from.
            api_key: Sora API key (if None, uses SORA_API_KEY env var).
            budget_level: Token budget for prompt compression.
            monthly_budget_usd: Monthly spending limit.
        """
        self.repo_path = Path(repo_path)
        self.budget_level = budget_level
        self.monthly_budget_usd = monthly_budget_usd

        # Initialize Sora client
        if api_key:
            self.client = SoraClient(
                api_key=api_key,
                monthly_budget_usd=monthly_budget_usd,
            )
        else:
            try:
                self.client = self._create_client_from_env()
            except ValueError as e:
                logger.error("Cannot initialize Sora client: %s", str(e))
                raise

        self.prompt: Optional[str] = None
        self.video_id: Optional[str] = None

    @staticmethod
    def _create_client_from_env() -> SoraClient:
        """Create client from environment variables."""
        import os

        api_key = os.getenv("SORA_API_KEY")
        if not api_key:
            raise ValueError(
                "SORA_API_KEY not set. Set environment variable or pass --api-key"
            )

        budget = float(os.getenv("SORA_BUDGET_USD", "50"))
        return SoraClient(api_key=api_key, monthly_budget_usd=budget)

    def step_1_extract_and_generate_prompt(self) -> str:
        """Step 1: Analyze repo and generate optimized prompt.

        Returns:
            Generated prompt text.
        """
        logger.info("=" * 70)
        logger.info("STEP 1: Repository Analysis & Prompt Generation")
        logger.info("=" * 70)

        generator = SoraPromptGenerator(
            repo_path=self.repo_path,
            budget=self.budget_level,
        )

        self.prompt = generator.generate()

        # Calculate token count
        tokens = PromptOptimizer.estimate_tokens(self.prompt)
        logger.info("Generated prompt: %d tokens (budget: %d)", 
                    tokens, self.budget_level.value)

        # Print prompt (first 500 chars)
        print("\n" + "-" * 70)
        print("GENERATED PROMPT (first 500 chars):")
        print("-" * 70)
        print(self.prompt[:500])
        print("...\n")

        return self.prompt

    def step_2_cost_validation(self) -> bool:
        """Step 2: Validate cost is within budget.

        Returns:
            True if cost is acceptable.
        """
        logger.info("=" * 70)
        logger.info("STEP 2: Cost Validation")
        logger.info("=" * 70)

        request = VideoGenerationRequest(
            prompt=self.prompt or "",
            duration=90.0,
            aspect_ratio=AspectRatio.WIDESCREEN,
            quality="high",
        )

        estimated = request.estimate_cost_usd()
        logger.info("Estimated video cost: $%.2f", estimated)

        within_budget = self.client.check_budget(estimated)

        if within_budget:
            logger.info("✓ Cost validation: PASSED")
            return True
        else:
            logger.error("✗ Cost validation: FAILED - exceeds budget")
            return False

    def step_3_generate_video_dry_run(self) -> bool:
        """Step 3: Dry run (estimate only, no API calls).

        Returns:
            True if ready to proceed.
        """
        logger.info("=" * 70)
        logger.info("STEP 3: Dry Run (No API Calls)")
        logger.info("=" * 70)

        if not self.prompt:
            logger.error("No prompt generated. Run step_1 first.")
            return False

        request = VideoGenerationRequest(
            prompt=self.prompt,
            duration=90.0,
            aspect_ratio=AspectRatio.WIDESCREEN,
            quality="high",
        )

        response = self.client.generate_video(request, dry_run=True)

        logger.info("Dry run simulation:")
        logger.info("  Video ID: %s", response.video_id)
        logger.info("  Status: %s", response.status)
        logger.info("  Duration: %.0fs", response.duration)

        return response.status == "dry_run_estimated"

    def step_4_generate_video_real(self) -> str:
        """Step 4: Generate video (real API call).

        Returns:
            Video ID for status polling.

        Raises:
            ValueError: If cost exceeds budget.
            RuntimeError: If API call fails.
        """
        logger.info("=" * 70)
        logger.info("STEP 4: Video Generation (Real API Call)")
        logger.info("=" * 70)

        if not self.prompt:
            raise ValueError("No prompt generated. Run step_1 first.")

        request = VideoGenerationRequest(
            prompt=self.prompt,
            duration=90.0,
            aspect_ratio=AspectRatio.WIDESCREEN,
            quality="high",
        )

        response = self.client.generate_video(request, dry_run=False)
        self.video_id = response.video_id

        logger.info("✓ Video generation started")
        logger.info("  Video ID: %s", response.video_id)
        logger.info("  Status: %s", response.status)
        logger.info("  Created: %s", response.created_at)

        return self.video_id

    def step_5_poll_status(self, max_wait_seconds: int = 600) -> bool:
        """Step 5: Poll for video generation completion.

        Args:
            max_wait_seconds: Maximum time to wait (default 10 min).

        Returns:
            True if completed successfully.
        """
        logger.info("=" * 70)
        logger.info("STEP 5: Polling for Video Completion")
        logger.info("=" * 70)

        if not self.video_id:
            raise ValueError("No video ID. Run step_4 first.")

        start_time = time.time()
        poll_interval = 5  # Start with 5 second intervals

        while True:
            elapsed = time.time() - start_time

            response = self.client.get_video_status(str(self.video_id))

            logger.info(
                "[%ds] Status: %s",
                int(elapsed),
                response.status,
            )

            if response.status == "completed":
                logger.info("✓ Video completed successfully")
                logger.info("  URL: %s", response.video_url)
                return True

            if response.status == "failed":
                logger.error("✗ Video generation failed")
                logger.error("  Error: %s", response.error_message)
                return False

            if elapsed > max_wait_seconds:
                logger.error("✗ Timeout waiting for video (max %ds)", max_wait_seconds)
                return False

            time.sleep(poll_interval)

            # Increase poll interval as time goes on
            if elapsed > 60:
                poll_interval = 10
            if elapsed > 300:
                poll_interval = 30

    def step_6_show_summary(self) -> None:
        """Step 6: Show budget and performance summary."""
        logger.info("=" * 70)
        logger.info("STEP 6: Summary & Budget Report")
        logger.info("=" * 70)

        summary = self.client.get_budget_summary()

        print("\n" + "-" * 70)
        print("BUDGET SUMMARY:")
        print("-" * 70)
        print(f"Total Budget:      ${summary['total_budget_usd']:.2f}/month")
        print(f"Total Spent:       ${summary['total_spent_usd']:.2f}")
        print(f"Remaining:         ${summary['remaining_usd']:.2f}")
        print(f"Budget Used:       {summary['budget_used_percent']:.1f}%")
        print(f"Videos Generated:  {summary['videos_generated']}")
        print("-" * 70)

        # Save report
        report_path = Path("sora_budget_report.txt")
        self.client.save_budget_report(report_path)
        logger.info("Budget report saved to: %s", report_path)

    def run_full_workflow(
        self,
        dry_run: bool = True,
        wait_for_completion: bool = True,
    ) -> Optional[str]:
        """Run complete workflow.

        Args:
            dry_run: If True, stop after dry run (don't actually generate).
            wait_for_completion: If True, poll until video is ready.

        Returns:
            Video URL on success, None on failure.
        """
        try:
            # Step 1: Generate prompt
            self.step_1_extract_and_generate_prompt()

            # Step 2: Validate cost
            if not self.step_2_cost_validation():
                return None

            # Step 3: Dry run
            if not self.step_3_generate_video_dry_run():
                return None

            # Optionally stop here for dry run
            if dry_run:
                logger.info("DRY RUN COMPLETE: Use --real to generate actual video")
                return None

            # Step 4: Generate video (real API call)
            self.step_4_generate_video_real()

            # Step 5: Poll for completion
            if wait_for_completion:
                if self.step_5_poll_status():
                    # Get final status
                    response = self.client.get_video_status(str(self.video_id))
                    return response.video_url
                else:
                    return None

            return self.video_id

        except (ValueError, RuntimeError) as e:
            logger.error("Workflow failed: %s", str(e))
            return None
        finally:
            # Always show summary
            self.step_6_show_summary()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Sora video from IDE Recorder repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (test prompt, no video generation)
  python sora_integration.py --repo-path e:/projects/python/hello --dry-run

  # Generate video (real API call)
  python sora_integration.py --repo-path e:/projects/python/hello --real

  # Ultra-low budget (compress aggressively)
  python sora_integration.py --repo-path e:/projects/python/hello --budget ultra-low --real

  # Set custom budget and API key
  python sora_integration.py \\
    --repo-path e:/projects/python/hello \\
    --api-key sk-... \\
    --monthly-budget 100 \\
    --real
        """,
    )

    parser.add_argument(
        "--repo-path",
        type=Path,
        default=Path("e:/projects/python/hello"),
        help="Path to repository (default: e:/projects/python/hello)",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="Sora API key (default: SORA_API_KEY env var)",
    )

    parser.add_argument(
        "--budget",
        choices=["ultra-low", "low", "medium", "standard"],
        default="low",
        help="Token budget level for prompt compression (default: low)",
    )

    parser.add_argument(
        "--monthly-budget",
        type=float,
        default=50.0,
        help="Monthly spending limit in USD (default: $50)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Estimate cost only, don't generate video (default: True)",
    )

    parser.add_argument(
        "--real",
        action="store_true",
        help="Generate actual video (real API call)",
    )

    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for video completion",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    # Convert budget string to enum
    budget_map = {
        "ultra-low": TokenBudgetLevel.ULTRA_LOW,
        "low": TokenBudgetLevel.LOW,
        "medium": TokenBudgetLevel.MEDIUM,
        "standard": TokenBudgetLevel.STANDARD,
    }
    budget_level = budget_map[args.budget]

    print("=" * 70)
    print("SORA VIDEO GENERATION WORKFLOW")
    print("=" * 70)
    print(f"Repository: {args.repo_path}")
    print(f"Budget Level: {args.budget}")
    print(f"Monthly Limit: ${args.monthly_budget:.2f}")
    print(f"Mode: {'DRY RUN (no video)' if args.dry_run and not args.real else 'REAL (generate video)'}")
    print("=" * 70)

    # Validate repo exists
    if not args.repo_path.exists():
        logger.error("Repository path not found: %s", args.repo_path)
        return 1

    # Create workflow
    try:
        workflow = SoraWorkflow(
            repo_path=args.repo_path,
            api_key=args.api_key,
            budget_level=budget_level,
            monthly_budget_usd=args.monthly_budget,
        )
    except ValueError as e:
        logger.error("Failed to initialize workflow: %s", str(e))
        return 1

    # Run workflow
    dry_run = not args.real
    wait_for_completion = not args.no_wait

    result = workflow.run_full_workflow(
        dry_run=dry_run,
        wait_for_completion=wait_for_completion,
    )

    if result:
        print(f"\n✓ SUCCESS: {result}")
        return 0
    else:
        print("\n✗ WORKFLOW FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
