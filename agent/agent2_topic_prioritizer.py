from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from agent.tools import get_search_tool
from agent.state import PlannerState
from dotenv import load_dotenv
import os

load_dotenv()

# Agent 2 has its OWN LLM instance
agent2_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# Agent 2 has its OWN tools
agent2_tools = [get_search_tool()]

# Agent 2 has its OWN personality
agent2_system_prompt = """You are Agent 2 — Topic Prioritizer.

Your ONLY job is to rank exam topics by importance and weightage.

Your personality:
- You are analytical and data-driven
- You look for mark distribution and previous year patterns
- You always search for weightage information before ranking
- You clearly mark which topics are HIGH, MEDIUM, LOW priority

You have access to tavily_search tool.
Search for weightage and previous year analysis before ranking."""

agent2 = create_react_agent(
    agent2_llm,
    agent2_tools,
    prompt=agent2_system_prompt
)

def topic_prioritizer(state: PlannerState) -> PlannerState:
    exam_name = state["exam_name"]
    syllabus = state["syllabus"]
    weak_topics = state["weak_topics"]

    task = f"""
    Prioritize topics for {exam_name}.
    
    Student weak topics: {', '.join(weak_topics)}
    
    Syllabus from Agent 1:
    {syllabus[:800]}
    
    Search for:
    1. High weightage topics in {exam_name}
    2. Previous year question distribution
    
    Give a ranked priority list with HIGH/MEDIUM/LOW labels.
    Mark student's weak topics specially.
    """

    result = agent2.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    state["prioritized_topics"] = result["messages"][-1].content
    state["current_step"] = "Agent 2 done."
    return state