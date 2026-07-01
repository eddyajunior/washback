from fastapi import APIRouter, Depends
from sqlalchemy import text 
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

# from app.core.responses import success_response

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def healthcheck(
    db: Session = Depends(get_db)
):
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "app": "WashBack",
        "database": "connected"
    }

    # return success_response(
    #     "API online",
    #     {
    #         "status": "ok"
    #     }
    # )