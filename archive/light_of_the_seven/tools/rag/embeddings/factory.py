"""Factory for creating embedding providers."""

from enum import Enum
from typing import Optional

from ..config import RAGConfig
from .base import BaseEmbeddingProvider
from .nomic_v2 import NomicEmbeddingV2


class EmbeddingProviderType(str, Enum):
    """Types of embedding providers."""

    NOMIC_V2 = "nomic-v2"  # nomic-embed-text-v2 (default, recommended)
    SIMPLE = "simple"  # Simple fallback (word frequency)


def get_embedding_provider(
    provider_type: Optional[str] = None, config: Optional[RAGConfig] = None
) -> BaseEmbeddingProvider:
    """Get an embedding provider.

    Args:
        provider_type: Type of provider (default: nomic-v2)
        config: RAG configuration (optional)

    Returns:
        Embedding provider instance
    """
    if config is None:
        config = RAGConfig.from_env()

    if provider_type is None:
        provider_type = EmbeddingProviderType.NOMIC_V2.value

    provider_type = provider_type.lower()

    if provider_type == EmbeddingProviderType.NOMIC_V2.value:
        return NomicEmbeddingV2(model=config.embedding_model, base_url=config.ollama_base_url)
    elif provider_type == EmbeddingProviderType.SIMPLE.value:
        from .simple import SimpleEmbedding

        return SimpleEmbedding()
    else:
        raise ValueError(
            f"Unknown embedding provider type: {provider_type}. "
            f"Available: {', '.join([e.value for e in EmbeddingProviderType])}"
        )
