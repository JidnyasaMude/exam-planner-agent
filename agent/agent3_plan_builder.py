from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from agent.tools import get_search_tool
from agent.state import PlannerState
from dotenv import load_dotenv
import os

load_dotenv()

# Agent 3 has its OWN LLM instance
agent3_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.4
)

# Agent 3 has its OWN tools
agent3_tools = [get_search_tool()]

# Agent 3 has its OWN personality
agent3_system_prompt = """You are Agent 3 — Study Plan Builder.

Your ONLY job is to build realistic week-by-week study plans.

Your personality:
- You are practical and realistic
- You always find real resources with actual links
- You never make a plan without searching for resources first
- You always include revision week at the end
- When given feedback, you carefully fix every issue

You have access to tavily_search tool.
Always search for real resources before building the plan."""

agent3 = create_react_agent(
    agent3_llm,
    agent3_tools,
    prompt=agent3_system_prompt
)

def plan_builder(state: PlannerState) -> PlannerState:
    exam_name = state["exam_name"]
    weeks_available = state["weeks_available"]
    weak_topics = state["weak_topics"]
    hours_per_day = state["hours_per_day"]
    prioritized_topics = state["prioritized_topics"]
    revision_count = state.get("revision_count", 0)
    previous_feedback = state.get("evaluation", "")

    revision_note = ""
    if revision_count > 0:
        revision_note = f"""
        THIS IS REVISION #{revision_count}.
        Judge feedback you MUST fix:
        {previous_feedback}
        """

    task = f"""
    Build a week-by-week study plan for {exam_name}.
    
    Student details:
    - Weeks: {weeks_available}
    - Hours/day: {hours_per_day}
    - Weak topics: {', '.join(weak_topics)}
    
    {revision_note}
    
    Priority topics from Agent 2:
    {prioritized_topics[:600]}
    
    Search for:
    1. Best resources for {weak_topics[0]} for {exam_name}
    2. Best YouTube or websites for {exam_name} preparation
    
    Then build complete week-by-week plan:
    Week | Topics | Daily Target | Resources | Goal
    
    Last week must be revision + mock tests.
    """

    result = agent3.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    state["study_plan"] = result["messages"][-1].content
    state["revision_count"] = revision_count + 1
    state["current_step"] = f"Agent 3 done: revision {revision_count}"
    return state