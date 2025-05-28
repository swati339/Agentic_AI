import json
import logging
from langchain_openai import ChatOpenAI
from Rag_agents.basemodel import BaseNode, OverallState

logger = logging.getLogger(__name__)


class StepBreakdownNode(BaseNode):
    """
    This node analyzes a user prompt and breaks it into a sequence of high-level tasks
    selected from a fixed set: Hashtag_gen, Script Generation, Video Generation.
    After breaking down the user prompt, the llm decides which tool to call and processes according to that.
    """

    def __init__(self):
        self.llm_model = ChatOpenAI(model="gpt-4o-mini")

    def run(self, state: OverallState) -> OverallState:
        """
        Processes the user prompt to generate a list of high-level steps.

        Args:
            state (OverallState): The current system state, which includes the user prompt.

        Returns:
            OverallState: Updated system state with identified steps and routing info.
        """
        user_prompt = state.get("topic", "").strip()
        logger.info(
            "[StepBreakdownNode] Generating steps for user prompt: '%s'", user_prompt
        )

        prompt_str = (
            "You are an AI workflow planner. Based on the user prompt below, "
            "break the task into 2–5 high-level steps.\n"
            "The steps must be selected from the following: Hashtag_gen, Script Generation, Video Generation.\n"
            "Select tools based on user prompt. Donot generate always generate all while asking for only one.\n"
            "Respond only with a JSON list of strings, for example:\n"
            '["Hashtag_gen", "Script Generation", "Video Generation"]\n\n'
            f"User prompt: {user_prompt}"
        )

        try:
            response = self.llm_model.invoke(prompt_str)
            logger.debug("[StepBreakdownNode] Raw response: %s", response)

            content = getattr(response, "content", str(response)).strip()
            steps = json.loads(content)

            if not isinstance(steps, list) or not all(
                isinstance(step, str) for step in steps
            ):
                raise ValueError("LLM response is not a valid JSON list of strings.")

            logger.info("[StepBreakdownNode] Steps generated: %s", steps)

            state["steps"] = steps
            state["current_step_index"] = 0
            state["next_route"] = "LLM Reasoning"
            state["steps_generated"] = True

        except json.JSONDecodeError as json_err:
            logger.warning("[StepBreakdownNode] JSON parsing error: %s", json_err)
            self._set_failure_state(state)

        except Exception as e:
            logger.warning("[StepBreakdownNode] Unexpected error: %s", e)
            self._set_failure_state(state)

        return state

    def _set_failure_state(self, state: OverallState):
        state["steps"] = []
        state["next_route"] = "complete"
        state["steps_generated"] = False
