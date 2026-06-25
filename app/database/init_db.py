from app.database.database import engine, Base

# Import all models
from app.models.supplier import Supplier

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()