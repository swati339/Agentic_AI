from langchain_openai import ChatOpenAI
from Rag_agents.schemas.pydantic_schema import OverallState
from Rag_agents.basemodel import BaseNode

llm_model = ChatOpenAI(model="gpt-4o-mini")

class VoiceOverNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        prompt = f"""Convert the following video script into a voice-over narration:

Script:
'{state.script}'

The tone should be energetic and engaging. Keep it natural and concise."""
        
        response = llm_model.invoke(prompt)
        print(f"[Voice-Over Node]\n{response.content}")
        
        return state.copy(update={"voice_over": response.content})
