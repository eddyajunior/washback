from fastapi import APIRouter, Depends

from app.core.dependencies import get_customer_service
from app.core.exceptions import BusinessException
from app.core.responses import paginated_response, success_response
from app.core.security import get_current_user
from app.core.logger import logger

from app.infrastructure.database.models.customer import Customer

from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.common import DefaultResponse

from app.application.services.customer_service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=DefaultResponse
)
def create_customer(
    customer: CustomerCreate,
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service)
):
    current_company_id = current_user["company_id"]

    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        car_plate=customer.car_plate,
        car_model=customer.car_model,
        company_id=current_company_id
    )

    customer_created = service.create_customer(new_customer)

    logger.info(
        f"Cliente criado: {customer_created.id}"
    )

    return success_response(
        "Cliente criado com sucesso.",
        CustomerResponse
            .model_validate(customer_created)
            .model_dump()
    )

@router.get("/", response_model=DefaultResponse)
def list_customers(
    page: int = 1,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service)
):
    skip = (page - 1) * limit

    current_company_id = current_user["company_id"]

    customer_list = service.list_customer_by_company_id(current_company_id)
    total = len(customer_list)

    customers = customer_list[skip: skip + limit]

    customers_response = [
        CustomerResponse.model_validate(customer).model_dump()
        for customer in customers
    ]

    logger.info(
        f"Clientes listados empresa {current_company_id}"
    )

    return paginated_response(
        "Clientes listados com sucesso.",
        customers_response,
        page,
        limit,
        total
    )

@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service)
):
    
    current_company_id = current_user["company_id"]
    
    customer = service.list_customer_by_id(customer_id, current_company_id)

    if not customer:
        raise BusinessException(
            "Cliente não encontrado.",
            404
        )
    
    return success_response(
        "Cliente encontrado com sucesso.",
        CustomerResponse
            .model_validate(customer)
            .model_dump()
    )

@router.delete(
    "/{customer_id}",
    response_model=DefaultResponse
)
def delete_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service)
):
    
    if service.delete_customer(customer_id, current_user["company_id"]):
        logger.info(
            f"Cliente excluído: {customer_id}"
        )

        return success_response(
            "Cliente excluído com sucesso."
        )
    
@router.put(
    "/{customer_id}",
    response_model=DefaultResponse
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    current_user: dict = Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service)
):
    
    updated_customer = service.update_customer(
        customer_id,
        current_user["company_id"],
        customer
    )

    if not updated_customer:
        raise BusinessException(
            "Cliente não encontrado.",
            404
        )

    logger.info(
        f"Cliente atualizado: {customer_id}"
    )

    return success_response(
        "Cliente atualizado com sucesso.",
        CustomerResponse
            .model_validate(updated_customer)
            .model_dump()
    )
