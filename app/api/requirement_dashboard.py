from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.requirement_dashboard_service import RequirementDashboardService

router = APIRouter(
    prefix="/dashboard/requirements",
    tags=["Requirement Dashboard"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


# =====================================================
# Requirement Management
# =====================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
def requirement_management(
    request: Request,
    db: Session = Depends(get_db),
    search: str = "",
    status: str = ""
):

    requirements = RequirementDashboardService.get_all_requirements(
        db=db,
        search=search,
        status=status
    )

    return templates.TemplateResponse(
        request=request,
        name="requirement_management.html",
        context={
            "request": request,
            "requirements": requirements,
            "search": search,
            "status": status
        }
    )


# =====================================================
# Create Requirement Page
# =====================================================

@router.get(
    "/create",
    response_class=HTMLResponse
)
def create_requirement_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="requirement_create.html",
        context={
            "request": request
        }
    )