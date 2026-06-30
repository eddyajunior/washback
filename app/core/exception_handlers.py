from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.exceptions import (
    BusinessException,
    ValidationException
)

import logging

logger = logging.getLogger(__name__)

async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Dados de entrada inválidos",
            "errors": exc.errors()
        }
    )

# async def request_validation_exception_handler(
#     request: Request,
#     exc: RequestValidationError
# ):
#     return JSONResponse(
#         status_code=422,
#         content={
#             "success": False,
#             "message": "Dados de entrada inválidos"
#         }
#     )


async def business_exception_handler(
    request: Request,
    exc: BusinessException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: ValidationException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )



async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(
        f"Erro interno: {str(exc)}"
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno do servidor"
        }
    )