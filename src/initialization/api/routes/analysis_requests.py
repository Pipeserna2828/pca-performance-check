from fastapi import APIRouter, Depends

from src.application.dtos.analysis_request_dto import CreateAnalysisRequestDTO
from src.application.use_cases.create_analysis_request import CreateAnalysisRequestUseCase
from src.application.use_cases.execute_analysis_request import ExecuteAnalysisRequestUseCase
from src.application.use_cases.get_analysis_request import GetAnalysisRequestUseCase
from src.application.use_cases.get_analysis_result import GetAnalysisResultUseCase
from src.initialization.api.dependencies import (
    get_analysis_request_use_case,
    get_analysis_result_use_case,
    get_create_analysis_request_use_case,
    get_execute_analysis_request_use_case,
)

router = APIRouter(prefix="/analysis-requests", tags=["analysis-requests"])


@router.post("")
def create_analysis_request(
    payload: CreateAnalysisRequestDTO,
    use_case: CreateAnalysisRequestUseCase = Depends(get_create_analysis_request_use_case),
) -> dict:
    request = use_case.execute(payload)
    return {
        "request_id": request.request_id,
        "lifecycle_status": request.lifecycle_status.value,
        "message": "Solicitud registrada correctamente.",
    }


@router.post("/{request_id}/execute")
def execute_analysis_request(
    request_id: str,
    use_case: ExecuteAnalysisRequestUseCase = Depends(get_execute_analysis_request_use_case),
) -> dict:
    result = use_case.execute(request_id)
    return {
        "request_id": result.request_id,
        "lifecycle_status": "COMPLETED",
        "message": "Análisis ejecutado correctamente.",
    }


@router.get("/{request_id}")
def get_analysis_request(
    request_id: str,
    use_case: GetAnalysisRequestUseCase = Depends(get_analysis_request_use_case),
) -> dict:
    request = use_case.execute(request_id)
    return {
        "request_id": request.request_id,
        "system_name": request.system_name,
        "component_type": request.component_type.value,
        "service_criticality": request.service_criticality.value,
        "change_type": request.change_type.value,
        "expected_demand_value": request.expected_demand_value,
        "expected_demand_unit": request.expected_demand_unit.value,
        "target_p95_ms": request.target_p95_ms,
        "stable_environment_available": request.stable_environment_available,
        "observability_available": request.observability_available,
        "baseline_available": request.baseline_available,
        "external_dependencies": request.external_dependencies,
        "change_description": request.change_description,
        "lifecycle_status": request.lifecycle_status.value,
        "created_at": request.created_at.isoformat(),
        "updated_at": request.updated_at.isoformat(),
    }


@router.get("/{request_id}/result")
def get_analysis_result(
    request_id: str,
    use_case: GetAnalysisResultUseCase = Depends(get_analysis_result_use_case),
) -> dict:
    result = use_case.execute(request_id)
    return {
        "request_id": result.request_id,
        "readiness_score": result.readiness_score,
        "readiness_decision": result.readiness_decision.value,
        "risk_level": result.risk_level.value,
        "requires_performance_testing": result.requires_performance_testing,
        "recommended_test_type": result.recommended_test_type.value,
        "missing_prerequisites": result.missing_prerequisites,
        "risk_findings": result.risk_findings,
        "score_breakdown": result.score_breakdown,
        "explanation": {
            "executive_summary": result.explanation.executive_summary,
            "decision_explanation": result.explanation.decision_explanation,
            "recommended_next_steps": result.explanation.recommended_next_steps,
            "source": result.explanation.source,
        },
        "generated_at": result.generated_at.isoformat(),
    }
