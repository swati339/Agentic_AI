from langgraph.graph import StateGraph, START, END
from Rag_agents.basemodel import OverallState
from Rag_agents.models.llm_models import LLMReasoningNode
from Rag_agents.services.serpai import SerpAPINode
from Rag_agents.services.script import ScriptNode
from Rag_agents.services.video import VideoNode


def build_graph():
    builder = StateGraph(OverallState)

    # Add nodes
    builder.add_node("LLM Reasoning", LLMReasoningNode().run)
    builder.add_node("Hashtag_gen", SerpAPINode().run)
    builder.add_node("Script Generation", ScriptNode().run)
    builder.add_node("Video Generation", VideoNode().run)

    builder.add_edge(START, "LLM Reasoning")

    def route_selector(state: OverallState) -> str:
        return state.get("next_route", "complete")

    builder.add_conditional_edges(
        "LLM Reasoning",
        route_selector,
        {
            "Hashtag_gen": "Hashtag_gen",
            "Script Generation": "Script Generation",
            "Video Generation": "Video Generation",
            "complete": END,
        },
    )

    # Return to LLM after tool execution
    builder.add_edge("Hashtag_gen", "LLM Reasoning")
    builder.add_edge("Script Generation", "LLM Reasoning")
    builder.add_edge("Video Generation", "LLM Reasoning")

    return builder.compile()
