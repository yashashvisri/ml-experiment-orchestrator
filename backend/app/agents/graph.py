from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from app.agents.state import AgentState
from app.agents.tools import get_user_projects, get_project_experiments, get_experiment_runs
from app.core.config import settings

# Define tools
tools = [get_user_projects, get_project_experiments, get_experiment_runs]

def build_graph():
    # Model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)
    
    # Tool Node
    tool_node = ToolNode(tools)
    
    # Agent Node
    def agent_node(state: AgentState):
        messages = state["messages"]
        system_prompt = SystemMessage(
            content=f"You are a helpful AI Data Scientist Assistant. "
                    f"You have tools to query the ML orchestration database. "
                    f"The current user's ID is {state['user_id']}. "
                    f"If they ask about their projects, use that user_id."
        )
        response = llm_with_tools.invoke([system_prompt] + messages)
        return {"messages": [response]}
        
    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    # Graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

# Compile statically
agent_app = build_graph()
