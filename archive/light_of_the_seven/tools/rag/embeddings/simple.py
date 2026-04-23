"""Simple fallback embedding provider."""

import math
import re
from typing import Dict, List

from .base import BaseEmbeddingProvider


class SimpleEmbedding(BaseEmbeddingProvider):
    """Simple word frequency-based embedding (fallback only).

    This is a basic fallback that should not be used for production.
    Use nomic-embed-text-v2 instead.
    """

    def __init__(self, use_tfidf: bool = True):
        """Initialize simple embedding provider.

        Args:
            use_tfidf: Whether to use TF-IDF weighting
        """
        self.use_tfidf = use_tfidf
        self.doc_freqs: Dict[str, int] = {}
        self.num_docs = 0

    def embed(self, text: str) -> List[float]:
        """Generate simple word-based embedding.

        Args:
            text: Input text

        Returns:
            Sparse-like embedding as dense vector (limited vocabulary)
        """
        # Tokenize
        words = self._tokenize(text.lower())

        if not words:
            return [0.0] * 100  # Return zero vector

        # Count word frequencies
        word_counts: Dict[str, int] = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        if not self.use_tfidf:
            # Simple frequency - convert to fixed-size vector
            # This is a very basic implementation
            vocab_size = 100
            embedding = [0.0] * vocab_size
            for i, (_word, count) in enumerate(word_counts.items()):
                if i < vocab_size:
                    embedding[i] = float(count) / len(words)
            return embedding

        # TF-IDF (simplified); guard num_docs==0 to avoid log(0) domain error
        tfidf_scores: Dict[str, float] = {}
        n_docs = max(1, self.num_docs)
        for word, count in word_counts.items():
            tf = count / len(words)
            denom = self.doc_freqs.get(word, 1) + 1
            idf = math.log(n_docs / denom) if (n_docs / denom) > 0 else 0.0
            tfidf_scores[word] = tf * idf

        # Convert to fixed-size vector
        vocab_size = 100
        embedding = [0.0] * vocab_size
        sorted_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (_word, score) in enumerate(sorted_words[:vocab_size]):
            embedding[i] = score

        return embedding

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        tokens = re.findall(r"\b\w+\b", text)
        return [t for t in tokens if len(t) > 2]

    def update_doc_freqs(self, docs: List[str]) -> None:
        """Update document frequencies for TF-IDF."""
        self.doc_freqs = {}
        self.num_docs = len(docs)

        for doc in docs:
            words = set(self._tokenize(doc.lower()))
            for word in words:
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return 100  # Fixed size for simple embedding
