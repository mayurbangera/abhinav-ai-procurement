from fastapi import FastAPI


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.supplier import router as supplier_router
from app.api.upload import router as upload_router


# Import Models
from app.models.supplier import Supplier
from app.models.supplier_conversation import SupplierConversation

from app.api.whatsapp import router as whatsapp_router

from app.api.dashboard import router as dashboard_router

from app.api.requirement import router as requirement_router
from app.api.requirement_dashboard import router as requirement_dashboard_router
from app.api.material_master import router as material_master_router

from app.api.material_master_dashboard import (
    router as material_master_dashboard_router
)

app = FastAPI(
    title="Abhinav Group Supplier Registration System"
)





app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

app.include_router(supplier_router)
app.include_router(upload_router)
app.include_router(whatsapp_router)
app.include_router(dashboard_router)
app.include_router(requirement_router)
app.include_router(requirement_dashboard_router)
app.include_router(material_master_router)
app.include_router(material_master_dashboard_router)


@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Supplier Registration"
    }