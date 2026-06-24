from fastapi import APIRouter

from app.core.responses import success_response

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def healthcheck():

    return success_response(
        "API online",
        {
            "status": "ok"
        }
    )