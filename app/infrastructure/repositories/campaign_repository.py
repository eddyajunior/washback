from datetime import datetime

from sqlalchemy.orm import Session

from app.infrastructure.database.models.campaign import Campaign
from app.infrastructure.database.models.customer import Customer

class CampaignRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_campaign(self, campaign):
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign
    
    def get_active_campaigns(self, start_date: datetime):
        return self.db.query(Campaign).filter(Campaign.created_at >= start_date).count()
    
    def get_all_campaigns(self):
        return self.db.query(Campaign).all()
    
    def get_total_campaigns(self):
        return self.db.query(Campaign).count()
    
    def get_recently_campaigns(self, start_date: datetime):
        return self.db.query(
            Campaign.customer_id,
            Campaign.title,
            Campaign.status,
            Campaign.coupon,
            Customer.name
        ).join(Customer, Customer.id == Campaign.customer_id).filter(Campaign.created_at >= start_date).order_by(Campaign.created_at.desc()).limit(10).all()
