# services/tools.py
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import json
from services.model import get_llm
from services.config import Config

llm = get_llm()

@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information."""
    try:
        search = TavilySearch(max_results=3, include_answer=True, tavily_api_key=Config.TAVILY_API_KEY)
        result = search.invoke(query)
        return result.get("answer", "No answer found.")
    except Exception as e:
        return f"Search error: {str(e)}"

@tool
def generate_personalized_questions(country: str, skills: str, goal: str) -> list:
    """Generate 8 adaptive personality questions based on user context."""
    prompt = f"""
    Create 8 short personality questions (1–5 scale) for someone from {country},
    with skills in {skills}, wanting to learn {goal}.
    One per line.
    """
    response = llm.invoke([{"role": "user", "content": prompt}])
    questions = [q.strip() for q in response.content.strip().split("\n") if q.strip()]
    return questions[:8]

@tool
def analyze_personality(answers: dict) -> dict:
    """Analyze personality using Big Five (OCEAN) model and return score, summary, and tips."""
    prompt = """
    Analyze responses using Big Five (OCEAN). Calculate score out of 100.
    Format:
    ### SCORE
    [Number]/100

    ### SUMMARY
    [5 lines]

    ### TIPS
    [2 lines]
    """
    full_prompt = prompt + "\n" + json.dumps(answers, indent=2)
    response = llm.invoke([{"role": "user", "content": full_prompt}])
    content = response.content.strip()

    try:
        score = int(content.split("### SCORE")[1].split("### SUMMARY")[0].strip().split("/")[0])
        summary = content.split("### SUMMARY")[1].split("### TIPS")[0].strip()
        tips = content.split("### TIPS")[1].strip()
    except Exception:
        score, summary, tips = 65, "Balanced and capable of growth.", "Set small goals and reflect daily."

    return {"score": score, "summary": summary, "tips": tips}

@tool
def create_skill_plan(current_skills: str, target_skill: str, timeline: str, level: str) -> str:
    """Create a personalized learning plan with real resources."""
    search_query = f"best free resources to learn {target_skill} for {level}"
    search_result = web_search.invoke({"query": search_query})

    prompt = f"""
    Create a step-by-step plan for:
    - Current: {current_skills}
    - Target: {target_skill}
    - Timeline: {timeline}
    - Level: {level}

    Use: {search_result}
    Include: weekly milestones, free courses, mini-projects.
    """
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip()