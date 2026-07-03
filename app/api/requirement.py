from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.requirement import (
    RequirementCreate,
    RequirementResponse,
    RequirementListResponse,
    RequirementMaterialCreate,
    RequirementMaterialResponse
)

from app.services.requirement_service import RequirementService
from app.services.requirement_material_service import RequirementMaterialService

router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"]
)


# =====================================================
# Requirement
# =====================================================

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


# =====================================================
# Requirement Materials
# =====================================================

@router.post(
    "/{requirement_id}/materials",
    response_model=RequirementMaterialResponse
)
def add_material(
    requirement_id: int,
    material: RequirementMaterialCreate,
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

    return RequirementMaterialService.create_material(

        db=db,

        requirement_id=requirement_id,

        material_name=material.material_name,

        category=material.category,

        specification=material.specification,

        preferred_brand=material.preferred_brand,

        alternate_brand_allowed=material.alternate_brand_allowed,

        quantity=material.quantity,

        unit=material.unit,

        delivery_location=material.delivery_location,

        purpose=material.purpose,

        additional_requirements=material.additional_requirements,

        remarks=material.remarks
    )


@router.get(
    "/{requirement_id}/materials",
    response_model=list[RequirementMaterialResponse]
)
def get_requirement_materials(
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

    return RequirementMaterialService.get_materials_by_requirement(
        db=db,
        requirement_id=requirement_id
    )


@router.get(
    "/materials/{material_id}",
    response_model=RequirementMaterialResponse
)
def get_material(
    material_id: int,
    db: Session = Depends(get_db)
):

    material = RequirementMaterialService.get_material_by_id(
        db=db,
        material_id=material_id
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return material


@router.put(
    "/materials/{material_id}",
    response_model=RequirementMaterialResponse
)
def update_material(
    material_id: int,
    material_data: RequirementMaterialCreate,
    db: Session = Depends(get_db)
):

    material = RequirementMaterialService.get_material_by_id(
        db=db,
        material_id=material_id
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return RequirementMaterialService.update_material(

        db=db,

        material=material,

        material_name=material_data.material_name,

        category=material_data.category,

        specification=material_data.specification,

        preferred_brand=material_data.preferred_brand,

        alternate_brand_allowed=material_data.alternate_brand_allowed,

        quantity=material_data.quantity,

        unit=material_data.unit,

        delivery_location=material_data.delivery_location,

        purpose=material_data.purpose,

        additional_requirements=material_data.additional_requirements,

        remarks=material_data.remarks
    )


@router.delete(
    "/materials/{material_id}"
)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db)
):

    material = RequirementMaterialService.get_material_by_id(
        db=db,
        material_id=material_id
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    RequirementMaterialService.delete_material(
        db=db,
        material=material
    )

    return {
        "success": True,
        "message": "Material deleted successfully."
    }