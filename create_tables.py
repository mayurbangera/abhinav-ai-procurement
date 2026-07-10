from app.database.database import Base, engine

from app.models.supplier import Supplier
from app.models.supplier_conversation import SupplierConversation
from app.models.supplier_reference import SupplierReference

from app.models.requirement import Requirement
from app.models.requirement_material import RequirementMaterial
from app.models.material_master import MaterialMaster
from app.models.material_category import MaterialCategory
from app.models.material_subcategory import MaterialSubCategory

from app.models.rfq import RFQ
from app.models.rfq_item import RFQItem
from app.models.rfq_vendor import RFQVendor

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")