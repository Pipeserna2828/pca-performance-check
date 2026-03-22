# PCA Performance Check

**Evaluación de alistamiento y priorización para pruebas de performance**

PCA Performance Check es un MVP de plataforma interna para el área de performance. Su objetivo es recibir una solicitud de análisis, evaluar si la solicitud está lista para entrar al flujo de performance y devolver un resultado estructurado con score, riesgos, decisión, recomendación de tipo de prueba y una explicación entendible para el usuario.

El producto usa dos capas claramente separadas:

- **Motor determinístico**: calcula score, riesgos, estado final y recomendación de prueba.
- **Asistente de Resultados**: usa IA solo para explicar el resultado en lenguaje claro. Si la IA no está disponible, el sistema responde con una explicación local controlada.

## 1. Objetivo del MVP

Este MVP responde al reto de construir una mini plataforma de Quality Engineering con:

- un **núcleo común** reutilizable;
- un **módulo especializado de performance**;
- una **API en Python**;
- un **resultado estándar**;
- y una base clara para evolucionar a una capacidad interna de plataforma.

## 2. Alcance funcional

### Núcleo común

El núcleo común permite:

- registrar una solicitud de análisis;
- ejecutar el análisis;
- consultar la solicitud registrada;
- consultar el resultado estructurado.

### Módulo especializado

El módulo especializado de performance evalúa:

- alistamiento de la solicitud;
- prerequisitos mínimos;
- criticidad y riesgo;
- necesidad de pruebas de performance;
- tipo de prueba recomendado (`Baseline`, `Load` o `Stress`).

### Capa IA

La IA **no decide**. La IA solo:

- resume el resultado;
- explica la decisión;
- propone siguientes pasos.

## 3. Arquitectura resumida

La solución está separada en dos aplicaciones:

- **Backend**: FastAPI + motor determinístico + integración con Azure OpenAI desplegado en Microsoft Foundry.
- **Frontend**: Streamlit con branding de Sistecrédito para la demo funcional.

## 4. Estructura del proyecto

```text
pca-performance-check/
├── docs/
├── examples/
├── frontend/
├── src/
├── tests/
├── .env.example
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 5. Requisitos

- Python 3.11, 3.12 o 3.13
- Acceso a Microsoft Foundry / Azure OpenAI (opcional para la demo local; hay fallback)

## 6. Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements-dev.txt
```

Si prefieres instalar el proyecto como paquete editable:

```bash
pip install -e .
```

## 7. Configuración

1. Copia `.env.example` a `.env`.
2. Reemplaza la API key real.
3. Ajusta `AI_ENABLED=true` si quieres usar Foundry.
4. Si aún no tienes la key lista, puedes dejar `AI_ENABLED=false` y el sistema funcionará con el fallback local.

## 8. Ejecución del backend

```bash
uvicorn src.main:app --reload --port 8000
```

Documentación Swagger:

- `http://localhost:8000/docs`

## 9. Ejecución del frontend

En otra terminal:

```bash
streamlit run frontend/streamlit_app.py
```

## 10. Flujo recomendado de demo

1. Crear la solicitud desde Streamlit.
2. Ejecutar el análisis.
3. Revisar el resultado técnico.
4. Revisar el texto generado por el **Asistente de Resultados**.

## 11. Endpoints principales

- `POST /api/v1/analysis-requests`
- `POST /api/v1/analysis-requests/{request_id}/execute`
- `GET /api/v1/analysis-requests/{request_id}`
- `GET /api/v1/analysis-requests/{request_id}/result`
- `GET /health`

## 12. Reglas principales del motor determinístico

### Readiness score (0 a 100)

- demanda esperada definida: 20
- objetivo p95 definido: 15
- ambiente estable disponible: 20
- observabilidad disponible: 15
- baseline previo disponible: 10
- dependencias externas identificadas: 10
- descripción del cambio clara: 10

### Estados finales

- `NOT_READY`
- `GO_WITH_GAPS`
- `READY`

### Recomendación de prueba

- `Baseline`
- `Load`
- `Stress`

## 13. Pruebas automatizadas

```bash
pytest
```

## 14. Consideraciones para la sustentación

- El diseño es modular y extensible.
- El núcleo común puede reutilizarse por otros módulos de calidad.
- La IA está acotada a explicación y acompañamiento, no a decisiones críticas.
- El despliegue en Azure está documentado en `docs/architecture/azure-deployment.md`.

## 15. Próximas mejoras

- persistencia en base de datos;
- autenticación corporativa;
- dashboard histórico;
- despliegue completo en Azure;
- parametrización dinámica de reglas;
- analítica histórica de performance.
