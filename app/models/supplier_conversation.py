from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database.database import Base

from sqlalchemy.ext.mutable import MutableDict


class SupplierConversation(Base):
    __tablename__ = "supplier_conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    phone_number = Column(
        String(15),
        nullable=False
    )

    current_step = Column(
        String(100),
        nullable=False
    )

    collected_data = Column(
        MutableDict.as_mutable(JSONB),
        nullable=True
    )

    conversation_status = Column(
        String(50),
        default="IN_PROGRESS"
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