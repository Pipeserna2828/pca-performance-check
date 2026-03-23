# Topología actual y despliegue objetivo

## 1. Topología actual del proyecto

La topología actual corresponde a una ejecución local orientada a demostración y validación funcional.

```mermaid
flowchart TB
    usuario["Usuario / Analista PCA"]
    navegador["Navegador"]
    frontend["Streamlit local"]
    backend["FastAPI local"]
    jsonrepo["analysis_requests.json"]
    foundry["Microsoft Foundry / Azure OpenAI"]

    usuario --> navegador
    navegador --> frontend
    frontend --> backend
    backend --> jsonrepo
    backend --> foundry
```

### Características de la topología actual

- orientada a demo,
- persistencia local,
- configuración vía `.env`,
- integración opcional con Foundry,
- fallback local si la IA falla.

## 2. Despliegue objetivo recomendado en Azure

Para una evolución más empresarial, la topología sugerida sería esta:

```mermaid
flowchart TB
    usuario["Usuario interno"]
    browser["Navegador corporativo"]

    frontend["Frontend Streamlit<br/>Azure App Service o Container Apps"]
    backend["Backend FastAPI<br/>Azure App Service o Container Apps"]

    keyvault["Azure Key Vault"]
    foundry["Microsoft Foundry / Azure OpenAI"]
    persistence["Persistencia administrada<br/>Azure SQL / Cosmos DB / Blob Storage"]
    observability["Application Insights / Log Analytics"]
    cicd["Azure DevOps o GitHub Actions"]

    usuario --> browser
    browser --> frontend
    frontend --> backend
    backend --> keyvault
    backend --> foundry
    backend --> persistence
    backend --> observability
    cicd --> frontend
    cicd --> backend
```

## Principios recomendados

### Separación de responsabilidades
Frontend y backend deben desplegar de manera independiente.

### Gestión de secretos
Las credenciales deben salir del `.env` local y pasar a **Key Vault**.

### Persistencia empresarial
El JSON local debe reemplazarse por un almacenamiento administrado.

### Observabilidad
El backend debe emitir métricas, logs y trazas a una plataforma central.

### Continuidad funcional
El patrón de **explicador resiliente** debe mantenerse incluso en entornos productivos.
