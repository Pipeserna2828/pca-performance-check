from src.application.interfaces.result_explainer import ResultExplainer
from src.infrastructure.ai.templated_result_explainer import TemplatedResultExplainer


class ResilientResultExplainer(ResultExplainer):
    def __init__(self, primary: ResultExplainer | None, fallback: ResultExplainer | None = None) -> None:
        self.primary = primary
        self.fallback = fallback or TemplatedResultExplainer()

    def explain(self, payload: dict) -> dict:
        if self.primary is None:
            return self.fallback.explain(payload)
        try:
            return self.primary.explain(payload)
        except Exception:
            return self.fallback.explain(payload)
