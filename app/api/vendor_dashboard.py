from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.supplier import Supplier

router = APIRouter(
    prefix="/dashboard/vendor-master",
    tags=["Vendor Master Dashboard"]
)

templates = Jinja2Templates(
    directory="app/templates"
)

@router.get(
    "/",
    response_class=HTMLResponse
)
def vendor_master(
    request: Request,
    db: Session = Depends(get_db),
    search: str = "",
    category: str = ""
):
    query = db.query(Supplier).filter(
        Supplier.registration_status == "APPROVED"
    )

    if search:
        query = query.filter(
            Supplier.company_name.ilike(f"%{search}%")
        )

    if category:
        query = query.filter(
            Supplier.supplier_category.ilike(f"%{category}%")
        )

    vendors = query.order_by(
        Supplier.supplier_code
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="vendor_master.html",
        context={
            "request": request,
            "vendors": vendors,
            "search": search,
            "category": category
        }
    )
