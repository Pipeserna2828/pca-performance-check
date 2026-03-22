from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.enums.change_type import ChangeType
from src.core.enums.component_type import ComponentType
from src.core.enums.demand_unit import DemandUnit
from src.core.enums.lifecycle_status import LifecycleStatus
from src.core.enums.service_criticality import ServiceCriticality


@dataclass
class AnalysisRequest:
    request_id: str
    system_name: str
    component_type: ComponentType
    service_criticality: ServiceCriticality
    change_type: ChangeType
    expected_demand_value: float
    expected_demand_unit: DemandUnit
    target_p95_ms: int
    stable_environment_available: bool
    observability_available: bool
    baseline_available: bool
    external_dependencies: bool
    change_description: str
    lifecycle_status: LifecycleStatus = LifecycleStatus.REGISTERED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_completed(self) -> None:
        self.lifecycle_status = LifecycleStatus.COMPLETED
        self.updated_at = datetime.now(timezone.utc)
