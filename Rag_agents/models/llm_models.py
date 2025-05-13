from langchain_openai import ChatOpenAI
from Rag_agents.schemas.pydantic_schema import OverallState
from Rag_agents.prompts.prompt_templates import SystemPrompts
from Rag_agents.basemodel import BaseNode  # <-- use the base class

class LLMReasoningNode(BaseNode):
    def __init__(self):
        self.llm_model = ChatOpenAI(model="gpt-4o-mini")
        self.system_prompts = SystemPrompts()

    def run(self, state: OverallState) -> OverallState:
        prompt_str = self.system_prompts.prompt_template.format(topic=state.topic)
        response = self.llm_model.invoke(prompt_str)
        print(f"[LLM Reasoning]\n{response.content}")
        return state.copy(update={"llm_output": response.content})
