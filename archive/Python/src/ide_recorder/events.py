"""
events.py - IDE event tracking and classification.

Monitors IDE activity including:
- File system changes (file saves, renames, deletes)
- Cursor movements and selections
- IDE-specific events (test runs, debug sessions, git operations)
- Code completions and suggestions

Events are timestamped and categorized for use in timeline generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Enumeration of IDE event types."""

    # File operations
    FILE_SAVED = "file_saved"
    FILE_CREATED = "file_created"
    FILE_DELETED = "file_deleted"
    FILE_RENAMED = "file_renamed"
    FILE_MODIFIED = "file_modified"

    # Editor operations
    CURSOR_MOVED = "cursor_moved"
    SELECTION_CHANGED = "selection_changed"
    TEXT_INSERTED = "text_inserted"
    TEXT_DELETED = "text_deleted"

    # IDE operations
    TEST_RUN_STARTED = "test_run_started"
    TEST_RUN_COMPLETED = "test_run_completed"
    TEST_FAILED = "test_failed"
    DEBUG_SESSION_STARTED = "debug_session_started"
    DEBUG_SESSION_ENDED = "debug_session_ended"
    BUILD_STARTED = "build_started"
    BUILD_COMPLETED = "build_completed"

    # VCS operations
    GIT_COMMIT = "git_commit"
    GIT_PUSH = "git_push"
    GIT_PULL = "git_pull"
    BRANCH_CHANGED = "branch_changed"

    # Code operations
    CODE_COMPLETION = "code_completion"
    REFACTOR_APPLIED = "refactor_applied"
    SEARCH_EXECUTED = "search_executed"

    # Recording operations
    RECORDING_STARTED = "recording_started"
    RECORDING_PAUSED = "recording_paused"
    RECORDING_RESUMED = "recording_resumed"
    RECORDING_STOPPED = "recording_stopped"


class EventSeverity(Enum):
    """Event severity levels for filtering."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class IDEEvent:
    """Represents a single IDE event captured during recording."""

    event_type: EventType
    timestamp: datetime
    severity: EventSeverity = EventSeverity.INFO

    # Event-specific metadata
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    content: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity.value,
            "file_path": str(self.file_path) if self.file_path else None,
            "line_number": self.line_number,
            "column_number": self.column_number,
            "content": self.content,
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        """String representation of event."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] {self.event_type.value}: {self.file_path or self.content or 'N/A'}"


class EventTracker:
    """Tracks and manages IDE events during recording."""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize event tracker.

        Args:
            config: Configuration dictionary with tracking options.
        """
        self.config = config or {}
        self.events: List[IDEEvent] = []
        self.callbacks: dict[EventType, List[Callable[[IDEEvent], None]]] = {}
        self.recording_active = False

    def start_tracking(self) -> None:
        """Start tracking events."""
        self.recording_active = True
        event = IDEEvent(
            event_type=EventType.RECORDING_STARTED,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO,
        )
        self.track_event(event)
        logger.info("Event tracking started")

    def stop_tracking(self) -> None:
        """Stop tracking events."""
        self.recording_active = False
        event = IDEEvent(
            event_type=EventType.RECORDING_STOPPED,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO,
        )
        self.track_event(event)
        logger.info("Event tracking stopped")

    def track_event(self, event: IDEEvent) -> None:
        """Record an IDE event.

        Args:
            event: The IDEEvent to track.
        """
        if not self.recording_active:
            return

        self.events.append(event)
        logger.debug(f"Event tracked: {event}")

        # Trigger callbacks for this event type
        if event.event_type in self.callbacks:
            for callback in self.callbacks[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")

    def track_file_saved(self, file_path: Path, content: Optional[str] = None) -> None:
        """Track file save event.

        Args:
            file_path: Path to saved file.
            content: Optional file content.
        """
        event = IDEEvent(
            event_type=EventType.FILE_SAVED,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO,
            file_path=file_path,
            content=content,
        )
        self.track_event(event)

    def track_file_modified(self, file_path: Path) -> None:
        """Track file modification.

        Args:
            file_path: Path to modified file.
        """
        event = IDEEvent(
            event_type=EventType.FILE_MODIFIED,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO,
            file_path=file_path,
        )
        self.track_event(event)

    def track_test_run(self, test_name: str, passed: bool) -> None:
        """Track test execution.

        Args:
            test_name: Name of the test.
            passed: Whether test passed.
        """
        event = IDEEvent(
            event_type=EventType.TEST_RUN_COMPLETED,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO if passed else EventSeverity.WARNING,
            content=test_name,
            metadata={"passed": passed},
        )
        self.track_event(event)

    def track_git_commit(self, commit_message: str, files_changed: int) -> None:
        """Track git commit.

        Args:
            commit_message: Commit message.
            files_changed: Number of files changed.
        """
        event = IDEEvent(
            event_type=EventType.GIT_COMMIT,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO,
            content=commit_message,
            metadata={"files_changed": files_changed},
        )
        self.track_event(event)

    def track_cursor_moved(
        self, file_path: Path, line: int, column: int
    ) -> None:
        """Track cursor movement.

        Args:
            file_path: File being edited.
            line: Line number.
            column: Column number.
        """
        event = IDEEvent(
            event_type=EventType.CURSOR_MOVED,
            timestamp=datetime.now(),
            severity=EventSeverity.INFO,
            file_path=file_path,
            line_number=line,
            column_number=column,
        )
        self.track_event(event)

    def register_callback(
        self, event_type: EventType, callback: Callable[[IDEEvent], None]
    ) -> None:
        """Register a callback for specific event type.

        Args:
            event_type: Type of event to listen for.
            callback: Function to call when event occurs.
        """
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)

    def get_events_by_type(self, event_type: EventType) -> List[IDEEvent]:
        """Get all events of a specific type.

        Args:
            event_type: Type of events to retrieve.

        Returns:
            List of matching events.
        """
        return [e for e in self.events if e.event_type == event_type]

    def get_events_in_timerange(
        self, start: datetime, end: datetime
    ) -> List[IDEEvent]:
        """Get events within a time range.

        Args:
            start: Start timestamp.
            end: End timestamp.

        Returns:
            List of events in range.
        """
        return [e for e in self.events if start <= e.timestamp <= end]

    def clear_events(self) -> None:
        """Clear all tracked events."""
        self.events.clear()
        logger.info("Events cleared")

    def get_statistics(self) -> dict[str, Any]:
        """Get event tracking statistics.

        Returns:
            Dictionary with event statistics.
        """
        event_counts = {}
        for event in self.events:
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            "total_events": len(self.events),
            "event_types": len(event_counts),
            "event_counts": event_counts,
            "duration_seconds": (
                (self.events[-1].timestamp - self.events[0].timestamp).total_seconds()
                if self.events
                else 0
            ),
        }
