from Rag_agents.schemas.pydantic_schema import OverallState
from Rag_agents.basemodel import BaseNode

class ScriptNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        script = f"""Script for topic '{state.topic}':
{state.llm_output}

Trending Hashtags: {state.hashtags}
"""
        print(f"[Script Node]\n{script}")
        return state.copy(update={"script": script})
