# Flujo de ejecución

## Propósito

Mostrar el flujo real del sistema desde que el usuario diligencia la solicitud hasta que recibe el resultado final.

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

    FE->>API: POST /analysis-requests
    API->>CREATE: Crear solicitud
    CREATE->>RID: Generar request_id
    RID-->>CREATE: request_id
    CREATE->>REPO: Guardar solicitud
    REPO-->>CREATE: ok
    CREATE-->>API: request_id
    API-->>FE: Solicitud registrada

    FE->>API: POST /analysis-requests/{id}/execute
    API->>EXEC: Ejecutar análisis
    EXEC->>ORQ: Orquestar flujo
    ORQ->>REPO: Obtener solicitud
    REPO-->>ORQ: request
    ORQ->>RULES: Evaluar reglas
    RULES-->>ORQ: Resultado técnico
    ORQ->>EXP: Solicitar explicación

    alt Foundry disponible
        EXP->>AOAI: Generar explicación
        AOAI-->>EXP: Explicación con IA
    else Foundry no disponible
        EXP->>FALL: Generar explicación local
        FALL-->>EXP: Explicación fallback
    end

    ORQ->>REPO: Guardar solicitud actualizada
    ORQ->>REPO: Guardar resultado
    ORQ-->>EXEC: Resultado final
    EXEC-->>API: Análisis completado
    API-->>FE: Ejecución completada

    FE->>API: GET /analysis-requests/{id}/result
    API->>REPO: Obtener resultado
    REPO-->>API: Resultado estructurado
    API-->>FE: Resultado final
    FE-->>U: Muestra score, decisión, riesgo y explicación
```

## Puntos clave

- La decisión técnica se toma en el **motor determinístico**.
- La IA **no decide**.
- Foundry se usa solo para explicar.
- Si Foundry falla, el sistema sigue funcionando con fallback.
- El frontend actual simplifica la experiencia en un solo botón visible.
