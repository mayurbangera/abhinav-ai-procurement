from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BigInteger
)
from sqlalchemy.sql import func
from app.database.database import Base


class DocumentIngestionLog(Base):
    """
    Tracks every incoming procurement document that enters the
    Document Intelligence Engine. One row per file ingested —
    regardless of source (WhatsApp or manual upload).

    Processing status lifecycle:
        PENDING -> PROCESSING -> DONE
                             -> FAILED
    """
    __tablename__ = "document_ingestion_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Unique identifier for this ingest transaction.
    # Used as the external reference across all pipeline stages.
    document_uuid = Column(
        String(36),
        unique=True,
        index=True,
        nullable=False
    )

    # File information
    original_filename = Column(
        String(255),
        nullable=True
    )

    stored_filename = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    # SHA-256 hex digest. Used for duplicate detection.
    file_hash = Column(
        String(64),
        unique=True,
        index=True,
        nullable=False
    )

    file_size_bytes = Column(
        BigInteger,
        nullable=False
    )

    mime_type = Column(
        String(100),
        nullable=True
    )

    file_extension = Column(
        String(10),
        nullable=True
    )

    # Origin metadata
    # MANUAL_UPLOAD = uploaded via dashboard
    # WHATSAPP = received via WhatsApp webhook
    source = Column(
        String(50),
        nullable=False,
        default="MANUAL_UPLOAD"
    )

    # WhatsApp sender number — nullable for manual uploads
    sender_phone = Column(
        String(20),
        nullable=True
    )

    # Resolved supplier — nullable until matched in Phase 7
    supplier_id = Column(
        Integer,
        nullable=True
    )

    # Processing pipeline status
    # Filled by Phase 4 (Document Classifier)
    document_type = Column(
        String(50),
        nullable=True
    )

    # PENDING, PROCESSING, DONE, FAILED
    processing_status = Column(
        String(50),
        nullable=False,
        default="PENDING"
    )

    # Optional: short reason if processing failed
    processing_error = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
