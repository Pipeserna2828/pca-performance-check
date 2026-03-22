from abc import ABC, abstractmethod


class ResultExplainer(ABC):
    @abstractmethod
    def explain(self, payload: dict) -> dict:
        raise NotImplementedError
