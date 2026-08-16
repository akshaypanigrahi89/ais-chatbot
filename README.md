# SIA Chatbot

**Your Enterprise AI Knowledge Assistant**

*Intelligent. Secure. Scalable.*

---

## Overview

SIA Chatbot is an enterprise-grade Retrieval-Augmented Generation (RAG) chatbot platform that enables organizations to create intelligent, secure, and scalable AI assistants for internal knowledge management.

## Features

### Core Features
- 🤖 **LangGraph Agent** — Multi-step reasoning with tool-calling
- 📄 **Multi-format Ingestion** — PDF, DOCX, PPTX, CSV, XLSX, HTML, Images, Audio
- 🔍 **Hybrid Search** — Semantic (ChromaDB) + BM25 (Elasticsearch)
- 🎯 **Reranking** — Cohere Rerank / bge-reranker
- 💬 **Real-time Streaming** — SSE/WebSocket responses
- 🔄 **Query Expansion** — HyDE, Multi-query retrieval

### Enterprise Features
- 🔐 **5-Layer Guardrails** — Input, Auth, Retrieval, Prompt, Output
- 👥 **RBAC** — Role-based access control with department isolation
- ✅ **HITL** — Human-in-the-loop review workflow
- 🚨 **Risk Engine** — Automated threat classification
- 🎛️ **Feature Flags** — Toggle features without deployment
- 📊 **Audit Logging** — Complete action history

### Security
- 🔑 **JWT Authentication** — Secure token-based auth
- 🛡️ **Input Validation** — 40+ injection patterns
- 🔒 **Data Encryption** — At rest and in transit
- 📋 **Compliance** — SOC 2, GDPR, HIPAA ready

---

## Pricing

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/mo | 1 bot, 1,000 queries/mo, 100MB storage |
| **Pro** | $49/mo | 5 bots, 10,000 queries/mo, 1GB storage |
| **Enterprise** | Custom | Unlimited everything, SSO, dedicated support |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend | Python 3.11, FastAPI, LangGraph |
| Vector DB | ChromaDB + Elasticsearch |
| Database | PostgreSQL |
| Cache | Redis |
| Storage | S3/MinIO |
| LLM | Gemini (default), OpenAI-compatible |
| Embeddings | Euron API |
| Queue | Celery + Redis |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/sia-chatbot.git
cd sia-chatbot

# Backend setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install

# Start services
docker-compose up -d

# Run migrations
alembic upgrade head

# Start backend
cd ..
uvicorn backend.main:app --reload --port 8000

# Start frontend
cd frontend
npm run dev
```

### Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/sia_chatbot
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_key
EURON_API_KEY=your_key
JWT_SECRET=your_random_secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — System design and data flow
- [Implementation Plan](docs/PLAN.md) — 8-week development roadmap
- [API Reference](docs/API_REFERENCE.md) — Complete API documentation
- [Deployment Guide](docs/DEPLOYMENT.md) — Production deployment
- [Security](docs/SECURITY.md) — Security considerations
- [Pricing](docs/PRICING.md) — Pricing details

---

## Project Structure

```
SIA Chatbot/
├── docs/                          # Documentation
│   ├── README.md                  # Project overview
│   ├── ARCHITECTURE.md            # System architecture
│   ├── PLAN.md                    # Implementation plan
│   ├── API_REFERENCE.md           # API documentation
│   ├── DEPLOYMENT.md              # Deployment guide
│   ├── SECURITY.md                # Security considerations
│   └── PRICING.md                 # Pricing details
├── backend/                       # Python backend
│   ├── main.py                    # FastAPI application
│   ├── config/                    # Configuration
│   ├── api/                       # API routes
│   ├── auth/                      # Authentication
│   ├── models/                    # Database models
│   ├── services/                  # Business logic
│   ├── guardrails/                # Security layers
│   ├── vectorstore/               # Vector database
│   └── cache/                     # Caching layer
├── frontend/                      # Next.js frontend
│   ├── app/                       # Pages and routes
│   ├── components/                # React components
│   ├── lib/                       # Utilities
│   └── types/                     # TypeScript types
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Docker configuration
└── vercel.json                    # Vercel deployment
```

---

## Development

### Running Tests

```bash
# Backend tests
pytest

# Frontend tests
npm test

# Coverage
pytest --cov=backend
```

### Code Quality

```bash
# Python linting
ruff check backend/
black backend/

# TypeScript linting
npm run lint
npm run typecheck
```

---

## Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel --prod
```

### Docker (Backend)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## License

Proprietary — All rights reserved.

---

## Support

- 📧 Email: support@sia-chatbot.com
- 💬 Discord: [Join our community](https://discord.gg/sia-chatbot)
- 📖 Documentation: [docs.sia-chatbot.com](https://docs.sia-chatbot.com)

---

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Frontend by [Next.js](https://nextjs.org/)
