import gradio as gr
from Rag_agents.graph_builder import build_graph
from Rag_agents.schemas.pydantic_schema import OverallState

# Build the LangGraph pipeline once
graph = build_graph()

def run_pipeline(topic: str) -> str:
    try:
        input_data = {"topic": topic}
        # Run the graph
        state_output = graph.invoke(input_data)

        # Cast the result to OverallState for attribute access
        final_state = OverallState(**state_output)

        result = f"""
Topic: {final_state.topic or 'N/A'}

LLM Output:
{final_state.llm_output or 'N/A'}

Search Results:
{final_state.search_results or 'N/A'}

Hashtags:
{final_state.hashtags or 'N/A'}

Script:
{final_state.script or 'N/A'}

Video Content:
{final_state.video or 'N/A'}

Voice Over:
{final_state.voice_over or 'N/A'}
"""
        return result.strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Gradio Interface
iface = gr.Interface(
    fn=run_pipeline,
    inputs=gr.Textbox(lines=1, placeholder="Enter a topic...", label="Topic"),
    outputs=gr.Textbox(lines=25, label="Generated Output"),
    title="Content Creator Assistant",
    description="Enter a topic to generate reasoning, search results, script, video content, and voice-over narration."
)

if __name__ == "__main__":
    iface.launch()
