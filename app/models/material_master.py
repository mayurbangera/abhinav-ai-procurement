from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    Numeric
)
from sqlalchemy.sql import func

from app.database.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class MaterialMaster(Base):

    __tablename__ = "material_master"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    material_code = Column(
        String(30),
        unique=True,
        nullable=False
    )

    material_name = Column(
        String(255),
        nullable=False,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey("material_categories.id"),
        nullable=False
    )

    subcategory_id = Column(
        Integer,
        ForeignKey("material_subcategories.id"),
        nullable=True
    )

    category = relationship(
        "MaterialCategory"
    )

    subcategory = relationship(
        "MaterialSubCategory"
    )

    description = Column(
        Text,
        nullable=True
    )

    default_unit = Column(
        String(50),
        nullable=False
    )

    preferred_brand = Column(
        String(255),
        nullable=True
    )

    gst_percentage = Column(
        Numeric(5,2),
        nullable=True
    )

    hsn_code = Column(
        String(20),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
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