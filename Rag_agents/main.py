from Rag_agents.graph_builder import build_graph


def main():
    topic = input("Enter your prompt: ").strip()

    if not topic:
        print("Topic is required.")
        return

    graph = build_graph()

    state = {
        "topic": topic,
        "llm_output": "",
        "script": "",
        "video": "",
        "search_results": "",
        "hashtags": "",
        "next_route": "",  # Empty initially; LLM decides next step
    }

    try:
        result = graph.invoke(state)
        print("\n[Final Output State]:\n")
        print(result)
    except Exception as e:
        print(f"[Error]: {str(e)}")


if __name__ == "__main__":
    main()
