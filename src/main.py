from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.initialization.api.exception_handlers import (
    business_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)
from src.initialization.api.routes.analysis_requests import router as analysis_router
from src.initialization.api.routes.health import router as health_router
from src.infrastructure.settings.config import get_settings
from src.core.exceptions.business_exception import BusinessException

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description=(
        "API del núcleo común de PCA Performance Check. "
        "Permite registrar solicitudes, ejecutar análisis y consultar resultados."
    ),
)

app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(health_router)
app.include_router(analysis_router, prefix=settings.api_prefix)
