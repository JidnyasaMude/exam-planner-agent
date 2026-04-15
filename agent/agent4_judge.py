from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from agent.state import PlannerState
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Agent 4 has its OWN LLM instance
agent4_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

# Judge does NOT need search tool — only critiques
agent4_tools = []

# Agent 4 has its OWN personality
agent4_system_prompt = """You are Agent 4 — The Judge.

Your ONLY job is to critically evaluate study plans.

Your personality:
- You are strict, honest, and fair
- You check every criterion carefully
- You never give high scores unless the plan truly deserves it
- You give specific, actionable feedback
- You think step by step before scoring

You do NOT use any tools.
You only read the plan and evaluate it carefully."""

agent4 = create_react_agent(
    agent4_llm,
    agent4_tools,
    prompt=agent4_system_prompt
)

def judge_agent(state: PlannerState) -> PlannerState:
    study_plan = state["study_plan"]
    exam_name = state["exam_name"]
    weeks_available = state["weeks_available"]
    weak_topics = state["weak_topics"]
    revision_count = state.get("revision_count", 0)

    task = f"""
    Evaluate this study plan for {exam_name}.
    Revision number: {revision_count}

    Weak topics that MUST be covered: {', '.join(weak_topics)}
    Weeks available: {weeks_available}

    Study plan:
    {study_plan}

    Check each criterion carefully:
    1. All weak topics covered? (0-3 points)
    2. Realistic for {weeks_available} weeks? (0-3 points)
    3. Good resources with links? (0-2 points)
    4. Revision week at end? (0-2 points)

    Respond in EXACTLY this format:
    Score: X/10
    Feasibility: (one sentence)
    Coverage: (one sentence)
    Suggestion: (one specific improvement)
    """

    result = agent4.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    final_response = result["messages"][-1].content

    score = 6
    match = re.search(r"Score:\s*(\d+)/10", final_response)
    if match:
        score = int(match.group(1))

    state["evaluation"] = final_response
    state["score"] = score
    state["current_step"] = f"Agent 4 done: Score {score}/10"
    return state