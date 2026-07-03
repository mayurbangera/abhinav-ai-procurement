from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    Numeric
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
        nullable=False,
        index=True
    )

    requirement = relationship(
        "Requirement",
        back_populates="materials"
    )

    # ============================
    # Material Information
    # ============================

    material_name = Column(
        String(255),
        nullable=False,
        index=True
    )

    category = Column(
        String(100),
        nullable=True,
        index=True
    )

    specification = Column(
        Text,
        nullable=True
    )

    preferred_brand = Column(
        String(255),
        nullable=True
    )

    alternate_brand_allowed = Column(
        Boolean,
        default=True,
        nullable=False
    )

    quantity = Column(
        Numeric(18, 3),
        nullable=False
    )

    unit = Column(
        String(50),
        nullable=False
    )

    delivery_location = Column(
        String(255),
        nullable=True
    )

    purpose = Column(
        Text,
        nullable=True
    )

    # =====================================================
    # Free text field
    # Stores any procurement requirement that does not fit
    # into predefined columns.
    # =====================================================

    additional_requirements = Column(
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