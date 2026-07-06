from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.material_category import MaterialCategory


categories = [

    "Cement",
    "Steel",
    "Sand",
    "Aggregates",
    "Bricks & Blocks",
    "Electrical",
    "Plumbing",
    "Paint",
    "Tiles",
    "Hardware",
    "Doors & Windows",
    "Roofing",
    "Waterproofing",
    "Chemicals",
    "Safety",
    "Tools",
    "HVAC",
    "Glass",
    "Aluminium",
    "Miscellaneous"

]


db: Session = SessionLocal()

try:

    for index, name in enumerate(categories, start=1):

        exists = (

            db.query(MaterialCategory)

            .filter(

                MaterialCategory.category_name == name

            )

            .first()

        )

        if exists:
            continue

        db.add(

            MaterialCategory(

                category_code=f"CAT{index:04d}",

                category_name=name,

                is_active=True

            )

        )

    db.commit()

    print("Categories inserted successfully.")

finally:

    db.close()