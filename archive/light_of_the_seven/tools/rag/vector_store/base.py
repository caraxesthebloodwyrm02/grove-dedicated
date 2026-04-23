"""Base vector store interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseVectorStore(ABC):
    """Base interface for vector stores."""

    @abstractmethod
    def add(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add documents with embeddings to the store.

        Args:
            ids: Document IDs
            documents: Document texts
            embeddings: Dense embedding vectors
            metadatas: Optional metadata for each document
        """
        pass

    @abstractmethod
    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query the vector store.

        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            where: Optional metadata filter
            include: Optional list of fields to include

        Returns:
            Dictionary with 'ids', 'documents', 'metadatas', 'distances'
        """
        pass

    @abstractmethod
    def delete(
        self, ids: Optional[List[str]] = None, where: Optional[Dict[str, Any]] = None
    ) -> None:
        """Delete documents from the store.

        Args:
            ids: Optional list of IDs to delete
            where: Optional metadata filter
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Get the number of documents in the store.

        Returns:
            Number of documents
        """
        pass
