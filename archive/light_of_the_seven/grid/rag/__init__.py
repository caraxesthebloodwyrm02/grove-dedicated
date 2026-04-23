from dataclasses import dataclass, field
from hashlib import md5
from typing import Any, Dict, Iterable, List, Optional, Protocol, runtime_checkable


@dataclass
class Doc:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    doc_id: Optional[str] = None


@dataclass(frozen=True)
class ScoredChunk:
    chunk_id: str
    text: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.score, (int, float)):
            raise TypeError("score must be numeric")


@runtime_checkable
class BaseIndex(Protocol):
    def add(self, docs: Iterable[Doc]) -> int: ...
    def query(self, text: str, top_k: int = 5) -> List[ScoredChunk]: ...


def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks."""
    if not text or chunk_size <= 0:
        return [text] if text else []
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip() or text[start:end])
        start = end - overlap if overlap < chunk_size else end
    return [c for c in chunks if c]


class InMemoryIndex:
    def __init__(self) -> None:
        self.docs: List[Doc] = []

    @property
    def chunks(self) -> List[Doc]:
        """Expose docs as chunks for Retriever compatibility."""
        return self.docs

    def __len__(self) -> int:
        return len(self.docs)

    def add(self, docs: Iterable[Doc]) -> int:
        docs_list = list(docs)
        self.docs.extend(docs_list)
        return len(docs_list)

    def add_documents(
        self,
        ids: List[str],
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Contract: add by (ids, texts, metadatas)."""
        metas = metadatas or [{} for _ in texts]
        for i, (doc_id, text) in enumerate(zip(ids, texts, strict=True)):
            meta = metas[i] if i < len(metas) else {}
            self.docs.append(Doc(doc_id=doc_id, text=text, metadata=meta))

    def add_documents_chunked(
        self,
        docs: Iterable[Doc],
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        """Chunk documents and add to index."""
        for doc in docs:
            for j, chunk_text in enumerate(_chunk_text(doc.text, chunk_size, overlap)):
                cid = f"{doc.doc_id or md5(doc.text.encode('utf-8')).hexdigest()}#{j}"
                self.docs.append(
                    Doc(doc_id=cid, text=chunk_text, metadata={**doc.metadata, "chunk_index": j})
                )

    def query(self, text: str, top_k: int = 5) -> List[ScoredChunk]:
        # Simple text overlap scoring so ordering is stable for ties
        scored: List[tuple[float, Doc]] = []
        q_words = set(text.lower().split())
        for d in self.docs:
            d_words = set(d.text.lower().split())
            overlap_count = len(q_words & d_words)
            score = overlap_count / len(q_words) if q_words else 1.0
            scored.append((score, d))
        scored.sort(key=lambda x: (-x[0], x[1].doc_id or ""))
        return [
            ScoredChunk(
                chunk_id=d.doc_id or md5(d.text.encode("utf-8")).hexdigest(),
                text=d.text,
                score=score,
                metadata=d.metadata,
            )
            for score, d in scored[:top_k]
        ]

    def search(self, text: str, top_k: int = 5) -> List[ScoredChunk]:
        """Alias for query for Retriever/contract compatibility."""
        return self.query(text, top_k=top_k)


class DummyLLMAdapter:
    """Dummy LLM for tests; returns a fixed string."""

    def generate(self, prompt: str) -> str:
        return "DummyLLM"

    def __call__(self, prompt: str) -> str:
        return self.generate(prompt)


class RagQA:
    def __init__(
        self,
        index: Optional[InMemoryIndex] = None,
        generator: Optional[Any] = None,
    ) -> None:
        self.index = index or InMemoryIndex()
        self.generator = generator

    def index_documents(
        self,
        docs: Iterable[Doc],
        chunked: bool = False,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        """Index documents, optionally chunked."""
        if chunked:
            self.index.add_documents_chunked(docs, chunk_size=chunk_size, overlap=overlap)
        else:
            self.index.add(list(docs))

    def answer(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        results = self.index.search(query, top_k=top_k)
        if self.generator is not None:
            context = "\n".join(r.text for r in results)
            answer_text = (
                self.generator.generate(context + "\n" + query)
                if hasattr(self.generator, "generate")
                else str(self.generator(context + "\n" + query))
            )
        else:
            answer_text = results[0].text if results else ""
        sources = [{"doc_id": r.chunk_id, "text": r.text[:100], **r.metadata} for r in results]
        return {"answer": answer_text, "sources": sources}


def to_scored_chunk(
    text: str,
    score: float,
    chunk_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> ScoredChunk:
    cid = chunk_id or md5(text.encode("utf-8")).hexdigest()
    return ScoredChunk(chunk_id=cid, text=text, score=float(score), metadata=metadata or {})


def normalize_results(
    docs: List[str], scores: List[float], metas: Optional[List[Dict[str, Any]]] = None
) -> List[ScoredChunk]:
    metas = metas or [{} for _ in docs]
    out = []
    for i, text in enumerate(docs):
        score = scores[i] if i < len(scores) else 0.0
        meta = metas[i] if i < len(metas) else {}
        out.append(to_scored_chunk(text=text, score=score, metadata=meta))
    return out
