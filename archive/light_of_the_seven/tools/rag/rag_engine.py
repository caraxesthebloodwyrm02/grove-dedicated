"""Unified RAG engine orchestrating embedding, retrieval, and generation."""

from typing import Any, Dict, List, Optional

from .config import RAGConfig
from .embeddings.factory import get_embedding_provider
from .indexer import index_repository
from .llm.factory import get_llm_provider
from .vector_store.chromadb_store import ChromaDBVectorStore


class RAGEngine:
    """Unified RAG engine for querying project knowledge base.

    Orchestrates embedding, retrieval, and generation with proper local-only operation.
    """

    def __init__(self, config: Optional[RAGConfig] = None):
        """Initialize RAG engine.

        Args:
            config: RAG configuration (default: from environment)
        """
        from .utils import check_ollama_connection, find_embedding_model, find_llm_model

        if config is None:
            config = RAGConfig.from_env()

        # Ensure local-only operation
        config.ensure_local_only()

        # Check Ollama connection
        if not check_ollama_connection(config.ollama_base_url):
            raise RuntimeError(
                f"Ollama is not running or not accessible at {config.ollama_base_url}.\n"
                f"Please start Ollama: ollama serve\n"
                f"Or check if it's running on a different port."
            )

        # Find available models (don't fail if not found; embedding provider may fallback)
        try:
            available_embedding_model = find_embedding_model(
                preferred=config.embedding_model, base_url=config.ollama_base_url
            )
            if available_embedding_model and available_embedding_model != config.embedding_model:
                print(
                    f"Info: Using '{available_embedding_model}' instead of "
                    f"'{config.embedding_model}'"
                )
                config.embedding_model = available_embedding_model
        except Exception:
            # If we can't check, let the embedding provider handle it with fallbacks
            pass

        try:
            available_llm_model = find_llm_model(
                preferred=config.llm_model_local, base_url=config.ollama_base_url
            )
            if available_llm_model and available_llm_model != config.llm_model_local:
                print(f"Info: Using '{available_llm_model}' instead of '{config.llm_model_local}'")
                config.llm_model_local = available_llm_model
        except Exception:
            # If we can't check, let the LLM provider handle it
            pass

        self.config = config

        # Initialize components
        self.embedding_provider = get_embedding_provider(config=config)
        self.llm_provider = get_llm_provider(config=config)
        self.vector_store = ChromaDBVectorStore(
            collection_name=config.collection_name, persist_directory=config.vector_store_path
        )

    def index(
        self,
        repo_path: str,
        rebuild: bool = False,
        exclude_dirs: Optional[List[str]] = None,
        include_patterns: Optional[List[str]] = None,
    ) -> None:
        """Index a repository.

        Args:
            repo_path: Path to repository
            rebuild: Whether to rebuild index
            exclude_dirs: Optional directories to exclude
            include_patterns: Optional file patterns to include
        """
        # Use the refactored indexer

        index_repository(
            repo_path=repo_path,
            store_path=None,  # We use ChromaDB directly
            chunk_size=self.config.chunk_size,
            overlap=self.config.chunk_overlap,
            rebuild=rebuild,
            embedding_provider=self.embedding_provider,
            exclude_dirs=exclude_dirs,
            include_patterns=include_patterns,
            vector_store=self.vector_store,
        )

    def query(
        self,
        query_text: str,
        top_k: Optional[int] = None,
        temperature: float = 0.7,
        include_sources: bool = True,
    ) -> Dict[str, Any]:
        """Query the RAG system.

        Args:
            query_text: Query text
            top_k: Number of documents to retrieve (default: from config)
            temperature: LLM temperature
            include_sources: Whether to include source documents

        Returns:
            Dictionary with 'answer', 'sources', 'context'
        """
        top_k = top_k or self.config.top_k

        # Generate query embedding
        query_embedding = self.embedding_provider.embed(query_text)

        # Retrieve relevant documents
        results = self.vector_store.query(query_embedding=query_embedding, n_results=top_k)

        if not results["documents"]:
            return {
                "answer": "No relevant documents found in the knowledge base.",
                "sources": [],
                "context": "",
            }

        # Build context from retrieved documents
        context_parts = []
        sources = []

        for i, (doc, metadata, distance) in enumerate(
            zip(
                results["documents"],
                results["metadatas"],
                results["distances"],
                strict=True,
            )
        ):
            source_info = {"index": i + 1, "distance": distance, "metadata": metadata}
            sources.append(source_info)

            context_parts.append(f"[{i + 1}] {doc}")

        context = "\n\n".join(context_parts)

        # Generate answer using LLM
        prompt = f"""Based on the following context, answer the query.

Context:
{context}

Query: {query_text}

Answer:"""

        answer = self.llm_provider.generate(prompt=prompt, temperature=temperature)

        result = {
            "answer": answer,
            "context": context if include_sources else "",
        }

        if include_sources:
            result["sources"] = sources

        return result

    def add_documents(
        self,
        documents: List[str],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add documents directly to the vector store.

        Args:
            documents: List of document texts
            ids: Optional document IDs
            metadatas: Optional metadata for each document
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        # Generate embeddings
        embeddings = self.embedding_provider.embed_batch(documents)

        # Add to vector store
        self.vector_store.add(
            ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base.

        Returns:
            Dictionary with statistics
        """
        return {
            "document_count": self.vector_store.count(),
            "collection_name": self.config.collection_name,
            "embedding_model": self.config.embedding_model,
            "llm_model": self.config.llm_model_local
            if self.config.llm_mode.value == "local"
            else self.config.llm_model_cloud,
        }
