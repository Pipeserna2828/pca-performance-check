# Arquitectura – PCA Performance Check

Esta carpeta contiene la documentación de arquitectura **alineada al estado real del proyecto**.

## Documentos incluidos

1. [C4 – Contexto](01-c4-contexto.md)
2. [C4 – Contenedores](02-c4-contenedores.md)
3. [C4 – Componentes del backend](03-c4-componentes-backend.md)
4. [Secuencia de ejecución](04-secuencia-ejecucion.md)
5. [Topología actual y despliegue objetivo](05-topologia-y-despliegue.md)

## Criterios de diseño de los diagramas

Los diagramas fueron corregidos con base en el **código real del proyecto** y no solo desde una visión conceptual.

Se cuidó especialmente:

- respetar niveles correctos de arquitectura;
- representar el flujo real entre frontend, backend, motor de reglas, repositorio y explicadores;
- reflejar el comportamiento de **Foundry o fallback**;
- usar sintaxis Mermaid que se vea correctamente en **GitHub Preview**.

## Guía de lectura

- **Contexto**: actores y sistemas externos.
- **Contenedores**: aplicaciones o procesos desplegables.
- **Componentes**: piezas internas relevantes del backend.
- **Secuencia**: orden real de ejecución en runtime.
