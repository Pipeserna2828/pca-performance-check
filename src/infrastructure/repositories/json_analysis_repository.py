from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from src.application.interfaces.analysis_repository import AnalysisRepository
from src.core.entities.analysis_request import AnalysisRequest
from src.core.entities.analysis_result import AnalysisResult, ResultExplanation
from src.core.enums.change_type import ChangeType
from src.core.enums.component_type import ComponentType
from src.core.enums.demand_unit import DemandUnit
from src.core.enums.lifecycle_status import LifecycleStatus
from src.core.enums.readiness_decision import ReadinessDecision
from src.core.enums.recommended_test_type import RecommendedTestType
from src.core.enums.risk_level import RiskLevel
from src.core.enums.service_criticality import ServiceCriticality


class JsonAnalysisRepository(AnalysisRepository):
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps({"requests": {}, "results": {}}), encoding="utf-8")

    def save_request(self, request: AnalysisRequest) -> None:
        payload = self._load()
        payload["requests"][request.request_id] = self._serialize_request(request)
        self._save(payload)

    def get_request(self, request_id: str) -> AnalysisRequest | None:
        payload = self._load()
        item = payload["requests"].get(request_id)
        if item is None:
            return None
        return self._deserialize_request(item)

    def save_result(self, result: AnalysisResult) -> None:
        payload = self._load()
        payload["results"][result.request_id] = self._serialize_result(result)
        self._save(payload)

    def get_result(self, request_id: str) -> AnalysisResult | None:
        payload = self._load()
        item = payload["results"].get(request_id)
        if item is None:
            return None
        return self._deserialize_result(item)

    def _load(self) -> dict:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _save(self, payload: dict) -> None:
        self.file_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def _serialize_request(self, request: AnalysisRequest) -> dict:
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

    def _deserialize_request(self, payload: dict) -> AnalysisRequest:
        return AnalysisRequest(
            request_id=payload["request_id"],
            system_name=payload["system_name"],
            component_type=ComponentType(payload["component_type"]),
            service_criticality=ServiceCriticality(payload["service_criticality"]),
            change_type=ChangeType(payload["change_type"]),
            expected_demand_value=payload["expected_demand_value"],
            expected_demand_unit=DemandUnit(payload["expected_demand_unit"]),
            target_p95_ms=payload["target_p95_ms"],
            stable_environment_available=payload["stable_environment_available"],
            observability_available=payload["observability_available"],
            baseline_available=payload["baseline_available"],
            external_dependencies=payload["external_dependencies"],
            change_description=payload["change_description"],
            lifecycle_status=LifecycleStatus(payload["lifecycle_status"]),
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"]),
        )

    def _serialize_result(self, result: AnalysisResult) -> dict:
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

    def _deserialize_result(self, payload: dict) -> AnalysisResult:
        explanation = payload["explanation"]
        return AnalysisResult(
            request_id=payload["request_id"],
            readiness_score=payload["readiness_score"],
            readiness_decision=ReadinessDecision(payload["readiness_decision"]),
            risk_level=RiskLevel(payload["risk_level"]),
            requires_performance_testing=payload["requires_performance_testing"],
            recommended_test_type=RecommendedTestType(payload["recommended_test_type"]),
            missing_prerequisites=payload["missing_prerequisites"],
            risk_findings=payload["risk_findings"],
            score_breakdown=payload["score_breakdown"],
            explanation=ResultExplanation(
                executive_summary=explanation["executive_summary"],
                decision_explanation=explanation["decision_explanation"],
                recommended_next_steps=explanation["recommended_next_steps"],
                source=explanation["source"],
            ),
            generated_at=datetime.fromisoformat(payload["generated_at"]),
        )
