from langgraph.graph import StateGraph, END
from services.agents import router_agent, personality_agent, skill_planner_agent, random_question_agent, feedback_agent
from schemas.schema import State

def get_react_agent():
    from langgraph.prebuilt import create_react_agent
    from services.model import get_llm
    from services.tools import web_search
    return create_react_agent(get_llm(), [web_search])

def build_graph():
    graph = StateGraph(State)
    graph.add_node("router_agent", router_agent)
    graph.add_node("personality_agent", personality_agent)
    graph.add_node("skill_planner_agent", skill_planner_agent)
    graph.add_node("random_question_agent", random_question_agent)
    graph.add_node("feedback_agent", feedback_agent)

    graph.add_conditional_edges("router_agent", lambda s: s["current_mode"], {
        "personality": "personality_agent",
        "skill": "skill_planner_agent",
        "random": "random_question_agent"
    })

    graph.add_edge("personality_agent", "feedback_agent")
    graph.add_edge("skill_planner_agent", "feedback_agent")
    graph.add_edge("random_question_agent", "feedback_agent")
    graph.add_edge("feedback_agent", END)
    graph.set_entry_point("router_agent")
    return graph.compile()