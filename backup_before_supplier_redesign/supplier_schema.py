import re
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from datetime import datetime


class SupplierCreate(BaseModel):
    company_name: str
    principal_business: Optional[str] = None

    business_classification: str

    gst_number: str
    pan_number: str

    date_of_incorporation: Optional[str] = None

    registered_address: str
    godown_address: Optional[str] = None

    contact_person_name: str
    contact_person_mobile: str
    contact_person_email: EmailStr

    telephone_number: Optional[str] = None

    supplier_category: Optional[str] = None
    material_types: Optional[str] = None

    bank_account_name: str
    bank_account_number: str
    bank_ifsc: str
    bank_name: str
    branch_name: Optional[str] = None

    is_msme: bool = False
    msme_number: Optional[str] = None
    msme_certificate_path: Optional[str] = None

    gst_certificate_path: str

    customer_reference_1: Optional[str] = None
    customer_reference_2: Optional[str] = None
    customer_reference_3: Optional[str] = None
    customer_reference_4: Optional[str] = None
    customer_reference_5: Optional[str] = None

    authorized_person_name: Optional[str] = None
    designation: Optional[str] = None

    declaration_accepted: bool = False

    whatsapp_number: Optional[str] = None

    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, value):
        value = value.strip()

        if len(value) < 3:
            raise ValueError(
                "Company name must be at least 3 characters"
            )

        company_pattern = r'^[A-Za-z0-9&.,()\- ]+$'

        if not re.match(company_pattern, value):
            raise ValueError(
                "Invalid company name"
            )

        return value

    @field_validator("contact_person_name")
    @classmethod
    def validate_contact_person_name(cls, value):
        value = value.strip()

        if len(value) < 3:
            raise ValueError(
                "Contact person name must be at least 3 characters"
            )

        name_pattern = r'^[A-Za-z ]+$'

        if not re.match(name_pattern, value):
            raise ValueError(
                "Contact person name can contain only letters and spaces"
            )

        return value

    @field_validator("gst_number")
    @classmethod
    def validate_gst(cls, value):
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{1}Z[0-9A-Z]{1}$'

        value = value.upper()

        if not re.match(gst_pattern, value):
            raise ValueError("Invalid GST Number")

        return value

    @field_validator("pan_number")
    @classmethod
    def validate_pan(cls, value):
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'

        value = value.upper()

        if not re.match(pan_pattern, value):
            raise ValueError("Invalid PAN Number")

        return value

    @field_validator("contact_person_mobile")
    @classmethod
    def validate_mobile(cls, value):
        if not value.isdigit():
            raise ValueError(
                "Mobile number must contain digits only"
            )

        if len(value) != 10:
            raise ValueError(
                "Mobile number must be exactly 10 digits"
            )

        return value

    @field_validator("bank_account_number")
    @classmethod
    def validate_bank_account_number(cls, value):

        if not value.isdigit():
            raise ValueError(
                "Bank account number must contain digits only"
            )

        if len(value) < 8:
            raise ValueError(
                "Bank account number must be at least 8 digits"
            )

        if len(value) > 20:
            raise ValueError(
                "Bank account number cannot exceed 20 digits"
            )

        return value

    @field_validator("bank_ifsc")
    @classmethod
    def validate_ifsc(cls, value):
        value = value.upper()

        ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'

        if not re.match(ifsc_pattern, value):
            raise ValueError("Invalid IFSC Code")

        return value

    @field_validator("whatsapp_number")
    @classmethod
    def validate_whatsapp_number(cls, value):

        if value is None:
            return value

        if not value.isdigit():
            raise ValueError(
                "WhatsApp number must contain digits only"
            )

        if len(value) != 10:
            raise ValueError(
                "WhatsApp number must be exactly 10 digits"
            )

        return value
    
class SupplierResponse(BaseModel):
    id: int

    company_name: str
    principal_business: Optional[str] = None

    business_classification: str

    gst_number: str
    pan_number: str

    date_of_incorporation: Optional[str] = None

    registered_address: str
    godown_address: Optional[str] = None

    contact_person_name: str
    contact_person_mobile: str
    contact_person_email: Optional[EmailStr] = None

    telephone_number: Optional[str] = None
    whatsapp_number: Optional[str] = None

    supplier_category: Optional[str] = None
    material_types: Optional[str] = None

    bank_account_name: str
    bank_account_number: str
    bank_ifsc: str
    bank_name: str
    branch_name: Optional[str] = None

    is_msme: bool
    msme_number: Optional[str] = None
    msme_certificate_path: Optional[str] = None

    gst_certificate_path: str

    authorized_person_name: Optional[str] = None
    designation: Optional[str] = None

    declaration_accepted: bool

    registration_status: str
    approval_remarks: Optional[str] = None
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
    
    
class SupplierReferenceResponse(BaseModel):
    id: int

    supplier_id: int

    company_name: str
    contact_person: str
    contact_number: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    
    

class SupplierListResponse(BaseModel):

    id: int

    company_name: str

    contact_person_name: str

    contact_person_mobile: str

    supplier_category: Optional[str] = None

    registration_status: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }