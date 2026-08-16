from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # === Application ===
    APP_NAME: str = "SIA Chatbot"
    APP_TAGLINE: str = "Your Enterprise AI Knowledge Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # === LLM Configuration ===
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = "gemini-flash-latest"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 2048

    # === API Keys ===
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    EURON_API_KEY: Optional[str] = None
    EURON_BASE_URL: str = "https://api.euron.one/api/v1/euri"

    # === Vector Store ===
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8000
    CHROMADB_COLLECTION: str = "knowledge_base"

    # === Elasticsearch (Hybrid Search) ===
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_INDEX: str = "documents"

    # === Database ===
    DATABASE_URL: str = "sqlite:///./sia_chatbot.db"

    # === Redis ===
    REDIS_URL: str = "redis://localhost:6379/0"

    # === Authentication ===
    JWT_SECRET: str = "change-me-jwt-secret-to-something-random"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    # === Storage ===
    STORAGE_PROVIDER: str = "local"
    STORAGE_BUCKET: str = "sia-chatbot-storage"
    STORAGE_PATH: str = "./storage"

    # === Chunking ===
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100

    # === Retrieval ===
    SIMILARITY_THRESHOLD: float = 0.70
    MAX_RESULTS: int = 10
    RERANKER_ENABLED: bool = False

    # === Rate Limiting ===
    RATE_LIMIT_PER_MINUTE: int = 60

    # === CORS ===
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
