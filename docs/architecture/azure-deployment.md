# Enfoque de despliegue en Azure

## Objetivo

Proponer un despliegue razonable para demostrar que el MVP puede crecer a una solución interna.

## Componentes sugeridos

- **Azure App Service o Azure Container Apps** para el backend FastAPI.
- **Azure App Service** para el frontend Streamlit, o integración interna en la misma red corporativa.
- **Azure Key Vault** para secretos.
- **Microsoft Foundry / Azure OpenAI** para el Asistente de Resultados.
- **Azure Blob Storage o Cosmos DB** para persistencia futura.
- **Azure DevOps** para pipeline CI/CD.

## Escalabilidad básica

- La API puede escalar horizontalmente por ser stateless.
- La persistencia local del MVP debe migrar a un repositorio administrado.
- La capa IA puede seguir desacoplada del motor determinístico.

## Razón de diseño

El MVP separa la lógica crítica de performance de la capa IA, lo que facilita escalar, gobernar y auditar el comportamiento del sistema.
