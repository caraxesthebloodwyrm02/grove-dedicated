"""Type definitions and protocols for RAG components."""

from typing import Any, Dict, Optional, Protocol


class EmbeddingProvider(Protocol):
    """Protocol for embedding providers."""

    def embed(self, text: str) -> Dict[str, float]:
        """Convert text to embedding vector as sparse dict."""
        ...


class LLMProvider(Protocol):
    """Protocol for LLM providers."""

    def generate(self, prompt: str) -> str:
        """Generate text completion."""
        ...


class Document:
    """Represents a document with metadata."""

    def __init__(self, id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.id = id
        self.text = text
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"id": self.id, "text": self.text, "metadata": self.metadata}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create from dictionary representation."""
        return cls(data["id"], data["text"], data.get("metadata", {}))


class Chunk:
    """Represents a chunk of a document."""

    def __init__(self, id: str, text: str, doc_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.id = id
        self.text = text
        self.doc_id = doc_id
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {"id": self.id, "text": self.text, "doc_id": self.doc_id, "metadata": self.metadata}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chunk":
        """Create from dictionary representation."""
        return cls(data["id"], data["text"], data["doc_id"], data.get("metadata", {}))


class VectorStoreConfig:
    """Configuration for vector store."""

    def __init__(
        self,
        similarity_threshold: float = 0.0,
        max_results: int = 10,
        include_metadata: bool = True,
    ):
        self.similarity_threshold = similarity_threshold
        self.max_results = max_results
        self.include_metadata = include_metadata
