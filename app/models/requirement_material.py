from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class RequirementMaterial(Base):
    __tablename__ = "requirement_materials"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    requirement_id = Column(
        Integer,
        ForeignKey("requirements.id"),
        nullable=False
    )
    
    requirement = relationship(
        "Requirement",
        back_populates="materials"
    )

    material_name = Column(
        String(255),
        nullable=False
    )

    specification = Column(
        Text,
        nullable=False
    )

    preferred_brand = Column(
        String(255),
        nullable=True
    )

    alternate_brand_allowed = Column(
        Boolean,
        default=True
    )

    quantity = Column(
        String(50),
        nullable=False
    )

    unit = Column(
        String(50),
        nullable=False
    )

    delivery_location = Column(
        String(255),
        nullable=False
    )

    

    purpose = Column(
        Text,
        nullable=False
    )

    additional_specification = Column(
        Text,
        nullable=True
    )

    remarks = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )