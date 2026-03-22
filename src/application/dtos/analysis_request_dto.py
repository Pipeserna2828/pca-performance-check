from pydantic import BaseModel, Field

from src.core.enums.change_type import ChangeType
from src.core.enums.component_type import ComponentType
from src.core.enums.demand_unit import DemandUnit
from src.core.enums.service_criticality import ServiceCriticality


class CreateAnalysisRequestDTO(BaseModel):
    system_name: str = Field(min_length=3, max_length=120)
    component_type: ComponentType
    service_criticality: ServiceCriticality
    change_type: ChangeType
    expected_demand_value: float = Field(gt=0)
    expected_demand_unit: DemandUnit
    target_p95_ms: int = Field(gt=0)
    stable_environment_available: bool
    observability_available: bool
    baseline_available: bool
    external_dependencies: bool
    change_description: str = Field(min_length=10, max_length=1000)
