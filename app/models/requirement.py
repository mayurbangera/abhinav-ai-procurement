from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    requirement_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    project_name = Column(
        String(255),
        nullable=False
    )

    site_name = Column(
        String(255),
        nullable=False
    )

    requested_by = Column(
        String(255),
        nullable=False
    )

    priority = Column(
        String(20),
        default="MEDIUM"
    )

    required_date = Column(
        Date,
        nullable=False
    )

    purpose = Column(
        Text,
        nullable=False
    )

    remarks = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        default="DRAFT"
    )

    materials = relationship(
        "RequirementMaterial",
        back_populates="requirement",
        cascade="all, delete-orphan"
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
    
    