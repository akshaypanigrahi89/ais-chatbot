# SIA Chatbot — API Reference

## Base URL
```
Production: https://api.sia-chatbot.com
Development: http://localhost:8000
```

## Authentication

All API endpoints require JWT authentication unless noted otherwise.

### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

---

## Auth Endpoints

### POST /api/auth/register
Register a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@company.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@company.com",
  "role": "USER",
  "departments": ["General"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

### POST /api/auth/login
Authenticate and receive JWT token.

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "USER"
  }
}
```

### GET /api/auth/me
Get current user profile.

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@company.com",
  "full_name": "John Doe",
  "role": "USER",
  "departments": ["HR", "Marketing"],
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Chat Endpoints

### POST /api/chat
Send a message and receive AI response.

**Request:**
```json
{
  "message": "What is the company's leave policy?",
  "conversation_id": "conv_abc123",
  "department": "HR"
}
```

**Response (Streaming):**
```
data: {"type": "start", "conversation_id": "conv_abc123"}
data: {"type": "token", "content": "The "}
data: {"type": "token", "content": "leave "}
data: {"type": "token", "content": "policy "}
data: {"type": "sources", "sources": [{"title": "HR_Policy.pdf", "page": 5}]}
data: {"type": "end", "groundedness": 0.92}
```

**Response (Non-streaming):**
```json
{
  "message": "The leave policy allows 20 days of annual leave...",
  "conversation_id": "conv_abc123",
  "message_id": "msg_xyz789",
  "sources": [
    {
      "title": "HR_Policy.pdf",
      "page": 5,
      "section": "Annual Leave",
      "snippet": "Employees are entitled to 20 days..."
    }
  ],
  "groundedness": 0.92,
  "guardrails": {
    "input": "passed",
    "output": "passed"
  }
}
```

### GET /api/chat/history
Get conversation history.

**Query Parameters:**
- `limit` (int): Number of conversations (default: 20)
- `offset` (int): Pagination offset

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_abc123",
      "title": "Leave Policy Question",
      "message_count": 5,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 45,
  "limit": 20,
  "offset": 0
}
```

### GET /api/chat/{conversation_id}
Get specific conversation with messages.

**Response:**
```json
{
  "id": "conv_abc123",
  "messages": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "What is the leave policy?",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "msg_002",
      "role": "assistant",
      "content": "The leave policy allows...",
      "sources": [...],
      "groundedness": 0.92,
      "created_at": "2024-01-15T10:30:05Z"
    }
  ]
}
```

---

## Document Endpoints

### POST /api/admin/documents/upload
Upload a document for ingestion.

**Request:**
```
Content-Type: multipart/form-data

file: [binary data]
department: "HR"
category: "Policy"
title: "Leave Policy 2024"
```

**Response:**
```json
{
  "id": 1,
  "title": "Leave Policy 2024",
  "file_name": "leave_policy.pdf",
  "status": "PROCESSING",
  "department": "HR",
  "category": "Policy",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### GET /api/admin/documents
List all documents.

**Query Parameters:**
- `department` (string): Filter by department
- `status` (string): Filter by status
- `limit` (int): Number of documents
- `offset` (int): Pagination offset

**Response:**
```json
{
  "documents": [
    {
      "id": 1,
      "title": "Leave Policy 2024",
      "file_name": "leave_policy.pdf",
      "status": "COMPLETED",
      "department": "HR",
      "category": "Policy",
      "version": 1,
      "chunk_count": 45,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 120,
  "limit": 20,
  "offset": 0
}
```

### DELETE /api/admin/documents/{document_id}
Delete a document.

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

### POST /api/admin/documents/{document_id}/reindex
Re-index a document.

**Response:**
```json
{
  "job_id": "job_xyz789",
  "status": "QUEUED"
}
```

---

## Admin Endpoints

### GET /api/admin/dashboard
Get dashboard statistics.

**Response:**
```json
{
  "total_documents": 120,
  "indexed_documents": 115,
  "processing_documents": 3,
  "failed_documents": 2,
  "total_chunks": 5400,
  "total_conversations": 234,
  "total_messages": 1567,
  "departments": ["HR", "Marketing", "Finance", "IT"]
}
```

### GET /api/admin/settings
Get system settings.

**Response:**
```json
{
  "llm_provider": "gemini",
  "llm_model": "gemini-flash-latest",
  "embedding_provider": "euron",
  "embedding_model": "text-embedding-3-small",
  "chunk_size": 800,
  "chunk_overlap": 100,
  "similarity_threshold": 0.70,
  "max_results": 10
}
```

### PUT /api/admin/settings
Update system settings.

**Request:**
```json
{
  "llm_provider": "gemini",
  "llm_model": "gemini-flash-latest",
  "chunk_size": 1000,
  "similarity_threshold": 0.75
}
```

### GET /api/admin/cache/stats
Get cache statistics.

**Response:**
```json
{
  "total_entries": 1234,
  "hit_rate": 0.85,
  "total_hits": 10500,
  "total_misses": 1850,
  "memory_usage_mb": 45.2
}
```

### POST /api/admin/cache/flush
Flush all cache entries.

**Response:**
```json
{
  "message": "Cache flushed successfully",
  "entries_removed": 1234
}
```

---

## Review Endpoints (HITL)

### GET /api/admin/reviews
Get pending reviews.

**Query Parameters:**
- `status` (string): PENDING, IN_REVIEW, APPROVED, REJECTED
- `limit` (int): Number of reviews
- `offset` (int): Pagination offset

**Response:**
```json
{
  "reviews": [
    {
      "id": 1,
      "conversation_id": "conv_abc123",
      "user_query": "What is the termination policy?",
      "draft_answer": "The termination policy requires...",
      "risk_level": "HIGH",
      "status": "PENDING",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 5,
  "limit": 20,
  "offset": 0
}
```

### POST /api/admin/reviews/{review_id}/approve
Approve a review.

**Request:**
```json
{
  "comment": "Looks good"
}
```

### POST /api/admin/reviews/{review_id}/reject
Reject a review.

**Request:**
```json
{
  "comment": "Contains sensitive information"
}
```

### POST /api/admin/reviews/{review_id}/edit
Edit and approve a review.

**Request:**
```json
{
  "edited_answer": "The termination policy requires 30 days notice...",
  "comment": "Removed sensitive details"
}
```

---

## Feature Flags

### GET /api/admin/flags
Get all feature flags.

**Response:**
```json
{
  "flags": [
    {
      "name": "AI_ASSISTANT_ENABLED",
      "description": "Master switch for AI assistant",
      "enabled": true,
      "default_value": true
    },
    {
      "name": "ENABLE_HILP",
      "description": "Human-in-the-loop review",
      "enabled": true,
      "default_value": true
    }
  ]
}
```

### PUT /api/admin/flags/{flag_name}
Toggle a feature flag.

**Request:**
```json
{
  "enabled": false
}
```

### POST /api/admin/flags/emergency-stop
Emergency stop - disable all critical flags.

**Response:**
```json
{
  "message": "Emergency stop activated",
  "disabled_flags": [
    "AI_ASSISTANT_ENABLED",
    "CHAT_ENABLED",
    "DOCUMENT_INGESTION_ENABLED"
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Rate Limited
```json
{
  "detail": "Rate limit exceeded",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits

| Plan | Requests/min | Burst |
|------|--------------|-------|
| Free | 10 | 20 |
| Pro | 60 | 100 |
| Enterprise | Custom | Custom |

---

## Pagination

All list endpoints support pagination:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 20 | Number of items per page |
| `offset` | int | 0 | Number of items to skip |

**Response includes:**
```json
{
  "total": 100,
  "limit": 20,
  "offset": 0
}
```
