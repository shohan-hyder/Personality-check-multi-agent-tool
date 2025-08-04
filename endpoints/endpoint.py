from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.graph import build_graph

router = APIRouter()
app = build_graph()

class QueryRequest(BaseModel):
    mode: str  # "personality", "skill", "random"
    name: Optional[str] = None
    country: Optional[str] = None
    age: Optional[str] = None
    skills: Optional[str] = None
    goal: Optional[str] = None
    target_skill: Optional[str] = None
    timeline: Optional[str] = None
    level: Optional[str] = None
    question: Optional[str] = None

@router.post("/query")
def run_agent(data: QueryRequest):
    try:
        initial_state = {
            "messages": [],
            "user_data": {
                "name": data.name,
                "country": data.country,
                "age": data.age,
                "skills": data.skills,
                "goal": data.goal
            },
            "current_mode": data.mode,
            "personality_score": 0,
            "personality_feedback": "",
            "improvement_tips": "",
            "skill_plan": "",
            "full_results": {}
        }

        if data.question and data.mode == "random":
            from langchain_core.messages import HumanMessage
            initial_state["messages"] = [HumanMessage(content=data.question)]

        if data.target_skill:
            initial_state["target_skill"] = data.target_skill
        if data.timeline:
            initial_state["timeline"] = data.timeline
        if data.level:
            initial_state["level"] = data.level

        result = app.invoke(initial_state)
        return {"status": "success", "data": result["full_results"], "pdf": result.get("pdf_report"), "json": result.get("json_file")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))