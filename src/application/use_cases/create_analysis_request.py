from src.application.dtos.analysis_request_dto import CreateAnalysisRequestDTO
from src.application.interfaces.analysis_repository import AnalysisRepository
from src.application.services.request_id_generator import RequestIdGenerator
from src.core.entities.analysis_request import AnalysisRequest


class CreateAnalysisRequestUseCase:
    def __init__(
        self,
        repository: AnalysisRepository,
        request_id_generator: RequestIdGenerator,
    ) -> None:
        self.repository = repository
        self.request_id_generator = request_id_generator

    def execute(self, payload: CreateAnalysisRequestDTO) -> AnalysisRequest:
        request = AnalysisRequest(
            request_id=self.request_id_generator.next_id(),
            **payload.model_dump(),
        )
        self.repository.save_request(request)
        return request
