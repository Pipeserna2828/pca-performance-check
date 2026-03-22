from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_end_to_end_flow():
    payload = {
        "system_name": "Credinet Credit API",
        "component_type": "API",
        "service_criticality": "CRITICAL",
        "change_type": "BACKEND",
        "expected_demand_value": 120,
        "expected_demand_unit": "CONCURRENT_USERS",
        "target_p95_ms": 500,
        "stable_environment_available": True,
        "observability_available": True,
        "baseline_available": False,
        "external_dependencies": True,
        "change_description": "Se actualiza la lógica de aprobación de crédito y el consumo del servicio de scoring.",
    }

    create_response = client.post("/api/v1/analysis-requests", json=payload)
    assert create_response.status_code == 200
    request_id = create_response.json()["request_id"]

    execute_response = client.post(f"/api/v1/analysis-requests/{request_id}/execute")
    assert execute_response.status_code == 200

    result_response = client.get(f"/api/v1/analysis-requests/{request_id}/result")
    assert result_response.status_code == 200
    body = result_response.json()
    assert body["readiness_decision"] in {"LISTA CON BRECHAS", "LISTA", "NO LISTA"}
    assert "explanation" in body
