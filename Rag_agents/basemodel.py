from abc import ABC, abstractmethod
from typing import TypedDict

class OverallState(TypedDict):
    topic: str
    llm_output: str
    script: str
    video: str
    search_results: str
    hashtags: str
    next_route: str

class BaseNode(ABC):
    @abstractmethod
    def run(self, state: OverallState) -> OverallState:
        pass
