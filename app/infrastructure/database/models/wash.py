from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.infrastructure.database.database import Base

from datetime import datetime

class Wash(Base):
    __tablename__ = "washes"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    wash_type = Column(
        String,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    notes = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="washes"
    )

    company = relationship(
        "Company",
        back_populates="washes"
    )