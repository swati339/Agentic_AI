from fastapi import FastAPI
from pydantic import BaseModel
from Rag_agents.graph_builder import build_graph
from Rag_agents.schemas.pydantic_schema import OverallState

app = FastAPI()

class ChatRequest(BaseModel):
    topic: str

graph = build_graph()

@app.post("/chat")
def chat(request: ChatRequest):
    input_data = {"topic": request.topic}
    raw_state = graph.invoke(input_data)

    # Convert LangGraph output (dict-like) to Pydantic model
    final_state = OverallState(**raw_state)
    return final_state.model_dump()
