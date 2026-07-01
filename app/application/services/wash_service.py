from app.core.exceptions import BusinessException
from app.infrastructure.database.models.wash import Wash


class WashService:
    def __init__(
            self, 
            wash_repository,
            customer_repository):
        self.wash_repository = wash_repository
        self.customer_repository = customer_repository

    def get_wash_by_wash_id(self, company_id: int, wash_id: int):
        return self.wash_repository.get_wash_by_wash_id(company_id, wash_id)

    def get_washes_by_company_id(self, company_id: int, skip: int = 0, limit: int = 0):
        return self.wash_repository.get_washes_by_company_id(company_id, skip, limit)
    
    def get_customer_by_id(self, customer_id: int, company_id: int):
        return self.customer_repository.get_by_id(company_id, customer_id)

    def create_wash(self, wash, company_id: int):
        customer = self.customer_repository.get_by_id(company_id, wash.customer_id)

        if not customer:
            raise BusinessException(
                "Cliente não encontrado.",
                404
            )

        new_wash = Wash(
            customer_id=wash.customer_id,
            company_id=company_id,
            wash_type=wash.wash_type,
            price=wash.price,
            notes=wash.notes
        )

        return self.wash_repository.create(new_wash)
    
    def get_total_washes_by_company_id(self, company_id: int):
        return self.wash_repository.get_total_washes_by_company(company_id)
        
