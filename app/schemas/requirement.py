from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator


# -----------------------------
# Create Requirement
# -----------------------------
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
            raise ValueError(
                "Project name is required."
            )

        return value

    @field_validator("site_name")
    @classmethod
    def validate_site(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Site name is required."
            )

        return value

    @field_validator("requested_by")
    @classmethod
    def validate_requested_by(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Requested By is required."
            )

        return value

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, value):

        value = value.strip()

        if len(value) < 10:
            raise ValueError(
                "Purpose should be descriptive."
            )

        return value


# -----------------------------
# Requirement Response
# -----------------------------
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


# -----------------------------
# Requirement List
# -----------------------------
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