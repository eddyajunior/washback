from datetime import datetime

from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from app.infrastructure.database.models.wash import Wash

class WashRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_washes_by_customer_id(
            self, 
            customer_id,
            skip: int = 0,
            limit: int = 10
            ):
        return (
            self.db.query(Wash)
                .filter(Wash.customer_id == customer_id)
                .order_by(Wash.created_at.asc())
                .offset(skip)
                .limit(limit)
                .all()
        )
    
    def get_washes_by_company_id(self, company_id: int, skip: int = 0, limit: int = 0):
        return (
            self.db.query(Wash)
                .filter(Wash.company_id == company_id)
                .offset(skip)
                .limit(limit)
                .all()
        )
    
    def get_kpi_total_revenue(self, start_date: datetime):
        return self.db.query(func.sum(Wash.price)).filter(Wash.created_at >= start_date).scalar()

    def get_kpi_total_washes(self, start_date: datetime):
        return self.db.query(Wash).filter(Wash.created_at >= start_date).count()
    
    def get_revenue_chart(self, start_date: datetime):
        return self.db.query(func.date(Wash.created_at).label("date"),
            func.sum(Wash.price).label("revenue")
        ).filter(Wash.created_at >= start_date).group_by(func.date(Wash.created_at)).order_by(func.date(Wash.created_at)).all()
    
    def get_wash_types(self, start_date: datetime):
        return self.db.query(
            Wash.wash_type,
            func.count(Wash.id).label("total"),
            func.sum(Wash.price).label("revenue")
        ).filter(Wash.created_at >= start_date).group_by(Wash.wash_type).order_by(func.count(Wash.id).desc()).all()
    
    def get_revenue_by_month(self):
        return self.db.query(
            extract("year", Wash.created_at).label("year"),
            extract("month", Wash.created_at).label("month"),
            func.sum(Wash.price).label("revenue")
        ).group_by(
            extract("year", Wash.created_at),
            extract("month", Wash.created_at)
        ).order_by(
            extract("year", Wash.created_at),
            extract("month", Wash.created_at)
        ).all()
    
    def get_monthly_revenue(self):
        return self.db.query(
                extract("month", Wash.created_at).label("month"),
                func.sum(Wash.price).label("revenue")
            ).group_by(
                extract("month", Wash.created_at)
            ).order_by(
                extract("month", Wash.created_at)
            ).all()

    def get_monthly_washes(self):
        return self.db.query(
                extract("month", Wash.created_at).label("month"),
                func.count(Wash.id).label("total")
            ).group_by(
                extract("month", Wash.created_at)
            ).order_by(
                extract("month", Wash.created_at)
            ).all()

    def get_total_revenues(self):
        return self.db.query(
            func.sum(Wash.price).label("revenue")
        ).count()
    
    def get_total_revenues_by_company(self, company_id: int):
        return self.db.query(
            func.sum(Wash.price)
        ).filter(
            Wash.company_id == company_id
        ).scalar()
    
    def get_recurring_customers_by_company(self, company_id: int):
        return self.db.query(
            Wash.customer_id
            ).filter(
                Wash.company_id == company_id
            ).group_by(
                Wash.customer_id
            ).having(
                func.count(Wash.id) > 1
            ).count()
    
    def get_top_wash_types(self):
        return self.db.query(
            Wash.wash_type,
            func.count(Wash.id).label("total")
        ).group_by(Wash.wash_type).order_by(
            func.count(Wash.id).desc()
        ).all()
    
    def get_total_washes(self):
        return self.db.query(Wash).count()
    
    def get_total_washes_by_company(self, company_id: int):
        return self.db.query(Wash).filter(Wash.company_id == company_id).count()
    
    def get_wash_by_wash_id(self, company_id: int, wash_id: int):
        wash = self.db.query(Wash).filter(
            Wash.id == wash_id,
            Wash.company_id == company_id
            ).first()
        
        return wash
    
    def get_average_ticket(self):
        avg = self.db.query(func.avg(Wash.price)).scalar()
        return round(float(avg or 0), 2)
    
    def create(self, wash: Wash):
        self.db.add(wash)
        self.db.commit()
        self.db.refresh(wash)

        return wash