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
    steps: list[str]
    current_step_index: int
    steps_generated: bool


class BaseNode(ABC):
    @abstractmethod
    def run(self, state: OverallState) -> OverallState:
        pass
