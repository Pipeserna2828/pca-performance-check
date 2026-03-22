from openai import OpenAI

from src.application.interfaces.result_explainer import ResultExplainer
from src.infrastructure.settings.config import Settings


class AzureOpenAIResultExplainer(ResultExplainer):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        # Convertimos el endpoint del recurso al formato v1 recomendado por Microsoft.
        base_endpoint = settings.azure_openai_endpoint.rstrip("/")
        if "openai.azure.com" not in base_endpoint:
            resource_name = (
                base_endpoint.replace("https://", "")
                .replace(".cognitiveservices.azure.com", "")
            )
            base_endpoint = f"https://{resource_name}.openai.azure.com"

        self.client = OpenAI(
            api_key=settings.azure_openai_api_key,
            base_url=f"{base_endpoint}/openai/v1/",
        )

    def explain(self, payload: dict) -> dict:
        response = self.client.responses.create(
            model=self.settings.azure_openai_deployment,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente de performance engineering. "
                        "Debes explicar un resultado técnico de forma clara, profesional y accionable. "
                        "No cambies valores, no inventes hallazgos y no agregues métricas nuevas. "
                        "Responde en español y en JSON con las llaves "
                        "executive_summary, decision_explanation y recommended_next_steps."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Explica este resultado de performance readiness para un usuario interno:\n"
                        f"{payload}"
                    ),
                },
            ],
        )

        content = response.output_text

        import json

        explanation = json.loads(content)
        explanation["source"] = "azure_openai"
        return explanation