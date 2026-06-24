from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship

from datetime import datetime

from app.infrastructure.database.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="company")
    customers = relationship("Customer", back_populates="company")
    washes = relationship("Wash", back_populates="company")
    campaigns = relationship("Campaign", back_populates="company")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )