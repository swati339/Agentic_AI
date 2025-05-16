import json
import logging
from langchain_openai import ChatOpenAI
from Rag_agents.basemodel import BaseNode, OverallState
from dotenv import load_dotenv
from Rag_agents.configs.logging_config import setup_logging

# Setup
load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)


class LLMReasoningNode(BaseNode):
    def __init__(self):
        self.llm_model = ChatOpenAI(model="gpt-4o-mini")

    def run(self, state: OverallState) -> OverallState:
        if not state.get("steps_generated", False):
            logger.warning(
                "[LLMReasoningNode] Steps not generated yet. Skipping execution."
            )
            state["next_route"] = "complete"
            return state

        steps = state.get("steps", [])
        index = state.get("current_step_index", 0)

        if index >= len(steps):
            logger.info("[LLMReasoningNode] No more steps. Finishing.")
            state["next_route"] = "complete"
            return state

        current_step = steps[index]
        user_input = state.get("topic", "")
        logger.info(
            "[LLMReasoningNode] Executing step %d/%d: %s",
            index + 1,
            len(steps),
            current_step,
        )

        prompt_str = (
            f"You are completing the step: {current_step} for the following user request.\n"
            "Generate only the relevant content for this step. Respond strictly in JSON like:\n"
            '{ "content": "<your generated output for this step>" }\n\n'
            f"User prompt: {user_input}"
        )

        try:
            response = self.llm_model.invoke(prompt_str)
            logger.info("[LLMReasoningNode] LLM Response:\n%s", response.content)

            if isinstance(response.content, str):
                parsed = json.loads(response.content.strip())
            elif isinstance(response.content, dict):
                parsed = response.content
            else:
                raise ValueError("Unexpected response content type")

            content = parsed.get("content", {})

            # Handle current step specifically
            if current_step == "Script Generation":
                state["video_concept"] = content
            elif current_step == "Hashtag_gen":
                state["hashtags"] = content if isinstance(content, list) else [content]
            elif current_step == "Video Generation":
                state["shoot_locations"] = content

            # Next step handling
            state["current_step_index"] += 1
            state["next_route"] = (
                state["steps"][state["current_step_index"]]
                if state["current_step_index"] < len(state["steps"])
                else "complete"
            )

        except Exception as e:
            logger.warning("[LLMReasoningNode] Failed to parse LLM output: %s", e)
            state["next_route"] = "complete"

        return state

