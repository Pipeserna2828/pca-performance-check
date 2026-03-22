from functools import lru_cache

from src.application.services.analysis_orchestrator import AnalysisOrchestrator
from src.application.services.request_id_generator import RequestIdGenerator
from src.application.use_cases.create_analysis_request import CreateAnalysisRequestUseCase
from src.application.use_cases.execute_analysis_request import ExecuteAnalysisRequestUseCase
from src.application.use_cases.get_analysis_request import GetAnalysisRequestUseCase
from src.application.use_cases.get_analysis_result import GetAnalysisResultUseCase
from src.infrastructure.ai.resilient_result_explainer import ResilientResultExplainer
from src.infrastructure.repositories.json_analysis_repository import JsonAnalysisRepository
from src.infrastructure.settings.config import get_settings


@lru_cache
def get_repository() -> JsonAnalysisRepository:
    settings = get_settings()
    return JsonAnalysisRepository(settings.data_store_path)


@lru_cache
def get_request_id_generator() -> RequestIdGenerator:
    return RequestIdGenerator()


@lru_cache
def get_result_explainer() -> ResilientResultExplainer:
    settings = get_settings()
    primary = None
    if (
        settings.ai_enabled
        and settings.azure_openai_endpoint
        and settings.azure_openai_api_key
        and settings.azure_openai_deployment
    ):
        try:
            from src.infrastructure.ai.azure_openai_result_explainer import AzureOpenAIResultExplainer

            primary = AzureOpenAIResultExplainer(settings)
        except Exception:
            primary = None
    return ResilientResultExplainer(primary=primary)


def get_create_analysis_request_use_case() -> CreateAnalysisRequestUseCase:
    return CreateAnalysisRequestUseCase(
        repository=get_repository(),
        request_id_generator=get_request_id_generator(),
    )


def get_execute_analysis_request_use_case() -> ExecuteAnalysisRequestUseCase:
    orchestrator = AnalysisOrchestrator(
        repository=get_repository(),
        explainer=get_result_explainer(),
    )
    return ExecuteAnalysisRequestUseCase(orchestrator)


def get_analysis_request_use_case() -> GetAnalysisRequestUseCase:
    return GetAnalysisRequestUseCase(get_repository())


def get_analysis_result_use_case() -> GetAnalysisResultUseCase:
    return GetAnalysisResultUseCase(get_repository())
