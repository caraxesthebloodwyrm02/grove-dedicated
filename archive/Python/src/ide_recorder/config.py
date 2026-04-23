"""
config.py - Configuration management for IDE recorder.

Handles recorder settings including:
- Screen capture parameters (FPS, resolution, codec)
- Event tracking options
- AI narration settings (model, API key, voice)
- Video processing parameters (transitions, overlays, quality)
- Upload destination (YouTube credentials, channel)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import json


@dataclass
class ScreenCaptureConfig:
    """Screen capture settings."""

    fps: int = 30
    resolution_width: int = 1920
    resolution_height: int = 1080
    codec: str = "libx264"
    bitrate: str = "5000k"
    monitor_index: int = 0


@dataclass
class EventTrackingConfig:
    """Event tracking settings."""

    track_file_changes: bool = True
    track_cursor_movement: bool = True
    track_keystrokes: bool = False  # Privacy concern
    track_ide_events: bool = True
    update_interval_ms: int = 500


@dataclass
class NarrationConfig:
    """AI narration settings."""

    enabled: bool = True
    model: str = "gpt-4"  # or "claude-3-sonnet", "gemini-pro"
    api_key: str = ""
    api_endpoint: Optional[str] = None
    voice_model: str = "tts-1"  # OpenAI TTS
    language: str = "en"
    temperature: float = 0.7
    max_tokens: int = 150


@dataclass
class VideoProcessingConfig:
    """Video processing settings."""

    enable_transitions: bool = True
    transition_duration_ms: int = 500
    transition_type: str = "fade"  # fade, dissolve, slide, etc.
    enable_overlays: bool = True
    overlay_font_size: int = 32
    overlay_position: str = "bottom"  # bottom, top, side
    output_quality: str = "1080p"  # 720p, 1080p, 4k
    output_format: str = "mp4"
    output_path: Path = field(default_factory=lambda: Path("./output"))


@dataclass
class YouTubeUploadConfig:
    """YouTube upload settings."""

    enabled: bool = False
    client_id: str = ""
    client_secret: str = ""
    refresh_token: str = ""
    channel_id: str = ""
    title_template: str = "IDE Recording - {timestamp}"
    description_template: str = "Auto-generated IDE recording with AI narration"
    tags: list[str] = field(default_factory=lambda: ["coding", "tutorial", "ide"])
    privacy_level: str = "private"  # private, unlisted, public


@dataclass
class RecorderConfig:
    """Main recorder configuration combining all sub-configs."""

    project_name: str = "ide_recording"
    output_directory: Path = field(default_factory=lambda: Path("./recordings"))
    temp_directory: Path = field(default_factory=lambda: Path("./temp"))

    screen_capture: ScreenCaptureConfig = field(default_factory=ScreenCaptureConfig)
    event_tracking: EventTrackingConfig = field(default_factory=EventTrackingConfig)
    narration: NarrationConfig = field(default_factory=NarrationConfig)
    video_processing: VideoProcessingConfig = field(
        default_factory=VideoProcessingConfig
    )
    youtube: YouTubeUploadConfig = field(default_factory=YouTubeUploadConfig)

    debug_mode: bool = False
    log_level: str = "INFO"

    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "project_name": self.project_name,
            "output_directory": str(self.output_directory),
            "temp_directory": str(self.temp_directory),
            "screen_capture": {
                "fps": self.screen_capture.fps,
                "resolution": {
                    "width": self.screen_capture.resolution_width,
                    "height": self.screen_capture.resolution_height,
                },
                "codec": self.screen_capture.codec,
                "bitrate": self.screen_capture.bitrate,
            },
            "event_tracking": {
                "track_file_changes": self.event_tracking.track_file_changes,
                "track_cursor_movement": self.event_tracking.track_cursor_movement,
                "track_keystrokes": self.event_tracking.track_keystrokes,
                "track_ide_events": self.event_tracking.track_ide_events,
            },
            "narration": {"enabled": self.narration.enabled, "model": self.narration.model},
            "debug_mode": self.debug_mode,
        }

    @classmethod
    def from_json(cls, json_path: Path) -> RecorderConfig:
        """Load config from JSON file."""
        with open(json_path, "r") as f:
            data = json.load(f)

        config = cls()
        if "project_name" in data:
            config.project_name = data["project_name"]
        if "output_directory" in data:
            config.output_directory = Path(data["output_directory"])
        if "debug_mode" in data:
            config.debug_mode = data["debug_mode"]

        return config

    def to_json(self, json_path: Path) -> None:
        """Save config to JSON file."""
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
