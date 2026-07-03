from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text
)

from sqlalchemy.sql import func

from app.database.database import Base


class MaterialCategory(Base):

    __tablename__ = "material_categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    category_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    category_name = Column(
        String(100),
        unique=True,
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

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )