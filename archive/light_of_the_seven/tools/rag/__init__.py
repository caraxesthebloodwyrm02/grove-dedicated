"""
RAG (Retrieval-Augmented Generation) module for GRID.

Heavy optional deps (Chroma, embeddings) load on first attribute access, so
`import tools.rag.config` and `import tools.rag.llm` work without a full
vector store install.
"""
from __future__ import annotations

import typing as t
from importlib import import_module

# Lightweight, always available
from .config import ModelMode, RAGConfig

if t.TYPE_CHECKING:
    from .embeddings import NomicEmbeddingV2, get_embedding_provider
    from .indexer import chunk_text, index_repository, read_file_content
    from .llm import OllamaLocalLLM, get_llm_provider
    from .rag_engine import RAGEngine
    from .vector_store import ChromaDBVectorStore

__all__ = [
    "RAGEngine",
    "RAGConfig",
    "ModelMode",
    "get_embedding_provider",
    "NomicEmbeddingV2",
    "get_llm_provider",
    "OllamaLocalLLM",
    "ChromaDBVectorStore",
    "index_repository",
    "chunk_text",
    "read_file_content",
]

__version__ = "2.0.0"

_LAZY: dict[str, tuple[str, str]] = {
    "NomicEmbeddingV2": (".embeddings", "NomicEmbeddingV2"),
    "get_embedding_provider": (".embeddings", "get_embedding_provider"),
    "chunk_text": (".indexer", "chunk_text"),
    "index_repository": (".indexer", "index_repository"),
    "read_file_content": (".indexer", "read_file_content"),
    "OllamaLocalLLM": (".llm", "OllamaLocalLLM"),
    "get_llm_provider": (".llm", "get_llm_provider"),
    "RAGEngine": (".rag_engine", "RAGEngine"),
    "ChromaDBVectorStore": (".vector_store", "ChromaDBVectorStore"),
}


def __getattr__(name: str) -> t.Any:  # noqa: ANN401
    if name in _LAZY:
        mod_path, sym = _LAZY[name]
        sub = import_module(mod_path, __name__)
        return getattr(sub, sym)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> list[str]:
    return sorted(__all__)
