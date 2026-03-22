from src.application.services.analysis_orchestrator import AnalysisOrchestrator
from src.core.entities.analysis_result import AnalysisResult


class ExecuteAnalysisRequestUseCase:
    def __init__(self, orchestrator: AnalysisOrchestrator) -> None:
        self.orchestrator = orchestrator

    def execute(self, request_id: str) -> AnalysisResult:
        return self.orchestrator.execute(request_id)
