from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# === Auth Schemas ===
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: str
    departments: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# === Chat Schemas ===
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[str] = None
    department: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    message_id: str
    sources: List[Dict[str, Any]] = []
    groundedness: Optional[float] = None
    guardrails: Dict[str, str] = {}


class ConversationResponse(BaseModel):
    id: str
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    sources: List[Dict[str, Any]] = []
    groundedness: Optional[float]
    created_at: datetime


# === Document Schemas ===
class DocumentResponse(BaseModel):
    id: int
    title: str
    file_name: str
    status: str
    department: str
    category: Optional[str]
    version: int
    chunk_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    id: int
    title: str
    file_name: str
    status: str
    department: str
    category: Optional[str]
    created_at: datetime


# === Admin Schemas ===
class DashboardStats(BaseModel):
    total_documents: int
    indexed_documents: int
    processing_documents: int
    failed_documents: int
    total_chunks: int
    total_conversations: int
    total_messages: int
    departments: List[str]


class SettingsUpdate(BaseModel):
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
    similarity_threshold: Optional[float] = None
    max_results: Optional[int] = None


class CacheStats(BaseModel):
    total_entries: int
    hit_rate: float
    total_hits: int
    total_misses: int
    memory_usage_mb: float


class FeatureFlagResponse(BaseModel):
    name: str
    description: str
    enabled: bool
    default_value: bool


class ReviewResponse(BaseModel):
    id: int
    conversation_id: int
    user_query: str
    draft_answer: str
    risk_level: str
    status: str
    created_at: datetime


class ReviewAction(BaseModel):
    comment: Optional[str] = None


class ReviewEdit(BaseModel):
    edited_answer: str
    comment: Optional[str] = None
