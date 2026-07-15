from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    Text,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.database import Base

class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False)
    rfq_item_id = Column(Integer, ForeignKey("rfq_items.id", ondelete="CASCADE"), nullable=False)
    
    is_quoted = Column(Boolean, default=True, nullable=False)
    quoted_quantity = Column(Numeric(18, 3), nullable=True)
    
    brand_offered = Column(String(255), nullable=True)
    specs_offered = Column(JSONB, nullable=True, default=dict)
    
    # Commercial fields
    basic_rate = Column(Numeric(18, 3), default=0.0, nullable=False)
    discount_percent = Column(Numeric(5, 2), default=0.0, nullable=False)
    tax_percent = Column(Numeric(5, 2), default=0.0, nullable=False)
    freight_amount = Column(Numeric(18, 3), default=0.0, nullable=False)
    
    # Mathematical totals per item row
    final_landed_rate = Column(Numeric(18, 3), default=0.0, nullable=False)
    total_item_amount = Column(Numeric(18, 3), default=0.0, nullable=False)
    
    remarks = Column(Text, nullable=True)

    quotation = relationship("Quotation", back_populates="items")
    rfq_item = relationship("RFQItem")
