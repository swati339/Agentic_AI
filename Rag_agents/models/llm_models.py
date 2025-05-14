# from langchain_openai import ChatOpenAI
# from Rag_agents.prompts.prompt_templates import SystemPrompts
# from Rag_agents.basemodel import BaseNode, OverallState
# from Rag_agents.configs.logging_config import setup_logging
# import logging

# setup_logging()
# logger = logging.getLogger(__name__)

# class LLMReasoningNode(BaseNode):
#     def __init__(self):
#         self.llm_model = ChatOpenAI(model="gpt-4o-mini")
#         self.system_prompts = SystemPrompts()

#     def run(self, state: OverallState) -> OverallState:
#         topic = state["topic"].lower()
#         logger.info("----------123-------")
#         # Update the state based on the result
#         if "hashtag" in topic:
#             state["llm_output"] = response.content.strip()
#             state["next_route"] = "Hashtag_gen"
#         elif "video" in topic:
#             state["video"] = response.content.strip()
#             state["next_route"] = "Video Generation"
#         elif "script" in topic:
#             state["script"] = response.content.strip()
#             state["next_route"] = "Script Generation"
#         else:
#             state["llm_output"] = response.content.strip()


#         # Get the response from the model
#         response = self.llm_model.invoke(prompt_str)
#         print(f"[LLM Reasoning]\n{response.content}")
        
#         # Update the state based on the result
#         if "hashtag" in topic:
#             state["llm_output"] = response.content.strip()  # Only hashtags

#         elif "video" in topic:
#             state["video"] = response.content.strip()  # Video content
#         elif "script" in topic:
#             state["script"] = response.content.strip()  # Script content
#         else:
#             state["llm_output"] = response.content.strip()

#         return state

import json
from langchain_openai import ChatOpenAI
from Rag_agents.prompts.prompt_templates import SystemPrompts
from Rag_agents.basemodel import BaseNode, OverallState
from Rag_agents.configs.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class LLMReasoningNode(BaseNode):
    def __init__(self):
        self.llm_model = ChatOpenAI(model="gpt-4o-mini")
        self.system_prompts = SystemPrompts()

    def run(self, state: OverallState) -> OverallState:
        topic = state["topic"]
        logger.info("[LLMReasoningNode] Received topic: %s", topic)

        # Prompt asking for structured output
        prompt_str = (
            "You are a routing assistant.\n"
            "Given the following user prompt, detect the user's intent among: "
            "'Hashtag_gen', 'Script Generation', 'Video Generation', or 'None'.\n"
            "Then generate appropriate content. Respond strictly in this JSON format:\n"
            "{ \"intent\": \"<intent>\", \"content\": \"<your generated content>\" }\n\n"
            f"User prompt: {topic}"
        )

        # Call LLM
        response = self.llm_model.invoke(prompt_str)
        logger.info("[LLMReasoningNode] Raw LLM Response:\n%s", response.content)

        # Try parsing JSON output from LLM
        try:
            parsed = json.loads(response.content.strip())
            intent = parsed.get("intent", "").strip()
            content = parsed.get("content", "").strip()

            logger.info("[LLMReasoningNode] Parsed Intent: %s", intent)
            logger.info("[LLMReasoningNode] Parsed Content: %s", content)

            # Save content based on intent
            if intent == "Hashtag_gen":
                state["llm_output"] = content
                state["next_route"] = "Hashtag_gen"
            elif intent == "Script Generation":
                state["script"] = content
                state["next_route"] = "Script Generation"
            elif intent == "Video Generation":
                state["video"] = content
                state["next_route"] = "Video Generation"
            else:
                state["llm_output"] = content
                state["next_route"] = ""

        except json.JSONDecodeError as e:
            logger.warning("[LLMReasoningNode] Failed to parse JSON: %s", e)
            state["llm_output"] = response.content.strip()
            state["next_route"] = ""

        logger.info("[LLMReasoningNode] Final State after reasoning: %s", state)
        return state
