"""Configuration for RAG system."""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ModelMode(str, Enum):
    """Model execution mode."""

    LOCAL = "local"  # Use local Ollama models
    CLOUD = "cloud"  # Use cloud Ollama models


@dataclass
class RAGConfig:
    """Configuration for RAG system."""

    # Embedding configuration
    embedding_model: str = "nomic-embed-text-v2-moe:latest"
    embedding_mode: ModelMode = ModelMode.LOCAL

    # LLM configuration
    llm_model_local: str = "ministral"  # Default local model
    llm_model_cloud: Optional[str] = None  # Cloud model if using cloud mode
    llm_mode: ModelMode = ModelMode.LOCAL

    # Vector store configuration
    vector_store_path: str = ".rag_db"
    collection_name: str = "grid_knowledge_base"

    # Ollama configuration
    ollama_base_url: str = "http://localhost:11434"  # Local Ollama
    ollama_cloud_url: Optional[str] = None  # Cloud Ollama URL if using cloud

    # Chunking configuration
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Retrieval configuration
    top_k: int = 5
    similarity_threshold: float = 0.0

    @classmethod
    def from_env(cls) -> "RAGConfig":
        """Create configuration from environment variables."""
        return cls(
            embedding_model=os.getenv("RAG_EMBEDDING_MODEL", "nomic-embed-text-v2"),
            embedding_mode=ModelMode(os.getenv("RAG_EMBEDDING_MODE", "local")),
            llm_model_local=os.getenv("RAG_LLM_MODEL_LOCAL", "ministral"),
            llm_model_cloud=os.getenv("RAG_LLM_MODEL_CLOUD", None),
            llm_mode=ModelMode(os.getenv("RAG_LLM_MODE", "local")),
            vector_store_path=os.getenv("RAG_VECTOR_STORE_PATH", ".rag_db"),
            collection_name=os.getenv("RAG_COLLECTION_NAME", "grid_knowledge_base"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_cloud_url=os.getenv("OLLAMA_CLOUD_URL"),
            chunk_size=int(os.getenv("RAG_CHUNK_SIZE", "500")),
            chunk_overlap=int(os.getenv("RAG_CHUNK_OVERLAP", "50")),
            top_k=int(os.getenv("RAG_TOP_K", "5")),
            similarity_threshold=float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.0")),
        )

    def ensure_local_only(self) -> None:
        """Ensure configuration is set for local-only operation."""
        if self.embedding_mode == ModelMode.CLOUD:
            raise ValueError(
                "Cloud embedding mode not allowed. Set RAG_EMBEDDING_MODE=local or use local mode."
            )
        if self.llm_mode == ModelMode.CLOUD and not self.ollama_cloud_url:
            raise ValueError(
                "Cloud LLM mode requires OLLAMA_CLOUD_URL to be set. "
                "For local-only operation, set RAG_LLM_MODE=local"
            )
