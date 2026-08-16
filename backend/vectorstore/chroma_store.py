import chromadb
from typing import List, Dict, Any, Optional
from backend.config.settings import settings


class ChromaStore:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMADB_HOST,
            port=settings.CHROMADB_PORT
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMADB_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(
        self,
        chunk_ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> None:
        batch_size = 500
        for i in range(0, len(chunk_ids), batch_size):
            batch_end = min(i + batch_size, len(chunk_ids))
            self.collection.add(
                ids=chunk_ids[i:batch_end],
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end],
                embeddings=embeddings[i:batch_end]
            )

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        where: Optional[Dict[str, Any]] = None,
        threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        n_results = top_k * 3
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

        chunks = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i]
                similarity = 1 - distance
                if similarity >= threshold:
                    chunks.append({
                        "id": results["ids"][0][i],
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity": similarity
                    })

        return chunks[:top_k]

    def delete_by_document(self, document_id: int) -> None:
        self.collection.delete(
            where={"document_id": document_id}
        )

    def get_stats(self) -> Dict[str, Any]:
        count = self.collection.count()
        return {"total_chunks": count}


chroma_store = ChromaStore()
