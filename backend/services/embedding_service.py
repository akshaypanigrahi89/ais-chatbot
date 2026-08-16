from openai import OpenAI
from typing import List
from backend.config.settings import settings


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.EURON_API_KEY,
            base_url=settings.EURON_BASE_URL
        )
        self.model = "text-embedding-3-small"

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=[text]
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        batch_size = 100
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            all_embeddings.extend([item.embedding for item in response.data])

        return all_embeddings


embedding_service = EmbeddingService()
