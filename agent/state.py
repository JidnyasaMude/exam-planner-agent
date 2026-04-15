from typing import TypedDict, List, Dict, Any

class PlannerState(TypedDict):
    # User inputs
    exam_name: str
    weeks_available: int
    weak_topics: List[str]
    hours_per_day: int

    # Agent 1 output
    syllabus: str

    # Agent 2 output
    prioritized_topics: str

    # Agent 3 output
    study_plan: str

    # Agent 4 output
    evaluation: str
    score: int

    # Revision tracking
    revision_count: int
    current_step: str