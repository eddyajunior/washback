from fastapi import APIRouter, Depends

from app.application.services.auth_service import AuthService
from app.core.dependencies import get_auth_service
from app.core.responses import success_response

from app.schemas.user import LoginRequest, Token
from app.schemas.common import DefaultResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/register",
    response_model=DefaultResponse
)
def register(
    user: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    added_user = service.register_user(user)

    return success_response(
        "Usuário criado com sucesso"
    )

@router.post("/login", response_model=Token)
def login(
    user: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):

    token = service.authenticate_user(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }