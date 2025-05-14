from Rag_agents.basemodel import BaseNode, OverallState

class ScriptNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        script = f"""Script for topic '{state['topic']}':
{state['llm_output']}

Trending Hashtags: {state['hashtags']}
"""
        print(f"[Script Node]\n{script}")
        
        # Update state dictionary directly
        state["script"] = script
        
        return state  # Return the updated state
