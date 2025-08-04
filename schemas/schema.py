from typing import Dict, List, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage

class State(TypedDict):
    messages: Annotated[List[HumanMessage], "add_messages"]  # List of messages
    user_data: dict  # User profile data (Fixed NameError)
    current_mode: str  # Current agent mode
    personality_score: int  # Final score out of 100
    personality_feedback: str  # 5-line summary
    improvement_tips: str  # 2-line tips
    skill_plan: str  # Generated learning plan
    full_results: dict  # For JSON/PDF export