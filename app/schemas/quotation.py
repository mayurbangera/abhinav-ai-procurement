from typing import Optional, List, Dict, Any
from pydantic import BaseModel, model_validator, Field
from datetime import date, datetime

# ─────────────────────────────────────────────────────────
# Quotation Item Schemas
# ─────────────────────────────────────────────────────────

class QuotationItemCreate(BaseModel):
    rfq_item_id: int
    is_quoted: bool = True
    quoted_quantity: Optional[float] = None
    brand_offered: Optional[str] = None
    specs_offered: Optional[Dict[str, Any]] = None
    
    basic_rate: float = 0.0
    discount_percent: float = 0.0
    tax_percent: float = 0.0
    freight_amount: float = 0.0
    remarks: Optional[str] = None
    
    # Mathematical validation for line items
    @model_validator(mode='after')
    def validate_and_calculate_item(self) -> 'QuotationItemCreate':
        if not self.is_quoted:
            self.basic_rate = 0.0
            self.discount_percent = 0.0
            self.tax_percent = 0.0
            self.freight_amount = 0.0
            self.quoted_quantity = 0.0
            return self
            
        if self.quoted_quantity is None or self.quoted_quantity <= 0:
            raise ValueError("quoted_quantity must be greater than 0 if is_quoted is True.")
            
        if self.basic_rate < 0:
            raise ValueError("basic_rate cannot be negative.")
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValueError("discount_percent must be between 0 and 100.")
        if self.tax_percent < 0 or self.tax_percent > 100:
            raise ValueError("tax_percent must be between 0 and 100.")
            
        return self


class QuotationItemResponse(BaseModel):
    id: int
    quotation_id: int
    rfq_item_id: int
    is_quoted: bool
    quoted_quantity: Optional[float]
    brand_offered: Optional[str]
    specs_offered: Optional[Dict[str, Any]]
    
    basic_rate: float
    discount_percent: float
    tax_percent: float
    freight_amount: float
    final_landed_rate: float
    total_item_amount: float
    remarks: Optional[str]
    
    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────────
# Quotation Header Schemas
# ─────────────────────────────────────────────────────────

class QuotationCreate(BaseModel):
    rfq_id: int
    vendor_id: int
    date_received: date
    validity_date: Optional[date] = None
    payment_terms: Optional[str] = None
    delivery_timeline: Optional[str] = None
    
    freight_amount_total: float = 0.0
    loading_unloading_total: float = 0.0
    
    attachment_path: Optional[str] = None
    creation_source: str = "MANUAL"
    created_by: str
    
    items: List[QuotationItemCreate]
    
    @model_validator(mode='after')
    def validate_header(self) -> 'QuotationCreate':
        if self.freight_amount_total < 0:
            raise ValueError("freight_amount_total cannot be negative.")
        if self.loading_unloading_total < 0:
            raise ValueError("loading_unloading_total cannot be negative.")
        if not self.items:
            raise ValueError("Quotation must contain at least one item.")
        return self


class QuotationResponse(BaseModel):
    id: int
    quotation_number: str
    revision_number: int
    rfq_id: int
    vendor_id: int
    is_latest: bool
    date_received: date
    validity_date: Optional[date]
    payment_terms: Optional[str]
    delivery_timeline: Optional[str]
    
    freight_amount_total: float
    loading_unloading_total: float
    grand_total: float
    
    attachment_path: Optional[str]
    status: str
    creation_source: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class QuotationDetailResponse(QuotationResponse):
    items: List[QuotationItemResponse] = []
