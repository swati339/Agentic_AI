from abc import ABC, abstractmethod
from typing import TypedDict

class OverallState(TypedDict):
    topic: str
    llm_output: str
    script: str
    video: str
    voice_over: str
    search_results: str
    hashtags: str

class BaseNode(ABC):
    @abstractmethod
    def run(self, state: OverallState) -> OverallState:
        pass
