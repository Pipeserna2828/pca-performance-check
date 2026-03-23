# C4 – Componentes del backend

## Propósito

Mostrar las piezas internas más relevantes del backend y cómo colaboran entre sí.

```mermaid
flowchart TB
    routes["Rutas API<br/>analysis_requests.py + health.py"]
    deps["Composición de dependencias<br/>dependencies.py"]

    createUC["CreateAnalysisRequestUseCase"]
    executeUC["ExecuteAnalysisRequestUseCase"]
    getReqUC["GetAnalysisRequestUseCase"]
    getResUC["GetAnalysisResultUseCase"]

    idgen["RequestIdGenerator"]
    orchestrator["AnalysisOrchestrator"]
    rules["PerformanceReadinessRules"]
    resilient["ResilientResultExplainer"]
    azure["AzureOpenAIResultExplainer"]
    fallback["TemplatedResultExplainer"]
    repo["JsonAnalysisRepository"]

    routes --> createUC
    routes --> executeUC
    routes --> getReqUC
    routes --> getResUC

    deps -. construye .-> createUC
    deps -. construye .-> executeUC
    deps -. construye .-> getReqUC
    deps -. construye .-> getResUC

    createUC --> idgen
    createUC --> repo

    executeUC --> orchestrator
    orchestrator --> repo
    orchestrator --> rules
    orchestrator --> resilient

    resilient --> azure
    resilient --> fallback

    getReqUC --> repo
    getResUC --> repo
```

## Explicación de los componentes

### Rutas API
Reciben la solicitud HTTP y delegan a casos de uso específicos.

### Casos de uso
Cada endpoint tiene una responsabilidad clara:
- crear solicitud,
- ejecutar análisis,
- consultar solicitud,
- consultar resultado.

### RequestIdGenerator
Genera el identificador funcional de cada solicitud.

### AnalysisOrchestrator
Coordina el flujo completo de ejecución:
1. recupera la solicitud,
2. llama al motor determinístico,
3. arma el payload para la explicación,
4. invoca al explicador,
5. persiste el resultado.

### PerformanceReadinessRules
Contiene el conocimiento del dominio del MVP:
- score,
- brechas,
- riesgos,
- decisión,
- prueba recomendada.

### ResilientResultExplainer
Aísla la aplicación de fallos del proveedor IA:
- usa Azure OpenAI si está disponible,
- usa fallback templado si falla o no está configurado.

### JsonAnalysisRepository
Abstrae el acceso a la persistencia local.
