from enum import Enum


class RecommendedTestType(str, Enum):
    BASELINE = "LÍNEA BASE"
    LOAD = "CARGA"
    STRESS = "ESTRÉS"
    SPIKE = "PICO"
    ENDURANCE = "RESISTENCIA"
