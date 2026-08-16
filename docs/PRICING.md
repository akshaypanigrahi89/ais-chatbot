# SIA Chatbot — Pricing

## Pricing Plans

### Free Plan — $0/month
**Perfect for: Individuals and small teams evaluating SIA Chatbot**

| Feature | Limit |
|---------|-------|
| Bots | 1 |
| Queries/month | 1,000 |
| Documents/bot | 10 |
| Storage | 100MB |
| Users | 1 |
| Conversations | Unlimited |
| Query history | 7 days |
| Guardrails | Basic (Input/Output) |
| Support | Community |
| Uptime SLA | None |

**Includes:**
- ✅ Multi-format document ingestion (PDF, DOCX, TXT)
- ✅ Semantic search
- ✅ Basic guardrails
- ✅ Chat interface
- ✅ Mobile responsive

**Excluded:**
- ❌ HITL review workflow
- ❌ Advanced guardrails
- ❌ Hybrid search
- ❌ Reranking
- ❌ SSO/SAML
- ❌ API access
- ❌ Custom branding

---

### Pro Plan — $49/month
**Perfect for: Growing teams and departments**

| Feature | Limit |
|---------|-------|
| Bots | 5 |
| Queries/month | 10,000 |
| Documents/bot | 100 |
| Storage | 1GB |
| Users | 25 |
| Conversations | Unlimited |
| Query history | 90 days |
| Guardrails | Full (5-layer) |
| Support | Email (24h response) |
| Uptime SLA | 99.5% |

**Everything in Free, plus:**
- ✅ HITL review workflow
- ✅ Full 5-layer guardrails
- ✅ Risk engine
- ✅ Feature flags
- ✅ Audit logging
- ✅ All document parsers (9)
- ✅ Audio/Image OCR
- ✅ Admin dashboard

**Add-ons:**
- +$10/month: 5 additional bots
- +$10/month: 10,000 additional queries
- +$5/month: 500MB additional storage

---

### Enterprise Plan — Custom Pricing
**Perfect for: Large organizations with strict requirements**

| Feature | Limit |
|---------|-------|
| Bots | Unlimited |
| Queries/month | Unlimited |
| Documents/bot | Unlimited |
| Storage | Unlimited |
| Users | Unlimited |
| Conversations | Unlimited |
| Query history | 1 year |
| Guardrails | Full + Custom |
| Support | Dedicated (1h response) |
| Uptime SLA | 99.9% |

**Everything in Pro, plus:**
- ✅ SSO/SAML integration
- ✅ Custom guardrails
- ✅ Hybrid search (BM25 + Semantic)
- ✅ Reranking
- ✅ Query expansion (HyDE, Multi-query)
- ✅ Multi-tenant isolation
- ✅ Custom integrations
- ✅ On-premise deployment option
- ✅ Dedicated support engineer
- ✅ Custom SLA
- ✅ Security audit reports
- ✅ Compliance certifications

**Pricing starts at $499/month**

Contact sales@sia-chatbot.com for custom pricing.

---

## Feature Comparison

| Feature | Free | Pro | Enterprise |
|---------|------|-----|------------|
| Bots | 1 | 5 | Unlimited |
| Queries/month | 1,000 | 10,000 | Unlimited |
| Storage | 100MB | 1GB | Unlimited |
| Users | 1 | 25 | Unlimited |
| Document parsers | 3 | 9 | 9 + Custom |
| Semantic search | ✅ | ✅ | ✅ |
| Hybrid search | ❌ | ❌ | ✅ |
| Reranking | ❌ | ❌ | ✅ |
| Query expansion | ❌ | ❌ | ✅ |
| Basic guardrails | ✅ | ✅ | ✅ |
| Full guardrails | ❌ | ✅ | ✅ |
| Custom guardrails | ❌ | ❌ | ✅ |
| HITL workflow | ❌ | ✅ | ✅ |
| Risk engine | ❌ | ✅ | ✅ |
| Feature flags | ❌ | ✅ | ✅ |
| Audit logging | ❌ | ✅ | ✅ |
| SSO/SAML | ❌ | ❌ | ✅ |
| API access | ❌ | ❌ | ✅ |
| Webhooks | ❌ | ❌ | ✅ |
| Custom branding | ❌ | ❌ | ✅ |
| On-premise | ❌ | ❌ | ✅ |
| SLA | None | 99.5% | 99.9% |
| Support | Community | Email | Dedicated |

---

## Query Limits

| Plan | Monthly Queries | Rate Limit | Burst |
|------|----------------|------------|-------|
| Free | 1,000 | 10/min | 20 |
| Pro | 10,000 | 60/min | 100 |
| Enterprise | Unlimited | Custom | Custom |

---

## Storage Limits

| Plan | Storage | Max File Size | Retention |
|------|---------|---------------|-----------|
| Free | 100MB | 10MB | 30 days |
| Pro | 1GB | 50MB | 90 days |
| Enterprise | Unlimited | 500MB | 1 year |

---

## Overage Pricing

| Resource | Free | Pro | Enterprise |
|----------|------|-----|------------|
| Queries | N/A (blocked) | $0.005/query | Custom |
| Storage | N/A (blocked) | $0.10/GB/month | Custom |

---

## Annual Discounts

| Plan | Monthly | Annual | Savings |
|------|---------|--------|---------|
| Free | $0 | $0 | - |
| Pro | $49/month | $470/year | $418 (17% off) |
| Enterprise | Custom | Custom | Up to 25% off |

---

## Implementation Notes

### Usage Tracking
- Track queries per bot per organization
- Track storage usage per organization
- Daily aggregation for billing
- Real-time usage dashboard

### Limits Enforcement
- Soft limits: Warning at 80% usage
- Hard limits: Block at 100% usage
- Grace period: 3 days for overage

### Billing Integration
- Stripe for payment processing
- Webhook for subscription events
- Invoice generation
- Usage-based billing for overages
