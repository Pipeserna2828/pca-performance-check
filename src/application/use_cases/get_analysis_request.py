from src.application.interfaces.analysis_repository import AnalysisRepository
from src.core.exceptions.business_exception import BusinessException


class GetAnalysisRequestUseCase:
    def __init__(self, repository: AnalysisRepository) -> None:
        self.repository = repository

    def execute(self, request_id: str):
        request = self.repository.get_request(request_id)
        if request is None:
            raise BusinessException(
                code="NOT_FOUND",
                message=f"No existe una solicitud registrada con id {request_id}.",
            )
        return request
