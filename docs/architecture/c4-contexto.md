# C4 – Contexto

## Propósito

Mostrar cómo PCA Performance Check se relaciona con sus actores y sistemas externos.

```mermaid
flowchart LR
    usuario["Usuario / Analista PCA"]
    frontend["Frontend Streamlit<br/>PCA Performance Check"]
    backend["Backend FastAPI<br/>PCA Performance Check"]
    foundry["Microsoft Foundry / Azure OpenAI"]
    jsonrepo["Archivo JSON local<br/>analysis_requests.json"]

    usuario -->|"Diligencia la solicitud y consulta resultados"| frontend
    frontend -->|"Consume endpoints REST"| backend
    backend -->|"Solicita explicación del resultado"| foundry
    backend -->|"Guarda solicitudes y resultados"| jsonrepo
```

## Lectura

- El **usuario** interactúa con el **frontend Streamlit**.
- El **frontend** consume la **API FastAPI**.
- El **backend** usa **Foundry** solo para explicar el resultado.
- El **backend** persiste solicitudes y resultados en un **JSON local**, propio del MVP actual.

## Qué no muestra este diagrama

No muestra clases ni componentes internos del backend.  
Solo muestra el sistema en relación con actores y dependencias externas.
