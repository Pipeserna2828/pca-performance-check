from src.application.interfaces.result_explainer import ResultExplainer


class TemplatedResultExplainer(ResultExplainer):
    def explain(self, payload: dict) -> dict:
        decision = payload["readiness_decision"]
        score = payload["readiness_score"]
        recommended_test = payload["recommended_test_type"]
        missing = payload.get("missing_prerequisites", [])
        risks = payload.get("risk_findings", [])

        executive_summary = (
            f"La solicitud del sistema {payload['system_name']} obtuvo un score de alistamiento "
            f"de {score}/100 y quedó en estado {decision}."
        )

        decision_explanation = (
            f"El motor determinístico recomienda una validación de tipo {recommended_test}. "
            f"La decisión se soporta en el nivel de riesgo identificado y en las brechas detectadas en el intake."
        )

        next_steps: list[str] = []
        if missing:
            next_steps.append(f"Completar los siguientes puntos: {', '.join(missing[:2])}")
        if risks:
            next_steps.append(f"Revisar riesgos principales: {', '.join(risks[:2])}")
        if not next_steps:
            next_steps.append("La solicitud puede avanzar a la siguiente fase de performance.")

        return {
            "executive_summary": executive_summary,
            "decision_explanation": decision_explanation,
            "recommended_next_steps": next_steps,
            "source": "fallback_template",
        }
