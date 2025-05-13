from langgraph.graph import StateGraph, END, START
from Rag_agents.schemas.pydantic_schema import OverallState

# Import the .run method from each class-based node
from Rag_agents.models.llm_models import LLMReasoningNode
from Rag_agents.services.serpai import SerpAPINode
from Rag_agents.services.script import ScriptNode
from Rag_agents.services.video import VideoNode
from Rag_agents.services.voiceover import VoiceOverNode

def build_graph():
    builder = StateGraph(OverallState)

    # Register each node's run method
    builder.add_node("llm_reasoning", LLMReasoningNode().run)
    builder.add_node("serpapi_enrichment", SerpAPINode().run)
    builder.add_node("create_script", ScriptNode().run)
    builder.add_node("create_video", VideoNode().run)
    builder.add_node("create_voice", VoiceOverNode().run)

    # Define graph flow
    builder.add_edge(START, "llm_reasoning")
    builder.add_edge("llm_reasoning", "serpapi_enrichment")
    builder.add_edge("serpapi_enrichment", "create_script")
    builder.add_edge("create_script", "create_video")
    builder.add_edge("create_video", "create_voice")
    builder.add_edge("create_voice", END)

    return builder.compile()
