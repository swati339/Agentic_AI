# import gradio as gr
# from Rag_agents.graph_builder import build_graph
# from Rag_agents.basemodel import OverallState

# # Build the LangGraph pipeline once
# graph = build_graph()


# # def run_pipeline(topic: str) -> str:
# #     try:
# #         input_data = {"topic": topic}
# #         # Run the graph
# #         state_output = graph.invoke(input_data)

# #         # Cast the result to OverallState for attribute access
# #         final_state = OverallState(**state_output)

# #         result = f"""
# # Topic: {final_state.topic or "N/A"}

# # LLM Output:
# # {final_state.llm_output or "N/A"}

# # Search Results:
# # {final_state.search_results or "N/A"}

# # Hashtags:
# # {final_state.hashtags or "N/A"}

# # Script:
# # {final_state.script or "N/A"}

# # Video Content:
# # {final_state.video or "N/A"}

# # Voice Over:
# # {final_state.voice_over or "N/A"}
# # """
# #         return result.strip()

# #     except Exception as e:
# #         return f"An error occurred: {str(e)}"


# # # Gradio Interface
# # iface = gr.Interface(
# #     fn=run_pipeline,
# #     inputs=gr.Textbox(lines=1, placeholder="Enter a topic...", label="Topic"),
# #     outputs=gr.Textbox(lines=25, label="Generated Output"),
# #     title="Content Creator Assistant",
# #     description="Enter a topic to generate reasoning, search results, script, video content, and voice-over narration.",
# # )

# # if __name__ == "__main__":
# #     iface.launch()
# def run_pipeline(topic: str) -> str:
#     try:
#         input_data = {"topic": topic}
#         state_output = graph.invoke(input_data)

#         print("DEBUG: state_output =", state_output)

#         # Flatten dicts
#         if "llm_output" in state_output and isinstance(state_output["llm_output"], dict):
#             state_output["llm_output"] = state_output["llm_output"].get("content", "")

#         # Access values directly from dict instead of OverallState
#         result = f"""
# Topic: {state_output.get('topic', 'N/A')}

# LLM Output:
# {state_output.get('llm_output', 'N/A')}

# Search Results:
# {state_output.get('search_results', 'N/A')}

# Hashtags:
# {state_output.get('hashtags', 'N/A')}

# Script:
# {state_output.get('script', 'N/A')}

# Video Content:
# {state_output.get('video', 'N/A')}


# """
#         return result.strip()

#     except Exception as e:
#         return f"An error occurred: {str(e)}"


# #  Gradio Interface
# iface = gr.Interface(
#     fn=run_pipeline,
#     inputs=gr.Textbox(lines=1, placeholder="Enter a topic...", label="Topic"),
#     outputs=gr.Textbox(lines=25, label="Generated Output"),
#     title="Content Creator Assistant",
#     description="Enter a topic to generate reasoning, search results, script, video content ideas with script.",
# )

# if __name__ == "__main__":
#     iface.launch()

import gradio as gr
import requests

FASTAPI_URL = "http://localhost:8000/run-agent"  

def call_agent_api(prompt):
    if not prompt.strip():
        return "Prompt cannot be empty."

    try:
        response = requests.post(FASTAPI_URL, json={"prompt": prompt}, timeout=120)

        if response.status_code == 200:
            result = response.json()
            return result.get("result", "No result returned.")
        else:
            try:
                detail = response.json().get("detail", "Unknown error")
            except Exception:
                detail = response.text
            return f"Error {response.status_code}: {detail}"
    except Exception as e:
        return f"Request failed: {str(e)}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 💻 Agent Interface via FastAPI")
    prompt_input = gr.Textbox(label="Enter your prompt", placeholder="generate hashtags for my laptop brand.")
    output_display = gr.Textbox(label="Agent Output", lines=10, interactive=False)
    run_button = gr.Button("Run Agent")

    run_button.click(fn=call_agent_api, inputs=prompt_input, outputs=output_display)

# Launch Gradio
demo.launch()
