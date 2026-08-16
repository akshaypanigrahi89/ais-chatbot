# SIA Chatbot — Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SIA CHATBOT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        FRONTEND (Next.js 14)                          │  │
│  │                                                                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │  │
│  │  │ Landing  │ │  Login   │ │   Chat   │ │ Register │ │   Admin   │  │  │
│  │  │   Page   │ │   Page   │ │ Interface│ │   Page   │ │ Dashboard │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────────┘  │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │              SSE/WebSocket Streaming Layer                      │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│                              REST API + SSE                                  │
│                                     │                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     FASTAPI BACKEND (Python 3.11)                     │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                   LANGGRAPH AGENT LAYER                         │  │  │
│  │  │                                                                 │  │  │
│  │  │  START → Router → [RAG / Web Search / Calculator] → LLM        │  │  │
│  │  │       ↓                                                        │  │  │
│  │  │  ToolNode (retriever, web_search, calculator)                  │  │  │
│  │  │       ↓                                                        │  │  │
│  │  │  Conditional: needs_tools? → continue / respond                │  │  │
│  │  │       ↓                                                        │  │  │
│  │  │  HITL: interrupt() for sensitive queries                       │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │              5-LAYER GUARDRAILS SYSTEM                          │  │  │
│  │  │                                                                 │  │  │
│  │  │  Layer 1: Input ──► Injection detection (40+ patterns)          │  │  │
│  │  │  Layer 2: Auth ──► Server-side RBAC + Dept filtering           │  │  │
│  │  │  Layer 3: Retrieval ──► Quality/conflict check                 │  │  │
│  │  │  Layer 4: Prompt ──► Security anchor + validation              │  │  │
│  │  │  Layer 5: Output ──► Secret leak/citation check                │  │  │
│  │  │                                                                 │  │  │
│  │  │  + Risk Engine + HILP + Feature Flags                          │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                    CORE SERVICES                                │  │  │
│  │  │                                                                 │  │  │
│  │  │  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐            │  │  │
│  │  │  │  Ingestion   │ │  Retrieval   │ │  LLM Service  │            │  │  │
│  │  │  │  Pipeline    │ │  Service     │ │  (Gemini/     │            │  │  │
│  │  │  │  (Celery)    │ │  + Hybrid    │ │   OpenAI)     │            │  │  │
│  │  │  └─────────────┘ └──────────────┘ └───────────────┘            │  │  │
│  │  │                                                                 │  │  │
│  │  │  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐            │  │  │
│  │  │  │  Reranker    │ │  Query       │ │  CAG Cache    │            │  │  │
│  │  │  │  Service     │ │  Expansion   │ │  (Redis)      │            │  │  │
│  │  │  └─────────────┘ └──────────────┘ └───────────────┘            │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                    STORAGE LAYER                                 │  │  │
│  │  │                                                                 │  │  │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │  │  │
│  │  │  │  ChromaDB     │  │  PostgreSQL   │  │  Redis               │  │  │  │
│  │  │  │  (Vectors)    │  │  (Metadata)   │  │  (Cache + Sessions)  │  │  │  │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │  │  │
│  │  │                                                                 │  │  │
│  │  │  ┌──────────────┐  ┌──────────────┐                            │  │  │
│  │  │  │  S3/MinIO     │  │  Elasticsearch│                            │  │  │
│  │  │  │  (Files)      │  │  (BM25)       │                            │  │  │
│  │  │  └──────────────┘  └──────────────┘                            │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Document Ingestion Flow
```
Upload → Celery Worker → Parser Registry (9 parsers)
    → Chunking Service (recursive, 800 chars)
    → Embedding Service (Euron API)
    → ChromaDB (vectors) + PostgreSQL (metadata)
    → Cache Invalidation
```

### 2. Query Flow
```
User Query → Input Guardrails → Auth Guardrails
    → Query Expansion (HyDE/Multi-query)
    → Hybrid Search (ChromaDB + Elasticsearch)
    → Reranking (Cohere/bge)
    → Retrieval Guardrails
    → LangGraph Agent (Tool calling)
    → LLM Generation (Gemini/OpenAI)
    → Output Guardrails
    → SSE Stream to Frontend
```

### 3. HITL Flow
```
Sensitive Query → Risk Engine (MEDIUM/HIGH/CRITICAL)
    → Agent interrupt() → Review Queue
    → Admin Reviews → Approve/Edit/Reject
    → Command(resume=...) → Response to User
```

## Database Schema

### Core Tables
- `users` — User accounts with roles and departments
- `documents` — Document metadata and versions
- `document_chunks` — Chunk references (vectors in ChromaDB)
- `conversations` — Chat sessions
- `messages` — Individual messages
- `ingestion_jobs` — Background job tracking
- `audit_logs` — Action history
- `review_queue` — HILP pending reviews
- `feature_flags` — Feature toggles
- `app_settings` — System configuration

## Security Architecture

### Authentication
- JWT tokens with 60-minute expiry
- bcrypt password hashing
- Optional SSO/SAML integration

### Authorization (RBAC)
- ADMIN: Full system access
- USER: Department-scoped access
- HR_ADMIN, MARKETING_ADMIN, COMPLIANCE_ADMIN: Department-specific admin

### Data Isolation
- Department-level ChromaDB filtering
- Server-side authorization (never trust frontend)
- Audit logging for all actions
