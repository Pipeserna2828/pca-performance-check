from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.enums.readiness_decision import ReadinessDecision
from src.core.enums.recommended_test_type import RecommendedTestType
from src.core.enums.risk_level import RiskLevel


@dataclass
class ResultExplanation:
    executive_summary: str
    decision_explanation: str
    recommended_next_steps: list[str]
    source: str


@dataclass
class AnalysisResult:
    request_id: str
    readiness_score: int
    readiness_decision: ReadinessDecision
    risk_level: RiskLevel
    requires_performance_testing: bool
    recommended_test_type: RecommendedTestType
    missing_prerequisites: list[str]
    risk_findings: list[str]
    score_breakdown: dict[str, int]
    explanation: ResultExplanation
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
