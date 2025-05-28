from Rag_agents.basemodel import BaseNode, OverallState
from langchain_openai import ChatOpenAI
import logging
from Rag_agents.configs.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)    

llm_model = ChatOpenAI(model="gpt-4o-mini")


class ScriptNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        topic = state.get("topic", "N/A")
        script = f"""Script for topic '{topic}':
Generate the script only for the topic based on the user prompt.
Output should describe the script in a very energetic and polite way and shouldn't go out of topic.
Do not generate video ideas when asked for script only in the user prompt.
Donot generate hashtags when asked for scripts only.
"""
        response = llm_model.invoke(script)
        logger.info("[ScriptNode] Generated script for topic: %s", topic)
        logger.debug("[ScriptNode] Script content:\n%s", script)

        # Update state dictionary directly

        state["script"] = response.content
        logger.info("[ScriptNode] Updated state with script.")

        return state #Returns the updated