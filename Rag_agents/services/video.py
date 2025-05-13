from langchain_openai import ChatOpenAI
from Rag_agents.schemas.pydantic_schema import OverallState
from Rag_agents.basemodel import BaseNode

llm_model = ChatOpenAI(model="gpt-4o-mini")

class VideoNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        prompt = f"""Using the following script, create a short visual plan or concept for a video:

Script:
'{state.script}'

Output should describe the video format, pacing, shots, and any visual ideas. Include hashtag ideas if relevant."""
        
        response = llm_model.invoke(prompt)
        print(f"[Video Node]\n{response.content}")

        return state.copy(update={"video": response.content})
