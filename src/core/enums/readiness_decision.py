from enum import Enum


class ReadinessDecision(str, Enum):
    NOT_READY = "NO LISTA"
    GO_WITH_GAPS = "LISTA CON BRECHAS"
    READY = "LISTA"
