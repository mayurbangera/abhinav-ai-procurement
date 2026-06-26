from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.supplier_service import SupplierService
from app.models.supplier import Supplier

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    stats = SupplierService.get_dashboard_stats(db)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "stats": stats
        }
    )


@router.get(
    "/suppliers/{supplier_id}",
    response_class=HTMLResponse
)
def supplier_details(
    supplier_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    supplier = db.query(
        Supplier
    ).filter(
        Supplier.id == supplier_id
    ).first()

    if not supplier:

        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="supplier_details.html",
        context={
            "request": request,
            "supplier": supplier
        }
    )