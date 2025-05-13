from langchain.prompts import PromptTemplate

class SystemPrompts:
    prompt_template = PromptTemplate.from_template(
    """You are a video content assistant.
Given a brand-related topic: {topic} and trending hashtags,
suggest a video theme or idea.
Mention the style, tone, and key points in 2-3 lines."""
)