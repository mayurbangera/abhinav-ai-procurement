from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base


class SupplierReference(Base):
    __tablename__ = "supplier_references"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    supplier_id = Column(
        Integer,
        ForeignKey(
            "suppliers.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    company_name = Column(
        String(255),
        nullable=False
    )

    contact_person = Column(
        String(255),
        nullable=False
    )

    contact_number = Column(
        String(15),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )