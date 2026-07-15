from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.quotation import QuotationCreate, QuotationResponse, QuotationDetailResponse
from app.services.quotation_service import QuotationService
from app.models.rfq import RFQ
from app.models.supplier import Supplier

router = APIRouter(
    prefix="/quotations",
    tags=["Quotation Management"]
)

@router.post("/", response_model=QuotationResponse)
def create_quotation(
    payload: QuotationCreate,
    db: Session = Depends(get_db)
):
    # Verify RFQ exists
    rfq = db.query(RFQ).filter(RFQ.id == payload.rfq_id).first()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")
        
    # Verify Vendor exists
    vendor = db.query(Supplier).filter(Supplier.id == payload.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    try:
        quotation = QuotationService.create_quotation(db, payload.model_dump())
        
        # Update RFQ status if not already Quotation Received or Negotiation
        if rfq.status not in ["Quotation Received", "Negotiation", "Closed", "Cancelled"]:
            rfq.status = "Quotation Received"
            db.commit()
            
        return quotation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{quotation_id}", response_model=QuotationDetailResponse)
def get_quotation(
    quotation_id: int,
    db: Session = Depends(get_db)
):
    quotation = QuotationService.get_quotation(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

@router.get("/rfq/{rfq_id}", response_model=list[QuotationResponse])
def get_rfq_quotations(
    rfq_id: int,
    only_latest: bool = True,
    db: Session = Depends(get_db)
):
    return QuotationService.get_rfq_quotations(db, rfq_id, only_latest)
