# SIA Chatbot — Implementation Plan

## Overview

This document outlines the implementation plan for SIA Chatbot, an enterprise-grade RAG chatbot platform. The plan is divided into 4 phases over 8 weeks.

## Phase 1: Core Agent Upgrade (Week 1-2)

### Objective
Integrate LangGraph agent architecture with tool-calling and HITL patterns.

### Tasks

| # | Task | Source | Priority | Est. Hours |
|---|------|--------|----------|------------|
| 1.1 | Install LangGraph + LangChain dependencies | Reference | HIGH | 2 |
| 1.2 | Create `AgentState` TypedDict with message history | Reference | HIGH | 4 |
| 1.3 | Build LangGraph StateGraph with conditional edges | Reference | HIGH | 8 |
| 1.4 | Create retriever tool (existing ChromaDB) | Reference | HIGH | 4 |
| 1.5 | Add off-topic tool for scope enforcement | Reference | HIGH | 2 |
| 1.6 | Implement ToolNode for automatic tool execution | Reference | HIGH | 4 |
| 1.7 | Add HITL interrupt/resume pattern | Reference | HIGH | 6 |
| 1.8 | Integrate existing 5-layer guardrails | Our code | HIGH | 8 |
| 1.9 | Unit tests for agent workflow | New | HIGH | 8 |

### Deliverables
- LangGraph agent with RAG + off-topic tools
- HITL workflow for sensitive queries
- Guardrails integration
- Test coverage > 80%

---

## Phase 2: Enhanced RAG (Week 3-4)

### Objective
Improve retrieval quality with hybrid search, reranking, and query expansion.

### Tasks

| # | Task | Priority | Est. Hours |
|---|------|----------|------------|
| 2.1 | Deploy Elasticsearch for BM25 search | HIGH | 8 |
| 2.2 | Implement hybrid search (semantic + BM25) | HIGH | 12 |
| 2.3 | Add reciprocal rank fusion for merging results | HIGH | 6 |
| 2.4 | Integrate Cohere Rerank API | HIGH | 6 |
| 2.5 | Implement bge-reranker (self-hosted option) | MEDIUM | 8 |
| 2.6 | Add multi-query retrieval | MEDIUM | 8 |
| 2.7 | Implement HyDE (Hypothetical Document Embeddings) | MEDIUM | 6 |
| 2.8 | Multi-tenant ChromaDB collections | MEDIUM | 8 |
| 2.9 | Retrieval quality metrics and A/B testing | LOW | 8 |

### Deliverables
- Hybrid search pipeline
- Reranking service
- Query expansion strategies
- Multi-tenant isolation

---

## Phase 3: Production Infrastructure (Week 5-6)

### Objective
Build production-ready infrastructure with caching, background jobs, and streaming.

### Tasks

| # | Task | Priority | Est. Hours |
|---|------|----------|------------|
| 3.1 | Deploy Redis for caching + sessions | HIGH | 4 |
| 3.2 | Migrate in-memory cache to Redis | HIGH | 8 |
| 3.3 | Add rate limiting middleware | HIGH | 6 |
| 3.4 | Deploy PostgreSQL with Alembic migrations | HIGH | 8 |
| 3.5 | Implement S3/MinIO storage service | MEDIUM | 8 |
| 3.6 | Set up Celery + Redis for background workers | HIGH | 12 |
| 3.7 | Move ingestion pipeline to Celery tasks | HIGH | 8 |
| 3.8 | Implement SSE streaming for chat responses | HIGH | 12 |
| 3.9 | Add WebSocket support (optional) | LOW | 8 |

### Deliverables
- Redis caching layer
- PostgreSQL with migrations
- Background job processing
- Real-time streaming responses

---

## Phase 4: Enterprise Features (Week 7-8)

### Objective
Add enterprise-grade features for security, compliance, and operations.

### Tasks

| # | Task | Priority | Est. Hours |
|---|------|----------|------------|
| 4.1 | SSO/SAML integration | MEDIUM | 12 |
| 4.2 | Enhanced audit logging | MEDIUM | 8 |
| 4.3 | Document version comparison | LOW | 8 |
| 4.4 | Conversation export (PDF/JSON) | LOW | 6 |
| 4.5 | Health check depth (DB, Redis, ChromaDB) | MEDIUM | 4 |
| 4.6 | Prometheus metrics + Grafana dashboards | MEDIUM | 8 |
| 4.7 | OpenTelemetry tracing | LOW | 8 |
| 4.8 | Backup and recovery procedures | MEDIUM | 6 |
| 4.9 | Security audit and penetration testing | HIGH | 12 |

### Deliverables
- SSO/SAML authentication
- Comprehensive audit logging
- Monitoring and observability
- Security hardening

---

## Pricing Implementation

### Free Plan (1 bot/month)
```
┌─────────────────────────────────────────────────────┐
│  FREE PLAN                                          │
├─────────────────────────────────────────────────────┤
│  • 1 bot                                            │
│  • 1,000 queries/month                              │
│  • 100MB document storage                           │
│  • Basic guardrails (input/output)                  │
│  • Community support                                │
│  • 7-day query history                              │
│  • Single user                                      │
└─────────────────────────────────────────────────────┘
```

### Implementation
- Add `plan` field to organization model
- Add query counter middleware
- Add storage limit enforcement
- Add feature gating based on plan

---

## Technology Decisions

### Why LangGraph over Linear Pipeline?

| Aspect | Linear Pipeline | LangGraph Agent |
|--------|----------------|-----------------|
| Flexibility | Fixed steps | Dynamic routing |
| Tool calling | Manual | Native support |
| HITL | Custom implementation | Built-in interrupt/resume |
| Multi-step reasoning | Limited | Full support |
| Extensibility | Hard to extend | Easy to add tools |

### Why Hybrid Search?

| Query Type | Semantic Only | Hybrid (Semantic + BM25) |
|------------|---------------|--------------------------|
| Factual | Good | Excellent |
| Keyword-based | Poor | Excellent |
| Conceptual | Excellent | Excellent |
| Noisy | Good | Good |

### Why Redis over In-Memory?

| Aspect | In-Memory | Redis |
|--------|-----------|-------|
| Persistence | None | Yes |
| Scalability | Single instance | Cluster |
| TTL support | Manual | Native |
| Shared state | No | Yes |
| Performance | Fastest | Fast |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LangGraph learning curve | Medium | Medium | Reference code + docs |
| Elasticsearch deployment | Low | High | Use managed service |
| Redis failure | Low | High | Sentinel + persistence |
| Migration issues | Medium | High | Alembic + backups |
| Security vulnerabilities | Low | Critical | Pen testing + audits |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Query response time | < 2s (p95) | Prometheus |
| Retrieval accuracy | > 85% | Human evaluation |
| Guardrail detection | > 95% | Test suite |
| System uptime | 99.9% | Health checks |
| User satisfaction | > 4.5/5 | Feedback surveys |

---

## Next Steps

1. **Immediate**: Set up development environment
2. **Week 1**: Begin Phase 1 - LangGraph agent integration
3. **Week 2**: Complete Phase 1 + testing
4. **Week 3**: Start Phase 2 - Enhanced RAG
5. **Week 4**: Complete Phase 2 + validation
6. **Week 5**: Start Phase 3 - Production infrastructure
7. **Week 6**: Complete Phase 3 + load testing
8. **Week 7**: Start Phase 4 - Enterprise features
9. **Week 8**: Complete Phase 4 + security audit
10. **Week 9**: Production deployment
