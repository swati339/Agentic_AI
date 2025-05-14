# from langgraph.graph import StateGraph, START, END
# from Rag_agents.basemodel import OverallState  
# from Rag_agents.models.llm_models import LLMReasoningNode
# from Rag_agents.services.serpai import SerpAPINode
# from Rag_agents.services.script import ScriptNode
# from Rag_agents.services.video import VideoNode

# # import nest_asyncio
# # nest_asyncio.apply()

# # from IPython.display import Image, display
# # from langchain_core.runnables.graph import MermaidDrawMethod



# def build_graph():
#     builder = StateGraph(OverallState)

#     # Add the nodes (they must implement .run(state) -> state)
#     builder.add_node("LLM Reasoning", LLMReasoningNode().run)
#     builder.add_node("Hashtag_gen", SerpAPINode().run)
#     builder.add_node("Script Generation", ScriptNode().run)
#     builder.add_node("Video Generation", VideoNode().run)

#     builder.add_edge(START, "LLM Reasoning")

#     # Define routing logic
#     def route_selector(state: OverallState) -> str:
#         if state.get("video"):
#             return "complete"

#         next_route = state.get("next_route")
#         if next_route in ["Hashtag_gen", "Script Generation", "Video Generation"]:
#             return next_route
#         return "complete"

#     builder.add_conditional_edges(
#         "LLM Reasoning",
#         route_selector,
#         {
#             "Hashtag_gen": "Hashtag_gen",
#             "Script Generation": "Script Generation",
#             "Video Generation": "Video Generation",
#             "complete": END,
#         },
#     )

#     # Loop edges back to LLM
#     builder.add_edge("Hashtag_gen", "LLM Reasoning")
#     builder.add_edge("Script Generation", "LLM Reasoning")
#     builder.add_edge("Video Generation", "LLM Reasoning")
#     workflow = builder.compile()
#     return workflow
   



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

    # Updated route selector with proper exit criteria
    def route_selector(state: OverallState) -> str:
        next_route = state.get("next_route", "")
        if not next_route or next_route == "complete":
            return "complete"
        return next_route

    # Add conditional routing logic
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

    # Add return edges to LLM Reasoning
    builder.add_edge("Hashtag_gen", "LLM Reasoning")
    builder.add_edge("Script Generation", "LLM Reasoning")
    builder.add_edge("Video Generation", "LLM Reasoning")

    return builder.compile()
