from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
    ,ForeignKey
)
from sqlalchemy.orm import relationship

from datetime import datetime

from app.infrastructure.database.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    car_plate = Column(String, nullable=False)
    car_model = Column(String, nullable=False)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    company = relationship("Company", back_populates="customers")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    washes = relationship(
        "Wash",
        back_populates="customer",
        cascade="all, delete"
    )
