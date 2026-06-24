from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    phone: str
    car_plate: str
    car_model: str

class CustomerUpdate(BaseModel):
    id: int
    name: str
    phone: str
    car_plate: str
    car_model: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    car_plate: str
    car_model: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )