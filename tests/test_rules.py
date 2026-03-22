from src.core.entities.analysis_request import AnalysisRequest
from src.core.enums.change_type import ChangeType
from src.core.enums.component_type import ComponentType
from src.core.enums.demand_unit import DemandUnit
from src.core.enums.readiness_decision import ReadinessDecision
from src.core.enums.recommended_test_type import RecommendedTestType
from src.core.enums.service_criticality import ServiceCriticality
from src.core.rules.performance_readiness_rules import PerformanceReadinessRules


def build_request(**overrides):
    base = {
        "request_id": "PPC-TEST-0001",
        "system_name": "Credinet Credit API",
        "component_type": ComponentType.API,
        "service_criticality": ServiceCriticality.CRITICAL,
        "change_type": ChangeType.BACKEND,
        "expected_demand_value": 120,
        "expected_demand_unit": DemandUnit.CONCURRENT_USERS,
        "target_p95_ms": 500,
        "stable_environment_available": True,
        "observability_available": True,
        "baseline_available": False,
        "external_dependencies": True,
        "change_description": "Cambio en lógica transaccional e integración externa.",
    }
    base.update(overrides)
    return AnalysisRequest(**base)


def test_readiness_rules_returns_expected_decision():
    result = PerformanceReadinessRules.evaluate(build_request())
    assert result["readiness_score"] == 90
    assert result["readiness_decision"] == ReadinessDecision.GO_WITH_GAPS
    assert result["recommended_test_type"] == RecommendedTestType.BASELINE


def test_readiness_rules_returns_not_ready_when_environment_is_missing():
    result = PerformanceReadinessRules.evaluate(
        build_request(stable_environment_available=False)
    )
    assert result["readiness_decision"] == ReadinessDecision.NOT_READY
