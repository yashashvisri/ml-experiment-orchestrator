from langchain_core.messages import HumanMessage
from app.agents.graph import agent_app
from app.models.user import User

class AgentService:
    @staticmethod
    async def chat(message: str, current_user: User, project_id: str | None = None) -> str:
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
