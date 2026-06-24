from pydantic import BaseModel
from typing import Any


class DefaultResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None