"""
Document Intelligence Service — Phase 1: Ingestion & Storage

This is the master service for the Document Intelligence Engine.
Each future phase will ADD new functions to this service.
This service must NEVER be broken by future additions.

Phase 1  : ingest_document()          — File save + hash + DB log
Phase 2  : extract_text_from_pdf()    — PyMuPDF parser
Phase 3  : extract_text_via_ocr()     — PaddleOCR engine
Phase 4  : classify_document()        — Document type classifier
Phase 6  : parse_with_llm()           — LLM provider abstraction
Phase 7  : resolve_entities()         — Semantic KB matching
Phase 8  : validate_document()        — Business validation engine
Phase 9  : create_draft_quotation()   — Auto-create quotation from extraction
"""

import os
import uuid
import hashlib
import shutil
import fitz

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.models.document_ingestion_log import DocumentIngestionLog


# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

INGEST_FOLDER = "uploads/quotation_documents"

# Maximum file size: 10 MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# Allowed file types for procurement document ingestion
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png"
}

# Maps MIME type to file extension when filename is not available
# (used for WhatsApp media downloads where original filename is unknown)
MIME_TO_EXTENSION = {
    "application/pdf": ".pdf",
    "image/jpeg":      ".jpg",
    "image/jpg":       ".jpg",
    "image/png":       ".png"
}


# ──────────────────────────────────────────────────────────────
# Utility Functions
# ──────────────────────────────────────────────────────────────

def _compute_sha256(file_bytes: bytes) -> str:
    """Compute SHA-256 hex digest of a file's binary content."""
    return hashlib.sha256(file_bytes).hexdigest()


def _ensure_ingest_folder() -> None:
    """Create the ingest folder if it does not exist."""
    os.makedirs(INGEST_FOLDER, exist_ok=True)


# ──────────────────────────────────────────────────────────────
# Phase 1: Ingest Document
# ──────────────────────────────────────────────────────────────

def ingest_document(
    db: Session,
    file: UploadFile,
    source: str = "MANUAL_UPLOAD",
    sender_phone: str = None,
    supplier_id: int = None
) -> DocumentIngestionLog:
    """
    Accept an uploaded file, validate it, deduplicate by SHA-256 hash,
    save it to disk, and create a DocumentIngestionLog database record.

    Args:
        db            : SQLAlchemy session.
        file          : Uploaded file from FastAPI.
        source        : 'MANUAL_UPLOAD' or 'WHATSAPP'.
        sender_phone  : WhatsApp number (nullable for manual uploads).
        supplier_id   : Resolved supplier FK (nullable, filled in Phase 7).

    Returns:
        DocumentIngestionLog instance (either new or existing duplicate).

    Raises:
        HTTPException 400: Invalid file type or file too large.
        HTTPException 500: Unexpected storage or database error.
    """
    _ensure_ingest_folder()

    # ── Step 1: Validate file extension ──────────────────────
    original_filename = file.filename or "unknown"
    file_extension = os.path.splitext(original_filename)[1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"File type '{file_extension}' is not allowed. "
                f"Accepted types: PDF, JPG, JPEG, PNG."
            )
        )

    # ── Step 2: Read file bytes once ─────────────────────────
    file_bytes = file.file.read()
    file_size = len(file_bytes)

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if file_size > MAX_FILE_SIZE_BYTES:
        size_mb = round(file_size / (1024 * 1024), 2)
        raise HTTPException(
            status_code=400,
            detail=(
                f"File size {size_mb} MB exceeds maximum allowed size of "
                f"{MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
            )
        )

    # ── Step 3: Compute SHA-256 hash ─────────────────────────
    file_hash = _compute_sha256(file_bytes)

    # ── Step 4: Duplicate detection ──────────────────────────
    existing = db.query(DocumentIngestionLog).filter(
        DocumentIngestionLog.file_hash == file_hash
    ).first()

    if existing:
        # Return the existing record — no duplicate storage
        return existing

    # ── Step 5: Determine MIME type ──────────────────────────
    content_type = file.content_type or ""
    mime_type = content_type.lower().split(";")[0].strip()

    # ── Step 6: Generate UUID filename and save to disk ──────
    doc_uuid = str(uuid.uuid4())
    stored_filename = doc_uuid + file_extension
    file_path = os.path.join(INGEST_FOLDER, stored_filename)

    try:
        with open(file_path, "wb") as f:
            f.write(file_bytes)
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file to storage: {str(e)}"
        )

    # Normalize path separator for cross-platform compatibility
    file_path = file_path.replace("\\", "/")

    # ── Step 7: Create database record ───────────────────────
    log = DocumentIngestionLog(
        document_uuid=doc_uuid,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        file_hash=file_hash,
        file_size_bytes=file_size,
        mime_type=mime_type if mime_type else None,
        file_extension=file_extension,
        source=source,
        sender_phone=sender_phone,
        supplier_id=supplier_id,
        document_type=None,       # Filled by Phase 4 (Classifier)
        processing_status="PENDING",
        processing_error=None
    )

    try:
        db.add(log)
        db.commit()
        db.refresh(log)
    except Exception as e:
        db.rollback()
        # Clean up saved file to avoid orphaned files
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Database error while logging ingestion: {str(e)}"
        )

    return log


# ──────────────────────────────────────────────────────────────
# Phase 1: List Ingested Documents
# ──────────────────────────────────────────────────────────────

def list_ingested_documents(
    db: Session,
    status: str = None,
    limit: int = 50,
    offset: int = 0
) -> list:
    """
    Return a paginated list of all ingested documents.

    Args:
        db     : SQLAlchemy session.
        status : Optional filter by processing_status.
        limit  : Max rows to return (default 50).
        offset : Pagination offset (default 0).

    Returns:
        List of DocumentIngestionLog instances.
    """
    query = db.query(DocumentIngestionLog)

    if status:
        query = query.filter(
            DocumentIngestionLog.processing_status == status
        )

    return (
        query
        .order_by(DocumentIngestionLog.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_ingested_document(
    db: Session,
    document_uuid: str
) -> DocumentIngestionLog:
    """
    Fetch a single ingested document by its UUID.

    Args:
        db            : SQLAlchemy session.
        document_uuid : UUID string assigned at ingest time.

    Returns:
        DocumentIngestionLog or None.
    """
    return db.query(DocumentIngestionLog).filter(
        DocumentIngestionLog.document_uuid == document_uuid
    ).first()


# ──────────────────────────────────────────────────────────────
# Phase 2: PDF Digital Text Extraction
# ──────────────────────────────────────────────────────────────

def extract_text_from_pdf(
    db: Session,
    document_uuid: str
) -> dict:
    """
    Open the ingested PDF using PyMuPDF (fitz) and extract the digital text layer.
    Saves the extracted text to a parallel text file on disk.
    If the PDF doesn't contain extractable text (< 50 chars), it flags it as requiring OCR.

    Args:
        db            : SQLAlchemy session.
        document_uuid : UUID string of the ingested document.

    Returns:
        dict containing extraction metrics and preview.
    """
    log = get_ingested_document(db, document_uuid)
    if not log:
        raise HTTPException(
            status_code=404,
            detail=f"Ingestion log for document UUID '{document_uuid}' not found."
        )

    # Scanned fallback for images
    if log.file_extension.lower() in [".jpg", ".jpeg", ".png"]:
        return {
            "document_uuid": document_uuid,
            "requires_ocr": True,
            "page_count": 0,
            "character_count": 0,
            "extracted_text_path": None,
            "preview": "Image file requires OCR (Phase 3)."
        }

    if log.file_extension.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail=f"Digital text extraction is only supported for PDF files. Document has extension '{log.file_extension}'."
        )

    if not os.path.exists(log.file_path):
        raise HTTPException(
            status_code=500,
            detail=f"Source PDF file not found at path '{log.file_path}'."
        )

    try:
        doc = fitz.open(log.file_path)
        page_count = len(doc)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to open PDF document with PyMuPDF: {str(e)}"
        )

    extracted_pages = []
    total_chars = 0

    try:
        for page in doc:
            page_text = page.get_text() or ""
            extracted_pages.append(page_text)
            total_chars += len(page_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred during PDF text extraction: {str(e)}"
        )
    finally:
        doc.close()

    total_text = "\n".join(extracted_pages).strip()

    # If the text length is very low, it indicates a scanned PDF
    if len(total_text) < 50:
        return {
            "document_uuid": document_uuid,
            "requires_ocr": True,
            "page_count": page_count,
            "character_count": len(total_text),
            "extracted_text_path": None,
            "preview": "Scanned PDF or empty vector document. Requires OCR (Phase 3)."
        }

    # Save extracted text to a parallel text file
    text_filename = f"{document_uuid}_extracted.txt"
    text_path = os.path.join(INGEST_FOLDER, text_filename).replace("\\", "/")

    try:
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(total_text)
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save extracted text to disk: {str(e)}"
        )

    # Update database log status
    try:
        log.processing_status = "PROCESSING"
        db.commit()
        db.refresh(log)
    except Exception as e:
        db.rollback()
        # Clean up text file on failure
        if os.path.exists(text_path):
            os.remove(text_path)
        raise HTTPException(
            status_code=500,
            detail=f"Database error while updating processing status: {str(e)}"
        )

    # Return summary details
    return {
        "document_uuid": document_uuid,
        "requires_ocr": False,
        "page_count": len(extracted_pages),
        "character_count": total_chars,
        "extracted_text_path": text_path,
        "preview": total_text[:250] + ("..." if len(total_text) > 250 else "")
    }

