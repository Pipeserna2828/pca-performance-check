from src.application.interfaces.analysis_repository import AnalysisRepository
from src.core.exceptions.business_exception import BusinessException


class GetAnalysisResultUseCase:
    def __init__(self, repository: AnalysisRepository) -> None:
        self.repository = repository

    def execute(self, request_id: str):
        result = self.repository.get_result(request_id)
        if result is None:
            raise BusinessException(
                code="NOT_FOUND",
                message=f"No existe un resultado para la solicitud {request_id}.",
            )
        return result
