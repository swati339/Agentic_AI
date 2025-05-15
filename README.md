## Markdown

# Rag Agents: A Modular Script, Video content and Hashtag Generation Pipeline

This project implements a modular pipeline for generating scripts and trending hashtags based on a given topic. It uses SerpAPI to fetch real-time search snippets and can integrate with a language model to generate scripts. The architecture is designed using a node-based pattern where each processing step is encapsulated in a reusable and testable class.

## Features

- Fetches real-time search results from Google using SerpAPI
- Extracts and generates relevant trending hashtags from search snippets
- Supports script generation using pre-generated or LLM-based content
- Clean modular design using shared state for flexibility and extensibility
- Built-in logging for monitoring intermediate steps


## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/swati339/rag-agents.git
cd rag-agents

## 2. **Create virtual environment and install dependencies**

uv venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

uv pip install -e .


## 3. **Keep API_keys in .env file**
SERPAPI_API_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_api_key_here


## Load api keys using load dotenv
load_dotenv()

## Run the project
uv run Rag_agents/main.py
