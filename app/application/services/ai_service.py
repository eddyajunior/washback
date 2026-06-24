from datetime import datetime

from app.infrastructure.database.models.campaign import Campaign

from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.repositories.wash_repository import WashRepository

class AIService:

    def __init__(
            self,
            customer_repository: CustomerRepository,
            campaign_repository: CampaignRepository,
            wash_repository: WashRepository
            ):
        self.customer_repository = customer_repository
        self.campaign_repository = campaign_repository
        self.wash_repository = wash_repository

    def recurring_customers(self):

        customers = self.get_all_customers()

        analysis = []

        for customer in customers:

            washes = self.get_washes_by_customer_id(customer.id)
    
            if len(washes) < 2:
                analysis.append({
                    "customer_id": customer.id,
                    "customer_name": customer.name,
                    "status": "insufficient_data",
                    "message": "Poucas lavagens para análise"
                })

            intervals = []

            for i in range(1, len(washes)):
                diff = (
                    washes[i].created_at -
                    washes[i - 1].created_at
                ).days

                intervals.append(diff)

            if len(intervals) == 0:
                analysis.append({
                    "customer_id": customer.id,
                    "customer_name": customer.name,
                    "status": "insufficient_data",
                    "message": "Poucas lavagens para análise"
                })

                continue
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

            analysis.append({
                "customer_id": customer.id,
                "customer_name": customer.name,
                "average_interval_days": round(average_interval, 1),
                "days_since_last_wash": days_since_last_wash,
                "status": status,
                "recommended_action":
                    "Enviar cupom"
                    if status == "risk"
                    else "Nenhuma ação"
            })

        return analysis

    def get_all_customers(self):
        return self.customer_repository.get_all()

    def generate_campaigns(self):

        customers = self.get_all_customers()

        campaigns_response = []

        for customer in customers:

            # Calculate customer status based on wash history
            washes = self.get_washes_by_customer_id(customer.id) 
   
            if len(washes) < 2:

                campaigns_response.append({
                    "customer": customer.name,
                    "status": "insufficient_data",
                    "campaign": {
                        "title": "Sem dados suficientes",
                        "message": "Continue utilizando o sistema",
                        "coupon": None
                    }
                })

                continue

            intervals = []

            for i in range(1, len(washes)):
                diff = (
                    washes[i].created_at - washes[i - 1].created_at
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

            customer_status = {
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
            
            # Generate campaign data
            campaign_data = {
                "status": "insufficient_data",
                "campaign": {
                    "title": "Sem dados suficientes",
                    "message": "Continue utilizando o sistema",
                    "coupon": None
                }
            }

            status = customer_status["status"]
            customer_name = customer_status["customer_name"]

            if status == "inactive":
                campaign_data = {
                    "status": status,
                    "campaign": {
                        "title": "Sentimos sua falta",
                        "message": f"{customer_name}, volte essa semana e ganhe 10% OFF",
                        "coupon": "VOLTA10"
                    }
                }

            elif status == "at_risk":                
                campaign_data = {
                    "status": status,
                    "campaign": {
                        "title": "Não perca seu benefício",
                        "message": f"{customer_name}, faça sua próxima lavagem e ganhe um upgrade grátis",
                        "coupon": "UPGRADE"
                    }
                }

            elif status == "loyal":
                campaign_data = {
                    "status": status,
                    "campaign": {
                        "title": "Cliente VIP",
                        "message": f"{customer_name}, você ganhou uma lavagem premium",
                        "coupon": "VIP20"
                    }
                }

            new_campaign = Campaign(
            customer_id=customer.id,
            company_id=customer.company_id,
            title=campaign_data["campaign"]["title"],
            message=campaign_data["campaign"]["message"],
            coupon=campaign_data["campaign"]["coupon"],
            status=campaign_data["status"]
            )

            self.campaign_repository.create_campaign(new_campaign)

            campaigns_response.append({
                "customer": customer.name,
                "status": status,
                "campaign": {
                    "title": new_campaign.title,
                    "message": new_campaign.message,
                    "coupon": new_campaign.coupon
                }
            })

        return campaigns_response

    def get_washes_by_customer_id(self, id: int):
        return self.wash_repository.get_washes_by_customer_id(id)