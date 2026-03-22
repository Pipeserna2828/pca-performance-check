from enum import Enum


class LifecycleStatus(str, Enum):
    REGISTERED = "REGISTERED"
    COMPLETED = "COMPLETED"
