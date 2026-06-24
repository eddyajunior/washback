from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.ai_service import AIService
from app.application.services.analytics_service import AnalyticsService
from app.application.services.auth_service import AuthService
from app.application.services.dashboard_service import DashboardService
from app.application.services.wash_service import WashService
from app.infrastructure.database.database import get_db

from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository

from app.application.services.customer_service import CustomerService
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.wash_repository import WashRepository


def get_wash_service(
    db: Session = Depends(get_db)
) -> WashService:
    return WashService(
        wash_repository=WashRepository(db),
        customer_repository=CustomerRepository(db)
    )

def get_dashboard_service(
    db: Session = Depends(get_db)
) -> DashboardService:
    return DashboardService(
        customer_repository=CustomerRepository(db),
        campaign_repository=CampaignRepository(db),
        wash_repository=WashRepository(db)
    )

def get_auth_service(
        db: Session = Depends(get_db)
) -> AuthService:
    
    return AuthService(
        user_repository = UserRepository(db),
        company_repository = CompanyRepository(db)
    )

def get_analytics_service(
    db: Session = Depends(get_db)
) -> AnalyticsService:

    return AnalyticsService(
        customer_repository=CustomerRepository(db),
        campaign_repository=CampaignRepository(db),
        wash_repository=WashRepository(db)
    )

def get_ai_service(
    db: Session = Depends(get_db)
) -> AIService:

    return AIService(
        customer_repository = CustomerRepository(db),
        campaign_repository = CampaignRepository(db),
        wash_repository = WashRepository(db)
    )

def get_customer_service(
    db: Session = Depends(get_db)
) -> CustomerService:

    repository = CustomerRepository(db)

    return CustomerService(repository)