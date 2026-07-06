from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.material_category_dashboard_service import (
    MaterialCategoryDashboardService
)

router = APIRouter(
    prefix="/dashboard/material-categories",
    tags=["Material Category Dashboard"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def material_category_dashboard(

    request: Request,

    db: Session = Depends(get_db),

    search: str = ""

):

    data = (
        MaterialCategoryDashboardService
        .get_dashboard_data(
            db=db,
            search=search
        )
    )

    return templates.TemplateResponse(

        request=request,

        name="material_category.html",

        context={

            "request": request,

            "categories": data["categories"],

            "search": search

        }

    )