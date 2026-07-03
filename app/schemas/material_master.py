from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator


# =====================================================
# Material Master Create
# =====================================================

class MaterialMasterCreate(BaseModel):

    material_code: Optional[str] = None

    material_name: str

    category_id: int

    subcategory_id: Optional[int] = None

    description: Optional[str] = None

    default_unit: str

    preferred_brand: Optional[str] = None

    gst_percentage: Optional[Decimal] = None

    hsn_code: Optional[str] = None

    is_active: bool = True

    @field_validator("material_name")
    @classmethod
    def validate_material_name(cls, value):

        value = value.strip()

        if len(value) < 2:

            raise ValueError(
                "Material name is required."
            )

        return value

    @field_validator("default_unit")
    @classmethod
    def validate_default_unit(cls, value):

        value = value.strip()

        if len(value) < 1:

            raise ValueError(
                "Default unit is required."
            )

        return value


# =====================================================
# Material Master Response
# =====================================================

class MaterialMasterResponse(BaseModel):

    id: int

    material_code: str

    material_name: str

    category_id: int

    subcategory_id: Optional[int]

    description: Optional[str]

    default_unit: str

    preferred_brand: Optional[str]

    gst_percentage: Optional[Decimal]

    hsn_code: Optional[str]

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =====================================================
# Material Master List
# =====================================================

class MaterialMasterListResponse(BaseModel):

    id: int

    material_code: str

    material_name: str

    category_id: int

    subcategory_id: Optional[int]

    default_unit: str

    is_active: bool

    model_config = {
        "from_attributes": True
    }