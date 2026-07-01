from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.routers.customer import router as customer_router
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.wash import router as wash_router
from app.routers.dashboard import router as dashboard_router
from app.routers.ai import router as ai_router
from app.routers.analytics import router as analytics_router

from app.core.middlewares.logging_middleware import LoggingMiddleware
from app.core.middlewares.request_id_middleware import RequestIdMiddleware

from app.core.logger import logger

from app.core.exception_handlers import (
    business_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    request_validation_exception_handler
)

from app.core.exceptions import (
    BusinessException,
    ValidationException
)

app = FastAPI(
    title="Lav.AI Rápido"
)

app.add_exception_handler(
    BusinessException,
    business_exception_handler
)

app.add_exception_handler(
    ValidationException,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIdMiddleware)

@app.on_event("startup")
def startup_event():
    logger.info("API WashBack iniciada")
    
app.include_router(customer_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(wash_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(analytics_router)

@app.get("/")
def home():
    return {"message": "WashBack API funcionando 🚀"}