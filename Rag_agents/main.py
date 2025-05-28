from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Rag_agents.services.serpai import SerpAPINode
from Rag_agents.services.script import ScriptNode
from Rag_agents.services.video import VideoNode
from Rag_agents.models.state_breakdown import StepBreakdownNode
from Rag_agents.models.llm_models import LLMReasoningNode

app = FastAPI()

# Tool map shared across requests
tool_map = {
    "StepBreakdown": StepBreakdownNode(),
    "Hashtag_gen": SerpAPINode(),
    "Script Generation": ScriptNode(),
    "Video Generation": VideoNode(),
    "LLM Reasoning": LLMReasoningNode(),
}

class PromptRequest(BaseModel):
    prompt: str


@app.post("/run-agent")
def run_agent(request: PromptRequest):
    topic = request.prompt.strip()

    if not topic:
        raise HTTPException(status_code=400, detail="Prompt is required.")

    # Initial state
    state = {
        "topic": topic,
        "llm_output": "",
        "script": "",
        "video": "",
        "search_results": "",
        "steps_generated": False,
        "hashtags": "",
        "next_route": "StepBreakdown",
        "steps": [],
        "current_step_index": 0,
    }

    try:
        while state.get("next_route") != "complete":
            current_route = state["next_route"]

            if current_route == "steps_loop":
                steps = state.get("steps", [])
                idx = state.get("current_step_index", 0)

                if idx >= len(steps):
                    state["next_route"] = "complete"
                    break

                next_step = steps[idx]
                tool = tool_map.get(next_step)
                if not tool:
                    state["next_route"] = "complete"
                    break

                state = tool.run(state)
                state["current_step_index"] += 1

            else:
                tool = tool_map.get(current_route)
                if not tool:
                    raise HTTPException(status_code=500, detail=f"Unknown node: {current_route}")

                state = tool.run(state)

                if current_route == "StepBreakdown":
                    if not state.get("steps"):
                        raise HTTPException(status_code=500, detail="No steps returned from StepBreakdown.")
                    state["next_route"] = "steps_loop"

        return {"result": state}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
