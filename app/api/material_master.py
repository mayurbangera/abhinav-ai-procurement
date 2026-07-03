from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.material_master import (
    MaterialMasterCreate,
    MaterialMasterResponse,
    MaterialMasterListResponse
)

from app.services.material_master_service import (
    MaterialMasterService
)

router = APIRouter(
    prefix="/material-master",
    tags=["Material Master"]
)


# =====================================================
# Create Material
# =====================================================

@router.post(
    "/",
    response_model=MaterialMasterResponse
)
def create_material(
    material: MaterialMasterCreate,
    db: Session = Depends(get_db)
):

    duplicate = (
        MaterialMasterService.check_duplicate_material(
            db=db,
            material_name=material.material_name
        )
    )

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Material already exists."
        )

    return MaterialMasterService.create_material(

        db=db,

        material_code=material.material_code,

        material_name=material.material_name,

        category_id=material.category_id,

        subcategory_id=material.subcategory_id,

        description=material.description,

        default_unit=material.default_unit,

        preferred_brand=material.preferred_brand,

        gst_percentage=material.gst_percentage,

        hsn_code=material.hsn_code,

        is_active=material.is_active

    )


# =====================================================
# Material List
# =====================================================

@router.get(
    "/",
    response_model=list[MaterialMasterListResponse]
)
def get_materials(
    db: Session = Depends(get_db),
    search: str = "",
    category_id: int | None = None,
    status: str = ""
):

    return MaterialMasterService.get_all_materials(

        db=db,

        search=search,

        category_id=category_id,

        status=status

    )


# =====================================================
# Get Material By ID
# =====================================================

@router.get(
    "/{material_id}",
    response_model=MaterialMasterResponse
)
def get_material(
    material_id: int,
    db: Session = Depends(get_db)
):

    material = MaterialMasterService.get_material_by_id(
        db=db,
        material_id=material_id
    )

    if not material:

        raise HTTPException(
            status_code=404,
            detail="Material not found."
        )

    return material


# =====================================================
# Update Material
# =====================================================

@router.put(
    "/{material_id}",
    response_model=MaterialMasterResponse
)
def update_material(
    material_id: int,
    material_data: MaterialMasterCreate,
    db: Session = Depends(get_db)
):

    material = MaterialMasterService.get_material_by_id(
        db=db,
        material_id=material_id
    )

    if not material:

        raise HTTPException(
            status_code=404,
            detail="Material not found."
        )

    return MaterialMasterService.update_material(

        db=db,

        material=material,

        material_code=material.material_code,

        material_name=material_data.material_name,

        category_id=material_data.category_id,

        subcategory_id=material_data.subcategory_id,

        description=material_data.description,

        default_unit=material_data.default_unit,

        preferred_brand=material_data.preferred_brand,

        gst_percentage=material_data.gst_percentage,

        hsn_code=material_data.hsn_code,

        is_active=material_data.is_active

    )


# =====================================================
# Delete Material
# =====================================================

@router.delete(
    "/{material_id}"
)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db)
):

    material = MaterialMasterService.get_material_by_id(
        db=db,
        material_id=material_id
    )

    if not material:

        raise HTTPException(
            status_code=404,
            detail="Material not found."
        )

    MaterialMasterService.delete_material(
        db=db,
        material=material
    )

    return {
        "success": True,
        "message": "Material deleted successfully."
    }