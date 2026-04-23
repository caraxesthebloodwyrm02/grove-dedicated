#!/usr/bin/env python3
"""
ide_recorder_cli.py - Command-line interface for IDE recorder.

Main entry point for recording IDE sessions, generating narration, and uploading videos.

Usage:
    ide_recorder_cli.py record --duration 300 --fps 30 --output recording.mp4
    ide_recorder_cli.py process --input recording.mp4 --add-narration --output final.mp4
    ide_recorder_cli.py upload --video final.mp4 --title "My Tutorial" --privacy private
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from src.ide_recorder import (
    AInarrator,
    EventTracker,
    RecorderConfig,
    ScreenRecorder,
    TimelineManager,
    VideoProcessor,
    YouTubeUploader,
)
from src.ide_recorder.events import EventType
from src.ide_recorder.narrator import AIProvider, TTSProvider
from src.ide_recorder.uploader import PrivacyLevel, VideoMetadata

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration.

    Args:
        debug: Enable debug logging.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.getLogger().setLevel(level)
    logger.debug("Debug logging enabled")


def cmd_record(args: argparse.Namespace) -> int:
    """Handle 'record' command.

    Args:
        args: Command arguments.

    Returns:
        Exit code (0 for success).
    """
    logger.info("Starting screen recording...")

    output_path = Path(args.output)
    duration = args.duration
    fps = args.fps
    width = args.width
    height = args.height

    try:
        # Create recorder
        recorder = ScreenRecorder(
            output_path=output_path,
            fps=fps,
            width=width,
            height=height,
        )

        # Create event tracker
        event_tracker = EventTracker()
        event_tracker.start_tracking()

        # Start recording
        logger.info(f"Recording for {duration} seconds ({fps}fps) to {output_path}")
        recorder.start()

        # Simulate some events during recording (in real scenario, these come from IDE)
        event_tracker.track_file_saved(Path("example.py"))
        event_tracker.track_test_run("test_example", passed=True)

        # In real use: monitor recording until duration expires or user stops
        import time

        time.sleep(min(duration, 5))  # Demo: record for 5 seconds max

        recorder.stop()
        event_tracker.stop_tracking()

        stats = recorder.get_statistics()
        logger.info(f"Recording complete: {stats}")

        return 0

    except Exception as e:
        logger.error(f"Recording failed: {e}")
        return 1


def cmd_process(args: argparse.Namespace) -> int:
    """Handle 'process' command.

    Args:
        args: Command arguments.

    Returns:
        Exit code (0 for success).
    """
    logger.info("Starting video processing...")

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        logger.error(f"Input video not found: {input_path}")
        return 1

    try:
        # Create video processor
        processor = VideoProcessor(
            input_video=input_path,
            output_path=output_path,
        )

        # Add narration if requested
        if args.add_narration:
            logger.info("Generating AI narration...")

            # Initialize narrator
            narrator = AInarrator(
                ai_provider=AIProvider.OPENAI,
                ai_api_key=args.ai_api_key or "",
                tts_provider=TTSProvider.OPENAI,
                tts_api_key=args.tts_api_key or "",
                debug=args.debug,
            )

            # Generate sample narration
            narration = narrator.generate_narration_for_step(
                step_name="Example Step",
                step_description="Recording IDE activity",
                events_summary="Multiple file saves and tests",
            )
            logger.info(f"Generated narration: {narration}")

            # Synthesize speech
            audio_path = narrator.synthesize_speech(narration)
            logger.info(f"Audio synthesized: {audio_path}")

            # Add to video
            processor.add_narration(audio_path)

        # Export video
        quality = args.quality or "1080p"
        output = processor.export(quality=quality)
        logger.info(f"Video exported: {output}")

        return 0

    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return 1


def cmd_upload(args: argparse.Namespace) -> int:
    """Handle 'upload' command.

    Args:
        args: Command arguments.

    Returns:
        Exit code (0 for success).
    """
    logger.info("Preparing video upload...")

    video_path = Path(args.video)

    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        return 1

    try:
        # Create uploader
        uploader = YouTubeUploader(
            client_id=args.client_id or "",
            client_secret=args.client_secret or "",
            refresh_token=args.refresh_token or "",
            channel_id=args.channel_id or "",
        )

        # Authenticate
        if not uploader.authenticate():
            logger.error("YouTube authentication failed")
            return 1

        # Prepare metadata
        metadata = VideoMetadata(
            title=args.title or "Untitled Recording",
            description=args.description or "Auto-generated IDE recording",
            tags=args.tags or ["coding", "tutorial"],
            privacy_level=PrivacyLevel(args.privacy),
        )

        # Upload video
        video_id = uploader.upload_video(video_path, metadata)

        if video_id:
            url = f"https://youtu.be/{video_id}"
            logger.info(f"Upload successful: {url}")
            print(f"Video URL: {url}")
            return 0
        else:
            logger.error("Upload failed")
            return 1

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return 1


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="IDE Screen Recorder - Capture, narrate, and share IDE sessions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Record command
    record_parser = subparsers.add_parser("record", help="Record IDE screen")
    record_parser.add_argument(
        "--output", "-o", required=True, help="Output video file path"
    )
    record_parser.add_argument(
        "--duration", "-d", type=int, default=300, help="Recording duration in seconds"
    )
    record_parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    record_parser.add_argument("--width", type=int, default=1920, help="Video width")
    record_parser.add_argument("--height", type=int, default=1080, help="Video height")
    record_parser.set_defaults(func=cmd_record)

    # Process command
    process_parser = subparsers.add_parser("process", help="Process recorded video")
    process_parser.add_argument(
        "--input", "-i", required=True, help="Input video file"
    )
    process_parser.add_argument(
        "--output", "-o", required=True, help="Output video file"
    )
    process_parser.add_argument(
        "--add-narration", action="store_true", help="Generate and add AI narration"
    )
    process_parser.add_argument(
        "--ai-api-key", help="AI service API key (OpenAI, etc.)"
    )
    process_parser.add_argument(
        "--tts-api-key", help="TTS service API key"
    )
    process_parser.add_argument(
        "--quality", choices=["480p", "720p", "1080p", "4k"], help="Output quality"
    )
    process_parser.set_defaults(func=cmd_process)

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload video to YouTube")
    upload_parser.add_argument(
        "--video", "-v", required=True, help="Video file to upload"
    )
    upload_parser.add_argument("--title", "-t", help="Video title")
    upload_parser.add_argument("--description", help="Video description")
    upload_parser.add_argument(
        "--tags", nargs="+", help="Video tags (space-separated)"
    )
    upload_parser.add_argument(
        "--privacy",
        choices=["public", "unlisted", "private"],
        default="private",
        help="Privacy level",
    )
    upload_parser.add_argument("--client-id", help="YouTube OAuth client ID")
    upload_parser.add_argument("--client-secret", help="YouTube OAuth client secret")
    upload_parser.add_argument("--refresh-token", help="YouTube OAuth refresh token")
    upload_parser.add_argument("--channel-id", help="YouTube channel ID")
    upload_parser.set_defaults(func=cmd_upload)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Setup logging
    setup_logging(args.debug)

    # Execute command
    try:
        return args.func(args)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
