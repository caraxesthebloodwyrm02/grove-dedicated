"""
ide_recorder - IDE screen recording and narration tool.

A comprehensive toolkit for capturing IDE screen activity, auto-detecting logical steps,
generating AI narration, and producing YouTube-ready videos with smooth transitions and overlays.

Key Components:
- Screen recorder: Captures IDE screen at configurable FPS
- Event tracker: Monitors file changes, cursor movements, IDE events
- Timeline manager: Organizes events into logical steps (saves, tests, commits)
- AI narrator: Generates descriptions for each step using LLM
- Video processor: Combines recordings with overlays and transitions
- YouTube uploader: Exports and uploads to YouTube

Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "IDE Recorder Contributors"

from src.ide_recorder.config import RecorderConfig
from src.ide_recorder.events import EventTracker, IDEEvent
from src.ide_recorder.narrator import AInarrator
from src.ide_recorder.recorder import ScreenRecorder
from src.ide_recorder.timeline import TimelineManager, LogicalStep
from src.ide_recorder.uploader import YouTubeUploader
from src.ide_recorder.video_processor import VideoProcessor

__all__ = [
    "ScreenRecorder",
    "EventTracker",
    "IDEEvent",
    "TimelineManager",
    "LogicalStep",
    "AInarrator",
    "VideoProcessor",
    "YouTubeUploader",
    "RecorderConfig",
]
