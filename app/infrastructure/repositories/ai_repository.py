from sqlalchemy.orm import Session

from app.infrastructure.database.models.customer import Customer

from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.application.services.customer_service import CustomerService


class AIRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_customers(self):
            
        repository = CustomerRepository(self.db)
        service = CustomerService(repository)
        customer_list = service.list_customer()