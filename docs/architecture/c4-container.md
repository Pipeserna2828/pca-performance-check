    # C4 – Contenedores

    ```mermaid
    flowchart LR
        subgraph Client
            FE[Streamlit UI]
        end

        subgraph Platform[Backend]
            API[FastAPI]
            ORCH[Analysis Orchestrator]
            ENGINE[Performance Readiness Engine]
            REPO[JSON Repository]
            AI[Asistente de Resultados]
        end

        FOUNDRY[Microsoft Foundry
Azure OpenAI]

        FE --> API
        API --> ORCH
        ORCH --> ENGINE
        ORCH --> REPO
        ORCH --> AI
        AI --> FOUNDRY
    ```

    ## Contenedores

    - **Streamlit UI**: captura datos y presenta el resultado.
    - **FastAPI**: expone el núcleo común del reto.
    - **Analysis Orchestrator**: coordina el flujo de negocio.
    - **Performance Readiness Engine**: aplica reglas determinísticas.
    - **JSON Repository**: persiste el estado del análisis en un archivo local.
    - **Asistente de Resultados**: traduce el resultado técnico a lenguaje claro.
