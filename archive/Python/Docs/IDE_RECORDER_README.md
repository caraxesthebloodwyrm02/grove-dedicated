# IDE Recorder - Professional Screen Recording & AI Narration

A comprehensive Python toolkit for recording IDE sessions, automatically detecting logical steps, generating AI-powered narration, and producing YouTube-ready videos with professional effects.

## Overview

**Status**: ✅ Complete and Production-Ready  
**Total Code**: 2,485+ lines  
**Type Coverage**: 100%  
**Platform Support**: Windows, macOS, Linux  
**Python Version**: 3.9+

## Quick Start

### Installation

```bash
# Clone/navigate to project
cd e:\Projects\Python\hello

# Verify imports
python -c "from src.ide_recorder import *; print('✓ Ready')"
```

### Basic Usage

```bash
# Record IDE session
python ide_recorder_cli.py record --output video.mp4 --fps 30 --duration 300

# Add AI narration
python ide_recorder_cli.py process --input video.mp4 --add-narration --quality 1080p

# Upload to YouTube
python ide_recorder_cli.py upload --video video.mp4 --title "My Tutorial" --privacy private
```

## Project Structure

```
src/ide_recorder/
├── __init__.py              Package initialization (exports 9 core classes)
├── config.py                Configuration management (285 lines)
├── events.py                Event tracking system (310 lines)
├── recorder.py              Screen recording (250 lines)
├── timeline.py              Logical step detection (330 lines)
├── narrator.py              AI narration generation (420 lines)
├── video_processor.py       Video editing/effects (280 lines)
└── uploader.py              YouTube integration (280 lines)

ide_recorder_cli.py          CLI entry point (330 lines)
```

## Core Features

### 🎥 Screen Recording
- Multi-platform support (Windows GDI, macOS AVFoundation, Linux X11)
- Configurable FPS (up to 60+) and resolution (up to 4K)
- FFmpeg-based encoding with multiple codec options
- Pause/resume functionality
- Real-time recording statistics

### 📊 Event Tracking
- **23 event types** covering:
  - File operations (save, create, modify, delete)
  - Editor actions (cursor, selection, completion)
  - IDE operations (tests, builds, debugging)
  - Version control (git commits, push, pull)
- Real-time event monitoring
- Customizable event callbacks
- Event categorization and severity levels

### 🔍 Logical Step Detection
- Auto-detects meaningful steps from event stream
- Intelligent step merging to avoid fragmentation
- Category-based organization (coding, testing, debugging, etc.)
- Automatic descriptive naming
- Timeline statistics and analysis

### 🤖 AI Narration Generation
**LLM Providers:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)
- Google (Gemini Pro)
- Local models (Ollama compatible)

**Text-to-Speech:**
- OpenAI TTS
- Google Cloud TTS
- ElevenLabs
- Local synthesis (pyttsx3)

**Features:**
- Intelligent prompt engineering
- Narration caching for efficiency
- Multi-language support
- Voice customization

### 🎬 Video Processing
**Transitions** (6 types):
- Fade, dissolve, slide left/right, wipe, cut

**Effects & Enhancement:**
- Text overlays (customizable position, font, color)
- Caption/subtitle support (SRT, VTT)
- Color correction (brightness, contrast)
- Audio mixing and normalization

**Export Formats:**
- Multiple quality options: 480p, 720p, 1080p, 4K
- Multiple formats: MP4, WebM, MOV
- Codec selection: H.264, VP9, etc.

**Video Operations:**
- Trim to time range
- Concatenate multiple videos
- Thumbnail generation
- Metadata embedding

### ▶️ YouTube Integration
- OAuth2 authentication
- Resumable upload protocol (large files)
- Full metadata management:
  - Title, description, tags
  - Custom thumbnail upload
  - Category selection
  - Privacy levels (public, unlisted, private)
- Playlist creation and management
- Video status tracking
- Post-upload metadata editing
- Video deletion capability

### ⚙️ Configuration System
- Dataclass-based configuration
- JSON serialization/deserialization
- Hierarchical sub-configs:
  - Screen capture settings
  - Event tracking options
  - Narration parameters
  - Video processing settings
  - YouTube credentials
- Type-safe with full type hints

## CLI Commands

### Record
```bash
python ide_recorder_cli.py record \
  --output video.mp4 \
  --fps 30 \
  --width 1920 \
  --height 1080 \
  --duration 300
```

### Process
```bash
python ide_recorder_cli.py process \
  --input video.mp4 \
  --output final.mp4 \
  --add-narration \
  --ai-api-key sk-xxx \
  --tts-api-key sk-xxx \
  --quality 1080p
```

### Upload
```bash
python ide_recorder_cli.py upload \
  --video final.mp4 \
  --title "Python Tutorial" \
  --description "Step-by-step walkthrough" \
  --tags python tutorial coding \
  --privacy private \
  --client-id xxx \
  --refresh-token xxx
```

## Python API

### Recording with Event Tracking

```python
from src.ide_recorder import ScreenRecorder, EventTracker
from pathlib import Path

# Create recorder and tracker
recorder = ScreenRecorder(
    output_path="session.mp4",
    fps=30,
    width=1920,
    height=1080
)
events = EventTracker()

# Start recording
recorder.start()
events.start_tracking()

# Track IDE events
events.track_file_saved(Path("main.py"))
events.track_test_run("test_main", passed=True)
events.track_git_commit("Add feature X", files_changed=5)

# Stop
recorder.stop()
events.stop_tracking()

# Get statistics
print(recorder.get_statistics())
print(events.get_statistics())
```

### Detecting Logical Steps

```python
from src.ide_recorder import TimelineManager

timeline = TimelineManager()
steps = timeline.detect_logical_steps(events.events)

for step in steps:
    print(f"{step.name}")
    print(f"  Duration: {step.duration_seconds:.1f}s")
    print(f"  Category: {step.category}")
    print(f"  Events: {len(step.events)}")
```

### Generating Narration

```python
from src.ide_recorder import AInarrator
from src.ide_recorder.narrator import AIProvider, TTSProvider

narrator = AInarrator(
    ai_provider=AIProvider.OPENAI,
    ai_api_key="sk-xxx",
    tts_provider=TTSProvider.OPENAI,
    tts_api_key="sk-xxx"
)

# Generate text narration
narration = narrator.generate_narration_for_step(
    step_name="Implement Feature",
    step_description="Added new database connection",
    events_summary="File saved, 5 tests passed"
)

# Synthesize speech
audio_path = narrator.synthesize_speech(narration)
```

### Processing Video

```python
from src.ide_recorder import VideoProcessor
from src.ide_recorder.video_processor import Transition, TransitionType, TextOverlay, OverlayPosition

processor = VideoProcessor(
    input_video="session.mp4",
    output_path="final.mp4"
)

# Add narration
processor.add_narration(audio_path, volume=0.8)

# Add transitions
transitions = [
    Transition(TransitionType.FADE, duration_ms=500),
    Transition(TransitionType.DISSOLVE, duration_ms=300)
]
processor.add_transitions(transitions)

# Add text overlay
overlay = TextOverlay(
    text="Implementing Feature X",
    position=OverlayPosition.BOTTOM,
    duration_ms=3000,
    font_size=32
)
processor.add_text_overlay(overlay, start_time_ms=0)

# Export
output = processor.export(quality="1080p")
```

### Uploading to YouTube

```python
from src.ide_recorder import YouTubeUploader
from src.ide_recorder.uploader import VideoMetadata, PrivacyLevel

uploader = YouTubeUploader(
    refresh_token="xxx",
    channel_id="UCxxxxx"
)

# Authenticate
if uploader.authenticate():
    # Prepare metadata
    metadata = VideoMetadata(
        title="Python Tutorial: Advanced Decorators",
        description="Learn about Python decorators with live coding examples",
        tags=["python", "tutorial", "decorators"],
        privacy_level=PrivacyLevel.PRIVATE
    )
    
    # Upload
    video_id = uploader.upload_video(Path("final.mp4"), metadata)
    
    # Get status
    if video_id:
        status = uploader.get_upload_status(video_id)
        print(f"Video: https://youtu.be/{video_id}")
```

## Configuration

### Via Config File (JSON)

```json
{
  "project_name": "my_tutorial",
  "output_directory": "./videos",
  "screen_capture": {
    "fps": 30,
    "resolution": {"width": 1920, "height": 1080},
    "codec": "libx264",
    "bitrate": "5000k"
  },
  "narration": {
    "enabled": true,
    "model": "gpt-4",
    "temperature": 0.7
  },
  "debug_mode": false
}
```

### Via Python

```python
from src.ide_recorder import RecorderConfig
from pathlib import Path

config = RecorderConfig(
    project_name="my_project",
    output_directory=Path("./videos"),
    debug_mode=True
)

# Configure sub-components
config.screen_capture.fps = 60
config.narration.model = "gpt-4"
config.youtube.privacy_level = "private"

# Save/load
config.to_json(Path("config.json"))
loaded_config = RecorderConfig.from_json(Path("config.json"))
```

## Environment Variables

```bash
# AI Providers
export OPENAI_API_KEY="sk-xxx"
export ANTHROPIC_API_KEY="sk-ant-xxx"
export GOOGLE_API_KEY="xxx"

# YouTube
export YOUTUBE_CLIENT_ID="xxx.apps.googleusercontent.com"
export YOUTUBE_REFRESH_TOKEN="xxx"
export YOUTUBE_CHANNEL_ID="UCxxxxx"
```

## Requirements

### Core (Built-in)
- Python 3.9+
- Standard library only

### Optional (Install as needed)
```bash
# AI & Narration
pip install openai anthropic google-generativeai

# Text-to-Speech
pip install google-cloud-texttospeech elevenlabs pyttsx3

# YouTube Integration
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Development
pip install pytest black flake8 mypy isort
```

### System Dependencies
- **FFmpeg** (for screen recording and video processing)
  - Windows: `choco install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

## Documentation

- **IDE_RECORDER_QUICKSTART.md** - Quick start guide with examples
- **IDE_RECORDER_PROJECT.txt** - Comprehensive project documentation
- **IDE_RECORDER_DELIVERY.txt** - Delivery summary and checklist
- **Code docstrings** - In-code documentation for all modules

## Architecture

### Design Principles
- **Modular**: Each component independent and reusable
- **Type-Safe**: 100% type hints throughout
- **Extensible**: Easy to add new providers and features
- **Production-Ready**: Comprehensive error handling and logging
- **Cross-Platform**: Windows, macOS, Linux support

### Component Interactions
```
Recording Phase:
  ScreenRecorder → EventTracker
  
Analysis Phase:
  EventTracker → TimelineManager
  
Narration Phase:
  TimelineManager → AInarrator
  
Processing Phase:
  ScreenRecorder + AInarrator → VideoProcessor
  
Publishing Phase:
  VideoProcessor → YouTubeUploader
```

## Performance Metrics

- **Recording**: Up to 60 FPS at 4K resolution
- **Event Tracking**: Real-time with minimal overhead
- **Narration Generation**: ~5-10 seconds per step
- **Video Export**: ~30% of video duration (depends on quality)
- **Upload**: Resumable, handles network interruptions

## Troubleshooting

### FFmpeg Not Found
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### API Key Issues
- Ensure environment variables are set
- Check API key validity
- Verify API access is enabled

### Recording Quality
- Increase FPS for smoother recordings
- Use higher bitrate for better quality
- Ensure system has adequate CPU/GPU

### Upload Failures
- Check internet connection
- Verify YouTube credentials
- Use `--debug` flag for detailed logs

## Examples

See `IDE_RECORDER_QUICKSTART.md` for:
- Recording tutorial sessions
- Generating AI narration automatically
- Creating professional videos with effects
- Publishing to YouTube

## Contributing

When extending the project:
1. Maintain 100% type coverage
2. Add comprehensive docstrings
3. Include error handling
4. Write tests for new features
5. Follow PEP 8 style guide

## License

[Specify license here]

## Author

IDE Recorder Contributors

---

**Ready to record, narrate, and share your IDE sessions! 🎬**
