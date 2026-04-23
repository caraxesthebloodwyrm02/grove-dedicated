"""Repository indexing functionality for RAG."""

import os
from pathlib import Path
from typing import List, Optional, Set

from .embeddings.base import BaseEmbeddingProvider
from .vector_store.base import BaseVectorStore


def read_file_content(path: Path, max_size: int = 1024 * 1024) -> Optional[str]:
    """Read file content with size limit."""
    try:
        if path.stat().st_size > max_size:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    separator: str = "\n\n",
    max_chunk_size: int = 8000,  # Maximum safe size for embedding models
) -> List[str]:
    """Split text into overlapping chunks."""
    if not text:
        return []

    # Split by separator first
    sections = text.split(separator)
    chunks = []
    current_chunk = ""

    for section in sections:
        # If adding this section would exceed chunk_size, start a new chunk
        if len(current_chunk) + len(section) + len(separator) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep overlap from previous chunk
            words = current_chunk.split()
            overlap_words = words[-overlap:] if len(words) > overlap else words
            current_chunk = " ".join(overlap_words) + separator + section
        else:
            if current_chunk:
                current_chunk += separator + section
            else:
                current_chunk = section

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Ensure no chunk exceeds max_chunk_size (for embedding model limits)
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_chunk_size:
            # Split oversized chunks further
            words = chunk.split()
            current_subchunk = ""
            for word in words:
                if len(current_subchunk) + len(word) + 1 > max_chunk_size and current_subchunk:
                    final_chunks.append(current_subchunk.strip())
                    current_subchunk = word
                else:
                    current_subchunk += " " + word if current_subchunk else word
            if current_subchunk:
                final_chunks.append(current_subchunk.strip())
        else:
            final_chunks.append(chunk)

    return final_chunks


def is_text_file(path: Path, text_extensions: Set[str]) -> bool:
    """Check if file is likely a text file."""
    # Check extension
    if path.suffix.lower() in text_extensions:
        return True

    # Check for common text files without extension
    if path.name.lower() in {"readme", "license", "changelog", "dockerfile"}:
        return True

    # Check for shebang
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline(100)
            return first_line.startswith("#!")
    except Exception:
        return False


def index_repository(
    repo_path: str,
    store_path: Optional[str] = None,
    chunk_size: int = 500,
    overlap: int = 50,
    rebuild: bool = False,
    embedding_provider: Optional[BaseEmbeddingProvider] = None,
    exclude_dirs: Optional[List[str]] = None,
    include_patterns: Optional[List[str]] = None,
    vector_store: Optional[BaseVectorStore] = None,
) -> BaseVectorStore:
    """Index a repository into a vector store.

    Args:
        repo_path: Path to the repository to index
        store_path: Path to save/load the vector store (deprecated, use vector_store)
        chunk_size: Maximum size of each chunk in characters
        overlap: Number of characters to overlap between chunks
        rebuild: Whether to rebuild the index even if store exists
        embedding_provider: Provider for generating embeddings (must return dense vectors)
        exclude_dirs: Directory names to exclude
        include_patterns: File patterns to include (glob patterns)
        vector_store: Vector store instance to use (if None, creates ChromaDB store)

    Returns:
        VectorStore with indexed documents
    """
    from .embeddings.simple import SimpleEmbedding
    from .vector_store.chromadb_store import ChromaDBVectorStore

    repo = Path(repo_path)
    if not repo.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    # Default exclude directories
    if exclude_dirs is None:
        exclude_dirs = {
            ".git",
            ".svn",
            ".hg",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "node_modules",
            ".venv",
            "venv",
            ".env",
            ".idea",
            ".vscode",
            "dist",
            "build",
            ".tox",
            ".rag_db",
        }

    # Default text file extensions
    text_extensions = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".md",
        ".txt",
        ".rst",
        ".yml",
        ".yaml",
        ".json",
        ".xml",
        ".html",
        ".css",
        ".sql",
        ".sh",
        ".bat",
        ".ps1",
        ".cfg",
        ".ini",
        ".toml",
        ".lock",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".rb",
        ".swift",
        ".kt",
        ".scala",
        ".r",
        ".m",
        ".pl",
        ".lua",
        ".vim",
        ".el",
        ".lisp",
        ".hs",
        ".ml",
    }

    # Initialize vector store
    if vector_store is None:
        vector_store = ChromaDBVectorStore()

    # Check if store has documents and rebuild is False
    if not rebuild and vector_store.count() > 0:
        print(f"Using existing vector store with {vector_store.count()} documents")
        if not rebuild:
            return vector_store

    if rebuild:
        vector_store.reset()
        print("Rebuilding index...")

    print(f"Indexing repository: {repo_path}")

    # Walk the repository
    chunk_ids = []
    chunk_texts = []
    chunk_metadatas = []

    for root, dirs, files in os.walk(repo):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = Path(root) / file

            # Check if file matches include patterns
            if include_patterns:
                if not any(file_path.match(pattern) for pattern in include_patterns):
                    continue

            # Check if it's a text file
            if not is_text_file(file_path, text_extensions):
                continue

            # Read file content
            content = read_file_content(file_path)
            if content is None or not content.strip():
                continue

            # Create relative path
            rel_path = file_path.relative_to(repo)

            # Chunk the document
            text_chunks = chunk_text(content, chunk_size, overlap)

            for i, chunk_text_content in enumerate(text_chunks):
                chunk_id = f"{rel_path}#{i}"
                chunk_ids.append(chunk_id)
                chunk_texts.append(chunk_text_content)
                chunk_metadatas.append(
                    {
                        "path": str(rel_path),
                        "chunk_index": i,
                        "type": "chunk",
                        "file_size": len(content),
                    }
                )

    print(f"Created {len(chunk_texts)} chunks from repository")

    # Generate embeddings
    if embedding_provider is None:
        print("Warning: No embedding provider provided, using simple fallback")
        embedding_provider = SimpleEmbedding()

    print(f"Generating embeddings using {embedding_provider.__class__.__name__}...")

    # Filter out chunks that are too long (will be handled by embedding provider, but warn)
    long_chunks = [i for i, text in enumerate(chunk_texts) if len(text) > 8000]
    if long_chunks:
        print(f"Warning: {len(long_chunks)} chunks exceed 8000 chars and will be truncated")

    # Generate embeddings with error handling
    embeddings_list = []
    valid_indices = []

    for i, text in enumerate(chunk_texts):
        try:
            emb = embedding_provider.embed(text)
            if isinstance(emb, list):
                embeddings_list.append(emb)
            else:
                # Convert numpy array to list
                embeddings_list.append(emb.tolist() if hasattr(emb, "tolist") else list(emb))
            valid_indices.append(i)
        except Exception as e:
            error_str = str(e).lower()
            if "context length" in error_str or "exceeds" in error_str:
                print(f"Warning: Skipping chunk {i} (length: {len(text)} chars) - too long")
                # Skip this chunk - don't add to valid_indices
                continue
            else:
                raise  # Re-raise other errors

    # Filter lists to only include valid chunks
    if len(valid_indices) < len(chunk_texts):
        print(f"Info: Processed {len(valid_indices)}/{len(chunk_texts)} chunks successfully")
        chunk_ids = [chunk_ids[i] for i in valid_indices]
        chunk_texts = [chunk_texts[i] for i in valid_indices]
        chunk_metadatas = [chunk_metadatas[i] for i in valid_indices]

    # Add to vector store in batches to avoid memory issues
    batch_size = 100
    for i in range(0, len(chunk_ids), batch_size):
        batch_ids = chunk_ids[i : i + batch_size]
        batch_texts = chunk_texts[i : i + batch_size]
        batch_embeddings = embeddings_list[i : i + batch_size]
        batch_metadatas = chunk_metadatas[i : i + batch_size]

        vector_store.add(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas,
        )

        if (i // batch_size + 1) % 10 == 0:
            print(f"Indexed {min(i + batch_size, len(chunk_ids))} chunks...")

    print(f"Indexing completed. Total documents: {vector_store.count()}")
    return vector_store


def update_index(
    repo_path: str,
    vector_store: BaseVectorStore,
    embedding_provider: Optional[BaseEmbeddingProvider] = None,
) -> BaseVectorStore:
    """Update an existing index with new/modified files."""
    # This is a placeholder for incremental updates
    # For now, just rebuild the entire index
    return index_repository(
        repo_path=repo_path,
        embedding_provider=embedding_provider,
        rebuild=True,
        vector_store=vector_store,
    )
