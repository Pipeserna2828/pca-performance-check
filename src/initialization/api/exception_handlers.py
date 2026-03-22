from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.exceptions.business_exception import BusinessException


async def business_exception_handler(_: Request, exc: BusinessException) -> JSONResponse:
    return JSONResponse(
        status_code=404 if exc.code == "NOT_FOUND" else 400,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        {"field": ".".join(map(str, item["loc"])), "issue": item["msg"]}
        for item in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "La solicitud contiene campos inválidos.",
                "details": details,
            }
        },
    )


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Ocurrió un error inesperado durante la ejecución.",
                "details": [{"issue": str(exc)}],
            }
        },
    )
