from sqlalchemy.orm import Session

from app.models.requirement import Requirement


class RequirementDetailsService:

    @staticmethod
    def get_requirement(
        db: Session,
        requirement_id: int
    ):

        return (
            db.query(Requirement)
            .filter(
                Requirement.id == requirement_id
            )
            .first()
        )