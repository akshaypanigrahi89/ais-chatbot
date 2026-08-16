# SIA Chatbot — Project Overview

## Product Name
**SIA Chatbot** — Your Enterprise AI Knowledge Assistant

## Tagline
*"Intelligent. Secure. Scalable."*

## Product Vision
SIA Chatbot is an enterprise-grade Retrieval-Augmented Generation (RAG) chatbot platform that enables organizations to create intelligent, secure, and scalable AI assistants for internal knowledge management.

## Key Features

### Core
- Multi-format document ingestion (PDF, DOCX, PPTX, CSV, XLSX, HTML, Images, Audio)
- Hybrid search (Semantic + BM25) with reranking
- Human-in-the-loop (HITL) review workflow
- 5-layer guardrails system (Input, Auth, Retrieval, Prompt, Output)
- Real-time streaming responses (SSE/WebSocket)

### Enterprise
- Role-based access control (RBAC) with department-level isolation
- Audit logging and compliance tracking
- Feature flags and emergency stop
- Multi-tenant architecture
- SSO/SAML integration ready

### AI Agent
- LangGraph-based agent architecture
- Tool-calling (retrieval, web search, calculator)
- Multi-step reasoning capabilities
- Query expansion (HyDE, Multi-query)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend | Python 3.11, FastAPI, LangGraph |
| Vector DB | ChromaDB (primary), Elasticsearch (hybrid) |
| Metadata DB | PostgreSQL with Alembic migrations |
| Cache | Redis |
| Storage | S3/MinIO |
| LLM | Gemini (default), OpenAI-compatible |
| Embeddings | Euron API (text-embedding-3-small) |
| Reranker | Cohere Rerank / bge-reranker |
| Queue | Celery + Redis |
| Deployment | Vercel (frontend), Docker (backend) |

## Pricing Model

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/mo | 1 bot, 1,000 queries/mo, 100MB storage, basic guardrails |
| **Pro** | $49/mo | 5 bots, 10,000 queries/mo, 1GB storage, full guardrails, HITL |
| **Enterprise** | Custom | Unlimited bots, custom storage, SSO, dedicated support, SLA |

## Deployment

- **Frontend**: Vercel (serverless)
- **Backend**: Docker containers on AWS/GCP/Azure
- **Database**: Managed PostgreSQL + Redis
- **Storage**: S3/MinIO

## Documentation Structure

```
docs/
├── README.md                    # This file
├── ARCHITECTURE.md              # System architecture
├── PLAN.md                      # Implementation plan
├── API_REFERENCE.md             # API documentation
├── DEPLOYMENT.md                # Deployment guide
├── SECURITY.md                  # Security considerations
└── PRICING.md                   # Pricing details
```
