from sqlalchemy.orm import Session

from app.models.automation_schedule import (
    AutomationSchedule
)


class ScheduleService:

    @staticmethod
    def get_interval(

        db: Session,

        job_name: str,

        default_minutes: int
    ):

        schedule = (
            db.query(
                AutomationSchedule
            )
            .filter(
                AutomationSchedule.job_name
                == job_name
            )
            .first()
        )

        if schedule:

            return (
                schedule
                .interval_minutes
            )

        return default_minutes