"""GRID RetrievalService — vectorized similarity search over document embeddings.

Replaces the previous naive O(N) Python-loop cosine similarity with numpy-vectorized
batch computation. For a corpus of N documents with embedding dimension D, similarity
computation drops from O(N·D) per query in pure Python to a single numpy matmul —
effectively O(N·D) but with BLAS-level constant factors, yielding ~100-1000× speedup
on typical hardware.

The service implements the RetrievalServiceProtocol expected by PatternEngine
(`retrieve_context(query) -> dict`) and can also be used standalone for any
semantic-search workload within the GRID intelligence layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np  # type: ignore[import-untyped]
import structlog  # type: ignore[import-untyped]

logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class Document:
    """A stored document with its embedding vector and metadata."""

    doc_id: str
    content: str
    embedding: np.ndarray  # shape (dim,)
    metadata: dict[str, Any] = field(default_factory=dict)


class RetrievalService:
    """Vectorized semantic retrieval service for the GRID intelligence layer.

    Stores documents as numpy embedding vectors and performs cosine similarity
    search via matrix multiplication rather than per-document Python loops.

    Usage::

        service = RetrievalService(dim=384)
        service.add_document("doc1", "Example text", embedding_vec)
        results = service.retrieve_context("search query", embed_fn=my_embed_fn)
    """

    def __init__(self, dim: int = 384) -> None:
        """Initialize the retrieval service.

        Args:
            dim: Embedding dimension. Must match the vectors passed to :meth:`add_document`.
        """
        self._dim: int = dim
        self._documents: dict[str, Document] = {}
        self._matrix: np.ndarray | None = None  # shape (N, dim), rebuilt on mutation
        self._doc_ids: list[str] = []  # parallel index for _matrix rows
        self._dirty: bool = True  # whether _matrix needs rebuild
        self._log: Any = logger.bind(component="retrieval_service")

    # ── Index management ────────────────────────────────────────────────

    def add_document(
        self,
        doc_id: str,
        content: str,
        embedding: np.ndarray | list[float],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add or replace a document in the index.

        Args:
            doc_id: Unique document identifier.
            content: Raw document text.
            embedding: Embedding vector of shape ``(dim,)``.
            metadata: Optional metadata dict stored alongside the document.
        """
        vec = np.asarray(embedding, dtype=np.float32)
        if vec.shape != (self._dim,):
            raise ValueError(f"Embedding shape {vec.shape} does not match expected ({self._dim},)")

        self._documents[doc_id] = Document(
            doc_id=doc_id,
            content=content,
            embedding=vec,
            metadata=metadata or {},
        )
        self._dirty = True
        self._log.debug("document_indexed", doc_id=doc_id)

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index.

        Args:
            doc_id: Document to remove.

        Returns:
            ``True`` if the document existed and was removed, ``False`` otherwise.
        """
        if doc_id not in self._documents:
            return False
        del self._documents[doc_id]
        self._dirty = True
        self._log.debug("document_removed", doc_id=doc_id)
        return True

    @property
    def document_count(self) -> int:
        """Number of documents currently in the index."""
        return len(self._documents)

    # ── Matrix rebuild ──────────────────────────────────────────────────

    def _rebuild_matrix(self) -> None:
        """Rebuild the embedding matrix from stored documents.

        Called lazily on first search after any mutation (add/remove).
        The matrix is L2-normalized row-wise so that dot product equals
        cosine similarity directly — no per-query normalization needed.
        """
        if not self._documents:
            self._matrix = None
            self._doc_ids = []
            self._dirty = False
            return

        self._doc_ids = list(self._documents.keys())
        raw = np.stack([self._documents[did].embedding for did in self._doc_ids])

        # L2-normalize rows → dot product = cosine similarity
        norms = np.linalg.norm(raw, axis=1, keepdims=True)
        # Guard against zero vectors
        norms = np.where(norms == 0.0, 1.0, norms)
        self._matrix = raw / norms
        self._dirty = False

        self._log.debug(
            "matrix_rebuilt",
            n_docs=len(self._doc_ids),
            dim=self._dim,
        )

    # ── Vectorized search ───────────────────────────────────────────────

    def search(
        self,
        query_embedding: np.ndarray | list[float],
        top_k: int = 10,
        threshold: float = 0.0,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        """Perform vectorized cosine similarity search.

        Instead of looping over each document and computing cosine similarity
        one at a time (O(N) Python iterations), this method computes all
        similarities in a single numpy matrix multiplication::

            similarities = normalized_matrix @ normalized_query  # shape (N,)

        This leverages BLAS routines and is orders of magnitude faster than
        the naive per-document Python loop.

        Args:
            query_embedding: Query vector of shape ``(dim,)``.
            top_k: Maximum number of results to return.
            threshold: Minimum cosine similarity to include a result.

        Returns:
            List of ``(doc_id, similarity, metadata)`` tuples sorted by
            similarity descending.
        """
        if not self._documents:
            return []

        if self._dirty:
            self._rebuild_matrix()

        if self._matrix is None:
            return []

        query_vec = np.asarray(query_embedding, dtype=np.float32)
        if query_vec.shape != (self._dim,):
            raise ValueError(f"Query embedding shape {query_vec.shape} does not match expected ({self._dim},)")

        # Normalize query vector (matrix rows already normalized)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0.0:
            self._log.warning("zero_query_vector")
            return []
        normalized_query = query_vec / query_norm

        # Vectorized cosine similarity: single matmul → all scores at once
        similarities: np.ndarray = self._matrix @ normalized_query  # shape (N,)

        # Apply threshold filter
        if threshold > 0.0:
            mask = similarities >= threshold
            candidate_indices = np.where(mask)[0]
        else:
            candidate_indices = np.arange(len(similarities))

        if len(candidate_indices) == 0:
            return []

        # Sort by similarity descending, take top_k
        sorted_order = candidate_indices[np.argsort(-similarities[candidate_indices])]
        top_indices = sorted_order[:top_k]

        results: list[tuple[str, float, dict[str, Any]]] = []
        for idx in top_indices:
            idx_int = int(idx)
            doc_id = self._doc_ids[idx_int]
            sim = float(similarities[idx_int])
            doc = self._documents[doc_id]
            results.append((doc_id, sim, doc.metadata))

        self._log.debug(
            "search_complete",
            n_candidates=len(candidate_indices),
            n_returned=len(results),
            top_score=results[0][1] if results else None,
        )

        return results

    # ── Protocol-compatible interface ───────────────────────────────────

    def retrieve_context(
        self,
        query: str,
        embed_fn: Any | None = None,
        top_k: int = 5,
        threshold: float = 0.3,
    ) -> dict[str, Any]:
        """Retrieve context for a query string.

        This method satisfies the ``RetrievalServiceProtocol`` expected by
        :class:`~grid.pattern.engine.PatternEngine`. It requires an ``embed_fn``
        to convert the query string into an embedding vector, then delegates
        to :meth:`search` for the vectorized similarity computation.

        If no ``embed_fn`` is provided and the index is empty, returns an
        empty dict — the caller always gets a usable result.

        Args:
            query: Search query string.
            embed_fn: Callable ``(str) -> np.ndarray`` that embeds text.
                      Required for text-based queries. If ``None`` and the
                      index is populated, a warning is logged and ``{}`` is
                      returned.
            top_k: Number of top results to return.
            threshold: Minimum similarity for inclusion.

        Returns:
            Dict with keys ``documents`` (list of matched content strings),
            ``scores`` (list of floats), and ``metadata`` (list of dicts).
        """
        if not self._documents:
            return {}

        if embed_fn is None:
            self._log.warning("retrieve_context_failed", reason="no_embed_fn")
            return {}

        try:
            query_embedding = embed_fn(query)
        except Exception as exc:
            self._log.error("embed_fn_failed", query=query, error=str(exc))
            return {}

        results = self.search(query_embedding, top_k=top_k, threshold=threshold)

        if not results:
            return {}

        return {
            "documents": [self._documents[did].content for did, _, _ in results],
            "scores": [score for _, score, _ in results],
            "metadata": [meta for _, _, meta in results],
        }

    # ── Diagnostics ─────────────────────────────────────────────────────

    def stats(self) -> dict[str, Any]:
        """Return diagnostic statistics about the index.

        Useful for monitoring and debugging retrieval performance.
        """
        return {
            "document_count": len(self._documents),
            "embedding_dim": self._dim,
            "matrix_built": self._matrix is not None,
            "matrix_dirty": self._dirty,
        }
