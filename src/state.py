from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    input: str
    intent: str
    list_of_tasks: List[str]
    approved: bool
    user_feedback: str
    messages: List[Dict[str, str]]
    step: str