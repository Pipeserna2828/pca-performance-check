# Ejemplo de entrada y salida

## Entrada

### Endpoint
`POST /api/v1/analysis-requests`

### Payload
```json
{
  "system_name": "Credinet Credit API",
  "component_type": "API",
  "service_criticality": "CRITICAL",
  "change_type": "BACKEND",
  "expected_demand_value": 120,
  "expected_demand_unit": "CONCURRENT_USERS",
  "target_p95_ms": 500,
  "stable_environment_available": true,
  "observability_available": true,
  "baseline_available": false,
  "external_dependencies": true,
  "change_description": "Actualización de lógica transaccional e integración con servicio externo de scoring."
}
```

## Salida

### Endpoint
`GET /api/v1/analysis-requests/{request_id}/result`

### Respuesta esperada
```json
{
  "readiness_score": 90,
  "readiness_decision": "LISTA CON BRECHAS",
  "risk_level": "ALTO",
  "recommended_test_type": "LÍNEA BASE",
  "requires_performance_testing": true,
  "missing_prerequisites": [
    "No existe línea base previa para comparar el cambio."
  ],
  "risk_findings": [
    "El servicio tiene criticidad alta o crítica.",
    "Se reportan dependencias externas que podrían impactar la latencia."
  ],
  "explanation": {
    "executive_summary": "Resumen generado por el explicador.",
    "decision_explanation": "Explicación de la decisión.",
    "recommended_next_steps": [
      "Definir una línea base de rendimiento.",
      "Mitigar dependencias externas relevantes."
    ],
    "source": "azure_openai"
  }
}
```

## Lectura del ejemplo

- El resultado técnico sale del motor determinístico.
- La explicación puede venir de Foundry o de fallback local.
- El ejemplo usa un caso típico con criticidad alta, dependencias externas y ausencia de baseline.
