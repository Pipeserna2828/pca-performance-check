from src.core.entities.analysis_request import AnalysisRequest
from src.core.enums.change_type import ChangeType
from src.core.enums.readiness_decision import ReadinessDecision
from src.core.enums.recommended_test_type import RecommendedTestType
from src.core.enums.risk_level import RiskLevel
from src.core.enums.service_criticality import ServiceCriticality


class PerformanceReadinessRules:
    """Aplica las reglas determinísticas del MVP."""

    @staticmethod
    def evaluate(request: AnalysisRequest) -> dict:
        score_breakdown = {
            "demanda_esperada_definida": 20 if request.expected_demand_value > 0 else 0,
            "objetivo_p95_definido": 15 if request.target_p95_ms > 0 else 0,
            "ambiente_estable_disponible": 20 if request.stable_environment_available else 0,
            "observabilidad_disponible": 15 if request.observability_available else 0,
            "baseline_previo_disponible": 10 if request.baseline_available else 0,
            "dependencias_externas_identificadas": 10,
            "descripcion_clara_del_cambio": 10 if len(request.change_description.strip()) >= 20 else 0,
        }
        readiness_score = sum(score_breakdown.values())

        missing_prerequisites: list[str] = []
        if request.expected_demand_value <= 0:
            missing_prerequisites.append("La demanda esperada no fue definida.")
        if request.target_p95_ms <= 0:
            missing_prerequisites.append("El objetivo de p95 no fue definido.")
        if not request.stable_environment_available:
            missing_prerequisites.append("No existe un ambiente estable disponible para la evaluación.")
        if not request.observability_available:
            missing_prerequisites.append("No existe observabilidad mínima para analizar el resultado.")
        if not request.baseline_available:
            missing_prerequisites.append("No existe línea base previa para comparar el cambio.")
        if len(request.change_description.strip()) < 20:
            missing_prerequisites.append("La descripción del cambio es insuficiente para analizar el impacto.")

        risk_points = 0
        risk_findings: list[str] = []

        if request.service_criticality in (ServiceCriticality.HIGH, ServiceCriticality.CRITICAL):
            risk_points += 2
            risk_findings.append("El servicio tiene criticidad alta o crítica.")

        if request.change_type in (
            ChangeType.BACKEND,
            ChangeType.DATABASE,
            ChangeType.INTEGRATION,
            ChangeType.INFRASTRUCTURE,
        ):
            risk_points += 2
            risk_findings.append("El cambio impacta backend, base de datos, integración o infraestructura.")

        if request.expected_demand_value >= 100:
            risk_points += 1
            risk_findings.append("La demanda esperada es material para una validación de performance.")

        if request.external_dependencies:
            risk_points += 1
            risk_findings.append("Se reportan dependencias externas que podrían impactar la latencia.")

        if not request.baseline_available:
            risk_points += 1
            risk_findings.append("No existe línea base previa para comparar el comportamiento del sistema.")

        if risk_points >= 4:
            risk_level = RiskLevel.HIGH
        elif risk_points >= 2:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        requires_performance_testing = PerformanceReadinessRules._requires_testing(request)
        recommended_test_type = PerformanceReadinessRules._recommend_test_type(
            request, risk_level
        )
        readiness_decision = PerformanceReadinessRules._decision(
            request=request,
            readiness_score=readiness_score,
            missing_prerequisites=missing_prerequisites,
        )

        return {
            "readiness_score": readiness_score,
            "readiness_decision": readiness_decision,
            "risk_level": risk_level,
            "requires_performance_testing": requires_performance_testing,
            "recommended_test_type": recommended_test_type,
            "missing_prerequisites": missing_prerequisites,
            "risk_findings": risk_findings,
            "score_breakdown": score_breakdown,
        }

    @staticmethod
    def _requires_testing(request: AnalysisRequest) -> bool:
        if request.service_criticality in (ServiceCriticality.HIGH, ServiceCriticality.CRITICAL):
            return True
        if request.change_type in (
            ChangeType.BACKEND,
            ChangeType.DATABASE,
            ChangeType.INTEGRATION,
            ChangeType.INFRASTRUCTURE,
        ):
            return True
        if request.expected_demand_value >= 50:
            return True
        if request.external_dependencies:
            return True
        return False

    @staticmethod
    def _recommend_test_type(
        request: AnalysisRequest,
        risk_level: RiskLevel,
    ) -> RecommendedTestType:
        # Orden de recomendación pensado para demo: primero lo más específico.
        if (
            request.service_criticality in (ServiceCriticality.HIGH, ServiceCriticality.CRITICAL)
            and request.stable_environment_available
            and request.observability_available
            and request.baseline_available
            and request.expected_demand_value >= 150
        ):
            return RecommendedTestType.ENDURANCE

        if (
            request.service_criticality in (ServiceCriticality.HIGH, ServiceCriticality.CRITICAL)
            and request.external_dependencies
            and request.expected_demand_value >= 150
        ):
            return RecommendedTestType.SPIKE

        if risk_level == RiskLevel.HIGH and request.change_type in (
            ChangeType.DATABASE,
            ChangeType.INTEGRATION,
            ChangeType.INFRASTRUCTURE,
        ):
            return RecommendedTestType.STRESS

        if not request.baseline_available:
            return RecommendedTestType.BASELINE

        if request.expected_demand_value >= 100 or risk_level in (RiskLevel.MEDIUM, RiskLevel.HIGH):
            return RecommendedTestType.LOAD

        return RecommendedTestType.BASELINE

    @staticmethod
    def _decision(
        request: AnalysisRequest,
        readiness_score: int,
        missing_prerequisites: list[str],
    ) -> ReadinessDecision:
        if (
            request.expected_demand_value <= 0
            or request.target_p95_ms <= 0
            or not request.stable_environment_available
            or len(request.change_description.strip()) < 20
        ):
            return ReadinessDecision.NOT_READY
        if readiness_score >= 90 and len(missing_prerequisites) == 0:
            return ReadinessDecision.READY
        return ReadinessDecision.GO_WITH_GAPS
