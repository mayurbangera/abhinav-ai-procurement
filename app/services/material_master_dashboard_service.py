from sqlalchemy.orm import Session

from app.models.material_master import MaterialMaster
from app.models.material_category import MaterialCategory
from app.models.material_subcategory import MaterialSubCategory


class MaterialMasterDashboardService:

    @staticmethod
    def get_dashboard_data(
        db: Session,
        search: str = ""
    ):

        query = db.query(MaterialMaster)

        if search:

            query = query.filter(
                MaterialMaster.material_name.ilike(
                    f"%{search}%"
                )
            )

        materials = (
            query.order_by(
                MaterialMaster.material_name.asc()
            )
            .all()
        )

        categories = (
            db.query(MaterialCategory)
            .filter(
                MaterialCategory.is_active == True
            )
            .order_by(
                MaterialCategory.category_name
            )
            .all()
        )

        subcategories = (
            db.query(MaterialSubCategory)
            .filter(
                MaterialSubCategory.is_active == True
            )
            .order_by(
                MaterialSubCategory.subcategory_name
            )
            .all()
        )

        return {

            "materials": materials,

            "categories": categories,

            "subcategories": subcategories

        }