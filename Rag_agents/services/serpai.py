import requests
from Rag_agents.configs.config import SERPAPI_API_KEY
from Rag_agents.schemas.pydantic_schema import OverallState
from Rag_agents.basemodel import BaseNode

class SerpAPINode(BaseNode):
    def run(self, state: OverallState) -> OverallState:
        topic = state.topic

        params = {
            "engine": "google",
            "q": topic + " trends",
            "api_key": SERPAPI_API_KEY
        }

        try:
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()

            snippets = []
            if "organic_results" in data:
                for result in data["organic_results"]:
                    if "snippet" in result:
                        snippets.append(result["snippet"])

            hashtags = []
            for snippet in snippets:
                words = snippet.lower().split()
                for word in words:
                    clean = ''.join(filter(str.isalpha, word))
                    if clean and len(clean) > 4:
                        hashtags.append(f"#{clean}")

            hashtags = list(dict.fromkeys(hashtags))[:5]  # Deduplicate and limit
            search_results_text = "\n".join(snippets)

        except Exception as e:
            print(f"[SerpAPI Error] {e}")
            hashtags = []
            search_results_text = ""

        print(f"[SerpAPI] Hashtags: {hashtags}")
        print(f"[SerpAPI] Snippets:\n{search_results_text}")

        return state.copy(update={
            "hashtags": ", ".join(hashtags),
            "search_results": search_results_text
        })
