"""
timeline.py - Timeline and logical step detection for recordings.

Organizes recorded events into logical steps (e.g., implement feature, run tests, commit).
Uses heuristics to detect meaningful boundaries based on IDE events.

Features:
- Auto-detection of logical steps
- Event clustering and grouping
- Step categorization and naming
- Timeline visualization and export
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

from src.ide_recorder.events import EventType, IDEEvent

logger = logging.getLogger(__name__)


@dataclass
class LogicalStep:
    """Represents a logical step in the recording."""

    step_number: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    events: List[IDEEvent] = field(default_factory=list)
    category: str = "general"  # e.g., "coding", "testing", "debugging", "commit"

    @property
    def duration(self) -> timedelta:
        """Duration of this step."""
        return self.end_time - self.start_time

    @property
    def duration_seconds(self) -> float:
        """Duration in seconds."""
        return self.duration.total_seconds()

    def to_dict(self) -> dict:
        """Convert step to dictionary."""
        return {
            "step_number": self.step_number,
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": self.duration_seconds,
            "category": self.category,
            "event_count": len(self.events),
        }

    def __str__(self) -> str:
        """String representation."""
        return f"Step {self.step_number}: {self.name} ({self.duration_seconds:.1f}s)"


class TimelineManager:
    """Manages timeline organization and logical step detection."""

    def __init__(self, min_step_duration_seconds: float = 2.0):
        """Initialize timeline manager.

        Args:
            min_step_duration_seconds: Minimum duration for a step (merge shorter ones).
        """
        self.steps: List[LogicalStep] = []
        self.min_step_duration = min_step_duration_seconds
        self.last_significant_event: Optional[IDEEvent] = None

    def detect_logical_steps(self, events: List[IDEEvent]) -> List[LogicalStep]:
        """Auto-detect logical steps from events.

        Args:
            events: List of recorded events.

        Returns:
            List of detected logical steps.
        """
        if not events:
            return []

        self.steps = []
        step_events: List[IDEEvent] = []
        step_start: Optional[datetime] = None
        step_category = "general"
        step_count = 1

        for event in events:
            # Detect step boundaries based on significant events
            is_boundary = self._is_step_boundary(event)

            if is_boundary and step_events:
                # Create step for accumulated events
                step = self._create_step(
                    step_count,
                    step_events,
                    step_start,
                    event.timestamp,
                    step_category,
                )
                if step.duration_seconds >= self.min_step_duration:
                    self.steps.append(step)
                    step_count += 1

                step_events = []
                step_start = None
                step_category = "general"

            step_events.append(event)
            if step_start is None:
                step_start = event.timestamp

            # Update category based on event type
            step_category = self._get_event_category(event)

        # Add final step
        if step_events and step_start:
            step = self._create_step(
                step_count, step_events, step_start, events[-1].timestamp, step_category
            )
            if step.duration_seconds >= self.min_step_duration:
                self.steps.append(step)

        logger.info(f"Detected {len(self.steps)} logical steps")
        return self.steps

    def _is_step_boundary(self, event: IDEEvent) -> bool:
        """Check if event marks a step boundary.

        Args:
            event: Event to check.

        Returns:
            True if event is a boundary marker.
        """
        boundary_events = {
            EventType.FILE_SAVED,
            EventType.TEST_RUN_COMPLETED,
            EventType.BUILD_COMPLETED,
            EventType.GIT_COMMIT,
            EventType.DEBUG_SESSION_ENDED,
        }
        return event.event_type in boundary_events

    def _get_event_category(self, event: IDEEvent) -> str:
        """Get category for event type.

        Args:
            event: Event to categorize.

        Returns:
            Category string.
        """
        categories = {
            EventType.TEST_RUN_COMPLETED: "testing",
            EventType.TEST_FAILED: "testing",
            EventType.BUILD_STARTED: "building",
            EventType.BUILD_COMPLETED: "building",
            EventType.DEBUG_SESSION_STARTED: "debugging",
            EventType.DEBUG_SESSION_ENDED: "debugging",
            EventType.GIT_COMMIT: "version_control",
            EventType.GIT_PUSH: "version_control",
            EventType.GIT_PULL: "version_control",
            EventType.FILE_SAVED: "editing",
            EventType.REFACTOR_APPLIED: "refactoring",
        }
        return categories.get(event.event_type, "general")

    def _create_step(
        self,
        step_number: int,
        events: List[IDEEvent],
        start_time: datetime,
        end_time: datetime,
        category: str,
    ) -> LogicalStep:
        """Create a logical step from events.

        Args:
            step_number: Step number.
            events: Events in this step.
            start_time: Step start time.
            end_time: Step end time.
            category: Step category.

        Returns:
            LogicalStep instance.
        """
        # Generate step name from events
        name = self._generate_step_name(events, category)
        description = self._generate_step_description(events)

        return LogicalStep(
            step_number=step_number,
            name=name,
            description=description,
            start_time=start_time,
            end_time=end_time,
            events=events,
            category=category,
        )

    def _generate_step_name(self, events: List[IDEEvent], category: str) -> str:
        """Generate descriptive name for step.

        Args:
            events: Events in step.
            category: Step category.

        Returns:
            Step name.
        """
        # Find key events
        for event in reversed(events):
            if event.event_type == EventType.GIT_COMMIT and event.content:
                return f"Commit: {event.content[:40]}"
            elif event.event_type == EventType.TEST_RUN_COMPLETED:
                return "Run Tests"
            elif event.event_type == EventType.BUILD_COMPLETED:
                return "Build Project"
            elif event.event_type == EventType.FILE_SAVED and event.file_path:
                return f"Edit {event.file_path.name}"

        # Fallback to category-based naming
        names = {
            "testing": "Testing",
            "building": "Building",
            "debugging": "Debugging",
            "version_control": "Version Control",
            "editing": "Editing",
            "refactoring": "Refactoring",
        }
        return names.get(category, "General Activity")

    def _generate_step_description(self, events: List[IDEEvent]) -> str:
        """Generate description for step.

        Args:
            events: Events in step.

        Returns:
            Step description.
        """
        event_types = {}
        for event in events:
            et = event.event_type.value
            event_types[et] = event_types.get(et, 0) + 1

        # Build description from event summary
        descriptions = []
        for event_type, count in sorted(event_types.items()):
            descriptions.append(f"{count} {event_type}")

        return "Events: " + ", ".join(descriptions[:3])

    def get_step_at_time(self, timestamp: datetime) -> Optional[LogicalStep]:
        """Find step containing given timestamp.

        Args:
            timestamp: Time to search for.

        Returns:
            Matching step or None.
        """
        for step in self.steps:
            if step.start_time <= timestamp <= step.end_time:
                return step
        return None

    def merge_steps(self, indices: List[int]) -> None:
        """Merge multiple steps into one.

        Args:
            indices: Indices of steps to merge.
        """
        if not indices:
            return

        indices_sorted = sorted(set(indices))
        merge_events = []
        first_step = self.steps[indices_sorted[0]]

        for idx in indices_sorted:
            merge_events.extend(self.steps[idx].events)

        merged = LogicalStep(
            step_number=first_step.step_number,
            name=f"Combined ({len(indices_sorted)} steps)",
            description="Merged logical steps",
            start_time=first_step.start_time,
            end_time=self.steps[indices_sorted[-1]].end_time,
            events=merge_events,
            category=first_step.category,
        )

        # Replace steps
        new_steps = []
        for i, step in enumerate(self.steps):
            if i not in indices_sorted:
                new_steps.append(step)
            elif i == indices_sorted[0]:
                new_steps.append(merged)

        self.steps = new_steps
        logger.info(f"Merged {len(indices_sorted)} steps")

    def get_statistics(self) -> dict:
        """Get timeline statistics.

        Returns:
            Dictionary with statistics.
        """
        total_duration = sum(s.duration_seconds for s in self.steps)
        categories = {}
        for step in self.steps:
            categories[step.category] = categories.get(step.category, 0) + 1

        return {
            "total_steps": len(self.steps),
            "total_duration_seconds": total_duration,
            "categories": categories,
            "average_step_duration": total_duration / len(self.steps) if self.steps else 0,
        }
