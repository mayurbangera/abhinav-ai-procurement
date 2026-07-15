"""
Document Intelligence API Router — Phase 1

Routes:
    POST   /document-intelligence/ingest    Ingest a new document
    GET    /document-intelligence/          List all ingested documents
    GET    /document-intelligence/{uuid}    Fetch a single document by UUID
"""

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    Query
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.document_intelligence_service import (
    ingest_document,
    list_ingested_documents,
    get_ingested_document,
    extract_text_from_pdf
)

router = APIRouter(
    prefix="/document-intelligence",
    tags=["Document Intelligence"]
)


# ──────────────────────────────────────────────────────────────
# POST /document-intelligence/ingest
# ──────────────────────────────────────────────────────────────

@router.post("/ingest")
def ingest(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Ingest a procurement document uploaded manually from the dashboard.

    - Validates file type (PDF, JPG, JPEG, PNG).
    - Validates file size (max 10 MB).
    - Detects and rejects duplicate files (by SHA-256 hash).
    - Saves file to uploads/quotation_documents/.
    - Creates a DocumentIngestionLog database record.
    - Returns the document UUID, file path, and processing status.
    """
    log = ingest_document(
        db=db,
        file=file,
        source="MANUAL_UPLOAD",
        sender_phone=None,
        supplier_id=None
    )

    return {
        "document_uuid": log.document_uuid,
        "original_filename": log.original_filename,
        "file_path": log.file_path,
        "file_size_bytes": log.file_size_bytes,
        "file_extension": log.file_extension,
        "source": log.source,
        "processing_status": log.processing_status,
        "created_at": str(log.created_at)
    }


# ──────────────────────────────────────────────────────────────
# GET /document-intelligence/
# ──────────────────────────────────────────────────────────────

@router.get("/")
def list_documents(
    status: str = Query(default=None, description="Filter by processing_status: PENDING, PROCESSING, DONE, FAILED"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    List all ingested procurement documents.

    Optional filter by processing_status.
    Supports pagination via limit and offset.
    """
    documents = list_ingested_documents(
        db=db,
        status=status,
        limit=limit,
        offset=offset
    )

    return [
        {
            "document_uuid": doc.document_uuid,
            "original_filename": doc.original_filename,
            "file_extension": doc.file_extension,
            "source": doc.source,
            "sender_phone": doc.sender_phone,
            "document_type": doc.document_type,
            "processing_status": doc.processing_status,
            "processing_error": doc.processing_error,
            "file_size_bytes": doc.file_size_bytes,
            "created_at": str(doc.created_at)
        }
        for doc in documents
    ]


# ──────────────────────────────────────────────────────────────
# GET /document-intelligence/{document_uuid}
# ──────────────────────────────────────────────────────────────

@router.get("/{document_uuid}")
def get_document(
    document_uuid: str,
    db: Session = Depends(get_db)
):
    """
    Fetch a single ingested document by its UUID.
    Returns full details including file path and processing status.
    """
    doc = get_ingested_document(db=db, document_uuid=document_uuid)

    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Document with UUID '{document_uuid}' not found."
        )

    return {
        "id": doc.id,
        "document_uuid": doc.document_uuid,
        "original_filename": doc.original_filename,
        "stored_filename": doc.stored_filename,
        "file_path": doc.file_path,
        "file_hash": doc.file_hash,
        "file_size_bytes": doc.file_size_bytes,
        "mime_type": doc.mime_type,
        "file_extension": doc.file_extension,
        "source": doc.source,
        "sender_phone": doc.sender_phone,
        "supplier_id": doc.supplier_id,
        "document_type": doc.document_type,
        "processing_status": doc.processing_status,
        "processing_error": doc.processing_error,
        "created_at": str(doc.created_at),
        "updated_at": str(doc.updated_at)
    }


# ──────────────────────────────────────────────────────────────
# POST /document-intelligence/{document_uuid}/extract-text
# ──────────────────────────────────────────────────────────────

@router.post("/{document_uuid}/extract-text")
def extract_text(
    document_uuid: str,
    db: Session = Depends(get_db)
):
    """
    Trigger digital text extraction for a specific PDF document.

    - Validates that the document is a PDF.
    - Extracts text from all pages using PyMuPDF.
    - Saves the extracted text as a parallel .txt file on disk.
    - Flags images or scanned PDFs as requiring OCR.
    - Updates log status to 'PROCESSING'.
    """
    result = extract_text_from_pdf(db=db, document_uuid=document_uuid)
    return result

