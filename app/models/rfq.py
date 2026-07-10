from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)
    rfq_number = Column(String(50), unique=True, index=True)
    project_name = Column(String(255), nullable=False)
    site_name = Column(String(255), nullable=False)
    delivery_location = Column(String(255), nullable=False)
    payment_terms = Column(String(255), nullable=True)
    
    # Draft, Pending Approval, Approved, Sent, Vendor Viewed, Vendor Responded, Quotation Received, Negotiation, Closed, Cancelled
    status = Column(String(50), default="Draft")
    
    created_by = Column(String(255), nullable=False)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    items = relationship("RFQItem", back_populates="rfq", cascade="all, delete-orphan")
    vendors = relationship("RFQVendor", back_populates="rfq", cascade="all, delete-orphan")
