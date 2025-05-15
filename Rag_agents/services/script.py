from Rag_agents.basemodel import BaseNode, OverallState
from Rag_agents.configs.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


class ScriptNode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        topic = state.get("topic", "N/A")
        llm_output = state.get("llm_output", "")
        hashtags = state.get("hashtags", "")

        script = f"""Script for topic '{topic}':
{llm_output}

Trending Hashtags: {hashtags}
"""

        logger.info("[ScriptNode] Generated script for topic: %s", topic)
        logger.debug("[ScriptNode] Script content:\n%s", script)

        # Update state dictionary directly
        state["script"] = script
        logger.info("[ScriptNode] Updated state with script.")

        return state  # Returns the updated state
