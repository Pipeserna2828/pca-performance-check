    # C4 – Contexto

    ```mermaid
    flowchart LR
        user[Equipo solicitante / Analista PCA]
        frontend[Frontend Streamlit
PCA Performance Check]
        api[API FastAPI
Núcleo común]
        foundry[Microsoft Foundry
Azure OpenAI Deployment]
        leadership[Líderes / Stakeholders]

        user --> frontend
        frontend --> api
        api --> foundry
        api --> leadership
    ```

    ## Lectura del diagrama

    - El usuario registra la solicitud desde el frontend.
    - El frontend consume la API del núcleo común.
    - La API ejecuta el módulo especializado de performance.
    - La explicación en lenguaje claro se solicita al deployment de Azure OpenAI en Foundry.
    - El resultado estructurado sirve para operación y para conversación con líderes.
