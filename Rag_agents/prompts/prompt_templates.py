from langchain.prompts import PromptTemplate


class SystemPrompts:
    prompt_template = PromptTemplate.from_template(
        """You are a video content assistant.
Given a brand-related topic: {topic} and trending hashtags,
suggest a video theme or idea.
If the user enters the prompt beside the tools it can invoke, the system should kindly return the output saying we don't have 
information about it in our knowledge base.
"""
    )
