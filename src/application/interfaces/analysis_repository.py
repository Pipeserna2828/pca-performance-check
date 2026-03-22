from abc import ABC, abstractmethod

from src.core.entities.analysis_request import AnalysisRequest
from src.core.entities.analysis_result import AnalysisResult


class AnalysisRepository(ABC):
    @abstractmethod
    def save_request(self, request: AnalysisRequest) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_request(self, request_id: str) -> AnalysisRequest | None:
        raise NotImplementedError

    @abstractmethod
    def save_result(self, result: AnalysisResult) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_result(self, request_id: str) -> AnalysisResult | None:
        raise NotImplementedError
