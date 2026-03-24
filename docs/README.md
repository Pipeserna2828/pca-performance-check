# PCA Performance Check

**Evaluación de alistamiento y priorización para pruebas de performance**

PCA Performance Check es un MVP orientado al área de performance. Su objetivo es evaluar si una solicitud está lista para pasar al flujo de performance y devolver un resultado técnico claro y entendible.

El sistema entrega:

- readiness score
- decisión de alistamiento
- nivel de riesgo
- tipo de prueba recomendado
- brechas detectadas
- explicación del resultado

La solución separa dos responsabilidades principales:

- **Motor determinístico:** calcula el resultado técnico.
- **Asistente de Resultados:** explica ese resultado usando Microsoft Foundry / Azure OpenAI o un fallback local.

## 1. Qué problema resuelve

Ayuda a estandarizar el análisis inicial de solicitudes de performance, reduciendo validaciones manuales repetitivas y mejorando la priorización técnica antes de ejecutar pruebas.

## 2. Componentes principales

### Frontend Streamlit
Captura la solicitud y muestra el resultado final.

### Backend FastAPI
Expone la API, ejecuta el análisis y coordina la persistencia y la explicación.

### Motor determinístico
Calcula:
- readiness score
- decisión de alistamiento
- riesgo
- necesidad de pruebas de performance
- tipo de prueba recomendado
- prerequisitos faltantes
- hallazgos de riesgo

### Asistente de Resultados
Genera el resumen del resultado:
- si Foundry está disponible, usa Azure OpenAI
- si falla o no está configurado, usa fallback local

### Repositorio JSON local
Guarda solicitudes y resultados del MVP.

## 3. Flujo funcional

1. El usuario diligencia la solicitud en el frontend.
2. El frontend registra la solicitud en el backend.
3. El backend ejecuta el motor determinístico.
4. El backend solicita la explicación al explicador resiliente.
5. El resultado se guarda en el repositorio local.
6. El frontend consulta y muestra el resultado final.

> En la interfaz actual, el usuario ve un solo botón visible: **Analizar solicitud**.  
> Internamente el frontend ejecuta tres pasos consecutivos:
> - crear solicitud
> - ejecutar análisis
> - consultar resultado

## 4. Estados del análisis

### Decisión
- **NO LISTA**
- **LISTA CON BRECHAS**
- **LISTA**

### Riesgo
- **BAJO**
- **MEDIO**
- **ALTO**

### Tipos de prueba recomendados
- **LÍNEA BASE**
- **CARGA**
- **ESTRÉS**
- **PICO**
- **RESISTENCIA**

## 5. Ejecución local

### Crear y activar entorno virtual

#### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Git Bash
```bash
python -m venv .venv
source .venv/Scripts/activate
```

### Instalar dependencias
```bash
pip install -r requirements-dev.txt
```

### Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

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

### Levantar backend
```bash
uvicorn src.main:app --reload --port 8000
```

### Levantar frontend
```bash
streamlit run frontend/streamlit_app.py
```

### Validaciones rápidas
- Health check: `http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`
- Frontend Streamlit: normalmente `http://localhost:8501`

## 6. Endpoints principales

- `POST /api/v1/analysis-requests`
- `POST /api/v1/analysis-requests/{request_id}/execute`
- `GET /api/v1/analysis-requests/{request_id}`
- `GET /api/v1/analysis-requests/{request_id}/result`
- `GET /health`

## 7. Documentación incluida

- `docs/architecture/01-resumen-arquitectura.md`
- `docs/architecture/01-c4-contexto.md`
- `docs/architecture/02-c4-contenedores.md`
- `docs/respuestas-reto.md`
- `examples/ejemplo-input-output.md`

## 8. Consideraciones técnicas

- la IA **no toma decisiones**
- el resultado técnico sale del motor determinístico
- Foundry se usa solo para explicar
- el fallback garantiza continuidad del flujo
- la persistencia actual es JSON local y está pensada para MVP
