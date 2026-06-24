from datetime import datetime
from pydantic import BaseModel


class CampaignResponse(BaseModel):
    id: int
    customer_id: int
    title: str
    message: str
    coupon: str | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }