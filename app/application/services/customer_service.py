from app.core.exceptions import BusinessException, ValidationException
from app.core.logger import logger

from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.database.models.customer import Customer

class CustomerService:

    def __init__(
            self, 
            repository: CustomerRepository
            ):
        self.repository = repository

    def create_customer(self, data):
        
        existing_customer = self.repository.get_by_car_plate(data.company_id, data.car_plate)

        if existing_customer:
            raise ValidationException(
                "Já existe um cliente com essa placa."
            )
        
        customer = Customer(
            name = data.name,
            phone = data.phone, 
            company_id = data.company_id,
            car_plate = data.car_plate,
            car_model = data.car_model
        )

        return self.repository.create(customer)

    def list_customer_by_company_id(self, company_id: int):
        return self.repository.get_all_by_company_id(company_id)
    
    def list_customer(self):
        return self.repository.get_all()
    
    def list_customer_by_id(self, customer_id: int, company_id: int):

        existing_customer = self.repository.get_by_id(company_id, customer_id)

        if not existing_customer:
            raise BusinessException(
                "Cliente não encontrado.",
                404
            )

        return existing_customer
    
    def list_customer_by_phone(self, phone: str, company_id: int):

        existing_customer = self.repository.get_by_phone(company_id, phone)

        if not existing_customer:
            raise BusinessException(
                "Cliente não encontrado.",
                404
            )
        
        return existing_customer
    
    def list_customer_by_car_plate(self, car_plate: str, company_id: int):

        existing_customer = self.repository.get_by_car_plate(company_id, car_plate)

        if not existing_customer:
            raise BusinessException(
                "Cliente não encontrado.",
                404
            )

        return existing_customer
    
    def delete_customer(self, customer_id: int, company_id: int):

        deleted = self.repository.delete(customer_id, company_id)

        if not deleted:
            logger.info(
                f"Cliente não encontrado para exclusão: {customer_id}"
            )

            raise BusinessException(
                "No content",
                204
            )
        
        return True
    
    def update_customer(self, customer_id: int, company_id: int, data):
        existing_customer = self.repository.get_by_id(company_id, customer_id)

        if not existing_customer:
            logger.info(
                f"Cliente não encontrado para alteração: {customer_id}"
            )

            raise BusinessException(
                "Cliente não encontrado.",
                404
            )

        existing_customer.name = data.name
        existing_customer.phone = data.phone
        existing_customer.car_plate = data.car_plate
        existing_customer.car_model = data.car_model

        return self.repository.create(existing_customer)