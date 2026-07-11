from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


# ─────────────────────────────────────────────────────
# RFQ Item Schemas
# ─────────────────────────────────────────────────────

class RFQItemCreate(BaseModel):
    material_category: str
    material_name: str
    quantity: float
    unit: str
    brand_required: Optional[str] = None
    # Completely open JSONB field — stores any key/value pair.
    # Example for Steel: {"grade": "Fe550D", "sizes": "8mm, 10-25mm", "chemical_guarantee": "Yes"}
    # Example for Cement: {"type": "OPC", "bags": "500"}
    # Example for ANY future requirement: {"colour": "Red", "thread_type": "BSP", "pressure_rating": "10 bar"}
    dynamic_fields: Optional[Dict[str, Any]] = None
    remarks: Optional[str] = None


class RFQItemResponse(BaseModel):
    id: int
    rfq_id: int
    material_category: str
    material_name: str
    quantity: float
    unit: str
    brand_required: Optional[str]
    dynamic_fields: Optional[Dict[str, Any]]
    remarks: Optional[str]

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────
# RFQ Vendor Schemas
# ─────────────────────────────────────────────────────

class RFQVendorAdd(BaseModel):
    vendor_id: int


class RFQVendorResponse(BaseModel):
    id: int
    rfq_id: int
    vendor_id: int
    whatsapp_status: Optional[str]
    sent_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────────────
# RFQ Main Schemas
# ─────────────────────────────────────────────────────

class RFQCreate(BaseModel):
    project_name: str
    site_name: str
    delivery_location: str
    payment_terms: Optional[str] = None
    created_by: str


class RFQStatusUpdate(BaseModel):
    status: str


class RFQUpdate(BaseModel):
    # RFQ-specific editable fields. Only payment_terms is persisted (existing
    # column); deadline / contact remain transient and are passed at send time.
    payment_terms: Optional[str] = None


class RFQResponse(BaseModel):
    id: int
    rfq_number: str
    project_name: str
    site_name: str
    delivery_location: str
    payment_terms: Optional[str]
    status: str
    created_by: str
    requirement_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RFQDetailResponse(RFQResponse):
    items: List[RFQItemResponse] = []
    vendors: List[RFQVendorResponse] = []
