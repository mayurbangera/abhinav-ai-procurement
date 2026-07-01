from sqlalchemy.orm import Session

from app.models.requirement import Requirement


class RequirementDashboardService:

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

        return query.order_by(
            Requirement.created_at.desc()
        ).all()
        