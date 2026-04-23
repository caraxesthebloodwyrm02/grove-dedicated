"""Periodic processing engine."""

import asyncio
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, Field


class ProcessingMode(str, Enum):
    """Processing modes."""

    PERIODIC = "periodic"  # Default: periodic processing
    REALTIME = "realtime"  # Emergency: real-time processing
    HYBRID = "hybrid"  # Mixed mode


class ProcessingSchedule(BaseModel):
    """Processing schedule configuration."""

    interval_seconds: float = Field(default=60.0, description="Processing interval in seconds")
    batch_size: int = Field(default=100, description="Batch size for processing")
    max_processing_time: Optional[float] = Field(
        default=None, description="Max processing time per cycle"
    )
    enabled: bool = Field(default=True, description="Whether schedule is enabled")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class PeriodicProcessor:
    """Processes operations periodically with configurable intervals."""

    def __init__(self, schedule: Optional[ProcessingSchedule] = None):
        """Initialize periodic processor.

        Args:
            schedule: Processing schedule (defaults to 60s interval)
        """
        self.schedule = schedule or ProcessingSchedule()
        self._processing_queue: List[Dict[str, Any]] = []
        self._processor_func: Optional[Callable[[List[Dict[str, Any]]], Any]] = None
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._stats: Dict[str, Any] = {
            "cycles": 0,
            "items_processed": 0,
            "last_cycle": None,
            "errors": 0,
        }

    def set_processor(self, processor_func: Callable[[List[Dict[str, Any]]], Any]) -> None:
        """Set the processing function.

        Args:
            processor_func: Function to process items
        """
        self._processor_func = processor_func

    def enqueue(self, item: Dict[str, Any]) -> None:
        """Enqueue an item for processing.

        Args:
            item: Item to process
        """
        self._processing_queue.append(item)

    def enqueue_batch(self, items: List[Dict[str, Any]]) -> None:
        """Enqueue multiple items.

        Args:
            items: Items to process
        """
        self._processing_queue.extend(items)

    async def start(self) -> None:
        """Start periodic processing."""
        if self._running:
            return

        if not self._processor_func:
            raise ValueError("No processor function set. Call set_processor first.")

        self._running = True
        self._task = asyncio.create_task(self._processing_loop())

    async def stop(self) -> None:
        """Stop periodic processing."""
        self._running = False
        if self._task:
            await self._task
            self._task = None

    async def _processing_loop(self) -> None:
        """Main processing loop."""
        while self._running:
            try:
                await self._process_cycle()
                await asyncio.sleep(self.schedule.interval_seconds)
            except Exception as e:
                self._stats["errors"] += 1
                print(f"Error in processing cycle: {e}")

    async def _process_cycle(self) -> None:
        """Process one cycle."""
        if not self._processing_queue:
            return

        # Get batch
        batch = self._processing_queue[: self.schedule.batch_size]
        self._processing_queue = self._processing_queue[self.schedule.batch_size :]

        # Process batch
        start_time = datetime.now(timezone.utc)

        # Set AsyncTemporalContext for this cycle (mode can differ between cycles)
        from grid.temporal_safety.context import (
            build_temporal_context,
            temporal_context_ctx,
        )

        ctx = build_temporal_context(now=start_time)
        token = temporal_context_ctx.set(ctx)

        try:
            if self._processor_func:
                await asyncio.to_thread(self._processor_func, batch)

            self._stats["cycles"] += 1
            self._stats["items_processed"] += len(batch)
            self._stats["last_cycle"] = start_time.isoformat()
        except Exception:
            self._stats["errors"] += 1
            raise
        finally:
            temporal_context_ctx.reset(token)

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics.

        Returns:
            Statistics dictionary
        """
        return {
            **self._stats,
            "queue_size": len(self._processing_queue),
            "schedule": self.schedule.model_dump(),
        }

    def get_queue_size(self) -> int:
        """Get current queue size."""
        return len(self._processing_queue)
