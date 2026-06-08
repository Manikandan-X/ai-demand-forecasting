from sqlalchemy.orm import Session

from app.models.automation_log import (
    AutomationLog
)


class AutomationLogService:

    @staticmethod
    def create_log(

        db: Session,

        job_name: str,

        status: str,

        message: str
    ):

        log = AutomationLog(

            job_name=job_name,

            status=status,

            message=message
        )

        db.add(log)

        db.commit()

        db.refresh(log)

        return log

    @staticmethod
    def get_logs(
        db: Session
    ):

        return (

            db.query(
                AutomationLog
            )

            .order_by(
                AutomationLog.created_at.desc()
            )

            .all()
        )