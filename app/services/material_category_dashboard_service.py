from sqlalchemy.orm import Session

from app.models.material_category import MaterialCategory


class MaterialCategoryDashboardService:

    @staticmethod
    def get_dashboard_data(
        db: Session,
        search: str = ""
    ):

        query = db.query(MaterialCategory)

        if search:

            query = query.filter(
                MaterialCategory.category_name.ilike(
                    f"%{search}%"
                )
            )

        categories = (

            query
            .order_by(
                MaterialCategory.category_name.asc()
            )
            .all()

        )

        return {
            "categories": categories
        }