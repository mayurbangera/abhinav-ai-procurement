from sqlalchemy.orm import Session

from app.models.material_master import MaterialMaster


class MaterialMasterService:

    # =====================================================
    # Create Material
    # =====================================================

    @staticmethod
    def create_material(
        db: Session,
        material_code: str | None,
        material_name: str,
        category_id: int,
        subcategory_id: int | None,
        description: str | None,
        default_unit: str,
        preferred_brand: str | None,
        gst_percentage,
        hsn_code: str | None,
        is_active: bool
    ):

        last_material = (

            db.query(MaterialMaster)

            .order_by(
                MaterialMaster.id.desc()
            )

            .first()

        )

        if last_material:
            next_number = last_material.id + 1
        else:
            next_number = 1

        generated_code = f"MAT{next_number:06d}"

        material = MaterialMaster(

            material_code=generated_code,

            material_name=material_name.strip(),

            category_id=category_id,

            subcategory_id=subcategory_id,

            description=(
                description.strip()
                if description else None
            ),

            default_unit=default_unit.strip(),

            preferred_brand=(
                preferred_brand.strip()
                if preferred_brand else None
            ),

            gst_percentage=gst_percentage,

            hsn_code=(
                hsn_code.strip()
                if hsn_code else None
            ),

            is_active=is_active

        )

        db.add(material)

        db.commit()

        db.refresh(material)

        return material

    # =====================================================
    # Get All Materials
    # =====================================================

    @staticmethod
    def get_all_materials(
        db: Session,
        search: str = "",
        category_id: int | None = None,
        status: str = ""
    ):

        query = db.query(MaterialMaster)

        if search:

            query = query.filter(
                MaterialMaster.material_name.ilike(
                    f"%{search}%"
                )
            )

        if category_id:

            query = query.filter(
                MaterialMaster.category_id == category_id
            )

        if status:

            if status.lower() == "active":

                query = query.filter(
                    MaterialMaster.is_active == True
                )

            elif status.lower() == "inactive":

                query = query.filter(
                    MaterialMaster.is_active == False
                )

        return (

            query.order_by(
                MaterialMaster.material_name.asc()
            )

            .all()

        )

    # =====================================================
    # Get Material By ID
    # =====================================================

    @staticmethod
    def get_material_by_id(
        db: Session,
        material_id: int
    ):

        return (

            db.query(MaterialMaster)

            .filter(
                MaterialMaster.id == material_id
            )

            .first()

        )

    # =====================================================
    # Update Material
    # =====================================================

    @staticmethod
    def update_material(
        db: Session,
        material: MaterialMaster,
        material_code: str,
        material_name: str,
        category_id: int,
        subcategory_id: int | None,
        description: str | None,
        default_unit: str,
        preferred_brand: str | None,
        gst_percentage,
        hsn_code: str | None,
        is_active: bool
    ):

        material.material_code = material_code.strip().upper()

        material.material_name = material_name.strip()

        material.category_id = category_id

        material.subcategory_id = subcategory_id

        material.description = (
            description.strip()
            if description else None
        )

        material.default_unit = default_unit.strip()

        material.preferred_brand = (
            preferred_brand.strip()
            if preferred_brand else None
        )

        material.gst_percentage = gst_percentage

        material.hsn_code = (
            hsn_code.strip()
            if hsn_code else None
        )

        material.is_active = is_active

        db.commit()

        db.refresh(material)

        return material

    # =====================================================
    # Delete Material
    # =====================================================

    @staticmethod
    def delete_material(
        db: Session,
        material: MaterialMaster
    ):

        db.delete(material)

        db.commit()

        return True

    # =====================================================
    # Duplicate Check
    # =====================================================

    @staticmethod
    def check_duplicate_material(
        db: Session,
        material_name: str
    ):

        return (

            db.query(MaterialMaster)

            .filter(

                MaterialMaster.material_name.ilike(
                    material_name.strip()
                )

            )

            .first()

        )