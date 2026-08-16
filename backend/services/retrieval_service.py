from typing import List, Dict, Any, Optional
from backend.vectorstore.chroma_store import chroma_store
from backend.services.embedding_service import embedding_service
from backend.cache.cag_cache import cag_cache


class RetrievalService:
    def __init__(self):
        self.similarity_threshold = 0.70
        self.max_results = 10

    def retrieve(
        self,
        query: str,
        departments: List[str],
        top_k: int = 10,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        cache_key = f"{query}|{','.join(sorted(departments))}"

        if use_cache:
            cached = cag_cache.get_retrieval(cache_key)
            if cached is not None:
                return cached

        query_embedding = embedding_service.embed_text(query)

        where_filter = None
        if departments:
            if len(departments) == 1:
                where_filter = {"department": departments[0]}
            else:
                where_filter = {"department": {"$in": departments}}

        chunks = chroma_store.query(
            query_embedding=query_embedding,
            top_k=top_k,
            where=where_filter,
            threshold=self.similarity_threshold
        )

        if use_cache:
            cag_cache.set_retrieval(cache_key, chunks)

        return chunks

    def format_context(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "No relevant information found."

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get("metadata", {})
            source_parts = [f"Source {i}:"]

            if metadata.get("file_name"):
                source_parts.append(metadata["file_name"])
            if metadata.get("page_number"):
                source_parts.append(f"Page {metadata['page_number']}")
            if metadata.get("section"):
                source_parts.append(f"Section {metadata['section']}")

            source_header = " -- ".join(source_parts)
            context_parts.append(f"[{source_header}]\n{chunk['content']}")

        return "\n\n---\n\n".join(context_parts)


retrieval_service = RetrievalService()
