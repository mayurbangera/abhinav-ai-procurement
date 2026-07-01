from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.requirement import (
    RequirementCreate,
    RequirementResponse,
    RequirementListResponse
)

from app.services.requirement_service import RequirementService

router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"]
)


@router.post(
    "/",
    response_model=RequirementResponse
)
def create_requirement(
    requirement: RequirementCreate,
    db: Session = Depends(get_db)
):

    return RequirementService.create_requirement(
        db=db,
        project_name=requirement.project_name,
        site_name=requirement.site_name,
        requested_by=requirement.requested_by,
        priority=requirement.priority,
        required_date=requirement.required_date,
        purpose=requirement.purpose,
        remarks=requirement.remarks
    )


@router.get(
    "/",
    response_model=list[RequirementListResponse]
)
def get_requirements(
    db: Session = Depends(get_db)
):

    return RequirementService.get_all_requirements(db)


@router.get(
    "/{requirement_id}",
    response_model=RequirementResponse
)
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db)
):

    requirement = RequirementService.get_requirement_by_id(
        db,
        requirement_id
    )

    if not requirement:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found"
        )

    return requirement