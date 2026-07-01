from fastapi import (
    APIRouter,
    Depends
)


from app.core.dependencies import get_dashboard_service
from app.core.responses import success_response

from app.application.services.dashboard_service import DashboardService

from app.schemas.common import DefaultResponse

from app.core.security import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get(
    "/metrics",
    response_model=DefaultResponse
)
def get_metrics(
    current_user: dict = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service)
):        
        data = service.get_metrics(current_user["company_id"])

        return success_response(
            "Métricas carregadas com sucesso.",
             data
        )

@router.get("/")
def dashboard(
    service: DashboardService = Depends(get_dashboard_service)
):
    data = {
        "total_customers": service.get_total_customers(),        
        "active_customers": service.get_active_customers(),
        "inactive_customers": service.get_inactive_customers(),
        "total_washes": service.get_total_washes(),
        "total_campaigns": service.get_total_campaigns(),
        "total_revenue": service.get_total_revenue(),
        "average_ticket": service.get_average_ticket(),
        "monthly_revenue": service.get_monthly_revenue(),
        "monthly_washes": service.get_monthly_washes(),
        "top_customers": service.get_top_customers(),
        "top_revenue_customers":
            service.get_top_revenue_customers()
    }

    return success_response(
        "Dashboard carregado com sucesso",
         data
    )