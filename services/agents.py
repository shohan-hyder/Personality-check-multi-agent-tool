from typing import Dict
import json
import datetime
from schemas.schema import State

# Will be filled during conversation
def router_agent(state: State) -> State:
    # This will be driven by API input, not CLI
    return state

def personality_agent(state: State) -> State:
    from services.tools import generate_personalized_questions, analyze_personality

    user_data = state.get("user_data", {})
    print("\n--- 🧠 PERSONALITY ASSESSMENT ---")

    # Generate dynamic questions based on user context
    questions = generate_personalized_questions.invoke({
        "country": user_data["country"],
        "skills": user_data["skills"],
        "goal": user_data["goal"]
    })

    if len(questions) < 8:
        questions = [
            "I enjoy trying new ways of doing things.",
            "I plan my tasks in advance.",
            "I feel energized after social events.",
            "I try to help others even if it costs me time.",
            "Small setbacks bother me a lot.",
            "I like to finish work before relaxing.",
            "I start conversations easily.",
            "I stay calm under pressure."
        ]

    # === REPLACED SECTION STARTS HERE ===
    print("\n📝 Please answer each question on a scale of 1 to 5:")
    print("1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree\n")

    answers = {}
    for i, q in enumerate(questions, 1):
        while True:
            try:
                print(f"({i}/{len(questions)})")
                answer = input(f"  {q}\n  Your answer [1-5]: ").strip()
                if answer in ["1", "2", "3", "4", "5"]:
                    answers[q] = answer
                    break
                else:
                    print("❌ Invalid input. Please enter 1–5.\n")
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Session canceled.")
                return state
    print("\n✅ All answers collected!\n")
    # === REPLACED SECTION ENDS HERE ===

    # Analyze personality
    analysis = analyze_personality.invoke({"answers": answers})

    state["personality_score"] = analysis["score"]
    state["personality_feedback"] = analysis["summary"]
    state["improvement_tips"] = analysis["tips"]
    state["full_results"] = {
        "mode": "personality",
        "user_data": user_data,
        "personality": {
            "score": analysis["score"],
            "summary": analysis["summary"],
            "improvement_tips": analysis["tips"],
            "responses": answers
        }
    }

    print(f"📊 Final Personality Score: {analysis['score']}/100")
    return state


def skill_planner_agent(state: State) -> State:
    from services.tools import create_skill_plan
    ud = state["user_data"]
    current = ud.get("skills", "Not given")
    target = state.get("target_skill", "a new skill")
    timeline = state.get("timeline", "3 months")
    level = state.get("level", "Beginner")

    plan = create_skill_plan.invoke({
        "current_skills": current,
        "target_skill": target,
        "timeline": timeline,
        "level": level
    })

    state["skill_plan"] = plan
    state["full_results"] = {
        "mode": "skill",
        "user_data": ud,
        "goal": {"target": target, "timeline": timeline, "level": level},
        "plan": plan
    }
    return state

def random_question_agent(state: State) -> State:
    from services.graph import get_react_agent
    query = state["messages"][0].content
    agent = get_react_agent()
    result = agent.invoke({"messages": [state["messages"][0]]})
    answer = result["messages"][-1].content

    state["full_results"] = {"mode": "random", "question": query, "answer": answer}
    return state

def feedback_agent(state: State) -> State:
    # Save JSON
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"result_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(state["full_results"], f, indent=2)
    state["json_file"] = json_file
    return state