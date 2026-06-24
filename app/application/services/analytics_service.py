from datetime import datetime

from sqlalchemy import func

from app.infrastructure.database.models.customer import Customer
from app.infrastructure.database.models.wash import Wash

from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.repositories.wash_repository import WashRepository

class AnalyticsService:
    def __init__(
            self,
            customer_repository: CustomerRepository,
            campaign_repository: CampaignRepository,
            wash_repository: WashRepository
            ):
        self.customer_repository = customer_repository
        self.campaign_repository = campaign_repository
        self.wash_repository = wash_repository

    def get_active_customers(self, start_date: datetime):
        return self.customer_repository.get_active_customers(start_date)
    
    def get_kpi_total_washes(self, start_date: datetime):
        return self.wash_repository.get_kpi_total_washes(start_date)

    def get_kpi_total_customers(self, start_date: datetime, customer_id: int, wash: Wash):
        return self.customer_repository.get_kpi_total_customers(start_date, customer_id, wash)

    def get_top_customers_by_initial_date(self, start_date: datetime, customer: Customer, wash: Wash, limit: int):

        customers_query = self.customer_repository.get_top_customers_by_initial_date(start_date, customer, wash, limit)
        
        top_customers = []

        for customer in customers_query:
            top_customers.append({
                "customer": customer.name,
                "total_washes": customer.total_washes,
                "total_revenue": round(float(customer.total_revenue or 0), 2)
            })

        return top_customers

    def get_top_revenue_customers(self):
        customers = self.customer_repository.get_top_revenue_customers()

        return [
            {
                "customer": item[0],
                "revenue": float(item[1])
            }
            for item in customers
        ]

    def get_active_customers(self):
        return self.customer_repository.get_active_customers()

    def get_kpi_total_revenue(self, start_date: datetime):
        return self.wash_repository.get_kpi_total_revenue(start_date)
    
    def get_active_campaigns(self, start_date: datetime):
        return self.campaign_repository.get_active_campaigns(start_date)
    
    def get_revenue_chart(self, start_date: datetime):
        revenue_chart_query = self.wash_repository.get_revenue_chart(start_date)

        revenue_chart = []

        for item in revenue_chart_query:
            revenue_chart.append({
                "date": item.date,
                "revenue": round(float(item.revenue or 0), 2)
            })

        return revenue_chart
    
    def get_wash_types(self, start_date: datetime):
        wash_types_result = self.wash_repository.get_wash_types(start_date)
        
        wash_types = []

        for item in wash_types_result:
            wash_types.append({
                "type": item.wash_type,
                "total": item.total,
                "revenue": round(float(item.revenue or 0), 2)
            })
            
        return wash_types
    
    def get_recently_campaigns(self, start_date: datetime):
        campaigns_result = self.campaign_repository.get_recently_campaigns(start_date)
        campaigns = []

        for item in campaigns_result:
            campaigns.append({
                "customer": item.name,
                "title": item.title,
                "status": item.status,
                "coupon": item.coupon
            })
        
        return campaigns
    
    def get_revenue_by_month(self):
        results = self.wash_repository.get_revenue_by_month()

        revenues = []

        for item in results:

            month = (
                f"{int(item.year)}-"
                f"{int(item.month):02d}"
            )

            revenues.append({
                "month": month,
                "revenue": round(item.revenue, 2)
            })

        return revenues

    def get_top_wash_types(self):
        results = self.wash_repository.get_top_wash_types()

        data = []

        for item in results:
            data.append({
                "wash_type": item.wash_type,
                "total": item.total
            })

        return data
   
    def get_kpis(self):
        total_customers = self.customer_repository.get_total_customers()
        total_washes = self.wash_repository.get_total_washes()
        total_revenue = self.wash_repository.get_total_revenues()
        total_campaigns = self.campaign_repository.get_all_campaigns()

        average_ticket = (
            round(total_revenue / total_washes, 2)
            if total_washes > 0 else 0
        )

        customers = self.customer_repository.get_all()

        recurring_customers = 0
        risk_customers = 0
        inactive_customers = 0

        for customer in customers:
            recurrence = self.calculate_customer_status(customer)

        status = recurrence.get("status")

        if status == "recurring":
            recurring_customers += 1

        elif status == "risk":
            risk_customers += 1

        elif status == "inactive":
            inactive_customers += 1

        data = {
                "total_customers": total_customers,
                "total_washes": total_washes,
                "total_campaigns": total_campaigns,
                "total_revenue": round(total_revenue, 2),
                "average_ticket": average_ticket,
                "recurring_customers": recurring_customers,
                "risk_customers": risk_customers,
                "inactive_customers": inactive_customers
            }
        
        return data
    
    def calculate_customer_status(self, customer: Customer):
        washes = self.wash_repository.get_washes_by_customer_id(customer.id)
        
        if len(washes) < 2:
            return {
                "customer_id": customer.id,
                "customer_name": customer.name,
                "status": "insufficient_data",
                "message": "Poucas lavagens para análise"
            }

        intervals = []

        for i in range(1, len(washes)):
            diff = (
                washes[i].created_at -
                washes[i - 1].created_at
            ).days

            intervals.append(diff)

        average_interval = sum(intervals) / len(intervals)

        last_wash = washes[-1].created_at

        days_since_last_wash = (
            datetime.utcnow() - last_wash
        ).days

        risk_limit = average_interval * 1.5

        status = (
            "risk"
            if days_since_last_wash > risk_limit
            else "healthy"
        )

        return {
            "customer_id": customer.id,
            "customer_name": customer.name,
            "average_interval_days": round(average_interval, 1),
            "days_since_last_wash": days_since_last_wash,
            "status": status,
            "recommended_action":
                "Enviar cupom"
                if status == "risk"
                else "Nenhuma ação"
        }
    

 