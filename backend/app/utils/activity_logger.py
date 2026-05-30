from sqlalchemy.orm import Session

from app.models.user_activity import (
    UserActivity
)


def log_user_activity(

    db: Session,

    user_id: int | None,

    action: str,

    details: str = None
):

    activity = UserActivity(

        user_id=user_id,

        action=action,

        details=details
    )

    db.add(activity)

    db.commit()