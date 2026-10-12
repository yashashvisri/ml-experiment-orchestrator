from langchain_core.messages import HumanMessage
from app.agents.graph import agent_app
from app.models.user import User
from app.core.config import settings

class AgentService:
    @staticmethod
    async def chat(message: str, current_user: User, project_id: str | None = None) -> str:
        if not settings.GEMINI_API_KEY:
            return "⚠️ Gemini API key is not configured. Please add `GEMINI_API_KEY=your_key` to your `backend/.env` file to chat with the AI Data Scientist."

        # Initialize state
        state = {
            "messages": [HumanMessage(content=message)],
            "user_id": str(current_user.id),
            "project_id": project_id
        }
        
        # Invoke agent
        try:
            result = await agent_app.ainvoke(state)
            return result["messages"][-1].content
        except Exception as e:
            return f"Agent error: {str(e)}"
