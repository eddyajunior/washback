from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.infrastructure.database.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    title = Column(String, nullable=False)

    message = Column(String, nullable=False)

    coupon = Column(String, nullable=True)

    status = Column(String, nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)    
    company = relationship("Company", back_populates="campaigns")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )