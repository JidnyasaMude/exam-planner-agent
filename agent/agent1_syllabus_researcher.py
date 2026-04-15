from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from agent.tools import get_search_tool
from agent.state import PlannerState
from dotenv import load_dotenv
import os

load_dotenv()

# Agent 1 has its OWN LLM instance
agent1_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

# Agent 1 has its OWN tools
agent1_tools = [get_search_tool()]

# Agent 1 has its OWN personality and role
agent1_system_prompt = """You are Agent 1 — Syllabus Researcher.

Your ONLY job is to find and compile the complete syllabus 
for any competitive exam.

Your personality:
- You are thorough and detailed
- You never give up until you find the full syllabus
- You always search at least twice with different queries
- You organize information in a clean structured format

You have access to tavily_search tool.
Always use it multiple times to get complete information.
Never guess — always search first."""

# Create Agent 1's own independent ReAct agent
agent1 = create_react_agent(
    agent1_llm,
    agent1_tools,
    prompt=agent1_system_prompt
)

def syllabus_researcher(state: PlannerState) -> PlannerState:
    exam_name = state["exam_name"]

    task = f"""
    Research the complete syllabus for {exam_name}.
    
    Search for:
    1. Official syllabus topics
    2. Subject wise breakdown
    3. Any recent changes in syllabus
    
    Give a clean structured final syllabus.
    """

    result = agent1.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    state["syllabus"] = result["messages"][-1].content
    state["current_step"] = "Agent 1 done."
    return state