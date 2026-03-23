# PCA Performance Check

## Descripción general
**PCA Performance Check** es un MVP orientado al área de performance que permite evaluar el alistamiento de una solicitud antes de ejecutar pruebas de rendimiento.

La solución recibe una solicitud con información mínima del sistema y del cambio, aplica reglas determinísticas de performance, calcula un **readiness score**, clasifica el **nivel de riesgo**, define una **decisión de alistamiento** y recomienda el **tipo de prueba** más conveniente.

Adicionalmente, incorpora una capa de explicación asistida con **Microsoft Foundry / Azure OpenAI** para traducir el resultado técnico a un lenguaje más claro y accionable para el usuario.

---

## Objetivo
Estandarizar el análisis inicial de solicitudes de performance, reduciendo validaciones manuales repetitivas y mejorando la priorización técnica antes de invertir esfuerzo en ejecución de pruebas.

---

## Alcance funcional del MVP
La solución permite:

- Registrar una solicitud de análisis de performance.
- Evaluar el nivel de alistamiento de la solicitud.
- Identificar brechas técnicas y riesgos relevantes.
- Recomendar el tipo de prueba más adecuado.
- Generar una explicación del resultado mediante IA o fallback local.
- Visualizar el resultado en una interfaz sencilla y enfocada en demostración.

---

## Capacidades principales

### 1. Motor determinístico
El motor central aplica reglas de negocio para calcular:

- **Readiness score** (0 a 100)
- **Decisión de alistamiento**
  - `NO LISTA`
  - `LISTA CON BRECHAS`
  - `LISTA`
- **Nivel de riesgo**
  - `BAJO`
  - `MEDIO`
  - `ALTO`
- **Necesidad de pruebas de performance**
- **Tipo de prueba recomendado**
  - `LÍNEA BASE`
  - `CARGA`
  - `ESTRÉS`
  - `PICO`
  - `RESISTENCIA`

### 2. Explicación asistida
La solución puede consumir **Microsoft Foundry / Azure OpenAI** para generar:

- resumen ejecutivo,
- explicación de la decisión,
- siguientes pasos sugeridos.

Si el servicio de IA no está disponible, la aplicación responde mediante un **fallback local** para no interrumpir el flujo.

### 3. Interfaz de usuario
El frontend está construido en **Streamlit** y permite:

- diligenciar la solicitud,
- ejecutar el análisis,
- visualizar resultados técnicos,
- consultar el resumen generado por IA.

---

## Arquitectura de la solución

### Backend
Construido en **FastAPI**, siguiendo una separación por capas:

- `core`: entidades, enums y reglas de negocio
- `application`: casos de uso, orquestación e interfaces
- `infrastructure`: persistencia, configuración e integración IA
- `initialization`: composición de dependencias y rutas API

### Frontend
Construido en **Streamlit**, orientado a una experiencia simple, clara y fácil de sustentar.

### Persistencia
Actualmente se usa un almacenamiento **JSON local** con fines de demostración.

### Integración IA
Se utiliza **Microsoft Foundry / Azure OpenAI** como proveedor de explicación asistida.

---

## Estructura principal del proyecto

```text
pca-performance-check/
├── frontend/
├── src/
│   ├── application/
│   ├── core/
│   ├── infrastructure/
│   └── initialization/
├── tests/
├── data/
├── scripts/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

---

## Requisitos
- Python 3.11 o superior
- Git
- Acceso a Microsoft Foundry / Azure OpenAI si se quiere usar explicación asistida real

---

## Instalación

### 1. Crear entorno virtual
En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias
```powershell
pip install -r requirements-dev.txt
```

### 3. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto con la configuración requerida.

Ejemplo:

```env
APP_NAME=PCA Performance Check
API_VERSION=1.0.0
API_PREFIX=/api/v1
DATA_STORE_PATH=data/analysis_requests.json
DEBUG=false

AI_ENABLED=true
AI_PROVIDER=azure_openai

AZURE_OPENAI_ENDPOINT=https://agente-pruebas-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=REEMPLAZAR_CON_LA_CLAVE_REAL
AZURE_OPENAI_DEPLOYMENT=gpt-5-nano
AZURE_OPENAI_API_VERSION=v1

BACKEND_BASE_URL=http://localhost:8000
```

> Importante: no subir `.env` al repositorio.

---

## Ejecución

### Levantar backend
```powershell
uvicorn src.main:app --reload --port 8000
```

### Levantar frontend
En otra terminal:

```powershell
streamlit run frontend/streamlit_app.py
```

---

## Endpoints principales
- `POST /api/v1/analysis-requests`
- `POST /api/v1/analysis-requests/{request_id}/execute`
- `GET /api/v1/analysis-requests/{request_id}`
- `GET /api/v1/analysis-requests/{request_id}/result`
- `GET /health`

Swagger:
- `http://localhost:8000/docs`

---

## Validación de Foundry / Azure OpenAI
La solución está preparada para usar Microsoft Foundry.  
Para validar la conexión de forma directa, puede ejecutarse un script de prueba interna.

El comportamiento esperado es:

- si la IA responde correctamente, el campo `source` será `azure_openai`,
- si la integración falla, el sistema responderá con `fallback_template`.

En la interfaz también se muestra una nota discreta indicando la fuente de explicación usada.

---

## Pruebas
Para ejecutar pruebas automatizadas:

```powershell
pytest
```

Estado esperado del proyecto:
- pruebas unitarias y de flujo base aprobadas.

---

## Consideraciones de diseño
- La lógica crítica de decisión **no depende de IA**.
- La IA se usa únicamente para **explicar** el resultado.
- El almacenamiento actual es local y está orientado a MVP.
- La solución está preparada para evolucionar a una arquitectura más empresarial en Azure.

---

## Próximos pasos recomendados
- Reemplazar persistencia JSON por una base de datos administrada.
- Incorporar autenticación y control de acceso.
- Externalizar reglas de negocio a configuración administrable.
- Agregar trazabilidad y observabilidad técnica.
- Fortalecer validaciones y pruebas de integración.
- Preparar despliegue productivo en Azure App Service o Container Apps.

---

## Autor
Proyecto preparado como solución técnica para el reto PCA, con enfoque en buenas prácticas, claridad arquitectónica y usabilidad para sustentación.
