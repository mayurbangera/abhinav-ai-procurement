from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator


# =====================================================
# Requirement Create
# =====================================================

class RequirementCreate(BaseModel):

    project_name: str
    site_name: str
    requested_by: str
    priority: str
    required_date: date
    purpose: str
    remarks: Optional[str] = None

    @field_validator("project_name")
    @classmethod
    def validate_project(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Project name is required.")

        return value

    @field_validator("site_name")
    @classmethod
    def validate_site(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Site name is required.")

        return value

    @field_validator("requested_by")
    @classmethod
    def validate_requested_by(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Requested By is required.")

        return value

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, value):

        value = value.strip()

        if len(value) < 10:
            raise ValueError("Purpose should be descriptive.")

        return value


# =====================================================
# Requirement Material Create
# =====================================================

class RequirementMaterialCreate(BaseModel):

    material_name: str

    specification: str

    preferred_brand: Optional[str] = None

    alternate_brand_allowed: bool = True

    quantity: str

    unit: str

    delivery_location: str

    purpose: str

    additional_specification: Optional[str] = None

    remarks: Optional[str] = None

    @field_validator("material_name")
    @classmethod
    def validate_material_name(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Material name is required.")

        return value

    @field_validator("specification")
    @classmethod
    def validate_specification(cls, value):

        value = value.strip()

        if len(value) < 5:
            raise ValueError("Specification is required.")

        return value

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):

        value = value.strip()

        if len(value) == 0:
            raise ValueError("Quantity is required.")

        return value

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value):

        value = value.strip()

        if len(value) == 0:
            raise ValueError("Unit is required.")

        return value

    @field_validator("delivery_location")
    @classmethod
    def validate_delivery_location(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Delivery location is required.")

        return value

    @field_validator("purpose")
    @classmethod
    def validate_material_purpose(cls, value):

        value = value.strip()

        if len(value) < 5:
            raise ValueError("Purpose is required.")

        return value


# =====================================================
# Requirement Response
# =====================================================

class RequirementResponse(BaseModel):

    id: int

    requirement_number: Optional[str]

    project_name: str

    site_name: str

    requested_by: str

    priority: str

    required_date: date

    purpose: str

    remarks: Optional[str]

    status: str

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =====================================================
# Requirement Material Response
# =====================================================

class RequirementMaterialResponse(BaseModel):

    id: int

    requirement_id: int

    material_name: str

    specification: str

    preferred_brand: Optional[str]

    alternate_brand_allowed: bool

    quantity: str

    unit: str

    delivery_location: str

    purpose: str

    additional_specification: Optional[str]

    remarks: Optional[str]

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =====================================================
# Requirement List
# =====================================================

class RequirementListResponse(BaseModel):

    id: int

    requirement_number: Optional[str]

    project_name: str

    site_name: str

    priority: str

    status: str

    required_date: date

    model_config = {
        "from_attributes": True
    }