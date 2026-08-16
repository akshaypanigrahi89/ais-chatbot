from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db, User
from backend.models.schemas import ChatRequest, ChatResponse
from backend.auth.dependencies import get_current_user
from backend.services.agent import run_agent

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = await run_agent(
        query=request.message,
        user_id=str(current_user.id),
        department=request.department or current_user.departments[0] if current_user.departments else "General"
    )

    return ChatResponse(
        message=result["response"],
        conversation_id="new",
        message_id="1",
        sources=result["sources"],
        groundedness=result["groundedness"],
        guardrails=result["guardrails"]
    )


@router.get("/history")
async def get_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
):
    return {"conversations": [], "total": 0, "limit": limit, "offset": offset}
