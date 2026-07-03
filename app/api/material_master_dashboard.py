from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.material_master_dashboard_service import (
    MaterialMasterDashboardService
)

router = APIRouter(
    prefix="/dashboard/material-master",
    tags=["Material Master Dashboard"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def material_dashboard(

    request: Request,

    db: Session = Depends(get_db),

    search: str = ""

):

    data = (
        MaterialMasterDashboardService
        .get_dashboard_data(
            db=db,
            search=search
        )
    )

    return templates.TemplateResponse(

        request=request,

        name="material_master.html",

        context={

            "request": request,

            "materials": data["materials"],

            "categories": data["categories"],

            "subcategories": data["subcategories"],

            "search": search

        }

    )