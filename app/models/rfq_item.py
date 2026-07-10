from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.database import Base

class RFQItem(Base):
    __tablename__ = "rfq_items"

    id = Column(Integer, primary_key=True, index=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False)
    
    material_category = Column(String(255), nullable=False)
    material_name = Column(String(255), nullable=False)
    
    quantity = Column(Numeric(18, 3), nullable=False)
    unit = Column(String(50), nullable=False)
    
    brand_required = Column(String(255), nullable=True)
    
    # Store arbitrary material-specific fields here (e.g. grade, size, chemical_guarantee)
    dynamic_fields = Column(JSONB, nullable=True, default=dict)
    
    remarks = Column(Text, nullable=True)

    rfq = relationship("RFQ", back_populates="items")
