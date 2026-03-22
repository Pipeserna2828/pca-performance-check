from src.application.interfaces.analysis_repository import AnalysisRepository
from src.application.interfaces.result_explainer import ResultExplainer
from src.core.entities.analysis_result import AnalysisResult, ResultExplanation
from src.core.exceptions.business_exception import BusinessException
from src.core.rules.performance_readiness_rules import PerformanceReadinessRules


class AnalysisOrchestrator:
    def __init__(self, repository: AnalysisRepository, explainer: ResultExplainer) -> None:
        self.repository = repository
        self.explainer = explainer

    def execute(self, request_id: str) -> AnalysisResult:
        request = self.repository.get_request(request_id)
        if request is None:
            raise BusinessException(
                code="NOT_FOUND",
                message=f"No existe una solicitud registrada con id {request_id}.",
            )

        deterministic_result = PerformanceReadinessRules.evaluate(request)
        explanation_payload = {
            "system_name": request.system_name,
            "readiness_score": deterministic_result["readiness_score"],
            "readiness_decision": deterministic_result["readiness_decision"].value,
            "risk_level": deterministic_result["risk_level"].value,
            "requires_performance_testing": deterministic_result[
                "requires_performance_testing"
            ],
            "recommended_test_type": deterministic_result[
                "recommended_test_type"
            ].value,
            "missing_prerequisites": deterministic_result["missing_prerequisites"],
            "risk_findings": deterministic_result["risk_findings"],
        }
        explanation = self.explainer.explain(explanation_payload)

        result = AnalysisResult(
            request_id=request.request_id,
            readiness_score=deterministic_result["readiness_score"],
            readiness_decision=deterministic_result["readiness_decision"],
            risk_level=deterministic_result["risk_level"],
            requires_performance_testing=deterministic_result[
                "requires_performance_testing"
            ],
            recommended_test_type=deterministic_result["recommended_test_type"],
            missing_prerequisites=deterministic_result["missing_prerequisites"],
            risk_findings=deterministic_result["risk_findings"],
            score_breakdown=deterministic_result["score_breakdown"],
            explanation=ResultExplanation(**explanation),
        )
        request.mark_completed()
        self.repository.save_request(request)
        self.repository.save_result(result)
        return result
