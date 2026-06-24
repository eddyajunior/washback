from fastapi import APIRouter, Depends

from app.application.services.ai_service import AIService

from app.core.dependencies import get_ai_service
from app.core.responses import success_response

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.get("/campaigns/recurring-customers")
def recurring_customers(
    service: AIService = Depends(get_ai_service)
):

    analysis = service.recurring_customers()

    return success_response(
        "Análise de recorrência gerada",
        analysis
    )

@router.post("/campaigns/generate")
def generate_campaigns(
    service: AIService = Depends(get_ai_service)
):
    
    campaigns_response = service.generate_campaigns()

    return success_response(
        "Campanhas geradas com sucesso.",
        campaigns_response
    )
