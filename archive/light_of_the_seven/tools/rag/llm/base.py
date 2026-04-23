"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate text completion.

        Args:
            prompt: Input prompt
            system: Optional system message
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model-specific parameters

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def stream(self, prompt: str, system: Optional[str] = None, temperature: float = 0.7, **kwargs):
        """Stream text generation.

        Args:
            prompt: Input prompt
            system: Optional system message
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Yields:
            Text chunks as they are generated
        """
        pass
