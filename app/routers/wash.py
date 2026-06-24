from fastapi import (
    APIRouter,
    Depends
)

from app.application.services.wash_service import WashService
from app.core.dependencies import get_wash_service
from app.core.exceptions import BusinessException
from app.core.responses import paginated_response, success_response

from app.schemas.wash import (
    WashCreate,
    WashResponse
)

from app.schemas.common import DefaultResponse

from app.core.security import get_current_user
from app.infrastructure.database.database import get_db

router = APIRouter(
    prefix="/washes",
    tags=["Washes"]
)

@router.post(
    "/",
    response_model=DefaultResponse
)
def create_wash(
    wash: WashCreate,
    current_user: dict = Depends(get_current_user),
    service: WashService = Depends(get_wash_service)
):
    wash = service.create_wash(wash, current_user["company_id"])

    if not wash:
        raise BusinessException(
            "Erro ao criar lavagem",
            500
        )
    
    return success_response(
        "Lavagem criada com sucesso",
        WashResponse.model_validate(
            wash
        ).model_dump()
    )

@router.get(
    "/",
    response_model=DefaultResponse
)
def list_washes(
    page: int = 1,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    service: WashService = Depends(get_wash_service),
):
    skip = (page - 1) * limit

    washes = service.get_washes_by_company_id(current_user["company_id"], skip, limit)

    wash_list = [
        WashResponse.model_validate(
            wash
        ).model_dump()
        for wash in washes
    ]

    total = service.get_total_washes_by_company_id(current_user["company_id"])

    return paginated_response(
        "Lavagens listadas com sucesso",
        wash_list,
        page,
        limit,
        total
    )

@router.get(
    "/{wash_id}",
    response_model=DefaultResponse
)
def get_wash(
    wash_id: int,
    current_user: dict = Depends(get_current_user),
    service: WashService = Depends(get_wash_service)
):
    wash = service.get_wash_by_wash_id(current_user["company_id"], wash_id)

    if not wash:
        raise BusinessException(
            "Lavagem não encontrada",
            404
        )
    
    return success_response(
        "Lavagem encontrada",
        WashResponse.model_validate(
            wash
        ).model_dump()
    )