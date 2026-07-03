from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


# =====================================================
# Category Create
# =====================================================

class MaterialCategoryCreate(BaseModel):

    category_code: Optional[str] = None

    category_name: str

    description: Optional[str] = None

    is_active: bool = True

    @field_validator("category_name")
    @classmethod
    def validate_category(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Category name is required."
            )

        return value


# =====================================================
# Category Response
# =====================================================

class MaterialCategoryResponse(BaseModel):

    id: int

    category_code: str

    category_name: str

    description: Optional[str]

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =====================================================
# Category List
# =====================================================

class MaterialCategoryListResponse(BaseModel):

    id: int

    category_code: str

    category_name: str

    is_active: bool

    model_config = {
        "from_attributes": True
    }