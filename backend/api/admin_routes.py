from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.models.database import get_db, User, Document
from backend.models.schemas import DashboardStats, SettingsUpdate, CacheStats, FeatureFlagResponse
from backend.auth.dependencies import require_admin
from backend.cache.cag_cache import cag_cache
from backend.vectorstore.chroma_store import chroma_store

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    total_docs = db.query(Document).count()
    completed = db.query(Document).filter(Document.status == "COMPLETED").count()
    processing = db.query(Document).filter(Document.status == "PROCESSING").count()
    failed = db.query(Document).filter(Document.status == "FAILED").count()

    stats = chroma_store.get_stats()

    return DashboardStats(
        total_documents=total_docs,
        indexed_documents=completed,
        processing_documents=processing,
        failed_documents=failed,
        total_chunks=stats.get("total_chunks", 0),
        total_conversations=0,
        total_messages=0,
        departments=["General", "HR", "Marketing", "Finance", "IT"]
    )


@router.get("/documents")
async def list_documents(
    limit: int = 20,
    offset: int = 0,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    docs = db.query(Document).offset(offset).limit(limit).all()
    total = db.query(Document).count()
    return {"documents": docs, "total": total, "limit": limit, "offset": offset}


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    department: str = Form(...),
    category: str = Form(None),
    title: str = Form(None),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    doc = Document(
        title=title or file.filename,
        file_name=file.filename,
        file_size=file.size,
        department=department,
        category=category,
        status="UPLOADED"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "title": doc.title,
        "file_name": doc.file_name,
        "status": doc.status,
        "department": doc.department,
        "category": doc.category,
        "created_at": doc.created_at
    }


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully"}


@router.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats(admin: User = Depends(require_admin)):
    stats = cag_cache.get_stats()
    return CacheStats(**stats)


@router.post("/cache/flush")
async def flush_cache(admin: User = Depends(require_admin)):
    count = cag_cache.flush()
    return {"message": "Cache flushed successfully", "entries_removed": count}


@router.get("/settings")
async def get_settings(admin: User = Depends(require_admin)):
    return {
        "llm_provider": "gemini",
        "llm_model": "gemini-flash-latest",
        "embedding_provider": "euron",
        "embedding_model": "text-embedding-3-small",
        "chunk_size": 800,
        "chunk_overlap": 100,
        "similarity_threshold": 0.70,
        "max_results": 10
    }


@router.put("/settings")
async def update_settings(settings: SettingsUpdate, admin: User = Depends(require_admin)):
    return {"message": "Settings updated successfully"}


@router.get("/flags")
async def get_flags(admin: User = Depends(require_admin)):
    flags = [
        {"name": "AI_ASSISTANT_ENABLED", "description": "Master switch for AI assistant", "enabled": True, "default_value": True},
        {"name": "CHAT_ENABLED", "description": "Chat interface enabled", "enabled": True, "default_value": True},
        {"name": "DOCUMENT_INGESTION_ENABLED", "description": "Document upload enabled", "enabled": True, "default_value": True},
        {"name": "ENABLE_HILP", "description": "Human-in-the-loop review", "enabled": True, "default_value": True},
        {"name": "ENABLE_INPUT_GUARDRAILS", "description": "Input validation", "enabled": True, "default_value": True},
        {"name": "ENABLE_OUTPUT_GUARDRAILS", "description": "Output validation", "enabled": True, "default_value": True},
    ]
    return {"flags": flags}


@router.post("/reviews/{review_id}/approve")
async def approve_review(
    review_id: int,
    admin: User = Depends(require_admin)
):
    return {"message": "Review approved"}


@router.post("/reviews/{review_id}/reject")
async def reject_review(
    review_id: int,
    admin: User = Depends(require_admin)
):
    return {"message": "Review rejected"}
