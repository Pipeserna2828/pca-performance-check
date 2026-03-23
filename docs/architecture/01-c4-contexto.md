# C4 – Contexto del sistema

## Propósito

Mostrar cómo **PCA Performance Check** se relaciona con sus actores y con los sistemas externos relevantes.

```mermaid
flowchart LR
    usuario["Usuario interno / Analista PCA"]
    frontend["Frontend Streamlit<br/>PCA Performance Check"]
    backend["Backend FastAPI<br/>PCA Performance Check"]
    foundry["Microsoft Foundry / Azure OpenAI"]
    jsonrepo["Archivo JSON local<br/>analysis_requests.json"]

    usuario -->|"Diligencia la solicitud y consulta resultados"| frontend
    frontend -->|"Consume endpoints REST"| backend
    backend -->|"Solicita explicación del resultado"| foundry
    backend -->|"Guarda solicitudes y resultados"| jsonrepo
```

## Lectura del diagrama

- El **usuario** interactúa con el **frontend Streamlit**.
- El **frontend** consume la **API FastAPI** para registrar solicitudes, ejecutar análisis y consultar resultados.
- El **backend** usa **Microsoft Foundry / Azure OpenAI** únicamente para explicar el resultado técnico.
- El **backend** persiste solicitudes y resultados en un **archivo JSON local**, propio del MVP actual.

## Observación importante

Este diagrama muestra **relaciones de contexto**, no componentes internos del backend.
