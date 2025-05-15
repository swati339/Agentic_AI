from langchain_openai import ChatOpenAI
from Rag_agents.basemodel import BaseNode, OverallState
from Rag_agents.configs.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

llm_model = ChatOpenAI(model="gpt-4o-mini")


class VideoNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        prompt = f"""Using the following script, create a short visual plan or concept for a video:

Script:
'{state["script"]}'

Output should describe the video format, pacing, shots, and any visual ideas. Include hashtag ideas if relevant."""

        response = llm_model.invoke(prompt)
        print(f"[Video Node]\n{response.content}")

        # Update state dictionary directly
        state["video"] = response.content
        logger.info("Successfully invoked video generation function.")

        return state  # Return the updated state
