# SIA Chatbot — Deployment Guide

## Overview

This guide covers deploying SIA Chatbot to production using:
- **Frontend**: Vercel (serverless)
- **Backend**: Docker containers (AWS/GCP/Azure)
- **Database**: Managed PostgreSQL + Redis
- **Storage**: S3/MinIO

## Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Vercel CLI
- AWS/GCP/Azure account
- Domain name (optional)

---

## 1. Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Configure Environment Variables
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=https://api.sia-chatbot.com
NEXT_PUBLIC_APP_NAME=SIA Chatbot
```

### Step 3: Deploy
```bash
cd frontend
vercel --prod
```

### Step 4: Configure Custom Domain
1. Go to Vercel Dashboard → Settings → Domains
2. Add your domain
3. Configure DNS records
4. Enable HTTPS

---

## 2. Backend Deployment (Docker)

### Step 1: Build Docker Image
```bash
docker build -t sia-chatbot-backend:latest .
```

### Step 2: Configure Environment Variables
```bash
# .env.production
DATABASE_URL=postgresql://user:pass@host:5432/sia_chatbot
REDIS_URL=redis://host:6379/0
CHROMADB_HOST=host
CHROMADB_PORT=8000
GEMINI_API_KEY=your_key
EURON_API_KEY=your_key
JWT_SECRET=your_random_secret
STORAGE_BUCKET=sia-chatbot-storage
```

### Step 3: Deploy with Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### docker-compose.prod.yml
```yaml
version: '3.8'

services:
  backend:
    image: sia-chatbot-backend:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - CHROMADB_HOST=chromadb
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - EURON_API_KEY=${EURON_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - chromadb
      - redis
      - postgres
    restart: always

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chromadb_data:/chroma/chroma
    restart: always

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: always

  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=sia_chatbot
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  celery:
    image: sia-chatbot-backend:latest
    command: celery -A backend.worker worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - redis
      - postgres
    restart: always

volumes:
  chromadb_data:
  redis_data:
  postgres_data:
```

---

## 3. Database Setup

### PostgreSQL
```bash
# Connect to PostgreSQL
psql -h host -U user -d sia_chatbot

# Run migrations
alembic upgrade head
```

### Alembic Setup
```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head
```

---

## 4. Redis Setup

### Configure Redis
```bash
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
```

### Test Connection
```bash
redis-cli ping
# Should return: PONG
```

---

## 5. Elasticsearch Setup (Phase 2)

### Deploy Elasticsearch
```bash
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.12.0
```

### Create Index
```bash
curl -X PUT "localhost:9200/documents" \
  -H 'Content-Type: application/json' \
  -d '{
    "mappings": {
      "properties": {
        "content": { "type": "text" },
        "document_id": { "type": "keyword" },
        "department": { "type": "keyword" }
      }
    }
  }'
```

---

## 6. Celery Worker Setup

### Start Worker
```bash
celery -A backend.worker worker \
  --loglevel=info \
  --concurrency=4 \
  -Q ingestion,default
```

### Start Beat (Scheduled Tasks)
```bash
celery -A backend.worker beat --loglevel=info
```

---

## 7. Monitoring (Phase 4)

### Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'sia-chatbot'
    static_configs:
      - targets: ['backend:8000']
```

### Grafana Dashboard
- Import dashboard: `grafana/dashboard.json`
- Configure Prometheus data source

---

## 8. SSL/TLS Configuration

### Using Certbot (Let's Encrypt)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d sia-chatbot.com -d api.sia-chatbot.com

# Auto-renew
sudo certbot renew --dry-run
```

### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name sia-chatbot.com;

    ssl_certificate /etc/letsencrypt/live/sia-chatbot.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sia-chatbot.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 9. Backup Procedures

### PostgreSQL Backup
```bash
# Daily backup
pg_dump -h host -U user sia_chatbot | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore
gunzip -c backup.sql.gz | psql -h host -U user sia_chatbot
```

### Redis Backup
```bash
# Trigger background save
redis-cli BGSAVE

# Copy dump.rdb to backup location
cp /data/dump.rdb /backup/redis_$(date +%Y%m%d).rdb
```

### ChromaDB Backup
```bash
# Copy ChromaDB data
tar -czf backup_chromadb_$(date +%Y%m%d).tar.gz /chroma/chroma
```

---

## 10. Scaling

### Horizontal Scaling
- Add more backend containers behind load balancer
- Scale Celery workers based on queue depth
- Use Redis Cluster for caching

### Vertical Scaling
- Increase CPU/RAM for backend containers
- Upgrade PostgreSQL instance
- Increase Redis memory

---

## 11. Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `CHROMADB_HOST` | ChromaDB host | localhost |
| `CHROMADB_PORT` | ChromaDB port | 8000 |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `EURON_API_KEY` | Euron embeddings API key | Required |
| `JWT_SECRET` | JWT signing secret | Required |
| `STORAGE_PROVIDER` | Storage provider (local/s3) | local |
| `STORAGE_BUCKET` | S3 bucket name | Required for S3 |
| `CELERY_BROKER_URL` | Celery broker URL | redis://localhost:6379/0 |

---

## 12. Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| ChromaDB connection refused | Check if ChromaDB container is running |
| Redis connection refused | Check if Redis container is running |
| PostgreSQL connection refused | Check if PostgreSQL container is running |
| Celery worker not processing | Check worker logs: `docker logs celery` |
| 502 Bad Gateway | Check if backend container is running |

### Logs
```bash
# Backend logs
docker logs sia-chatbot-backend

# Celery logs
docker logs celery

# Redis logs
docker logs redis

# PostgreSQL logs
docker logs postgres
```
