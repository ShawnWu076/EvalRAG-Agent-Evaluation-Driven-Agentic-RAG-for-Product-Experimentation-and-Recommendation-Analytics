"""Dependency-light document chunking and hybrid retrieval."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[a-z0-9]+(?:[._-][a-z0-9]+)?")


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source: str
    heading: str
    text: str


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: str
    source: str
    heading: str
    text: str
    score: float
    bm25_score: float
    vector_score: float
    rank: int


def tokenize(text: str) -> list[str]:
    """Normalize text into retrieval tokens."""

    return TOKEN_RE.findall(text.lower())


def _stable_chunk_id(source: str, ordinal: int) -> str:
    stem = Path(source).stem
    return f"{stem}_{ordinal:03d}"


def load_markdown_documents(playbook_dir: Path) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    for path in sorted(playbook_dir.glob("*.md")):
        docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def chunk_markdown(source: str, text: str, chunk_size: int = 420, overlap: int = 80) -> list[DocumentChunk]:
    """Chunk markdown by heading-aware paragraph windows."""

    chunks: list[DocumentChunk] = []
    heading = Path(source).stem.replace("_", " ").title()
    paragraphs: list[tuple[str, str]] = []

    for raw_block in re.split(r"\n\s*\n", text.strip()):
        block = raw_block.strip()
        if not block:
            continue
        if block.startswith("#"):
            heading = block.lstrip("#").strip() or heading
            continue
        paragraphs.append((heading, block))

    current_heading = heading
    current_words: list[str] = []
    ordinal = 1

    def flush() -> None:
        nonlocal ordinal, current_words, current_heading
        if not current_words:
            return
        chunk_text = " ".join(current_words).strip()
        chunks.append(
            DocumentChunk(
                chunk_id=_stable_chunk_id(source, ordinal),
                source=source,
                heading=current_heading,
                text=chunk_text,
            )
        )
        ordinal += 1
        current_words = current_words[-overlap:] if overlap > 0 else []

    for para_heading, paragraph in paragraphs:
        words = paragraph.split()
        if para_heading != current_heading and current_words:
            flush()
        current_heading = para_heading
        if len(words) > chunk_size:
            for start in range(0, len(words), max(1, chunk_size - overlap)):
                window = words[start : start + chunk_size]
                chunks.append(
                    DocumentChunk(
                        chunk_id=_stable_chunk_id(source, ordinal),
                        source=source,
                        heading=current_heading,
                        text=" ".join(window),
                    )
                )
                ordinal += 1
            current_words = []
            continue
        if len(current_words) + len(words) > chunk_size:
            flush()
        current_words.extend(words)

    flush()
    return chunks


def build_chunks(playbook_dir: Path, chunk_size: int = 420, overlap: int = 80) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for source, text in load_markdown_documents(playbook_dir):
        chunks.extend(chunk_markdown(source, text, chunk_size=chunk_size, overlap=overlap))
    return chunks


def save_chunks(chunks: Iterable[DocumentChunk], index_path: Path) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(chunk) for chunk in chunks]
    index_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_chunks(index_path: Path) -> list[DocumentChunk]:
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    return [DocumentChunk(**item) for item in payload]


def _hash_token(token: str, dimensions: int) -> tuple[int, float]:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    raw = int.from_bytes(digest, "big")
    return raw % dimensions, 1.0 if raw & 1 else -1.0


def _hashed_vector(tokens: Iterable[str], dimensions: int = 256) -> dict[int, float]:
    vector: dict[int, float] = defaultdict(float)
    for token in tokens:
        index, sign = _hash_token(token, dimensions)
        vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector.values()))
    if norm == 0:
        return {}
    return {index: value / norm for index, value in vector.items()}


def _dot(left: dict[int, float], right: dict[int, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(index, 0.0) for index, value in left.items())


class SimpleHybridRetriever:
    """BM25 plus hashed-vector retrieval over playbook chunks."""

    def __init__(self, chunks: list[DocumentChunk], alpha: float = 0.65) -> None:
        if not chunks:
            raise ValueError("Retriever needs at least one document chunk.")
        self.chunks = chunks
        self.alpha = alpha
        self._tokens = [tokenize(f"{chunk.heading} {chunk.text}") for chunk in chunks]
        self._term_counts = [Counter(tokens) for tokens in self._tokens]
        self._doc_lengths = [len(tokens) for tokens in self._tokens]
        self._avg_doc_length = sum(self._doc_lengths) / len(self._doc_lengths)
        self._idf = self._build_idf()
        self._vectors = [_hashed_vector(tokens) for tokens in self._tokens]

    def _build_idf(self) -> dict[str, float]:
        document_frequency: Counter[str] = Counter()
        for terms in self._term_counts:
            document_frequency.update(terms.keys())
        total_docs = len(self._term_counts)
        return {
            term: math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
            for term, df in document_frequency.items()
        }

    def _bm25_scores(self, query_tokens: list[str]) -> list[float]:
        k1 = 1.5
        b = 0.75
        query_terms = Counter(query_tokens)
        scores: list[float] = []
        for counts, doc_length in zip(self._term_counts, self._doc_lengths, strict=True):
            score = 0.0
            for term, query_tf in query_terms.items():
                tf = counts.get(term, 0)
                if tf == 0:
                    continue
                idf = self._idf.get(term, 0.0)
                denom = tf + k1 * (1 - b + b * doc_length / self._avg_doc_length)
                score += query_tf * idf * (tf * (k1 + 1)) / denom
            scores.append(score)
        return scores

    def search(self, query: str, top_k: int = 5, alpha: float | None = None) -> list[RetrievalResult]:
        query_tokens = tokenize(query)
        query_vector = _hashed_vector(query_tokens)
        bm25_scores = self._bm25_scores(query_tokens)
        vector_scores = [max(0.0, _dot(query_vector, vector)) for vector in self._vectors]
        max_bm25 = max(bm25_scores) or 1.0
        max_vector = max(vector_scores) or 1.0
        weight = self.alpha if alpha is None else alpha

        scored: list[tuple[float, float, float, int]] = []
        for index, (bm25_score, vector_score) in enumerate(zip(bm25_scores, vector_scores, strict=True)):
            bm25_norm = bm25_score / max_bm25 if max_bm25 else 0.0
            vector_norm = vector_score / max_vector if max_vector else 0.0
            final_score = weight * vector_norm + (1 - weight) * bm25_norm
            scored.append((final_score, bm25_score, vector_score, index))

        scored.sort(key=lambda item: item[0], reverse=True)
        results: list[RetrievalResult] = []
        for rank, (score, bm25_score, vector_score, index) in enumerate(scored[:top_k], start=1):
            chunk = self.chunks[index]
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    source=chunk.source,
                    heading=chunk.heading,
                    text=chunk.text,
                    score=round(score, 6),
                    bm25_score=round(bm25_score, 6),
                    vector_score=round(vector_score, 6),
                    rank=rank,
                )
            )
        return results


def results_to_dicts(results: Iterable[RetrievalResult]) -> list[dict[str, object]]:
    return [asdict(result) for result in results]
