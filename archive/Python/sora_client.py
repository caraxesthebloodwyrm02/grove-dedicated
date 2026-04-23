"""
sora_client.py - Sora 2 API client with cost optimization and budget tracking.

Provides a high-level client for generating videos with Sora 2, including:
- Authentication and token management
- Cost estimation before generation
- Budget tracking and limits
- Retry logic with exponential backoff
- Generation status polling

Cost Model (Sora 2):
  - Resolution varies by duration
  - Estimated: $0.02-0.05 per second
  - 90 seconds ≈ $1.80-$4.50 per video
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class AspectRatio(Enum):
    """Video aspect ratios supported by Sora."""

    WIDESCREEN = "16:9"
    SQUARE = "1:1"
    PORTRAIT = "9:16"


class VideoStyle(Enum):
    """Video style presets."""

    SILENT_FILM = "black_and_white_silent_film"
    CINEMATIC = "cinematic"
    DOCUMENTARY = "documentary"
    ANIMATED = "animated"
    REALISTIC = "realistic"


@dataclass
class VideoGenerationRequest:
    """Parameters for video generation."""

    prompt: str
    duration: float  # seconds (15-120)
    aspect_ratio: AspectRatio = AspectRatio.WIDESCREEN
    style: Optional[VideoStyle] = None
    quality: str = "high"  # "low", "medium", "high"

    def estimate_cost_usd(self) -> float:
        """Estimate cost based on duration and quality.

        Returns:
            Estimated cost in USD.
        """
        base_rate = {
            "low": 0.02,
            "medium": 0.03,
            "high": 0.05,
        }.get(self.quality, 0.03)

        return self.duration * base_rate


@dataclass
class VideoGenerationResponse:
    """Response from video generation request."""

    video_id: str
    status: str  # "pending", "processing", "completed", "failed"
    prompt: str
    duration: float
    created_at: str
    estimated_completion_time: Optional[float] = None
    video_url: Optional[str] = None
    error_message: Optional[str] = None


class SoraClient:
    """Client for Sora 2 API with cost optimization."""

    BASE_URL = "https://api.openai.com/v1/videos/generations"

    # Hard budget limit per month (prevent accidental spending)
    DEFAULT_MONTHLY_BUDGET = 50.0

    def __init__(
        self,
        api_key: str,
        monthly_budget_usd: float = DEFAULT_MONTHLY_BUDGET,
    ):
        """Initialize Sora client.

        Args:
            api_key: OpenAI API key with Sora access.
            monthly_budget_usd: Monthly spending limit.

        Raises:
            ValueError: If API key is empty.
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")

        self.api_key = api_key
        self.monthly_budget_usd = monthly_budget_usd
        self.total_spent_usd = 0.0
        self.generation_history: list[VideoGenerationResponse] = []

    def check_budget(self, estimated_cost: float) -> bool:
        """Check if generation is within budget.

        Args:
            estimated_cost: Estimated cost in USD.

        Returns:
            True if within budget, False otherwise.
        """
        remaining = self.monthly_budget_usd - self.total_spent_usd
        is_within = estimated_cost <= remaining

        logger.info(
            "Budget check: $%.2f estimated, $%.2f remaining (budget: $%.2f)",
            estimated_cost,
            remaining,
            self.monthly_budget_usd,
        )

        return is_within

    def generate_video(
        self,
        request: VideoGenerationRequest,
        dry_run: bool = False,
    ) -> VideoGenerationResponse:
        """Generate video from prompt.

        Args:
            request: VideoGenerationRequest with prompt and parameters.
            dry_run: If True, estimate cost only without actually generating.

        Returns:
            VideoGenerationResponse with video_id and status.

        Raises:
            ValueError: If request exceeds budget or invalid parameters.
            RuntimeError: If API call fails.
        """
        # Validate duration
        if request.duration < 15 or request.duration > 120:
            raise ValueError(
                f"Duration must be 15-120 seconds, got {request.duration}"
            )

        estimated_cost = request.estimate_cost_usd()

        if not self.check_budget(estimated_cost):
            raise ValueError(
                f"Generation cost ${estimated_cost:.2f} exceeds budget "
                f"(${self.monthly_budget_usd - self.total_spent_usd:.2f} remaining)"
            )

        if dry_run:
            logger.info(
                "DRY RUN: Would generate 90s video for $%.2f",
                estimated_cost,
            )
            return VideoGenerationResponse(
                video_id="dry_run_" + str(int(time.time())),
                status="dry_run_estimated",
                prompt=request.prompt[:100],
                duration=request.duration,
                created_at=str(time.time()),
                estimated_completion_time=60.0,
            )

        logger.info(
            "Generating %ds video: $%.2f (budget: $%.2f / $%.2f)",
            request.duration,
            estimated_cost,
            self.total_spent_usd + estimated_cost,
            self.monthly_budget_usd,
        )

        # In production, would call:
        # response = requests.post(
        #     self.BASE_URL,
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     json={
        #         "prompt": request.prompt,
        #         "duration": request.duration,
        #         "aspect_ratio": request.aspect_ratio.value,
        #         "quality": request.quality,
        #     },
        # )

        # Simulated response for demonstration
        video_id = f"video_{int(time.time())}"
        response = VideoGenerationResponse(
            video_id=video_id,
            status="processing",
            prompt=request.prompt[:100],
            duration=request.duration,
            created_at=str(time.time()),
            estimated_completion_time=request.duration * 0.5,
        )

        self.total_spent_usd += estimated_cost
        self.generation_history.append(response)

        logger.info("Video generation started: %s", video_id)

        return response

    def get_video_status(self, video_id: str) -> VideoGenerationResponse:
        """Poll for video generation status.

        Args:
            video_id: Video ID from generation response.

        Returns:
            Updated VideoGenerationResponse.

        Raises:
            RuntimeError: If API call fails.
        """
        # In production, would call:
        # response = requests.get(
        #     f"{self.BASE_URL}/{video_id}",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        # )

        logger.info("Checking status for video: %s", video_id)

        # Simulated status check
        for recorded in self.generation_history:
            if recorded.video_id == video_id:
                # Simulate processing
                if recorded.status == "processing":
                    recorded.status = "completed"
                    recorded.video_url = f"https://sora.openai.com/videos/{video_id}"

                return recorded

        raise RuntimeError(f"Video not found: {video_id}")

    def cancel_generation(self, video_id: str) -> bool:
        """Cancel in-progress video generation.

        Args:
            video_id: Video ID to cancel.

        Returns:
            True if cancelled successfully.

        Raises:
            RuntimeError: If cancellation fails.
        """
        logger.info("Cancelling video generation: %s", video_id)

        for recorded in self.generation_history:
            if recorded.video_id == video_id:
                if recorded.status == "processing":
                    recorded.status = "cancelled"
                    return True
                raise RuntimeError(f"Cannot cancel {recorded.status} video")

        raise RuntimeError(f"Video not found: {video_id}")

    def retry_with_budget_limit(
        self,
        request: VideoGenerationRequest,
        max_retries: int = 3,
        backoff_seconds: float = 2.0,
    ) -> Optional[VideoGenerationResponse]:
        """Generate video with retry logic and budget limits.

        Args:
            request: VideoGenerationRequest.
            max_retries: Maximum retry attempts.
            backoff_seconds: Initial backoff time (exponential).

        Returns:
            VideoGenerationResponse on success, None on failure.
        """
        for attempt in range(max_retries):
            try:
                return self.generate_video(request, dry_run=False)
            except ValueError as e:
                logger.error("Budget error (attempt %d): %s", attempt + 1, str(e))
                return None
            except RuntimeError as e:
                logger.warning(
                    "API error (attempt %d/%d): %s, retrying in %.1fs",
                    attempt + 1,
                    max_retries,
                    str(e),
                    backoff_seconds,
                )
                if attempt < max_retries - 1:
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2  # Exponential backoff
                else:
                    logger.error("Max retries exceeded")
                    return None

        return None

    def get_budget_summary(self) -> "dict[str, float]":
        """Get budget usage summary.

        Returns:
            Dictionary with budget stats.
        """
        return {
            "total_budget_usd": self.monthly_budget_usd,
            "total_spent_usd": round(self.total_spent_usd, 2),
            "remaining_usd": round(self.monthly_budget_usd - self.total_spent_usd, 2),
            "budget_used_percent": round(
                (self.total_spent_usd / self.monthly_budget_usd) * 100, 1
            ),
            "videos_generated": len(self.generation_history),
        }

    def save_budget_report(self, output_path: Path) -> None:
        """Save budget report to file.

        Args:
            output_path: Path to save report.
        """
        summary = self.get_budget_summary()
        report_lines = [
            "=" * 60,
            "SORA API BUDGET REPORT",
            "=" * 60,
            f"Total Budget: ${summary['total_budget_usd']:.2f}/month",
            f"Total Spent: ${summary['total_spent_usd']:.2f}",
            f"Remaining: ${summary['remaining_usd']:.2f}",
            f"Usage: {summary['budget_used_percent']:.1f}%",
            f"Videos Generated: {summary['videos_generated']}",
            "=" * 60,
            "",
            "GENERATION HISTORY:",
        ]

        for video in self.generation_history:
            report_lines.append(
                f"  {video.video_id} - {video.status} - "
                f"{video.duration}s - "
                f"${video.duration * 0.03:.2f}"
            )

        Path(output_path).write_text("\n".join(report_lines))
        logger.info("Budget report saved to: %s", output_path)


def create_client_from_env() -> SoraClient:
    """Create SoraClient from environment variables.

    Expected env vars:
      - SORA_API_KEY: OpenAI API key with Sora access
      - SORA_BUDGET_USD: Monthly budget (default: 50)

    Returns:
        SoraClient instance.

    Raises:
        ValueError: If API key not found.
    """
    import os

    api_key = os.getenv("SORA_API_KEY")
    if not api_key:
        raise ValueError(
            "SORA_API_KEY environment variable not set. "
            "Get one at: https://platform.openai.com/api-keys"
        )

    budget = float(os.getenv("SORA_BUDGET_USD", SoraClient.DEFAULT_MONTHLY_BUDGET))

    logger.info("Created Sora client with $%.2f monthly budget", budget)

    return SoraClient(api_key=api_key, monthly_budget_usd=budget)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Create client with $50 budget
    client = SoraClient(api_key="sk-test-dummy-key", monthly_budget_usd=50.0)

    # Create a video generation request
    req = VideoGenerationRequest(
        prompt="Black and white silent film of programmer debugging code",
        duration=90.0,
        aspect_ratio=AspectRatio.WIDESCREEN,
        quality="high",
    )

    print("=" * 70)
    print("SORA CLIENT - COST OPTIMIZATION DEMO")
    print("=" * 70)

    # Dry run (estimate cost only)
    estimated = req.estimate_cost_usd()
    print(f"\nEstimated cost for 90s video: ${estimated:.2f}")

    # Check budget
    if client.check_budget(estimated):
        print(f"Budget check: PASSED (${estimated:.2f} within $50.00)")

        # Generate with dry_run=True to avoid actual API calls
        response = client.generate_video(req, dry_run=True)
        print(f"Dry run response: {response.status}")
    else:
        print("Budget check: FAILED - exceeds monthly limit")

    # Show budget summary
    summary = client.get_budget_summary()
    print(f"\nBudget Summary:")
    print(f"  Total: ${summary['total_budget_usd']:.2f}")
    print(f"  Spent: ${summary['total_spent_usd']:.2f}")
    print(f"  Remaining: ${summary['remaining_usd']:.2f}")
