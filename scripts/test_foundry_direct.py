from pathlib import Path
import sys
import json

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.infrastructure.settings.config import get_settings
from src.infrastructure.ai.azure_openai_result_explainer import AzureOpenAIResultExplainer


def main() -> None:
    settings = get_settings()

    payload = {
        "system_name": "Credinet Credit API",
        "readiness_score": 90,
        "readiness_decision": "LISTA CON BRECHAS",
        "risk_level": "ALTO",
        "requires_performance_testing": True,
        "recommended_test_type": "LÍNEA BASE",
        "missing_prerequisites": [
            "No existe línea base previa para comparar el cambio."
        ],
        "risk_findings": [
            "El servicio tiene criticidad alta o crítica.",
            "Se reportan dependencias externas que podrían impactar la latencia."
        ],
    }

    explainer = AzureOpenAIResultExplainer(settings)
    result = explainer.explain(payload)

    print("=== RESPUESTA COMPLETA ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== VALIDACIÓN ===")
    print("source =", result.get("source"))


if __name__ == "__main__":
    main()