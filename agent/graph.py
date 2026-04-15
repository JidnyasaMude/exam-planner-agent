from langgraph.graph import StateGraph, END
from agent.state import PlannerState
from agent.agent1_syllabus_researcher import syllabus_researcher
from agent.agent2_topic_prioritizer import topic_prioritizer
from agent.agent3_plan_builder import plan_builder
from agent.agent4_judge import judge_agent

def should_revise(state: PlannerState) -> str:
    """
    Decision function.
    If score is low AND revision count is under 2,
    send back to plan_builder for revision.
    Otherwise end.
    """
    score = state.get("score", 0)
    revision_count = state.get("revision_count", 0)

    if score < 6 and revision_count < 2:
        return "revise"
    else:
        return "end"

def build_agent():
    graph = StateGraph(PlannerState)

    # Add all 4 agents
    graph.add_node("syllabus_researcher", syllabus_researcher)
    graph.add_node("topic_prioritizer", topic_prioritizer)
    graph.add_node("plan_builder", plan_builder)
    graph.add_node("judge_agent", judge_agent)

    # Straight edges
    graph.set_entry_point("syllabus_researcher")
    graph.add_edge("syllabus_researcher", "topic_prioritizer")
    graph.add_edge("topic_prioritizer", "plan_builder")
    graph.add_edge("plan_builder", "judge_agent")

    # Conditional edge — the real agent loop!
    graph.add_conditional_edges(
        "judge_agent",
        should_revise,
        {
            "revise": "plan_builder",  # loop back
            "end": END                 # finish
        }
    )

    agent = graph.compile()
    return agent