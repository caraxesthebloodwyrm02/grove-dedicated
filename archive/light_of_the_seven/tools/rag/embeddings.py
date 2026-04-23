"""Embedding providers for RAG."""

import json
import math
import re
import subprocess
from typing import Dict, List, Optional

from .types import EmbeddingProvider


class OllamaEmbedding(EmbeddingProvider):
    """Wrapper for Ollama's embedding models."""

    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model

    def embed(self, text: str) -> Dict[str, float]:
        """Get embeddings using Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, text],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            # Parse dense vector from output
            vector = json.loads(result.stdout)
            # Convert to sparse dict (keep only significant values)
            return {str(i): v for i, v in enumerate(vector) if abs(v) > 0.01}
        except Exception as e:
            print(f"Ollama embedding error: {e}")
            # Fallback to simple embedding
            return SimpleEmbedding().embed(text)


class SimpleEmbedding(EmbeddingProvider):
    """Simple word frequency and TF-IDF based embedding."""

    def __init__(self, use_tfidf: bool = True):
        self.use_tfidf = use_tfidf
        self.doc_freqs = {}  # For TF-IDF
        self.num_docs = 0

    def embed(self, text: str) -> Dict[str, float]:
        """Generate simple word-based embedding."""
        # Preprocess text
        words = self._tokenize(text.lower())

        if not words:
            return {}

        # Count word frequencies
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        if not self.use_tfidf:
            # Simple frequency
            return word_counts

        # TF-IDF scoring
        if self.num_docs == 0:
            # Initialize with some reasonable IDF values
            # Common words have lower scores
            common_words = {
                "the",
                "a",
                "an",
                "and",
                "or",
                "but",
                "in",
                "on",
                "at",
                "to",
                "for",
                "of",
                "with",
                "by",
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "have",
                "has",
                "had",
                "do",
                "does",
                "did",
                "will",
                "would",
                "could",
                "should",
            }
            self.doc_freqs = {word: 100 for word in common_words}
            self.num_docs = 1000

        # Calculate TF-IDF
        tfidf_scores = {}
        for word, count in word_counts.items():
            tf = count / len(words)  # Term frequency
            idf = math.log(
                self.num_docs / (self.doc_freqs.get(word, 1) + 1)
            )  # Inverse doc frequency
            tfidf_scores[word] = tf * idf

        return tfidf_scores

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        # Split on non-word characters
        tokens = re.findall(r"\b\w+\b", text)
        # Filter out very short tokens
        return [t for t in tokens if len(t) > 2]

    def update_doc_freqs(self, docs: List[str]) -> None:
        """Update document frequencies for better TF-IDF."""
        self.doc_freqs = {}
        self.num_docs = len(docs)

        for doc in docs:
            words = set(self._tokenize(doc.lower()))
            for word in words:
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1


class OpenAIEmbedding(EmbeddingProvider):
    """Wrapper for OpenAI's embedding API."""

    def __init__(self, model: str = "text-embedding-ada-002", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key

    def embed(self, text: str) -> Dict[str, float]:
        """Get embeddings using OpenAI API."""
        try:
            import openai

            if self.api_key:
                openai.api_key = self.api_key

            response = openai.Embedding.create(model=self.model, input=text)
            vector = response["data"][0]["embedding"]
            # Convert to sparse dict
            return {str(i): v for i, v in enumerate(vector) if abs(v) > 0.01}
        except Exception as e:
            print(f"OpenAI embedding error: {e}")
            return SimpleEmbedding().embed(text)


class HuggingFaceEmbedding(EmbeddingProvider):
    """Wrapper for Hugging Face sentence transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the Hugging Face model."""
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(self.model_name)
        except ImportError:
            print("sentence_transformers not installed. Use: pip install sentence-transformers")
            self.model = None
        except Exception as e:
            print(f"Failed to load Hugging Face model: {e}")
            self.model = None

    def embed(self, text: str) -> Dict[str, float]:
        """Get embeddings using Hugging Face model."""
        if self.model is None:
            return SimpleEmbedding().embed(text)

        try:
            vector = self.model.encode(text).tolist()
            # Convert to sparse dict
            return {str(i): v for i, v in enumerate(vector) if abs(v) > 0.01}
        except Exception as e:
            print(f"Hugging Face embedding error: {e}")
            return SimpleEmbedding().embed(text)


def get_embedding_provider(provider_type: str = "simple", **kwargs) -> EmbeddingProvider:
    """Get an embedding provider by type.

    Args:
        provider_type: Type of provider ("simple", "ollama", "openai", "huggingface")
        **kwargs: Additional arguments for the provider

    Returns:
        EmbeddingProvider instance
    """
    providers = {
        "simple": SimpleEmbedding,
        "ollama": OllamaEmbedding,
        "openai": OpenAIEmbedding,
        "huggingface": HuggingFaceEmbedding,
    }

    if provider_type not in providers:
        raise ValueError(f"Unknown provider type: {provider_type}")

    return providers[provider_type](**kwargs)
