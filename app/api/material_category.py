from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.material_category import (
    MaterialCategoryCreate,
    MaterialCategoryResponse,
    MaterialCategoryListResponse
)

from app.services.material_category_service import (
    MaterialCategoryService
)

router = APIRouter(
    prefix="/material-categories",
    tags=["Material Categories"]
)


# =====================================================
# Create Category
# =====================================================

@router.post(
    "/",
    response_model=MaterialCategoryResponse
)
def create_category(
    category: MaterialCategoryCreate,
    db: Session = Depends(get_db)
):

    duplicate = MaterialCategoryService.check_duplicate_category(
        db=db,
        category_name=category.category_name
    )

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Category already exists."
        )

    return MaterialCategoryService.create_category(

        db=db,

        category_code=category.category_code,

        category_name=category.category_name,

        description=category.description,

        is_active=category.is_active

    )