from Rag_agents.services.serpai import SerpAPINode
from Rag_agents.services.script import ScriptNode
from Rag_agents.services.video import VideoNode
from Rag_agents.models.state_breakdown import StepBreakdownNode
from Rag_agents.models.llm_models import LLMReasoningNode

import json


def main():
    topic = input("Enter your prompt: ").strip()

    if not topic:
        print("Topic is required.")
        return

    # Define tool routing map
    tool_map = {
        "StepBreakdown": StepBreakdownNode(),
        "Hashtag_gen": SerpAPINode(),
        "Script Generation": ScriptNode(),
        "Video Generation": VideoNode(),
        "LLM Reasoning": LLMReasoningNode(),
    }

    # Initial state
    state = {
        "topic": topic,
        "llm_output": "",
        "script": "",
        "video": "",
        "search_results": "",
        "steps_generated": False,
        "hashtags": "",
        "next_route": "StepBreakdown",  # Start with planner
        "steps": [],
        "current_step_index": 0,
    }

    try:
        while state.get("next_route") != "complete":
            current_route = state["next_route"]
            print(f"\nRunning node: {current_route}")

            if current_route == "steps_loop":
                # We're now going to iterate through planned steps
                steps = state.get("steps", [])
                idx = state.get("current_step_index", 0)

                if idx >= len(steps):
                    print("\nAll steps completed.")
                    state["next_route"] = "complete"
                    break

                next_step = steps[idx]
                tool = tool_map.get(next_step)
                if not tool:
                    print(f"[Warning]: Unknown step: {next_step}")
                    state["next_route"] = "complete"
                    break

                print(f"--> Executing step: {next_step}")
                state = tool.run(state)
                state["current_step_index"] += 1

            else:
                # Initial or special route (e.g., StepBreakdown or LLM Reasoning)
                tool = tool_map.get(current_route)
                if not tool:
                    print(f"[Error]: Unknown node: {current_route}")
                    break

                state = tool.run(state)

                # If StepBreakdown has completed, begin looping over steps
                if current_route == "StepBreakdown":
                    if not state.get("steps"):
                        print("[Error]: No steps returned from StepBreakdown.")
                        break
                    state["next_route"] = "steps_loop"

        print("\nFinal Output State:\n")
        print(json.dumps(state, indent=2))

    except Exception as e:
        print(f"[Exception Caught]: {str(e)}")


if __name__ == "__main__":
    main()

