# C4 – Componentes

```mermaid
flowchart TD
    ROUTES[API Routes]
    CREATE[Create Analysis Request Use Case]
    EXECUTE[Execute Analysis Request Use Case]
    GETREQ[Get Analysis Request Use Case]
    GETRES[Get Analysis Result Use Case]
    ORCH[Analysis Orchestrator]
    RULES[Performance Readiness Rules]
    EXPLAINER[Result Explainer Service]
    AZURE[Azure OpenAI Client]
    TEMPLATE[Templated Explainer]
    REPO[Analysis Repository]

    ROUTES --> CREATE
    ROUTES --> EXECUTE
    ROUTES --> GETREQ
    ROUTES --> GETRES
    EXECUTE --> ORCH
    ORCH --> RULES
    ORCH --> EXPLAINER
    EXPLAINER --> AZURE
    EXPLAINER --> TEMPLATE
    CREATE --> REPO
    EXECUTE --> REPO
    GETREQ --> REPO
    GETRES --> REPO
```

## Componentes clave

- **Performance Readiness Rules**: score, riesgos, decisión y recomendación.
- **Result Explainer Service**: decide si usa Foundry o fallback local.
- **Azure OpenAI Client**: integra el deployment configurado en Foundry.
- **Templated Explainer**: garantiza continuidad si la IA falla.
