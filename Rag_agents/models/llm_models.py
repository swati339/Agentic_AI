import json
from langchain_openai import ChatOpenAI
from Rag_agents.prompts.prompt_templates import SystemPrompts
from Rag_agents.basemodel import BaseNode, OverallState
from Rag_agents.configs.logging_config import setup_logging
import logging
from dotenv import load_dotenv


load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)


class LLMReasoningNode(BaseNode): 
    def __init__(self):
        self.llm_model = ChatOpenAI(model="gpt-4o-mini")
        self.system_prompts = SystemPrompts()

    def run(self, state: OverallState) -> OverallState:
        topic = state["topic"]
        logger.info("[LLMReasoningNode] Received topic: %s", topic)

        prompt_str = (
            "You are a routing assistant.\n"
            "Given the user prompt, identify which tool to use next.\n"
            "Choose only one intent per turn from: 'Hashtag_gen', 'Script Generation', 'Video Generation', or 'None'.\n"
            "Respond strictly in JSON:\n"
            '{ "intent": "<intent>", "content": "<your generated content>" }\n\n'
            f"User prompt: {topic}"
        )

        response = self.llm_model.invoke(prompt_str)
        logger.info("[LLMReasoningNode] Raw LLM Response:\n%s", response.content)

        try:
            parsed = json.loads(response.content.strip())
            intent = parsed.get("intent", "").strip()
            content = parsed.get("content", "").strip()

            logger.info("[LLMReasoningNode] Parsed Intent: %s", intent)
            logger.info("[LLMReasoningNode] Parsed Content: %s", content)

            if intent == "Hashtag_gen":
                if not state.get("hashtags"):
                    state["llm_output"] = content  
                    state["next_route"] = "Hashtag_gen"
                else:
                    state["next_route"] = "complete"

            elif intent == "Script Generation":
                if not state.get("script"):
                    state["script"] = content
                    state["next_route"] = "Script Generation"
                else:
                    state["next_route"] = "complete"

            elif intent == "Video Generation":
                if not state.get("video"):
                    state["video"] = content
                    state["next_route"] = "Video Generation"
                else:
                    state["next_route"] = "complete"

            else:
                logger.info("[LLMReasoningNode] LLM chose to complete the process.")
                state["next_route"] = "complete"

        except json.JSONDecodeError as e:
            logger.warning("[LLMReasoningNode] JSON parsing failed: %s", e)
            state["llm_output"] = response.content.strip()
            state["next_route"] = "complete"

        logger.info("[LLMReasoningNode] Final State after reasoning: %s", state)
        return state
