# Despliegue objetivo

## Propósito

Mostrar cómo podría evolucionar la solución a una arquitectura más empresarial sin complicar la lectura del MVP.

```mermaid
flowchart TB
    usuario["Usuario interno"]
    navegador["Navegador"]
    frontend["Frontend Streamlit"]
    backend["Backend FastAPI"]
    keyvault["Azure Key Vault"]
    foundry["Microsoft Foundry / Azure OpenAI"]
    db["Persistencia administrada"]
    monitor["Application Insights"]

    usuario --> navegador
    navegador --> frontend
    frontend --> backend
    backend --> keyvault
    backend --> foundry
    backend --> db
    backend --> monitor
```

## Evolución esperada

En una siguiente fase se recomienda:

- reemplazar el repositorio JSON por persistencia administrada
- mover secretos y configuración sensible a Key Vault
- agregar observabilidad técnica real
- desplegar frontend y backend como servicios separados
