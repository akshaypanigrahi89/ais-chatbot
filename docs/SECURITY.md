# SIA Chatbot — Security Considerations

## Overview

SIA Chatbot implements a comprehensive security architecture to protect enterprise data and ensure compliance with industry standards.

## Authentication

### JWT Tokens
- **Algorithm**: HS256
- **Expiry**: 60 minutes (configurable)
- **Refresh**: Not implemented (stateless)
- **Storage**: httpOnly cookie or Authorization header

### Password Hashing
- **Algorithm**: bcrypt
- **Salt rounds**: 12
- **Policy**: Minimum 8 characters, mixed case + numbers

### SSO/SAML (Enterprise)
- **Providers**: Okta, Azure AD, Google Workspace
- **Protocol**: SAML 2.0
- **Just-in-time provisioning**: Yes

---

## Authorization

### Role-Based Access Control (RBAC)

| Role | Permissions |
|------|-------------|
| `ADMIN` | Full system access |
| `USER` | Department-scoped access |
| `HR_ADMIN` | HR department admin |
| `MARKETING_ADMIN` | Marketing department admin |
| `COMPLIANCE_ADMIN` | Compliance department admin |

### Department-Level Isolation
- Users can only access documents in their assigned departments
- ChromaDB queries are filtered by department metadata
- Server-side enforcement (never trust frontend)

### Action Permissions

| Action | USER | ADMIN |
|--------|------|-------|
| `chat` | ✅ | ✅ |
| `view_documents` | ✅ | ✅ |
| `upload_documents` | ❌ | ✅ |
| `delete_documents` | ❌ | ✅ |
| `manage_users` | ❌ | ✅ |
| `manage_settings` | ❌ | ✅ |
| `manage_flags` | ❌ | ✅ |

---

## Input Validation

### Pydantic Schemas
- All inputs validated against Pydantic models
- Type checking and constraint validation
- Max length limits on all string fields

### Guardrails (5 Layers)

#### Layer 1: Input Guardrails
- **40+ regex patterns** for threat detection
- **Prompt injection** detection
- **System prompt extraction** detection
- **Credential request** detection
- **Role manipulation** detection
- **Code/SQL injection** detection
- **Sanitization**: Strip zero-width characters, control characters

#### Layer 2: Auth Guardrails
- Server-side RBAC enforcement
- Department access validation
- Request integrity checks

#### Layer 3: Retrieval Guardrails
- Quality classification (SUFFICIENT/LOW_CONFIDENCE/INSUFFICIENT)
- Conflict detection
- Unauthorized department leak detection

#### Layer 4: Prompt Guardrails
- **10 non-overridable security rules** (SECURITY_ANCHOR)
- Prompt validation (blocks "ignore security rules", "god mode")
- SHA-256 prompt hashing

#### Layer 5: Output Guardrails
- **Secret/credential leakage** detection (8 patterns)
- **Instruction leak** detection (5 patterns)
- **Sensitive info** detection (SSN, CC)
- **Fabricated citation** detection
- **Groundedness** verification

---

## Data Protection

### Encryption at Rest
- **Database**: PostgreSQL TDE (Transparent Data Encryption)
- **Storage**: S3 server-side encryption (SSE-S3)
- **Backups**: Encrypted backups

### Encryption in Transit
- **TLS 1.3** for all API calls
- **HTTPS** enforced (HSTS headers)
- **Certificate pinning** (optional)

### Data Retention
| Data Type | Free | Pro | Enterprise |
|-----------|------|-----|------------|
| Conversations | 7 days | 90 days | 1 year |
| Documents | 30 days | 90 days | 1 year |
| Audit logs | 30 days | 1 year | 7 years |

### Data Deletion
- Users can delete their conversations
- Admins can delete documents (cascading delete)
- Soft delete with 30-day purge

---

## Audit Logging

### Logged Events
| Event | Details |
|-------|---------|
| Login/Logout | User ID, IP, timestamp |
| Document upload | User ID, file, department |
| Document delete | User ID, document ID |
| Chat message | User ID, query, response |
| Guardrail block | Threat type, severity |
| Settings change | User ID, setting, old/new value |
| Review action | Reviewer ID, action, comment |

### Audit Log Format
```json
{
  "id": 1,
  "user_id": 1,
  "action": "document_upload",
  "resource_type": "document",
  "resource_id": 1,
  "details": {
    "file_name": "policy.pdf",
    "department": "HR"
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Rate Limiting

### Limits by Plan

| Plan | Requests/min | Burst | Query Limit |
|------|--------------|-------|-------------|
| Free | 10 | 20 | 1,000/month |
| Pro | 60 | 100 | 10,000/month |
| Enterprise | Custom | Custom | Unlimited |

### Implementation
- Redis-based sliding window
- Per-user and per-IP limiting
- Custom headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Security Headers

### Nginx Configuration
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## Vulnerability Management

### Dependency Scanning
- **npm audit** for frontend
- **pip-audit** for backend
- **Dependabot** for GitHub

### Penetration Testing
- Annual third-party penetration testing
- Quarterly internal security reviews
- Bug bounty program (Enterprise)

### Incident Response
1. **Detection**: Monitor logs and alerts
2. **Containment**: Isolate affected systems
3. **Eradication**: Remove threat
4. **Recovery**: Restore from backups
5. **Lessons Learned**: Post-incident review

---

## Compliance

### SOC 2 Type II (Enterprise)
- Access controls
- Audit logging
- Data encryption
- Incident response
- Vendor management

### GDPR
- Data minimization
- Right to deletion
- Data portability
- Privacy by design

### HIPAA (Enterprise)
- BAA available
- PHI encryption
- Access controls
- Audit logging

---

## Security Checklist

### Development
- [ ] No secrets in code
- [ ] Input validation on all endpoints
- [ ] Output sanitization
- [ ] Dependency scanning
- [ ] SAST (Static Application Security Testing)

### Deployment
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Database encrypted

### Operations
- [ ] Audit logging enabled
- [ ] Monitoring and alerting
- [ ] Backup procedures
- [ ] Incident response plan
- [ ] Regular security reviews

---

## Security Contacts

- **Security Team**: security@sia-chatbot.com
- **Bug Bounty**: https://sia-chatbot.com/security
- **Incident Response**: incident@sia-chatbot.com
