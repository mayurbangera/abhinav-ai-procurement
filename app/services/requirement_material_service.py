from sqlalchemy.orm import Session

from app.models.requirement_material import RequirementMaterial


class RequirementMaterialService:

    @staticmethod
    def create_material(
        db: Session,
        requirement_id: int,
        material_name: str,
        specification: str,
        preferred_brand: str | None,
        alternate_brand_allowed: bool,
        quantity: str,
        unit: str,
        delivery_location: str,
        purpose: str,
        additional_specification: str | None,
        remarks: str | None
    ):

        material = RequirementMaterial(

            requirement_id=requirement_id,

            material_name=material_name,

            specification=specification,

            preferred_brand=preferred_brand,

            alternate_brand_allowed=alternate_brand_allowed,

            quantity=quantity,

            unit=unit,

            delivery_location=delivery_location,

            purpose=purpose,

            additional_specification=additional_specification,

            remarks=remarks

        )

        db.add(material)

        db.commit()

        db.refresh(material)

        return material