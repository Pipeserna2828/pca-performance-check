from pydantic import BaseModel


class ExplanationSchema(BaseModel):
    executive_summary: str
    decision_explanation: str
    recommended_next_steps: list[str]
    source: str


class AnalysisResultSchema(BaseModel):
    request_id: str
    readiness_score: int
    readiness_decision: str
    risk_level: str
    requires_performance_testing: bool
    recommended_test_type: str
    missing_prerequisites: list[str]
    risk_findings: list[str]
    score_breakdown: dict[str, int]
    explanation: ExplanationSchema
    generated_at: str
