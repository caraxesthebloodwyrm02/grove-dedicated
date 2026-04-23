"""ChromaDB vector store implementation."""

from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings

from .base import BaseVectorStore


class ChromaDBVectorStore(BaseVectorStore):
    """ChromaDB-based vector store with proper dense embeddings.

    Uses ChromaDB for persistence and efficient similarity search.
    """

    def __init__(
        self,
        collection_name: str = "grid_knowledge_base",
        persist_directory: str = ".rag_db",
        embedding_function=None,
    ):
        """Initialize ChromaDB vector store.

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist data
            embedding_function: Optional embedding function (for ChromaDB's built-in)
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory, settings=Settings(anonymized_telemetry=False, allow_reset=True)
        )

        # Get or create collection
        # Note: We'll handle embeddings ourselves, so we don't pass embedding_function
        # to the collection - we'll add pre-computed embeddings
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except Exception:
            # Collection doesn't exist, create it
            # We'll use add with embeddings directly
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},  # Use cosine similarity
            )

    def add(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add documents with embeddings to ChromaDB.

        Args:
            ids: Document IDs
            documents: Document texts
            embeddings: Dense embedding vectors
            metadatas: Optional metadata for each document
        """
        if not (len(ids) == len(documents) == len(embeddings)):
            raise ValueError("ids, documents, and embeddings must have same length")

        if metadatas is None:
            metadatas = [{}] * len(documents)
        elif len(metadatas) != len(documents):
            raise ValueError("metadatas must have same length as documents")

        # ChromaDB expects embeddings as list of lists
        self.collection.add(
            ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas
        )

    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query ChromaDB with embedding.

        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            where: Optional metadata filter
            include: Optional list of fields to include (default: all)

        Returns:
            Dictionary with 'ids', 'documents', 'metadatas', 'distances'
        """
        if include is None:
            include = ["documents", "metadatas", "distances"]

        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=n_results, where=where, include=include
        )

        # ChromaDB returns lists of lists (one per query), so we extract first result
        return {
            "ids": results["ids"][0] if results["ids"] else [],
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
        }

    def delete(
        self, ids: Optional[List[str]] = None, where: Optional[Dict[str, Any]] = None
    ) -> None:
        """Delete documents from ChromaDB.

        Args:
            ids: Optional list of IDs to delete
            where: Optional metadata filter
        """
        if ids:
            self.collection.delete(ids=ids)
        elif where:
            self.collection.delete(where=where)
        else:
            raise ValueError("Must provide either ids or where filter")

    def count(self) -> int:
        """Get the number of documents in the collection.

        Returns:
            Number of documents
        """
        return self.collection.count()

    def reset(self) -> None:
        """Reset the collection (delete all documents)."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name, metadata={"hnsw:space": "cosine"}
        )
