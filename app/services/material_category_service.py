from sqlalchemy.orm import Session

from app.models.material_category import MaterialCategory


class MaterialCategoryService:

    # =====================================================
    # Create Category
    # =====================================================

    @staticmethod
    def create_category(
        db: Session,
        category_code: str | None,
        category_name: str,
        description: str | None,
        is_active: bool
    ):

        last = (
            db.query(MaterialCategory)
            .order_by(MaterialCategory.id.desc())
            .first()
        )

        next_number = 1

        if last:
            next_number = last.id + 1

        generated_code = f"CAT{next_number:04d}"

        category = MaterialCategory(

            category_code=generated_code,

            category_name=category_name.strip(),

            description=(
                description.strip()
                if description else None
            ),

            is_active=is_active

        )

        db.add(category)

        db.commit()

        db.refresh(category)

        return category


    # =====================================================
    # Get Category By ID
    # =====================================================

    @staticmethod
    def get_category_by_id(
        db: Session,
        category_id: int
    ):

        return (
            db.query(MaterialCategory)
            .filter(
                MaterialCategory.id == category_id
            )
            .first()
        )


    # =====================================================
    # Get All Categories
    # =====================================================

    @staticmethod
    def get_all_categories(
        db: Session
    ):

        return (
            db.query(MaterialCategory)
            .order_by(
                MaterialCategory.category_name.asc()
            )
            .all()
        )


    # =====================================================
    # Duplicate Check
    # =====================================================

    @staticmethod
    def check_duplicate_category(
        db: Session,
        category_name: str
    ):

        return (
            db.query(MaterialCategory)
            .filter(
                MaterialCategory.category_name.ilike(
                    category_name.strip()
                )
            )
            .first()
        )


    # =====================================================
    # Update Category
    # =====================================================

    @staticmethod
    def update_category(
        db: Session,
        category: MaterialCategory,
        category_name: str,
        description: str | None,
        is_active: bool
    ):

        category.category_name = category_name.strip()

        category.description = (
            description.strip()
            if description else None
        )

        category.is_active = is_active

        db.commit()

        db.refresh(category)

        return category


    # =====================================================
    # Delete Category
    # =====================================================

    @staticmethod
    def delete_category(
        db: Session,
        category: MaterialCategory
    ):

        db.delete(category)

        db.commit()

        return True