import requests
from Rag_agents.configs.config import SERPAPI_API_KEY
from Rag_agents.basemodel import BaseNode, OverallState
from Rag_agents.configs.logging_config import setup_logging
import logging
import os
from dotenv import load_dotenv
import json

load_dotenv()

setup_logging()
logger = logging.getLogger(__name__)

class SerpAPINode(BaseNode):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("SERPAPI_API_KEY")

    def run(self, state: OverallState) -> OverallState:
        topic = state["topic"]

        params = {
            "engine": "google",
            "q": topic + " trends",
            "api_key": self.api_key
        }

        try:
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            data = response.json()

            snippets = []
            if "organic_results" in data:
                for result in data["organic_results"]:
                    if "snippet" in result:
                        snippets.append(result["snippet"])
                        logger.info("Displayed the organic results.")

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

        # Update state dictionary directly
        state["hashtags"] = ", ".join(hashtags)
        state["search_results"] = search_results_text
        logger.info(f"Intermediate step after serpaip {json.dumps(state, indent=2)}")

        return state  # Return the updated state
