from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.notification import (
    Notification
)

from app.models.user import User

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# GET ALL NOTIFICATIONS
@router.get("/")
async def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    if current_user.role == "admin":

        notifications = db.query(
            Notification
        ).order_by(
            Notification.created_at.desc()
        ).all()

    else:

        notifications = db.query(
            Notification
        ).filter(
            Notification.user_id ==
            current_user.id
        ).order_by(
            Notification.created_at.desc()
        ).all()

    return notifications


# GET UNREAD COUNT
@router.get("/unread-count")
async def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    if current_user.role == "admin":

        count = db.query(
            Notification
        ).filter(
            Notification.is_read == False
        ).count()

    else:

        count = db.query(
            Notification
        ).filter(
            Notification.user_id ==
            current_user.id,

            Notification.is_read == False
        ).count()

    return {
        "unread_count": count
    }


# MARK ALL AS READ
@router.put("/mark-all/read")
async def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    query = db.query(
        Notification
    )

    if current_user.role != "admin":

        query = query.filter(
            Notification.user_id ==
            current_user.id
        )

    notifications = query.filter(
        Notification.is_read == False
    ).all()

    for item in notifications:
        item.is_read = True

    db.commit()

    return {
        "message":
        "All notifications marked as read"
    }


# MARK SINGLE NOTIFICATION AS READ
@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    query = db.query(
        Notification
    ).filter(
        Notification.id ==
        notification_id
    )

    if current_user.role != "admin":

        query = query.filter(
            Notification.user_id ==
            current_user.id
        )

    notification = query.first()

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()

    return {
        "message":
        "Notification marked as read"
    }