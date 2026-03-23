# PCA Performance Check

**Evaluación de alistamiento y priorización para pruebas de performance**

PCA Performance Check es un MVP orientado al área de performance. Su propósito es recibir una solicitud de análisis, evaluar si la solicitud está lista para entrar al flujo de performance y devolver un resultado estructurado con:

- readiness score
- decisión de alistamiento
- nivel de riesgo
- tipo de prueba recomendado
- brechas y riesgos detectados
- explicación asistida para el usuario

La solución separa dos responsabilidades clave:

- **Motor determinístico:** decide el resultado técnico.
- **Asistente de Resultados:** explica ese resultado usando Microsoft Foundry / Azure OpenAI o un fallback local.

---

## 1. Objetivo del MVP

Estandarizar el intake técnico de solicitudes de performance y reducir el esfuerzo manual previo a la ejecución de pruebas.

---

## 2. Alcance funcional

La solución permite:

- registrar una solicitud de análisis
- ejecutar el análisis
- consultar la solicitud registrada
- consultar el resultado estructurado
- mostrar una explicación generada por IA o por fallback

---

## 3. Arquitectura resumida

La solución está compuesta por:

- **Frontend Streamlit**
- **Backend FastAPI**
- **Repositorio JSON local**
- **Integración con Microsoft Foundry / Azure OpenAI**
- **Fallback local para continuidad**

---

## 4. Estructura principal

```text
pca-performance-check/
├── docs/
├── examples/
├── frontend/
├── scripts/
├── src/
├── tests/
├── data/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md