from enum import Enum


class ChangeType(str, Enum):
    UI = "UI"
    BACKEND = "BACKEND"
    DATABASE = "DATABASE"
    INTEGRATION = "INTEGRATION"
    INFRASTRUCTURE = "INFRASTRUCTURE"
