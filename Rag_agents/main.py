# from Rag_agents.graph_builder import build_graph

# def main():
#     # Step 1: Ask the user for a prompt
#     topic = input("Enter your prompt: ").strip()

#     if not topic:
#         print("Topic is required.")
#         return

#     # Step 2: Build the LangGraph
#     graph = build_graph()

#     # Step 3: Create the initial OverallState dict
#     state = {
#         "topic": topic,
#         "llm_output": "",
#         "script": "",
#         "video": "",
#         "search_results": "",
#         "hashtags": "",
#         "next_route": "",  
#     }

#     # Step 4: Invoke the graph
#     try:
#         result = graph.invoke(state)
#         print("\nResult:\n")
#         print(result)
#     except Exception as e:
#         print(f"\nError running graph: {str(e)}")

# if __name__ == "__main__":
#     main()

from Rag_agents.graph_builder import build_graph

MAX_RECURSION_LIMIT = 3

def main():
    # Step 1: Ask the user for a prompt
    topic = input("Enter your prompt: ").strip()

    if not topic:
        print("Topic is required.")
        return

    # Step 2: Build the LangGraph
    graph = build_graph()

    # Step 3: Create the initial OverallState dict
    state = {
        "topic": topic,
        "llm_output": "",
        "script": "",
        "video": "",
        "search_results": "",
        "hashtags": "",
        "next_route": "Hashtag_gen",  
    }

    previous_routes = set()
    steps = 0

    # Step 4: Step through the graph based on next_route
    while steps < MAX_RECURSION_LIMIT:
        current_route = state.get("next_route")

        if not current_route:
            print("[STOP] No 'next_route' defined. Ending execution.")
            break

        print(f"\n[STEP {steps+1}] Running route: {current_route}")

        if current_route in previous_routes:
            print(f"[STOP] Route '{current_route}' already visited. Stopping recursion.")
            break
        previous_routes.add(current_route)

        try:
            state = graph.invoke(state)
        except Exception as e:
            print(f"[ERROR] Error running graph at route '{current_route}': {str(e)}")
            break

        # Show intermediate LLM output (optional)
        if state.get("llm_output"):
            print("[LLM OUTPUT]:", state["llm_output"])

        steps += 1

    if steps >= MAX_RECURSION_LIMIT:
        print(f"[ERROR] Recursion limit of {MAX_RECURSION_LIMIT} reached without halting.")

    print("\nFinal State:\n")
    print(state)

if __name__ == "__main__":
    main()
