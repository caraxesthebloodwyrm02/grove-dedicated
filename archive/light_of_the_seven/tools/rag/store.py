"""In-memory vector store for document retrieval."""

import json
import math
import pickle
from typing import Any, Dict, List, Optional, Tuple

from .types import LLMProvider, VectorStoreConfig


class VectorStore:
    """In-memory vector store with similarity search."""

    def __init__(self, config: Optional[VectorStoreConfig] = None):
        self.config = config or VectorStoreConfig()
        self.docs: List[str] = []
        self.embeddings: List[Dict[str, float]] = []
        self.metadatas: List[Dict[str, Any]] = []
        self.ids: List[str] = []

    def add(
        self,
        ids: List[str],
        docs: List[str],
        embeddings: List[Dict[str, float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add documents with embeddings to the store."""
        if not (len(ids) == len(docs) == len(embeddings)):
            raise ValueError("ids, docs, and embeddings must have same length")

        if metadatas is None:
            metadatas = [{}] * len(docs)
        elif len(metadatas) != len(docs):
            raise ValueError("metadatas must have same length as docs")

        self.ids.extend(ids)
        self.docs.extend(docs)
        self.embeddings.extend(embeddings)
        self.metadatas.extend(metadatas)

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two sparse vectors."""
        # Get union of keys
        keys = set(vec1.keys()) | set(vec2.keys())

        # Calculate dot product
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in keys)

        # Calculate magnitudes
        mag1 = math.sqrt(sum(v * v for v in vec1.values()))
        mag2 = math.sqrt(sum(v * v for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def query(
        self, query_embedding: Dict[str, float], k: int = 5, threshold: Optional[float] = None
    ) -> Tuple[List[str], List[Dict[str, Any]], List[float]]:
        """Query for similar documents."""
        if k > len(self.docs):
            k = len(self.docs)

        threshold = threshold or self.config.similarity_threshold

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            sim = self._cosine_similarity(query_embedding, doc_embedding)
            if sim >= threshold:
                similarities.append((i, sim))

        # Sort by similarity and take top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        similarities = similarities[:k]

        # Extract results
        docs = []
        metadatas = []
        scores = []

        for idx, score in similarities:
            docs.append(self.docs[idx])
            metadatas.append(self.metadatas[idx] if self.config.include_metadata else {})
            scores.append(score)

        return docs, metadatas, scores

    def query_with_llm(
        self, query: str, llm: LLMProvider, k: int = 3, context_template: Optional[str] = None
    ) -> str:
        """Query and generate answer using LLM."""
        # For now, use a simple embedding approach
        # In a real implementation, you'd embed the query
        query_embedding = self._simple_embed(query)

        # Retrieve relevant docs
        docs, metadatas, scores = self.query(query_embedding, k=k)

        if not docs:
            return "No relevant information found."

        # Build context
        if context_template is None:
            context_template = """Context:
{context}

Question: {question}

Answer:"""

        context = "\n\n".join(f"[{i + 1}] {doc}" for i, doc in enumerate(docs))
        prompt = context_template.format(context=context, question=query)

        # Generate answer
        return llm.generate(prompt)

    def _simple_embed(self, text: str) -> Dict[str, float]:
        """Simple fallback embedding using word frequencies."""
        words = text.lower().split()
        return {word: words.count(word) for word in set(words)}

    def save(self, path: str) -> None:
        """Save store to file."""
        data = {
            "ids": self.ids,
            "docs": self.docs,
            "embeddings": self.embeddings,
            "metadatas": self.metadatas,
            "config": {
                "similarity_threshold": self.config.similarity_threshold,
                "max_results": self.config.max_results,
                "include_metadata": self.config.include_metadata,
            },
        }

        if path.endswith(".pickle"):
            with open(path, "wb") as f:
                pickle.dump(data, f)
        elif path.endswith(".json"):
            # Convert to NDJSON format
            lines = []
            for i in range(len(self.ids)):
                lines.append(
                    json.dumps(
                        {
                            "id": self.ids[i],
                            "doc": self.docs[i],
                            "embedding": self.embeddings[i],
                            "metadata": self.metadatas[i],
                        }
                    )
                )
            with open(path, "w") as f:
                f.write("\n".join(lines))
        else:
            raise ValueError("Unsupported file format. Use .pickle or .json")

    @classmethod
    def load(cls, path: str) -> "VectorStore":
        """Load store from file."""
        if path.endswith(".pickle"):
            with open(path, "rb") as f:
                data = pickle.load(f)

            store = cls()
            store.ids = data["ids"]
            store.docs = data["docs"]
            store.embeddings = data["embeddings"]
            store.metadatas = data["metadatas"]

            # Update config
            config_data = data.get("config", {})
            store.config = VectorStoreConfig(
                similarity_threshold=config_data.get("similarity_threshold", 0.0),
                max_results=config_data.get("max_results", 10),
                include_metadata=config_data.get("include_metadata", True),
            )

            return store

        elif path.endswith(".json"):
            with open(path, "r") as f:
                lines = f.readlines()

            store = cls()
            for line in lines:
                if line.strip():
                    data = json.loads(line)
                    store.ids.append(data["id"])
                    store.docs.append(data["doc"])
                    store.embeddings.append(data["embedding"])
                    store.metadatas.append(data["metadata"])

            return store

        else:
            raise ValueError("Unsupported file format. Use .pickle or .json")

    def to_ndjson(self) -> List[str]:
        """Convert to NDJSON format."""
        lines = []
        for i in range(len(self.ids)):
            lines.append(
                json.dumps(
                    {
                        "id": self.ids[i],
                        "doc": self.docs[i],
                        "embedding": self.embeddings[i],
                        "metadata": self.metadatas[i],
                    }
                )
            )
        return lines

    @classmethod
    def from_ndjson(cls, lines: List[str]) -> "VectorStore":
        """Create from NDJSON format."""
        store = cls()
        for line in lines:
            if line.strip():
                data = json.loads(line)
                store.ids.append(data["id"])
                store.docs.append(data["doc"])
                store.embeddings.append(data["embedding"])
                store.metadatas.append(data["metadata"])
        return store

    def __len__(self) -> int:
        """Return number of documents in store."""
        return len(self.docs)

    def clear(self) -> None:
        """Clear all documents from store."""
        self.docs.clear()
        self.embeddings.clear()
        self.metadatas.clear()
        self.ids.clear()
