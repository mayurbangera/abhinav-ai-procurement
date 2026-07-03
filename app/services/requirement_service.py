from sqlalchemy.orm import Session

from app.models.requirement import Requirement


class RequirementService:

    # =====================================================
    # Create Requirement
    # =====================================================

    @staticmethod
    def create_requirement(
        db: Session,
        project_name: str,
        site_name: str,
        requested_by: str,
        priority: str,
        required_date,
        purpose: str,
        remarks: str | None = None
    ):

        last_requirement = (
            db.query(Requirement)
            .order_by(
                Requirement.id.desc()
            )
            .first()
        )

        if last_requirement:
            next_number = last_requirement.id + 1
        else:
            next_number = 1

        requirement_number = f"REQ{next_number:06d}"

        requirement = Requirement(

            requirement_number=requirement_number,

            project_name=project_name,

            site_name=site_name,

            requested_by=requested_by,

            priority=priority,

            required_date=required_date,

            purpose=purpose,

            remarks=remarks,

            status="DRAFT"

        )

        db.add(requirement)

        db.commit()

        db.refresh(requirement)

        return requirement


    # =====================================================
    # Requirement List
    # =====================================================

    @staticmethod
    def get_all_requirements(
        db: Session,
        search: str = "",
        status: str = ""
    ):

        query = db.query(
            Requirement
        )

        if search:

            query = query.filter(
                Requirement.project_name.ilike(
                    f"%{search}%"
                )
            )

        if status:

            query = query.filter(
                Requirement.status == status
            )

        return (
            query
            .order_by(
                Requirement.created_at.desc()
            )
            .all()
        )


    # =====================================================
    # Requirement Details
    # =====================================================

    @staticmethod
    def get_requirement_by_id(
        db: Session,
        requirement_id: int
    ):

        return (
            db.query(
                Requirement
            )
            .filter(
                Requirement.id == requirement_id
            )
            .first()
        )