from typing import Annotated, List, Dict, Any, Optional
from typing_extensions import TypedDict 
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    success_criteria: str
    feedback_on_assist: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool