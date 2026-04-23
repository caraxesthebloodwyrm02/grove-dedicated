"""
narrator.py - AI-powered narration generation for recording steps.

Generates descriptive narration for each logical step using LLM APIs.
Supports multiple providers (OpenAI, Anthropic, Google) and text-to-speech synthesis.

Features:
- Auto-detection of what happened in each step
- Natural language narration generation
- Text-to-speech synthesis
- Multiple voice options and languages
- Caching of generated narrations
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """Supported AI providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"


class TTSProvider(Enum):
    """Supported text-to-speech providers."""

    OPENAI = "openai"
    GOOGLE = "google"
    ELEVENLABS = "elevenlabs"
    LOCAL = "local"


@dataclass
class NarrationSegment:
    """Represents a single narration segment."""

    step_number: int
    text: str
    duration_seconds: float
    audio_path: Optional[Path] = None
    language: str = "en"


class AInarrator:
    """Generates AI-powered narration for recording steps."""

    def __init__(
        self,
        ai_provider: AIProvider = AIProvider.OPENAI,
        ai_api_key: str = "",
        tts_provider: TTSProvider = TTSProvider.OPENAI,
        tts_api_key: str = "",
        cache_dir: Optional[Path] = None,
        debug: bool = False,
    ):
        """Initialize AI narrator.

        Args:
            ai_provider: Which AI service to use for text generation.
            ai_api_key: API key for AI provider.
            tts_provider: Which TTS service to use.
            tts_api_key: API key for TTS provider.
            cache_dir: Directory to cache generated narrations.
            debug: Enable debug logging.
        """
        self.ai_provider = ai_provider
        self.ai_api_key = ai_api_key
        self.tts_provider = tts_provider
        self.tts_api_key = tts_api_key
        self.cache_dir = cache_dir or Path("./narration_cache")
        self.debug = debug

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Narrator initialized: {ai_provider.value} + {tts_provider.value}")

    def generate_narration_for_step(
        self, step_name: str, step_description: str, events_summary: str
    ) -> str:
        """Generate narration text for a step.

        Args:
            step_name: Name of the step.
            step_description: Description of what happened.
            events_summary: Summary of events in the step.

        Returns:
            Generated narration text.
        """
        # Create prompt for LLM
        prompt = self._create_narration_prompt(step_name, step_description, events_summary)

        # Check cache first
        cache_key = hash(prompt) % (10 ** 8)
        cached = self._load_from_cache(cache_key)
        if cached:
            logger.debug(f"Loaded narration from cache: {cache_key}")
            return cached

        # Generate narration
        narration = self._call_ai_provider(prompt)

        # Cache result
        self._save_to_cache(cache_key, narration)

        return narration

    def synthesize_speech(self, text: str, voice: str = "default") -> Path:
        """Convert narration text to speech.

        Args:
            text: Text to synthesize.
            voice: Voice variant to use.

        Returns:
            Path to generated audio file.
        """
        # Check cache for audio
        audio_hash = hash(f"{text}_{voice}") % (10 ** 8)
        cached_audio = self.cache_dir / f"audio_{audio_hash}.mp3"

        if cached_audio.exists():
            logger.debug(f"Using cached audio: {cached_audio}")
            return cached_audio

        # Generate speech
        audio_path = self._call_tts_provider(text, voice)

        return audio_path

    def _create_narration_prompt(
        self, step_name: str, step_description: str, events_summary: str
    ) -> str:
        """Create prompt for narration generation.

        Args:
            step_name: Step name.
            step_description: Step description.
            events_summary: Events summary.

        Returns:
            Formatted prompt.
        """
        return f"""Generate a concise, professional narration for this IDE step:

Step: {step_name}
Description: {step_description}
Events: {events_summary}

Requirements:
- 1-3 sentences maximum
- Natural and conversational tone
- Explain what was accomplished
- Avoid technical jargon where possible
- Start with an action verb

Narration:"""

    def _call_ai_provider(self, prompt: str) -> str:
        """Call AI provider for text generation.

        Args:
            prompt: Prompt to send to AI.

        Returns:
            Generated text.
        """
        if self.ai_provider == AIProvider.OPENAI:
            return self._call_openai(prompt)
        elif self.ai_provider == AIProvider.ANTHROPIC:
            return self._call_anthropic(prompt)
        elif self.ai_provider == AIProvider.GOOGLE:
            return self._call_google(prompt)
        elif self.ai_provider == AIProvider.LOCAL:
            return self._call_local(prompt)
        else:
            return "Unable to generate narration"

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API.

        Args:
            prompt: Prompt text.

        Returns:
            Generated completion.
        """
        if not self.ai_api_key:
            logger.warning("OpenAI API key not configured")
            return f"[Placeholder narration for: {prompt[:50]}]"

        try:
            import openai

            openai.api_key = self.ai_api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"[Error: {str(e)[:50]}]"

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API.

        Args:
            prompt: Prompt text.

        Returns:
            Generated completion.
        """
        if not self.ai_api_key:
            logger.warning("Anthropic API key not configured")
            return f"[Placeholder narration for: {prompt[:50]}]"

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.ai_api_key)
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return f"[Error: {str(e)[:50]}]"

    def _call_google(self, prompt: str) -> str:
        """Call Google Generative AI API.

        Args:
            prompt: Prompt text.

        Returns:
            Generated completion.
        """
        if not self.ai_api_key:
            logger.warning("Google API key not configured")
            return f"[Placeholder narration for: {prompt[:50]}]"

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.ai_api_key)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt, safety_settings=[])
            return response.text.strip()
        except Exception as e:
            logger.error(f"Google API error: {e}")
            return f"[Error: {str(e)[:50]}]"

    def _call_local(self, prompt: str) -> str:
        """Use local model (e.g., Ollama).

        Args:
            prompt: Prompt text.

        Returns:
            Generated completion.
        """
        logger.info("Using local model for narration generation")
        # Placeholder for local model integration (Ollama, LLaMA, etc.)
        return f"[Local narration for: {prompt[:50]}...]"

    def _call_tts_provider(self, text: str, voice: str) -> Path:
        """Call TTS provider.

        Args:
            text: Text to synthesize.
            voice: Voice name.

        Returns:
            Path to audio file.
        """
        if self.tts_provider == TTSProvider.OPENAI:
            return self._tts_openai(text, voice)
        elif self.tts_provider == TTSProvider.GOOGLE:
            return self._tts_google(text, voice)
        elif self.tts_provider == TTSProvider.ELEVENLABS:
            return self._tts_elevenlabs(text, voice)
        elif self.tts_provider == TTSProvider.LOCAL:
            return self._tts_local(text, voice)
        else:
            return Path("./placeholder.mp3")

    def _tts_openai(self, text: str, voice: str) -> Path:
        """Synthesize speech using OpenAI TTS.

        Args:
            text: Text to synthesize.
            voice: Voice name.

        Returns:
            Path to audio file.
        """
        if not self.tts_api_key:
            logger.warning("OpenAI TTS API key not configured")
            return Path("./placeholder.mp3")

        try:
            import openai

            openai.api_key = self.tts_api_key
            output_path = self.cache_dir / f"audio_{hash(text) % (10**8)}.mp3"

            response = openai.Audio.create(
                model="tts-1",
                voice=voice or "alloy",
                input=text,
            )

            with open(output_path, "wb") as f:
                f.write(response.content)

            return output_path
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return Path("./placeholder.mp3")

    def _tts_google(self, text: str, voice: str) -> Path:
        """Synthesize speech using Google TTS.

        Args:
            text: Text to synthesize.
            voice: Voice name.

        Returns:
            Path to audio file.
        """
        if not self.tts_api_key:
            logger.warning("Google TTS API key not configured")
            return Path("./placeholder.mp3")

        try:
            from google.cloud import texttospeech

            client = texttospeech.TextToSpeechClient()
            input_text = texttospeech.SynthesisInput(text=text)
            voice_obj = texttospeech.VoiceSelectionParams(language_code="en-US")
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = client.synthesize_speech(
                request={"input": input_text, "voice": voice_obj, "audio_config": audio_config}
            )

            output_path = self.cache_dir / f"audio_{hash(text) % (10**8)}.mp3"
            with open(output_path, "wb") as f:
                f.write(response.audio_content)

            return output_path
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return Path("./placeholder.mp3")

    def _tts_elevenlabs(self, text: str, voice: str) -> Path:
        """Synthesize speech using ElevenLabs TTS.

        Args:
            text: Text to synthesize.
            voice: Voice name.

        Returns:
            Path to audio file.
        """
        logger.info("ElevenLabs TTS not yet implemented")
        return Path("./placeholder.mp3")

    def _tts_local(self, text: str, voice: str) -> Path:
        """Synthesize speech using local TTS.

        Args:
            text: Text to synthesize.
            voice: Voice name.

        Returns:
            Path to audio file.
        """
        logger.info("Local TTS (pyttsx3/espeak) not yet implemented")
        return Path("./placeholder.mp3")

    def _load_from_cache(self, cache_key: int) -> Optional[str]:
        """Load narration from cache.

        Args:
            cache_key: Cache key.

        Returns:
            Cached narration or None.
        """
        cache_file = self.cache_dir / f"narration_{cache_key}.txt"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Cache read error: {e}")
        return None

    def _save_to_cache(self, cache_key: int, text: str) -> None:
        """Save narration to cache.

        Args:
            cache_key: Cache key.
            text: Text to cache.
        """
        cache_file = self.cache_dir / f"narration_{cache_key}.txt"
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            logger.error(f"Cache write error: {e}")
