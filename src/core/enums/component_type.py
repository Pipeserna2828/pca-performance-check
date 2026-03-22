from enum import Enum


class ComponentType(str, Enum):
    API = "API"
    BATCH = "BATCH"
    WORKER = "WORKER"
    QUEUE_CONSUMER = "QUEUE_CONSUMER"
