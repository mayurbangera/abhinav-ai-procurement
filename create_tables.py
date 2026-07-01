from app.database.database import Base, engine

from app.models.supplier import Supplier
from app.models.supplier_conversation import SupplierConversation

from app.models.requirement import Requirement
from app.models.requirement_material import RequirementMaterial

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")