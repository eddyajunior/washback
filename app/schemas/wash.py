from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WashCreate(BaseModel):
    customer_id: int

    wash_type: str = Field(
        min_length=3,
        max_length=50
    )

    price: float = Field(
        gt=0
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=500
    )

class WashResponse(BaseModel):
    id: int
    customer_id: int
    company_id: int
    wash_type: str
    price: float
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True