from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.requirement_material import RequirementMaterial


class RequirementMaterialService:

    # =====================================================
    # Create Material
    # =====================================================

    @staticmethod
    def create_material(
        db: Session,
        requirement_id: int,
        material_name: str,
        category: str | None,
        specification: str | None,
        preferred_brand: str | None,
        alternate_brand_allowed: bool,
        quantity: Decimal,
        unit: str,
        delivery_location: str | None,
        purpose: str | None,
        additional_requirements: str | None,
        remarks: str | None
    ):

        material = RequirementMaterial(

            requirement_id=requirement_id,

            material_name=material_name.strip(),

            category=category.strip() if category else None,

            specification=specification.strip() if specification else None,

            preferred_brand=preferred_brand.strip() if preferred_brand else None,

            alternate_brand_allowed=alternate_brand_allowed,

            quantity=quantity,

            unit=unit.strip(),

            delivery_location=delivery_location.strip() if delivery_location else None,

            purpose=purpose.strip() if purpose else None,

            additional_requirements=(
                additional_requirements.strip()
                if additional_requirements else None
            ),

            remarks=remarks.strip() if remarks else None

        )

        db.add(material)

        db.commit()

        db.refresh(material)

        return material

    # =====================================================
    # Get Material By ID
    # =====================================================

    @staticmethod
    def get_material_by_id(
        db: Session,
        material_id: int
    ):

        return (
            db.query(RequirementMaterial)
            .filter(
                RequirementMaterial.id == material_id
            )
            .first()
        )

    # =====================================================
    # Get Materials By Requirement
    # =====================================================

    @staticmethod
    def get_materials_by_requirement(
        db: Session,
        requirement_id: int
    ):

        return (
            db.query(RequirementMaterial)
            .filter(
                RequirementMaterial.requirement_id == requirement_id
            )
            .order_by(
                RequirementMaterial.id.asc()
            )
            .all()
        )

    # =====================================================
    # Update Material
    # =====================================================

    @staticmethod
    def update_material(
        db: Session,
        material: RequirementMaterial,
        material_name: str,
        category: str | None,
        specification: str | None,
        preferred_brand: str | None,
        alternate_brand_allowed: bool,
        quantity: Decimal,
        unit: str,
        delivery_location: str | None,
        purpose: str | None,
        additional_requirements: str | None,
        remarks: str | None
    ):

        material.material_name = material_name.strip()

        material.category = (
            category.strip()
            if category else None
        )

        material.specification = (
            specification.strip()
            if specification else None
        )

        material.preferred_brand = (
            preferred_brand.strip()
            if preferred_brand else None
        )

        material.alternate_brand_allowed = (
            alternate_brand_allowed
        )

        material.quantity = quantity

        material.unit = unit.strip()

        material.delivery_location = (
            delivery_location.strip()
            if delivery_location else None
        )

        material.purpose = (
            purpose.strip()
            if purpose else None
        )

        material.additional_requirements = (
            additional_requirements.strip()
            if additional_requirements else None
        )

        material.remarks = (
            remarks.strip()
            if remarks else None
        )

        db.commit()

        db.refresh(material)

        return material

    # =====================================================
    # Delete Material
    # =====================================================

    @staticmethod
    def delete_material(
        db: Session,
        material: RequirementMaterial
    ):

        db.delete(material)

        db.commit()

        return True

    # =====================================================
    # Duplicate Check
    # (Warning only)
    # =====================================================

    @staticmethod
    def check_duplicate_material(
        db: Session,
        requirement_id: int,
        material_name: str
    ):

        return (
            db.query(RequirementMaterial)
            .filter(
                RequirementMaterial.requirement_id == requirement_id,
                RequirementMaterial.material_name.ilike(material_name.strip())
            )
            .first()
        )