from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from app.application.services.analytics_service import AnalyticsService
from app.core.dependencies import get_analytics_service
from app.core.responses import success_response

from app.infrastructure.database.models.customer import Customer
from app.infrastructure.database.models.wash import Wash

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)



@router.get("/kpis")
def get_kpis(
    service: AnalyticsService = Depends(get_analytics_service)
):

    data = service.get_kpis()  

    return success_response(
        "KPIs calculados.",
        data
    )

@router.get("/top-wash-types")
def top_wash_types(
    service: AnalyticsService = Depends(get_analytics_service)
):
    
    data = service.get_top_wash_types()

    return success_response(
        "Tipos de lavagem mais populares.",
        data
    )

@router.get("/revenue-by-month")
def revenue_by_month(
    service: AnalyticsService = Depends(get_analytics_service)
):
    
    data = service.get_revenue_by_month()

    return success_response(
        "Faturamento por mês.",
        data
    )

@router.get("/consolidated")
def consolidated(
    days: int = 30, 
    service: AnalyticsService = Depends(get_analytics_service)
    ):

    start_date = datetime.utcnow() - timedelta(days=days)

    # TOP CLIENTES
    top_customers = service.get_top_customers_by_initial_date(start_date, Customer, Wash, 5)

    # KPI TOTAL CLIENTES
    total_customers = service.get_kpi_total_customers(start_date, Customer.id, Wash)

    # KPI TOTAL LAVAGENS
    total_washes = service.get_kpi_total_washes(start_date)

    # KPI FATURAMENTO
    total_revenue = (service.get_kpi_total_revenue(start_date)) or 0

    # KPI CAMPANHAS
    active_campaigns = (service.get_active_campaigns(start_date)) or 0

    # GRÁFICO DE FATURAMENTO
    revenue_chart = service.get_revenue_chart(start_date)

    # TIPOS DE LAVAGEM
    wash_types = service.get_wash_types(start_date)

    # CAMPANHAS RECENTES
    campaigns = service.get_recently_campaigns(start_date)

    analytics_data = {
            "period": f"Últimos {days} dias",
            "kpis": {
                "total_customers": total_customers,
                "total_washes": total_washes,
                "total_revenue": round(float(total_revenue or 0), 2),
                "active_campaigns": active_campaigns
            },
            "revenue_chart": revenue_chart,
            "top_customers": top_customers,
            "wash_types": wash_types,
            "campaigns": campaigns
        }

    return success_response(
        "Dashboard carregado",
        analytics_data
    )