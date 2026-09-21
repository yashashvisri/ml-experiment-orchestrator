from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.service import AgentService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    req: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    reply = await AgentService.chat(req.message, current_user, req.project_id)
    return ChatResponse(reply=reply)
