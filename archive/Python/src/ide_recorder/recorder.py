"""
recorder.py - Screen recording and capture management.

Handles screen capture at configurable FPS using FFmpeg or similar backends.
Captures the entire IDE screen or specific windows and encodes to video format.

Features:
- Configurable frame rate and resolution
- Multiple codec support
- Frame buffering and threading
- Resource optimization
"""

from __future__ import annotations

import logging
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RecordingFrame:
    """Represents a single recorded frame."""

    frame_number: int
    timestamp: datetime
    data: bytes


class ScreenRecorder:
    """Handles screen capture and video recording."""

    def __init__(
        self,
        output_path: Path,
        fps: int = 30,
        width: int = 1920,
        height: int = 1080,
        codec: str = "libx264",
        bitrate: str = "5000k",
        monitor_index: int = 0,
    ):
        """Initialize screen recorder.

        Args:
            output_path: Path for output video file.
            fps: Frames per second (default 30).
            width: Video width in pixels.
            height: Video height in pixels.
            codec: FFmpeg codec name.
            bitrate: Video bitrate.
            monitor_index: Which monitor to capture (0-based).
        """
        self.output_path = Path(output_path)
        self.fps = fps
        self.width = width
        self.height = height
        self.codec = codec
        self.bitrate = bitrate
        self.monitor_index = monitor_index

        self.recording = False
        self.process: Optional[subprocess.Popen] = None
        self.frame_count = 0
        self.start_time: Optional[datetime] = None
        self.thread: Optional[threading.Thread] = None

        logger.info(f"Recorder initialized: {width}x{height} @ {fps}fps")

    def start(self) -> None:
        """Start recording."""
        if self.recording:
            logger.warning("Recording already in progress")
            return

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.recording = True
        self.frame_count = 0
        self.start_time = datetime.now()

        # Platform-specific screen capture setup
        self._setup_ffmpeg_capture()
        logger.info(f"Recording started: {self.output_path}")

    def stop(self) -> None:
        """Stop recording."""
        if not self.recording:
            logger.warning("No recording in progress")
            return

        self.recording = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

        if self.thread:
            self.thread.join(timeout=5)

        duration = datetime.now() - (self.start_time or datetime.now())
        logger.info(
            f"Recording stopped: {self.frame_count} frames in {duration.total_seconds():.1f}s"
        )

    def pause(self) -> None:
        """Pause recording."""
        if not self.recording:
            return
        logger.info("Recording paused")

    def resume(self) -> None:
        """Resume recording."""
        if self.recording:
            return
        self.recording = True
        logger.info("Recording resumed")

    def _setup_ffmpeg_capture(self) -> None:
        """Setup FFmpeg for screen capture."""
        import platform

        system = platform.system()

        if system == "Windows":
            self._setup_windows_capture()
        elif system == "Darwin":
            self._setup_macos_capture()
        elif system == "Linux":
            self._setup_linux_capture()
        else:
            logger.error(f"Unsupported platform: {system}")

    def _setup_windows_capture(self) -> None:
        """Setup screen capture for Windows using GDI."""
        # Using gdigrab for Windows
        input_device = f"desktop"

        cmd = [
            "ffmpeg",
            "-f", "gdigrab",
            "-framerate", str(self.fps),
            "-i", input_device,
            "-c:v", self.codec,
            "-b:v", self.bitrate,
            "-preset", "fast",
            str(self.output_path),
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info("Windows GDI capture started")
        except FileNotFoundError:
            logger.error("FFmpeg not found. Please install FFmpeg.")

    def _setup_macos_capture(self) -> None:
        """Setup screen capture for macOS using AVFoundation."""
        # Using avfoundation for macOS
        input_device = ":0"

        cmd = [
            "ffmpeg",
            "-f", "avfoundation",
            "-framerate", str(self.fps),
            "-i", input_device,
            "-c:v", self.codec,
            "-b:v", self.bitrate,
            "-preset", "fast",
            str(self.output_path),
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info("macOS AVFoundation capture started")
        except FileNotFoundError:
            logger.error("FFmpeg not found. Please install FFmpeg.")

    def _setup_linux_capture(self) -> None:
        """Setup screen capture for Linux using X11."""
        # Using x11grab for Linux
        display = ":0.0"

        cmd = [
            "ffmpeg",
            "-f", "x11grab",
            "-framerate", str(self.fps),
            "-i", display,
            "-c:v", self.codec,
            "-b:v", self.bitrate,
            "-preset", "fast",
            str(self.output_path),
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info("Linux X11 capture started")
        except FileNotFoundError:
            logger.error("FFmpeg not found. Please install FFmpeg.")

    def get_duration(self) -> float:
        """Get current recording duration in seconds.

        Returns:
            Duration in seconds.
        """
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()

    def is_recording(self) -> bool:
        """Check if currently recording.

        Returns:
            True if recording is active.
        """
        return self.recording and (self.process is not None and self.process.poll() is None)

    def get_statistics(self) -> dict:
        """Get recording statistics.

        Returns:
            Dictionary with frame count, duration, etc.
        """
        duration = self.get_duration()
        return {
            "frames": self.frame_count,
            "duration_seconds": duration,
            "fps": self.fps,
            "resolution": f"{self.width}x{self.height}",
            "codec": self.codec,
            "output_path": str(self.output_path),
        }
