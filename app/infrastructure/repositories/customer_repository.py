from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.infrastructure.database.models.customer import Customer
from app.infrastructure.database.models.wash import Wash

class CustomerRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, customer: Customer):
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def get_by_phone(self, company_id: int, phone: str):
        return self.db.query(Customer).filter(
            Customer.phone == phone,
            Customer.company_id == company_id
        ).first()
    
    def get_by_id(self, company_id: int, customer_id: int):
        return self.db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.company_id == company_id
        ).first()
    
    def get_all_by_company_id(self, company_id: int):
        return self.db.query(Customer).filter(Customer.company_id == company_id).all()
    
    def get_all(self):
        return self.db.query(Customer).all()
    
    def get_total_customers(self):
        return self.db.query(Customer).count()
    
    def get_total_customers_by_company(self, company_id: int):
        return self.db.query(Customer).filter(Customer.company_id == company_id).count()
    
    def get_by_car_plate(self, company_id: int, car_plate: str):
        return self.db.query(Customer).filter(
            Customer.car_plate == car_plate,
            Customer.company_id == company_id
        ).first()
    
    def delete(self, customer_id: int, company_id: int):
        customer = self.db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.company_id == company_id
        ).first()

        if not customer:
            return False

        self.db.delete(customer)

        self.db.commit()

        return True
    
    def update(self, customer_id: int, company_id: int, data: dict):
        customer = self.db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.company_id == company_id
        ).first()

        if not customer:
            return None
        
        for key, value in data.items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def get_top_customers_by_initial_date(self, start_date: datetime, customer: Customer, wash: Wash, limit: int):
        return self.db.query(
            customer.name,
            func.count(wash.id).label("total_washes"),
            func.sum(wash.price).label("total_revenue")
        ).join(wash, wash.customer_id == customer.id).filter(wash.created_at >= start_date).group_by(customer.name).order_by(func.sum(wash.price).desc()).limit(limit).all()
    
    def get_top_customers(self):
        return self.db.query(
                Customer.name,
                func.count(Wash.id).label("total_washes")
            ).join(Wash, Wash.customer_id == Customer.id).group_by(Customer.name).order_by(func.count(Wash.id).desc()).limit(5).all()
    
    def get_top_revenue_customers(self):
        return self.db.query(
                Customer.name,
                func.sum(Wash.price).label("revenue")
            ).join(Wash, Wash.customer_id == Customer.id).group_by(Customer.name).order_by(
                func.sum(Wash.price).desc()
            ).limit(5).all()

    def get_kpi_total_customers(self, start_date: datetime, customer_id: int, wash: Wash):
        return self.db.query(Customer).join(wash, wash.customer_id == customer_id).filter(wash.created_at >= start_date).distinct().count()
    
    def get_active_customers(self):
        limit_date = datetime.utcnow() - timedelta(days=30)

        return self.db.query(Wash.customer_id).filter(Wash.created_at >= limit_date).distinct().count()
   

    def get_inactive_customers(self):
        active_customers = self.db.query(Wash.customer_id).filter(
            Wash.created_at >= (
                datetime.utcnow() - timedelta(days=30)
                )
            ).distinct().subquery()

        return self.db.query(Customer).filter(~Customer.id.in_(active_customers)).count()
    
    # def get_customer_by_custumer_id(self, customer_id: int, company_id: int):
    #     return self.db.query(Customer).filter(
    #     Customer.id == customer_id,
    #     Customer.company_id == company_id
    # ).first()
    