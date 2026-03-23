# Secuencia de ejecución

## Propósito

Mostrar el flujo real del sistema desde el formulario hasta la visualización del resultado.

> **Nota:** el frontend actual usa un solo botón visible (**Analizar solicitud**) y por dentro ejecuta tres llamadas consecutivas: crear solicitud, ejecutar análisis y consultar resultado.

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario
    participant FE as Frontend Streamlit
    participant API as Backend FastAPI
    participant CREATE as CreateAnalysisRequestUseCase
    participant RID as RequestIdGenerator
    participant EXEC as ExecuteAnalysisRequestUseCase
    participant ORQ as AnalysisOrchestrator
    participant RULES as PerformanceReadinessRules
    participant EXP as ResilientResultExplainer
    participant AOAI as AzureOpenAIResultExplainer
    participant FALL as TemplatedResultExplainer
    participant REPO as JsonAnalysisRepository

    U->>FE: Diligencia la solicitud
    U->>FE: Selecciona "Analizar solicitud"

    FE->>API: POST /api/v1/analysis-requests
    API->>CREATE: execute(payload)
    CREATE->>RID: next_id()
    RID-->>CREATE: request_id
    CREATE->>REPO: save_request(request)
    REPO-->>CREATE: ok
    CREATE-->>API: request_id
    API-->>FE: solicitud registrada

    FE->>API: POST /api/v1/analysis-requests/{id}/execute
    API->>EXEC: execute(request_id)
    EXEC->>ORQ: execute(request_id)
    ORQ->>REPO: get_request(request_id)
    REPO-->>ORQ: request
    ORQ->>RULES: evaluate(request)
    RULES-->>ORQ: deterministic_result
    ORQ->>EXP: explain(payload)

    alt Foundry disponible y exitoso
        EXP->>AOAI: explain(payload)
        AOAI-->>EXP: explanation
    else Falla o no está configurado
        EXP->>FALL: explain(payload)
        FALL-->>EXP: explanation
    end

    EXP-->>ORQ: explanation
    ORQ->>REPO: save_request(updated_request)
    ORQ->>REPO: save_result(result)
    ORQ-->>EXEC: result
    EXEC-->>API: análisis completado
    API-->>FE: ejecución completada

    FE->>API: GET /api/v1/analysis-requests/{id}/result
    API->>REPO: get_result(request_id)
    REPO-->>API: result
    API-->>FE: resultado estructurado
    FE-->>U: métricas, brechas, riesgos y explicación
```

## Aspectos importantes del flujo

- La **decisión técnica** se obtiene antes de llamar a la IA.
- Foundry participa solo en la **explicación**, no en la decisión.
- El fallback garantiza continuidad del flujo.
- El frontend actual consolida el flujo en una experiencia sencilla de demo.
