# Ação recomendada agora: não refatorar ainda. 
# Apenas marcar como ponto de atenção. 
# Se algum método passar de 30–40 linhas ou misturar muitas responsabilidades.

from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.repositories.wash_repository import WashRepository


class DashboardService:

    def __init__(
            self,
            customer_repository: CustomerRepository,
            campaign_repository: CampaignRepository,
            wash_repository: WashRepository
            ):
        self.customer_repository = customer_repository
        self.campaign_repository = campaign_repository
        self.wash_repository = wash_repository
        
    def get_total_customers(self):
        return self.customer_repository.get_total_customers()    
    
    def get_active_customers(self):
        return self.customer_repository.get_active_customers()

    def get_total_washes(self):
        return self.wash_repository.get_total_washes()

    def get_inactive_customers(self):
        return self.customer_repository.get_inactive_customers()
    
    def get_total_campaigns(self):
        return self.campaign_repository.get_total_campaigns()

    def get_total_revenue(self):
        return self.wash_repository.get_total_revenues()
    
    def get_average_ticket(self):
        return self.wash_repository.get_average_ticket()

    def get_monthly_revenue(self):

        revenue = self.wash_repository.get_monthly_revenue()

        return [
            {
                "month": int(item[0]),
                "revenue": float(item[1])
            }
            for item in revenue
        ]

    def get_monthly_washes(self):
        washes = self.wash_repository.get_monthly_washes()

        return [
            {
                "month": int(item[0]),
                "total_washes": item[1]
            }
            for item in washes
        ]
    
    def get_top_customers(self):
        customers = self.customer_repository.get_top_customers()

        return [
            {
                "customer": customer[0],
                "total_washes": customer[1]
            }
            for customer in customers
        ] 

    def get_top_revenue_customers(self):
        customers = self.customer_repository.get_top_revenue_customers()

        return [
            {
                "customer": item[0],
                "revenue": float(item[1])
            }
            for item in customers
        ]
    
    def get_metrics(self, company_id: int):
        total_customers = self.customer_repository.get_total_customers_by_company(company_id)

        total_washes = self.wash_repository.get_total_washes_by_company(company_id)
        
        total_revenue = self.wash_repository.get_total_revenues_by_company(company_id)

        if total_revenue is None:
            total_revenue = 0.0

        average_ticket = 0
        if total_washes > 0:
            average_ticket = (
                total_revenue / total_washes
            )

        recurring_customers = self.wash_repository.get_recurring_customers_by_company(company_id)

        return {
            "total_customers": total_customers,
            "total_washes": total_washes,
            "total_revenue": total_revenue,
            "average_ticket": round(
                average_ticket,
                2
            ),
            "recurring_customers": recurring_customers
        }

        


