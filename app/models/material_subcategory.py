from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class MaterialSubCategory(Base):

    __tablename__ = "material_subcategories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subcategory_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("material_categories.id"),
        nullable=False
    )

    subcategory_name = Column(
        String(100),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    category = relationship(
        "MaterialCategory"
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