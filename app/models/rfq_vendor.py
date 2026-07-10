from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class RFQVendor(Base):
    __tablename__ = "rfq_vendors"

    id = Column(Integer, primary_key=True, index=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    
    # Sent, Delivered, Read, Failed
    whatsapp_status = Column(String(50), nullable=True)
    
    sent_at = Column(DateTime(timezone=True), nullable=True)

    rfq = relationship("RFQ", back_populates="vendors")
    vendor = relationship("Supplier")
