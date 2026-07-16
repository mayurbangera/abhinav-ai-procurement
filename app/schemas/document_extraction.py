from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# ──────────────────────────────────────────────────────────────
# Definitions
# ──────────────────────────────────────────────────────────────

class ExtractedFieldBase(BaseModel):
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    evidence: str = Field(..., description="Exact text snippet supporting extraction")
    page_number: int = Field(..., description="1-indexed page number where field resides")
    bounding_box: Optional[List[float]] = Field(None, description="[x_min, y_min, x_max, y_max] normalized coordinates")
    extraction_method: str = Field(..., description="Extraction engine (e.g. 'fitz-digital', 'paddleocr', 'llm-extraction')")
    validation_status: str = Field("UNVALIDATED", description="Field validation status: UNVALIDATED, PASSED, FAILED")


class ExtractedString(ExtractedFieldBase):
    value: Optional[str] = Field(None, description="Extracted text value")


class ExtractedNumber(ExtractedFieldBase):
    value: Optional[float] = Field(None, description="Extracted numeric value")


class ExtractedInteger(ExtractedFieldBase):
    value: Optional[int] = Field(None, description="Extracted integer value")


# ──────────────────────────────────────────────────────────────
# Validation Report Schemas
# ──────────────────────────────────────────────────────────────

class ValidationLogEntry(BaseModel):
    rule_name: str = Field(..., description="Name of validation rule run")
    status: str = Field(..., description="PASSED, WARNING, FAILED")
    message: str = Field(..., description="Explanation of validation outcome")


class ValidationReport(BaseModel):
    status: str = Field(..., description="PASSED, WARNING, FAILED")
    logs: List[ValidationLogEntry] = Field(default_factory=list)


class ValidationSummary(BaseModel):
    mathematical_validation: ValidationReport = Field(default_factory=lambda: ValidationReport(status="PASSED"))
    business_validation: ValidationReport = Field(default_factory=lambda: ValidationReport(status="PASSED"))
    semantic_validation: ValidationReport = Field(default_factory=lambda: ValidationReport(status="PASSED"))


# ──────────────────────────────────────────────────────────────
# Audit Trail Schemas
# ──────────────────────────────────────────────────────────────

class HumanChangeEntry(BaseModel):
    field_path: str = Field(..., description="JSON path of modified field (e.g., 'commercial_metadata.grand_total_amount')")
    ai_value: Optional[Any] = Field(None, description="Original value extracted by AI")
    human_value: Optional[Any] = Field(None, description="Value corrected by human reviewer")
    correction_reason: str = Field(..., description="Explanation for change")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user: str = Field(..., description="Reviewer identifier")


class AuditTrail(BaseModel):
    original_document_path: str
    raw_ocr_output: str
    human_changes: List[HumanChangeEntry] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Document Metadata
# ──────────────────────────────────────────────────────────────

class DocumentMetadata(BaseModel):
    document_id: ExtractedString
    document_type: ExtractedString
    document_number: ExtractedString
    document_date: ExtractedString
    revision_number: Optional[ExtractedInteger] = None
    vendor_reference_number: Optional[ExtractedString] = None
    total_pages: Optional[ExtractedInteger] = None
    original_document_path: Optional[str] = None


# ──────────────────────────────────────────────────────────────
# Vendor Metadata
# ──────────────────────────────────────────────────────────────

class VendorMetadata(BaseModel):
    vendor_name: ExtractedString
    supplier_code: Optional[ExtractedString] = None
    gst_number: Optional[ExtractedString] = None
    pan_number: Optional[ExtractedString] = None
    billing_address: Optional[ExtractedString] = None
    shipping_address: Optional[ExtractedString] = None
    contact_person: Optional[ExtractedString] = None
    mobile: Optional[ExtractedString] = None
    email: Optional[ExtractedString] = None
    bank_account_number: Optional[ExtractedString] = None
    bank_ifsc_code: Optional[ExtractedString] = None
    bank_name: Optional[ExtractedString] = None


# ──────────────────────────────────────────────────────────────
# Project Metadata
# ──────────────────────────────────────────────────────────────

class ProjectMetadata(BaseModel):
    project_name: Optional[ExtractedString] = None
    site_name: Optional[ExtractedString] = None
    delivery_location: Optional[ExtractedString] = None


# ──────────────────────────────────────────────────────────────
# Commercial Metadata
# ──────────────────────────────────────────────────────────────

class CommercialMetadata(BaseModel):
    currency: Optional[ExtractedString] = None
    payment_terms: Optional[ExtractedString] = None
    delivery_terms: Optional[ExtractedString] = None
    validity_date: Optional[ExtractedString] = None
    delivery_timeline: Optional[ExtractedString] = None
    freight_terms: Optional[ExtractedString] = None
    loading_unloading_terms: Optional[ExtractedString] = None
    insurance_terms: Optional[ExtractedString] = None
    warranty_terms: Optional[ExtractedString] = None
    total_basic_amount: Optional[ExtractedNumber] = None
    total_discount_amount: Optional[ExtractedNumber] = None
    total_tax_amount: Optional[ExtractedNumber] = None
    total_freight_amount: Optional[ExtractedNumber] = None
    total_loading_unloading_amount: Optional[ExtractedNumber] = None
    grand_total_amount: ExtractedNumber


# ──────────────────────────────────────────────────────────────
# Line Item Schema
# ──────────────────────────────────────────────────────────────

class LineItem(BaseModel):
    item_index: int
    material_name: ExtractedString
    material_id: Optional[int] = None
    requested_brand: Optional[ExtractedString] = None
    offered_brand: Optional[ExtractedString] = None
    requested_specification: Optional[ExtractedString] = None
    offered_specification: Optional[ExtractedString] = None
    quantity: ExtractedNumber
    unit_of_measure: ExtractedString
    basic_rate: ExtractedNumber
    discount_percent: Optional[ExtractedNumber] = None
    discount_amount: Optional[ExtractedNumber] = None
    tax_percent: Optional[ExtractedNumber] = None
    tax_amount: Optional[ExtractedNumber] = None
    freight_amount: Optional[ExtractedNumber] = None
    final_landed_rate: Optional[ExtractedNumber] = None
    total_item_amount: ExtractedNumber
    remarks: Optional[ExtractedString] = None


# ──────────────────────────────────────────────────────────────
# Unified Root Document Payload Schema
# ──────────────────────────────────────────────────────────────

class DocumentExtractionPayload(BaseModel):
    document_metadata: DocumentMetadata
    vendor_metadata: VendorMetadata
    project_metadata: ProjectMetadata
    commercial_metadata: CommercialMetadata
    line_items: List[LineItem] = Field(default_factory=list)
    validation_summary: ValidationSummary = Field(default_factory=ValidationSummary)
    audit_trail: Optional[AuditTrail] = None

    model_config = {"from_attributes": True}
